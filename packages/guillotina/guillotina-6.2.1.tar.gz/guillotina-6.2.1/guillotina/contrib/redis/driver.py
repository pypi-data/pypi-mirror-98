try:
    import aioredis
    import aioredis.errors
except ImportError:
    print("If you add guillotina.contrib.redis you need to add aioredis on your requirements")
    raise

from guillotina import app_settings
from guillotina import metrics
from guillotina.contrib.redis.exceptions import NoRedisConfigured
from typing import Any
from typing import List
from typing import Optional

import asyncio
import backoff
import logging


try:
    import prometheus_client

    REDIS_OPS = prometheus_client.Counter(
        "guillotina_cache_redis_ops_total",
        "Total count of ops by type of operation and the error if there was.",
        labelnames=["type", "error"],
    )
    REDIS_OPS_PROCESSING_TIME = prometheus_client.Histogram(
        "guillotina_cache_redis_ops_processing_time_seconds",
        "Histogram of operations processing time by type (in seconds)",
        labelnames=["type"],
    )

    class watch(metrics.watch):
        def __init__(self, operation: str):
            super().__init__(
                counter=REDIS_OPS, histogram=REDIS_OPS_PROCESSING_TIME, labels={"type": operation},
            )


except ImportError:
    watch = metrics.watch  # type: ignore


logger = logging.getLogger("guillotina.contrib.redis")


class RedisDriver:
    def __init__(self):
        self._pool = None
        self._pubsub = None
        self._loop = None
        self._receivers = {}
        self._pubsub_subscriptor = None
        self._conn = None
        self.initialized = False
        self.init_lock = asyncio.Lock()

    async def initialize(self, loop):
        self._loop = loop
        async with self.init_lock:
            if self.initialized is False:
                while True:
                    try:
                        await self._connect()
                        self.initialized = True
                        break
                    except Exception:  # pragma: no cover
                        logger.error("Error initializing pubsub", exc_info=True)

    @backoff.on_exception(backoff.expo, (OSError,), max_time=30, max_tries=4)
    async def _connect(self):
        settings = app_settings["redis"]
        with watch("create_pool"):
            self._pool = await aioredis.create_pool(
                (settings["host"], settings["port"]), **settings["pool"], loop=self._loop
            )
        with watch("acquire_conn"):
            self._conn = await self._pool.acquire()
        self._pubsub_subscriptor = aioredis.Redis(self._conn)

    async def finalize(self):
        if self._pool is not None:
            self._pool.close()
        await self._pool.wait_closed()
        self.initialized = False

    @property
    def pool(self):
        return self._pool

    async def info(self):
        return await self._pool.execute(b"COMMAND", b"INFO", "get")

    # VALUE API

    async def set(self, key: str, data: str, *, expire: Optional[int] = None):
        if self._pool is None:
            raise NoRedisConfigured()
        args: List[Any] = []
        if expire is not None:
            args[:] = [b"EX", expire]
        with watch("set"):
            ok = await self._pool.execute(b"SET", key, data, *args)
        assert ok == b"OK", ok

    async def get(self, key: str) -> str:
        if self._pool is None:
            raise NoRedisConfigured()
        with watch("get") as w:
            val = await self._pool.execute(b"GET", key)
            if not val:
                w.labels["type"] = "get_miss"
            return val

    async def delete(self, key: str):
        if self._pool is None:
            raise NoRedisConfigured()
        with watch("delete"):
            await self._pool.execute(b"DEL", key)

    async def expire(self, key: str, expire: int):
        if self._pool is None:
            raise NoRedisConfigured()
        await self._pool.execute(b"EXPIRE", key, expire)

    async def keys_startswith(self, key: str):
        if self._pool is None:
            raise NoRedisConfigured()
        return await self._pool.execute(b"KEYS", f"{key}*")

    async def delete_all(self, keys: List[str]):
        if self._pool is None:
            raise NoRedisConfigured()
        for key in keys:
            try:
                with watch("delete_many"):
                    await self._pool.execute(b"DEL", key)
                logger.debug("Deleted cache keys {}".format(keys))
            except Exception:
                logger.warning("Error deleting cache keys {}".format(keys), exc_info=True)

    async def flushall(self, *, async_op: Optional[bool] = False):
        if self._pool is None:
            raise NoRedisConfigured()
        ops = [b"FLUSHDB"]
        if async_op:
            ops.append(b"ASYNC")
        with watch("flush"):
            await self._pool.execute(*ops)

    # PUBSUB API

    async def publish(self, channel_name: str, data: str):
        if self._pool is None:
            raise NoRedisConfigured()
        with watch("publish"):
            await self._pool.execute(b"publish", channel_name, data)

    async def unsubscribe(self, channel_name: str):
        if self._pubsub_subscriptor is None:
            raise NoRedisConfigured()
        try:
            await self._pubsub_subscriptor.unsubscribe(channel_name)
        except aioredis.errors.ConnectionClosedError:
            if self.initialized:
                raise

    async def subscribe(self, channel_name: str):
        if self._pubsub_subscriptor is None:
            raise NoRedisConfigured()
        try:
            (channel,) = await self._pubsub_subscriptor.subscribe(channel_name)
        except aioredis.errors.ConnectionClosedError:  # pragma: no cover
            # closed in middle
            try:
                self._pool.close(self._conn)
            except Exception:
                pass
            self._conn = await self._pool.acquire()
            self._pubsub_subscriptor = aioredis.Redis(self._conn)
            (channel,) = await self._pubsub_subscriptor.subscribe(channel_name)

        return self._listener(channel)

    async def _listener(self, channel: aioredis.Channel):
        while await channel.wait_message():
            msg = await channel.get()
            yield msg
