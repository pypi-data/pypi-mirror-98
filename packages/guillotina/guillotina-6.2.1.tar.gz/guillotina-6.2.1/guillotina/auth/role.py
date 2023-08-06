from guillotina._settings import app_settings
from guillotina.component import get_utilities_for
from guillotina.interfaces import IRole
from zope.interface import implementer


@implementer(IRole)
class Role(object):
    def __init__(self, id, title, description="", local=True):
        self.id = id
        self.title = title
        self.description = description
        self.local = local


def check_role(context, role_id):
    names = [name for name, util in get_utilities_for(IRole, context)]
    if role_id not in names:
        raise ValueError(f'Undefined role id "{role_id}"')


def local_roles():
    if "local_roles" in app_settings:
        return app_settings["local_roles"]
    names = [name for name, util in get_utilities_for(IRole) if util.local]
    app_settings["local_roles"] = names
    return names


def global_roles():
    if "global_roles" in app_settings:
        return app_settings["global_roles"]
    names = [name for name, util in get_utilities_for(IRole) if not util.local]
    app_settings["global_roles"] = names
    return names
