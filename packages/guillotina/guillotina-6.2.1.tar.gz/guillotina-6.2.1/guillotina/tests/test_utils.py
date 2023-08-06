from guillotina import utils
from guillotina.behaviors.dublincore import IDublinCore
from guillotina.interfaces import IPrincipalRoleManager
from guillotina.interfaces import IResource
from guillotina.tests.utils import create_content
from guillotina.tests.utils import get_mocked_request
from guillotina.tests.utils import get_root
from guillotina.tests.utils import login
from guillotina.utils import get_behavior
from guillotina.utils.navigator import Navigator

import json
import pytest


def test_module_resolve_path():
    assert utils.resolve_module_path("guillotina") == "guillotina"
    assert utils.resolve_module_path("guillotina.tests") == "guillotina.tests"
    assert utils.resolve_module_path("..test_queue") == "guillotina.tests.test_queue"
    assert utils.resolve_module_path("....api") == "guillotina.api"


class FooBar(object):
    pass


def test_dotted_name():
    assert utils.get_dotted_name(FooBar()) == "guillotina.tests.test_utils.FooBar"
    assert utils.get_dotted_name(FooBar) == "guillotina.tests.test_utils.FooBar"
    assert utils.get_module_dotted_name(FooBar()) == "guillotina.tests.test_utils"
    assert utils.get_module_dotted_name(FooBar) == "guillotina.tests.test_utils"
    assert utils.get_dotted_name(IResource) == "guillotina.interfaces.content.IResource"


@pytest.mark.asyncio
async def test_get_content_path(container_requester):
    async with container_requester as requester:
        response, status = await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Item", "title": "Item1", "id": "item1"})
        )
        assert status == 201
        root = await get_root(db=requester.db)
        tm = requester.db.get_transaction_manager()
        txn = await tm.begin()
        container = await root.async_get("guillotina")
        obj = await container.async_get("item1")
        assert utils.get_content_path(container) == "/"
        assert utils.get_content_path(obj) == "/item1"
        await tm.abort(txn=txn)


@pytest.mark.asyncio
async def test_get_content_depth(container_requester):
    async with container_requester as requester:
        response, status = await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Item", "title": "Item1", "id": "item1"})
        )
        assert status == 201
        root = await get_root(db=requester.db)
        tm = requester.db.get_transaction_manager()
        txn = await tm.begin()
        container = await root.async_get("guillotina")
        obj = await container.async_get("item1")
        assert utils.get_content_depth(container) == 1
        assert utils.get_content_depth(obj) == 2
        await tm.abort(txn=txn)


def test_valid_id():
    assert utils.valid_id("FOObar")
    assert utils.valid_id("FooBAR-_-.")
    assert not utils.valid_id("FooBar-_-.,")
    assert not utils.valid_id("FooBar-_-.@#")
    assert not utils.valid_id("FooBar-_-.?")
    assert not utils.valid_id("..")
    assert not utils.valid_id(".")


def test_get_owners(dummy_guillotina, mock_txn):
    content = create_content()
    roleperm = IPrincipalRoleManager(content)
    roleperm.assign_role_to_principal("guillotina.Owner", "foobar")
    assert utils.get_owners(content) == ["foobar"]
    roleperm.assign_role_to_principal("guillotina.Owner", "foobar2")
    assert utils.get_owners(content) == ["foobar", "foobar2"]


def test_get_authenticated_user_without_request(dummy_guillotina):
    login()
    assert utils.get_authenticated_user() is not None


def _test_empty_func():
    return True


def _test_some_args(foo, bar):
    return foo, bar


def _test_some_kwargs(foo=None, bar=None):
    return foo, bar


def _test_some_stars(foo, bar=None, **kwargs):
    return foo, bar, kwargs


def test_lazy_apply():
    assert utils.lazy_apply(_test_empty_func, "blah", foo="bar")
    assert utils.lazy_apply(_test_some_args, "foo", "bar") == ("foo", "bar")
    assert utils.lazy_apply(_test_some_args, "foo", "bar", "ldkfks", "dsflk") == ("foo", "bar")
    assert utils.lazy_apply(_test_some_kwargs, "foo", bar="bar") == ("foo", "bar")
    assert utils.lazy_apply(_test_some_kwargs, "foo", bar="bar", rsdfk="ldskf") == ("foo", "bar")
    assert utils.lazy_apply(_test_some_stars, "foo", "blah", bar="bar", another="another") == (
        "foo",
        "bar",
        {"another": "another"},
    )


def test_get_random_string():
    utils.get_random_string()


def test_merge_dicts():
    result = utils.merge_dicts({"foo": {"foo": 2}}, {"bar": 5, "foo": {"bar": 3}})
    assert result["foo"]["foo"] == 2
    assert result["foo"]["bar"] == 3


@pytest.mark.asyncio
async def test_get_containers(container_requester):
    async with container_requester:
        containers = [c async for c in utils.get_containers()]
        assert len(containers) > 0


def test_safe_unidecode():
    assert "foobar" == utils.safe_unidecode(b"foobar")


@pytest.mark.asyncio
async def test_object_utils(container_requester):
    async with container_requester as requester:
        response, status = await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Item", "title": "Item1", "id": "item1"})
        )
        assert status == 201
        request = get_mocked_request(db=requester.db)
        root = await get_root(db=requester.db)
        tm = requester.db.get_transaction_manager()
        txn = await tm.begin()
        container = await root.async_get("guillotina")

        ob = await utils.get_object_by_uid(response["@uid"], txn)
        assert ob is not None
        assert ob.__uuid__ == response["@uid"]

        ob2 = await utils.navigate_to(container, "item1")
        assert ob2.__uuid__ == ob.__uuid__

        url = utils.get_object_url(ob, request)
        assert url.endswith("item1")

        await tm.abort(txn=txn)


@pytest.mark.asyncio
async def test_run_async():
    def _test():
        return "foobar"

    assert await utils.run_async(_test) == "foobar"


@pytest.mark.asyncio
async def test_navigator_preload(container_requester):
    async with container_requester as requester:
        response, status = await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Item", "title": "Item1", "id": "item1"})
        )
        assert status == 201
        root = await get_root(db=requester.db)
        tm = requester.db.get_transaction_manager()
        txn = await tm.begin()
        container = await root.async_get("guillotina")
        item1 = await container.async_get("item1")
        item1.title = "Item1bis"
        txn.register(item1)

        nav = Navigator(txn, container)
        item1_bis = await nav.get("/item1")

        assert item1_bis.title == "Item1bis"
        assert item1_bis is item1

        await tm.abort(txn=txn)


@pytest.mark.asyncio
async def test_navigator_get(container_requester):
    async with container_requester as requester:
        response, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps({"@type": "Folder", "title": "Folder1", "id": "folder1"}),
        )
        response, status = await requester(
            "POST",
            "/db/guillotina/folder1",
            data=json.dumps({"@type": "Folder", "title": "Folder2", "id": "folder2"}),
        )
        response, status = await requester(
            "POST", "/db/guillotina", data=json.dumps({"@type": "Item", "title": "Item0", "id": "item0"})
        )
        response, status = await requester(
            "POST",
            "/db/guillotina/folder1",
            data=json.dumps({"@type": "Item", "title": "Item1", "id": "item1"}),
        )
        response, status = await requester(
            "POST",
            "/db/guillotina/folder1/folder2",
            data=json.dumps({"@type": "Item", "title": "Item2", "id": "item2"}),
        )
        assert status == 201
        root = await get_root(db=requester.db)
        tm = requester.db.get_transaction_manager()
        txn = await tm.begin()
        container = await root.async_get("guillotina")
        item0 = await container.async_get("item0")
        txn.delete(item0)

        nav = Navigator(txn, container)
        item1 = await nav.get("/folder1/item1")
        assert item1.__name__ == "item1"
        item1_bis = await nav.get("/folder1/item1")
        item2 = await nav.get("/folder1/folder2/item2")
        folder2 = await nav.get("/folder1/folder2")
        assert item2.__parent__ is folder2
        assert item1_bis is item1

        nav.delete(item2)
        assert await nav.get("/folder1/folder2/item2") is None
        assert await nav.get("/folder1/item0") is None

        await tm.abort(txn=txn)


@pytest.mark.asyncio
async def test_get_behavior(container_requester):
    async with container_requester as requester:
        response, status = await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Item", "title": "Item1", "id": "item1"})
        )
        assert status == 201
        root = await get_root(db=requester.db)
        tm = requester.db.get_transaction_manager()
        txn = await tm.begin()
        container = await root.async_get("guillotina")
        item1 = await container.async_get("item1")
        behavior = await get_behavior(item1, IDublinCore)
        assert behavior is not None

        await tm.abort(txn=txn)


def test_bad_passphrase():
    assert utils.secure_passphrase("foobar agian something good here!")
    assert not utils.secure_passphrase("secret")
    assert not utils.secure_passphrase("secret123")
    assert not utils.secure_passphrase("DKK@7328*!&@@")
