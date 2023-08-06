from guillotina import configure
from guillotina.i18n import MessageFactory


_ = MessageFactory("guillotina.contrib.dbusers")


app_settings = {
    "auth_user_identifiers": ["guillotina.contrib.dbusers.users.DBUserIdentifier"],
    "auth_validation_tasks": {
        "register_user": {
            "executor": "guillotina.contrib.dbusers.register_user",
            "schema": {"title": "Register new user", "type": "object", "properties": {}},
        }
    },
    "min_username_length": 3,
}


def includeme(root, settings):
    configure.scan("guillotina.contrib.dbusers.content.users")
    configure.scan("guillotina.contrib.dbusers.content.groups")
    configure.scan("guillotina.contrib.dbusers.install")
    configure.scan("guillotina.contrib.dbusers.services")
    configure.scan("guillotina.contrib.dbusers.subscribers")
    configure.scan("guillotina.contrib.dbusers.permissions")
    configure.scan("guillotina.contrib.dbusers.serializers")
    configure.scan("guillotina.contrib.dbusers.adapters")
