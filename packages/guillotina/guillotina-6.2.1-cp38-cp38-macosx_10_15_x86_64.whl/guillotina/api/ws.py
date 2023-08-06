from guillotina import configure
from guillotina import logger
from guillotina import routes
from guillotina import task_vars
from guillotina._settings import app_settings
from guillotina.api.service import Service
from guillotina.auth.extractors import BasicAuthPolicy
from guillotina.component import get_utility
from guillotina.component import query_multi_adapter
from guillotina.interfaces import IApplication
from guillotina.interfaces import IContainer
from guillotina.interfaces import IPermission
from guillotina.interfaces import IResponse
from guillotina.request import WebSocketJsonDecodeError
from guillotina.security.utils import get_view_permission
from guillotina.transactions import get_tm
from guillotina.utils import get_jwk_key
from guillotina.utils import get_security_policy
from jwcrypto import jwe
from jwcrypto.common import json_encode
from urllib import parse

import orjson
import time


@configure.service(
    context=IContainer,
    method="GET",
    permission="guillotina.UseWebSockets",
    name="@wstoken",
    summary="Return a web socket token",
    responses={
        "200": {
            "description": "The new token",
            "content": {"application/json": {"schema": {"properties": {"token": {"type": "string"}}}}},
        }
    },
)
@configure.service(
    context=IApplication,
    method="GET",
    permission="guillotina.UseWebSockets",
    name="@wstoken",
    summary="Return a web socket token",
    responses={
        "200": {
            "description": "The new token",
            "content": {"application/json": {"schema": {"properties": {"token": {"type": "string"}}}}},
        }
    },
)
class WebsocketGetToken(Service):
    _websockets_ttl = 60

    def generate_websocket_token(self, real_token, data=None):
        data = data or {}
        claims = {
            "iat": int(time.time()),
            "exp": int(time.time() + self._websockets_ttl),
            "token": real_token,
        }
        claims.update(data)
        payload = orjson.dumps(claims)
        jwetoken = jwe.JWE(payload, json_encode({"alg": "A256KW", "enc": "A256CBC-HS512"}))
        jwetoken.add_recipient(get_jwk_key())
        token = jwetoken.serialize(compact=True)
        return token

    async def __call__(self):
        # Get token
        header_auth = self.request.headers.get("AUTHORIZATION")
        token = None
        data = {}
        if header_auth is not None:
            schema, _, encoded_token = header_auth.partition(" ")
            if schema.lower() == "basic":
                # special case, we need to hash passwd here...
                policy = BasicAuthPolicy(self.request)
                extracted = await policy.extract_token(header_auth)
                data["id"] = extracted["id"]
                token = extracted["token"]
            elif schema.lower() == "bearer":
                token = encoded_token

        # Create ws token
        new_token = self.generate_websocket_token(token, data)
        return {"token": new_token}


@configure.service(
    context=IContainer,
    method="GET",
    permission="guillotina.AccessContent",
    name="@ws",
    summary="Make a web socket connection",
)
class WebsocketsView(Service):
    async def handle_ws_request(self, ws, message):
        method = app_settings["http_methods"]["GET"]
        try:
            frame_id = message["id"]
        except KeyError:
            frame_id = "0"

        parsed = parse.urlparse(message.get("path", message.get("value")))
        path = tuple(p for p in parsed.path.split("/") if p)

        from guillotina.traversal import traverse

        obj, tail = await traverse(self.request, task_vars.container.get(), path)

        if tail and len(tail) > 0:
            # convert match lookups
            view_name = routes.path_to_view_name(tail)
        elif not tail:
            view_name = ""
        else:
            raise

        permission = get_utility(IPermission, name="guillotina.AccessContent")

        security = get_security_policy()
        allowed = security.check_permission(permission.id, obj)
        if not allowed:
            return await ws.send_bytes(orjson.dumps({"error": "Not allowed"}))

        try:
            view = query_multi_adapter((obj, self.request), method, name=view_name)
        except AttributeError:
            view = None

        try:
            view.__route__.matches(self.request, tail or [])
        except (KeyError, IndexError):
            view = None

        if view is None:
            return await ws.send_bytes(orjson.dumps({"error": "Not found", "id": frame_id}))

        ViewClass = view.__class__
        view_permission = get_view_permission(ViewClass)
        if not security.check_permission(view_permission, view):
            return await ws.send_bytes(orjson.dumps({"error": "No view access", "id": frame_id}))

        if hasattr(view, "prepare"):
            view = (await view.prepare()) or view

        view_result = await view()
        if IResponse.providedBy(view_result):
            raise Exception("Do not accept raw ASGI exceptions in ws")
        else:
            from guillotina.traversal import apply_rendering

            resp = await apply_rendering(view, self.request, view_result)

        # Return the value, body is always encoded
        response_object = orjson.dumps({"data": resp.body.decode("utf-8"), "id": frame_id})
        await ws.send_bytes(response_object)

        # Wait for possible value
        self.request.execute_futures()

    async def __call__(self):
        tm = get_tm()
        await tm.abort()
        ws = self.request.get_ws()
        await ws.prepare()

        async for msg in ws:
            try:
                message = msg.json
            except WebSocketJsonDecodeError:
                # We only care about json messages
                logger.warning("Invalid websocket payload, ignored: {}".format(msg))
                continue

            if message["op"].lower() == "close":
                break
            elif message["op"].lower() == "get":
                txn = await tm.begin()
                try:
                    await self.handle_ws_request(ws, message)
                except Exception:
                    logger.error("Exception on ws", exc_info=True)
                finally:
                    # only currently support GET requests which are *never*
                    # supposed to be commits
                    await tm.abort(txn=txn)

        logger.debug("websocket connection closed")
        await ws.close()
