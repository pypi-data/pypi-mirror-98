# Services

Services are synonymous with what other frameworks might call `endpoints` or `views`.

For the sake of our application, let's use services for getting a user's most
recent conversations and messages for a conversation.


## Creating the services

We'll name our endpoints `@conversations` and `@messages` and put them
in a file named `services.py`.

```python
from guillotina import configure
from guillotina.component import get_multi_adapter
from guillotina.interfaces import IContainer, IResourceSerializeToJsonSummary
from guillotina.utils import get_authenticated_user_id
from guillotina_chat.content import IConversation


@configure.service(context=IContainer, name='@conversations',
                   permission='guillotina.AccessContent')
async def get_conversations(context, request):
    results = []
    conversations = await context.async_get('conversations')
    user_id = get_authenticated_user_id()
    async for conversation in conversations.async_values():
        if user_id in getattr(conversation, 'users', []):
            summary = await get_multi_adapter(
                (conversation, request),
                IResourceSerializeToJsonSummary)()
            results.append(summary)
    results = sorted(results, key=lambda conv: conv['creation_date'])
    return results


@configure.service(context=IConversation, name='@messages',
                   permission='guillotina.AccessContent')
async def get_messages(context, request):
    results = []
    async for message in context.async_values():
        summary = await get_multi_adapter(
            (message, request),
            IResourceSerializeToJsonSummary)()
        results.append(summary)
    results = sorted(results, key=lambda mes: mes['creation_date'])
    return results
```

And make sure to add the scan.

```python
configure.scan('guillotina_chat.services')
```

These endpoints manually go through the content in the database and retrieve
the results for you. This is to demonstration some interaction with objects
and the database with services; however, you can do the same as what is
going on here with the `@search` endpoint.

Make sure `guillotina.contrib.catalog.pg` is listed in your `config.json` file.

```json
{
    "applications": [
        "guillotina.contrib.catalog.pg"
    ]
}
```

For example:

```
GET @search?type_name=Conversation
```

and...

```
GET @search?type_name=Message
```

You can take this further to query by dates and the text of the message as well.

```
GET @search?type_name=Message&text=foobar&creation_date__gte=2019-10-20T15:30:27.580369+00:00
```
