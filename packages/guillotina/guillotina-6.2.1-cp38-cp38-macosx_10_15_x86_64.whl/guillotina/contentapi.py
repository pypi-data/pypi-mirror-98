from guillotina import task_vars
from guillotina._settings import app_settings
from guillotina.auth.users import RootUser
from guillotina.auth.utils import set_authenticated_user
from guillotina.component import get_multi_adapter
from guillotina.db.interfaces import ITransaction
from guillotina.interfaces import ACTIVE_LAYERS_KEY
from guillotina.interfaces import IContainer
from guillotina.interfaces import IResource
from guillotina.tests.utils import get_mocked_request
from guillotina.utils import get_authenticated_user
from guillotina.utils import get_object_url
from guillotina.utils import get_registry
from guillotina.utils import import_class
from guillotina.utils import navigate_to
from zope.interface import alsoProvides

import typing


class ContentAPI:
    def __init__(self, db, user=RootUser("root")):
        self.db = db
        self.tm = None
        self.request = None
        self.old_request = None
        self.old_db = None
        self.old_user = None
        self.old_tm = None
        self.user = user
        self._active_txn = None

    async def __aenter__(self):
        self.old_request = task_vars.request.get()
        self.old_db = task_vars.db.get()
        self.old_tm = task_vars.tm.get()
        self.old_user = get_authenticated_user()
        self.request = get_mocked_request()
        task_vars.db.set(self.db)
        self.tm = self.db.get_transaction_manager()
        task_vars.tm.set(self.tm)
        set_authenticated_user(self.user)
        return self

    async def __aexit__(self, *args):
        task_vars.request.set(self.old_request)
        task_vars.db.set(self.old_db)
        task_vars.tm.set(self.old_tm)
        set_authenticated_user(self.old_user)
        # make sure to close out connection
        await self.abort()

    async def use_container(self, container: IContainer):
        task_vars.registry.set(None)
        task_vars.container.set(container)
        registry = await get_registry(container)
        if registry is not None:
            layers = registry.get(ACTIVE_LAYERS_KEY, [])
            for layer in layers:
                alsoProvides(self.request, import_class(layer))

    async def get_transaction(self) -> ITransaction:
        if self._active_txn is None:
            self._active_txn = await self.tm.begin()
            task_vars.txn.set(self._active_txn)
        return self._active_txn

    async def create(self, payload: dict, in_: IResource = None) -> IResource:
        await self.get_transaction()
        if in_ is None:
            in_ = self.db
        view = get_multi_adapter((in_, self.request), app_settings["http_methods"]["POST"], name="")

        async def json():
            return payload

        self.request.json = json
        resp = await view()
        await self.commit()
        path = resp.headers["Location"]
        if path.startswith("http://") or path.startswith("https://"):
            # strip off container prefix
            container_url = get_object_url(in_, self.request)  # type: ignore
            path = path[len(container_url or "") :]
        return await navigate_to(in_, path.strip("/"))  # type: ignore

    async def get(self, path: str, in_: IResource = None) -> typing.Optional[IResource]:
        await self.get_transaction()
        if in_ is None:
            in_ = self.db
        try:
            return await navigate_to(in_, path.strip("/"))  # type: ignore
        except KeyError:
            return None

    async def delete(self, ob):
        await self.get_transaction()
        parent = ob.__parent__
        await parent.async_del(ob.__name__)
        await self.commit()

    async def commit(self):
        if self._active_txn is None:
            return
        await self.tm.commit(txn=self._active_txn)
        self.request.execute_futures()
        self._active_txn = None
        await self.get_transaction()

    async def abort(self):
        if self._active_txn is None:
            return
        await self.tm.abort(txn=self._active_txn)
        self._active_txn = None
        await self.get_transaction()
