from guillotina import configure
from guillotina.api.service import Service
from guillotina.component import get_multi_adapter
from guillotina.component import get_utilities_for
from guillotina.component import query_utility
from guillotina.interfaces import IContainer
from guillotina.interfaces import IFactorySerializeToJson
from guillotina.interfaces import IResourceFactory
from guillotina.response import HTTPNotFound


@configure.service(
    context=IContainer,
    method="GET",
    permission="guillotina.AccessContent",
    name="@types",
    summary="Read information on available types",
    responses={
        "200": {
            "description": "Result results on types",
            "content": {"application/json": {"schema": {"properties": {}}}},
        }
    },
)
async def get_all_types(context, request):
    types = [x[1] for x in get_utilities_for(IResourceFactory)]
    result = []
    for x in types:
        serializer = get_multi_adapter((x, request), IFactorySerializeToJson)

        result.append(await serializer())
    return result


@configure.service(
    context=IContainer,
    method="GET",
    permission="guillotina.AccessContent",
    name="@types/{type_name}",
    summary="Read information on available types",
    parameters=[{"in": "path", "name": "type_name", "required": True, "schema": {"type": "string"}}],
    responses={
        "200": {
            "description": "Result results on types",
            "content": {"application/json": {"schema": {"properties": {}}}},
        }
    },
)
class Read(Service):
    async def prepare(self):
        type_name = self.request.matchdict["type_name"]
        self.value = query_utility(IResourceFactory, name=type_name)
        if self.value is None:
            raise HTTPNotFound(content={"reason": f"Could not find type {type_name}", "type_name": type_name})

    async def __call__(self):
        serializer = get_multi_adapter((self.value, self.request), IFactorySerializeToJson)

        return await serializer()
