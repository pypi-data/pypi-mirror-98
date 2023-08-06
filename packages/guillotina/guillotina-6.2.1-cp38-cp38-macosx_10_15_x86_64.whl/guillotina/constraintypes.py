from guillotina import app_settings
from guillotina import configure
from guillotina.content import get_cached_factory
from guillotina.interfaces import IConstrainTypes
from guillotina.interfaces import IDatabase
from guillotina.interfaces import IResource
from typing import List
from typing import Optional
from zope.interface import Interface


@configure.adapter(for_=Interface, provides=IConstrainTypes)
class FTIConstrainAllowedTypes:
    def __init__(self, context: IResource) -> None:
        self.context = context

    def is_type_allowed(self, type_id: str) -> bool:
        if type_id in app_settings["container_types"]:
            # Containers cannot be added inside containers
            return False

        allowed_types: Optional[List[str]] = self.get_allowed_types()
        if allowed_types is None:
            # Context does not define allowed types
            return self.is_globally_allowed(type_id)

        return type_id in allowed_types

    def get_allowed_types(self) -> Optional[List[str]]:
        tn = getattr(self.context, "type_name", None)
        if tn:
            factory = get_cached_factory(tn)
            return factory.allowed_types
        return []

    def is_globally_allowed(self, type_id: str) -> bool:
        factory = get_cached_factory(type_id)
        return factory.globally_addable


@configure.adapter(for_=IDatabase, provides=IConstrainTypes)
class DatabaseAllowedTypes:
    """
    Can only add containers to databases
    """

    def __init__(self, context: IResource) -> None:
        self.context = context

    def is_type_allowed(self, type_id: str) -> bool:
        return type_id in app_settings["container_types"]

    def get_allowed_types(self) -> Optional[List[str]]:
        return app_settings["container_types"]
