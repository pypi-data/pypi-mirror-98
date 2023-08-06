# Install an addons

Guillotina differentiates `applications` from `addons`.

An application is a python package you install into your environment and add to
your list of applications in the configuration file.

Addons on the otherhand are when you want to perform installation logic into
a container.


## Define addon

To define an addon for Guillotina, we use the `@configure.addon` decorator
in the `install.py` file.

For our case, we want to create a Folder with all our conversations with some
default permissions.


```python
from guillotina import configure
from guillotina.addons import Addon
from guillotina.content import create_content_in_container
from guillotina.interfaces import IRolePermissionManager


@configure.addon(
    name="guillotina_chat",
    title="Guillotina server application python project")
class ManageAddon(Addon):

    @classmethod
    async def install(cls, container, request):
        roleperm = IRolePermissionManager(container)
        roleperm.grant_permission_to_role_no_inherit(
            'guillotina.AccessContent', 'guillotina.Member')

        if not await container.async_contains('conversations'):
            conversations = await create_content_in_container(
                container, 'Folder', 'conversations',
                id='conversations', creators=('root',),
                contributors=('root',))
            roleperm = IRolePermissionManager(conversations)
            roleperm.grant_permission_to_role(
                'guillotina.AddContent', 'guillotina.Member')
            roleperm.grant_permission_to_role(
                'guillotina.AccessContent', 'guillotina.Member')

    @classmethod
    async def uninstall(cls, container, request):
        registry = task_vars.registry.get()  # noqa
        # uninstall logic here...
```

## Testing

Then, using Postman, do a `POST` request to the `@addons` endpoint:

```eval_rst
..  http:example:: curl wget httpie python-requests

    POST /db/container/@addons HTTP/1.1
    Accept: application/json
    Authorization: Basic cm9vdDpyb290
    Content-Type: application/json
    Host: localhost:8080

    {
        "id": "guillotina_chat"
    }
```
