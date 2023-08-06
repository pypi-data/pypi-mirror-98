# Async Utilities

An async utility is an object instantiation with an async function that is run
persistently on the asyncio event loop. It is useful for long running tasks.

For our training, we're going to use an async utility with a queue to send
messages to logged in users.

Create a `utility.py` file and put the following code in it.

```python
from guillotina.async_util import IAsyncUtility
from guillotina.component import get_multi_adapter
from guillotina.interfaces import IResourceSerializeToJsonSummary
from guillotina.utils import get_authenticated_user_id, get_current_request

import asyncio
import orjson
import logging

logger = logging.getLogger('guillotina_chat')


class IMessageSender(IAsyncUtility):
    pass


class MessageSenderUtility:

    def __init__(self, settings=None, loop=None):
        self._loop = loop
        self._settings = {}
        self._webservices = []
        self._closed = False

    def register_ws(self, ws, request):
        ws.user_id = get_authenticated_user_id()
        self._webservices.append(ws)

    def unregister_ws(self, ws):
        self._webservices.remove(ws)

    async def send_message(self, message):
        summary = await get_multi_adapter(
            (message, get_current_request()),
            IResourceSerializeToJsonSummary)()
        await self._queue.put((message, summary))

    async def finalize(self):
        self._closed = True

    async def initialize(self, app=None):
        self._queue = asyncio.Queue()

        while not self._closed:
            try:
                message, summary = await asyncio.wait_for(self._queue.get(), 0.2)
                for user_id in message.__parent__.users:
                    for ws in self._webservices:
                        if ws.user_id == user_id:
                            await ws.send_str(orjson.dumps(summary))
            except (RuntimeError, asyncio.CancelledError, asyncio.TimeoutError):
                pass
            except Exception:
                logger.warning(
                    'Error sending message',
                    exc_info=True)
                await asyncio.sleep(1)
```


Async utilities must implement an `initialize` method that performs the async
task. In our case, it is creating a queue and waiting to process messages
in the queue.

We will use this to send messages to registered websockets.

Like all other configured modules, make sure this file is scanned
by the packages `__init__.py` file.

Additionally, async utilities need to also be configured in `__init__.py`:

```python
app_settings = {
    "load_utilities": {
        "guillotina_chat.message_sender": {
            "provides": "guillotina_chat.utility.IMessageSender",
            "factory": "guillotina_chat.utility.MessageSenderUtility",
            "settings": {}
        },
    }
}
```

## Sending messages

We'll need to add another event subscriber to the `subscribers.py` file
in order for the utility to know to send out new messages to registered
web services.So your `subscribers.py` file will now look like:

```
from guillotina import configure
from guillotina.component import get_utility
from guillotina.interfaces import IObjectAddedEvent, IObjectModifiedEvent, IPrincipalRoleManager
from guillotina.utils import get_authenticated_user_id, get_current_request
from guillotina_chat.content import IConversation, IMessage
from guillotina_chat.utility import IMessageSender


@configure.subscriber(for_=(IConversation, IObjectAddedEvent))
@configure.subscriber(for_=(IConversation, IObjectModifiedEvent))
async def container_added(conversation, event):
    user_id = get_authenticated_user_id()
    if user_id not in conversation.users:
        conversation.users.append(user_id)

    manager = IPrincipalRoleManager(conversation)
    for user in conversation.users:
        manager.assign_role_to_principal(
            'guillotina_chat.ConversationParticipant', user)


@configure.subscriber(for_=(IMessage, IObjectAddedEvent))
async def message_added(message, event):
    utility = get_utility(IMessageSender)
    await utility.send_message(message)
```
