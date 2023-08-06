from guillotina import glogging
from guillotina import task_vars
from guillotina.browser import View
from guillotina.component import query_adapter
from guillotina.exc_resp import HTTPConflict
from guillotina.exceptions import ConflictError
from guillotina.exceptions import TIDConflictError
from guillotina.interfaces import IErrorResponseException
from guillotina.middlewares import ErrorsMiddleware
from guillotina.request import Request
from guillotina.response import Response
from guillotina.traversal import apply_cors
from guillotina.traversal import apply_rendering
from guillotina.utils import get_dotted_name
from guillotina.utils import resolve_dotted_name

import asyncio
import enum
import traceback
import uuid


logger = glogging.getLogger("guillotina")


class AppState(enum.IntEnum):

    STARTING = 0
    INITIALIZED = 1
    SHUTDOWN = 2


class AsgiApp:
    def __init__(self, config_file, settings, loop, router):
        self.config_file = config_file
        self.settings = settings
        self.loop = loop
        self.router = router
        self.app = None
        self.on_cleanup = []
        self.state = AppState.STARTING

    def __call__(self, scope, receive=None, send=None):
        """
        ASGI callable compatible with versions 2 and 3
        """

        if receive is None or send is None:

            async def run_asgi2(receive, send):
                return await self.real_asgi_app(scope, receive, send)

            return run_asgi2
        else:
            return self.real_asgi_app(scope, receive, send)

    async def real_asgi_app(self, scope, receive, send):
        if scope["type"] == "http" or scope["type"] == "websocket":
            return await self.handler(scope, receive, send)

        elif scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await self.startup()
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await self.shutdown()
                    await send({"type": "lifespan.shutdown.complete"})
                    return

    async def startup(self):
        if self.state == AppState.INITIALIZED:
            return

        try:
            from guillotina.factory.app import startup_app

            self.loop = self.loop or asyncio.get_event_loop()

            self.app = await startup_app(
                config_file=self.config_file, settings=self.settings, loop=self.loop, server_app=self
            )
            self.next_app = self.build_middleware_stack(self.app.settings)
            self.server_settings = self.app.settings.get("server_settings", {})
            self.state = AppState.INITIALIZED
            return self.app
        except Exception:
            logger.exception("Something crashed during app startup")
            raise

    async def shutdown(self):
        if self.state == AppState.SHUTDOWN:
            return
        for clean in self.on_cleanup:
            await clean(self)
        self.state = AppState.SHUTDOWN

    def build_middleware_stack(self, settings):
        user_middlewares = [ErrorsMiddleware] + [
            resolve_dotted_name(m) for m in settings.get("middlewares", [])
        ]

        # Guillotina is the last middleware in the chain
        last_middleware = Guillotina(self.app, self.router)
        for middleware in reversed(user_middlewares):
            last_middleware = middleware(last_middleware)
        return last_middleware

    async def handler(self, scope, receive, send):
        # Ensure the ASGI server has initialized the server before sending a request
        # Some ASGI servers (i.e. daphne) doesn't implement the lifespan protocol.
        if not self.state == AppState.INITIALIZED:
            raise RuntimeError("The app is not initialized")

        if scope["type"] == "websocket":
            scope["method"] = "GET"

        resp = await self.next_app(scope, receive, send)
        request = task_vars.request.get()

        if scope["type"] != "websocket":
            if not resp.prepared:
                await resp.prepare(request)
                await resp.send_body()

            if not resp.eof_sent:
                await resp.write(eof=True)

        self._cleanup(request, resp)

    def _cleanup(self, request, response):
        try:
            if isinstance(response, Exception):
                traceback.clear_frames(response.__traceback__)
            if response.exc is not None:
                traceback.clear_frames(response.exc.__traceback__)
        except AttributeError:  # pragma: no cover
            pass

        for attr in ("resource", "found_view", "exc"):
            if getattr(request, attr, None) is not None:
                setattr(request, attr, None)

        for attr in ("_cache_data", "_last_read_pos"):
            if hasattr(request, attr):
                delattr(request, attr)


class Guillotina:
    def __init__(self, asgi_app, router):
        self.asgi_app = asgi_app
        self.router = router

    async def __call__(self, scope, receive, send):
        """
        This method always returns a response object or raises a Exception for
        unhandled errors
        """
        request_settings = {
            k: v for k, v in self.asgi_app.server_settings.items() if k in ("client_max_size",)
        }
        request = Request.factory(scope, send, receive, **request_settings)
        task_vars.request.set(request)

        try:
            return await self.request_handler(request)
        except Response as exc:
            return exc
        except Exception as exc:
            # Try to render exception using IErrorResponseException
            eid = uuid.uuid4().hex
            view_result = query_adapter(
                exc, IErrorResponseException, kwargs={"error": "ServiceError", "eid": eid}
            )
            if view_result is not None:
                resp = await apply_rendering(View(None, request), request, view_result)
                return await apply_cors(request, resp)

            # Raise unhandled exceptions to ErrorMiddleware
            raise

    async def request_handler(self, request, retries=0):
        try:
            route = await self.router.resolve(request)
            # The key 'endpoint' in scope is used by sentry-sdk to display
            # the name of the failed view
            if hasattr(route, "view"):
                request.scope["endpoint"] = Endpoint(route.view)
            resp = await route.handler(request)
            return resp

        except (ConflictError, TIDConflictError) as e:
            if self.asgi_app.settings.get("conflict_retry_attempts", 3) > retries:
                label = "DB Conflict detected"
                if isinstance(e, TIDConflictError):
                    label = "TID Conflict Error detected"
                tid = getattr(getattr(request, "_txn", None), "_tid", "not issued")
                logger.debug(f"{label}, retrying request, tid: {tid}, retries: {retries + 1})", exc_info=True)
                request._retry_attempt = retries + 1
                request.clear_futures()
                for var in (
                    "txn",
                    "tm",
                    "futures",
                    "authenticated_user",
                    "security_policies",
                    "container",
                    "registry",
                    "db",
                ):
                    # and make sure to reset various task vars...
                    getattr(task_vars, var).set(None)
                return await self.request_handler(request, retries + 1)
            else:
                txn = task_vars.txn.get()
                logger.warning(
                    "Exhausted retry attempts for conflict error on tid: {}".format(
                        getattr(txn, "_tid", "not issued")
                    )
                )
                raise HTTPConflict()


class Endpoint:
    def __init__(self, view):
        self.__module__ = view.__module__
        self.__qualname__ = get_dotted_name(view).split(".")[-1]
