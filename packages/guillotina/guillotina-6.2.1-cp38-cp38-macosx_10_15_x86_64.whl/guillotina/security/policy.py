from guillotina import configure
from guillotina.auth.users import SystemUser
from guillotina.component import get_utility
from guillotina.component import query_adapter
from guillotina.db.orm.interfaces import IBaseObject
from guillotina.interfaces import Allow
from guillotina.interfaces import AllowSingle
from guillotina.interfaces import Deny
from guillotina.interfaces import IGroups
from guillotina.interfaces import IInheritPermissionMap
from guillotina.interfaces import IPrincipal
from guillotina.interfaces import IPrincipalPermissionMap
from guillotina.interfaces import IPrincipalRoleMap
from guillotina.interfaces import IRolePermissionMap
from guillotina.interfaces import ISecurityPolicy
from guillotina.interfaces import IView
from guillotina.interfaces import Public
from guillotina.interfaces import Unset
from guillotina.profile import profilable
from guillotina.security.security_code import principal_permission_manager
from guillotina.security.security_code import principal_role_manager
from guillotina.security.security_code import role_permission_manager
from lru import LRU
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


code_principal_permission_setting = principal_permission_manager.get_setting
code_roles_for_permission = role_permission_manager.get_roles_for_permission
code_roles_for_principal = principal_role_manager.get_roles_for_principal
code_principals_for_permission = principal_permission_manager.get_principals_for_permission

SettingAsBoolean = {Allow: True, Deny: False, Unset: None, AllowSingle: "o", None: None}


SettingType = Union[bool, None, str]


def level_setting_as_boolean(level, value) -> SettingType:
    # We want to check if its allow
    let = SettingAsBoolean[value]
    # Never return False on AllowSingle
    # If level is not o Allow single should not be taken care
    return level == let or None if type(let) is str else let


class CacheEntry:
    pass


@configure.adapter(for_=IPrincipal, provides=ISecurityPolicy)
class SecurityPolicy:
    def __init__(self, principal: IPrincipal):
        self.principal = principal
        self._cache = LRU(100)

    def invalidate_cache(self):
        self._cache.clear()

    @profilable
    def check_permission(self, permission, obj):
        # Always allow public attributes
        if permission == Public:
            return True

        if IView.providedBy(obj):
            obj = obj.__parent__

        # Iterate through participations ('principals')
        # and check permissions they give
        if self.principal is not None:

            # System user always has access
            if self.principal is SystemUser:
                return True

            # Check the permission
            groups = getattr(self.principal, "groups", None) or []
            if self.cached_decision(obj, self.principal.id, groups, permission):
                return True

        return False

    def cache(self, parent, level=""):
        serial = getattr(parent, "__serial__", "")
        oid = getattr(parent, "__uuid__", "")
        cache_key = f"{id(parent)}-{oid}-{serial}-{level}"
        cache = self._cache.get(cache_key)
        if cache is None:
            cache = CacheEntry()
            self._cache[cache_key] = cache
        return cache

    @profilable
    def cached_decision(self, parent, principal, groups, permission):
        # Return the decision for a principal and permission
        cache = self.cache(parent)
        try:
            cache_decision = cache.decision
        except AttributeError:
            cache_decision = cache.decision = {}

        cache_decision_prin = cache_decision.get(principal)
        if not cache_decision_prin:
            cache_decision_prin = cache_decision[principal] = {}

        try:
            return cache_decision_prin[permission]
        except KeyError:
            pass

        # cache_decision_prin[permission] is the cached decision for a
        # principal and permission.

        # Check direct permissions
        # First recursive function to get the permissions of a principal
        decision = self.cached_principal_permission(parent, principal, groups, permission, "o")

        if decision is not None:
            cache_decision_prin[permission] = decision
            return decision

        # Check Roles permission
        # First get the Roles needed
        roles = cached_roles(parent, permission, "o")
        if roles:
            # Get the roles from the user
            prin_roles = self.cached_principal_roles(parent, principal, groups, "o")
            for role, setting in prin_roles.items():
                if setting and (role in roles):
                    cache_decision_prin[permission] = decision = True
                    return decision

        cache_decision_prin[permission] = decision = False
        return decision

    @profilable
    def cached_principal_permission(self, parent, principal, groups, permission, level):
        # Compute the permission, if any, for the principal.
        cache = self.cache(parent, level)

        try:
            # We need to caches for first level and Allow Single
            if level == "o":
                cache_prin = cache.prino
            else:
                cache_prin = cache.prin
        except AttributeError:
            if level == "o":
                cache_prin = cache.prino = {}
            else:
                cache_prin = cache.prin = {}

        cache_prin_per = cache_prin.get(principal)
        if not cache_prin_per:
            cache_prin_per = cache_prin[principal] = {}

        try:
            return cache_prin_per[permission]
        except KeyError:
            pass

        # We reached the end of the recursive we check global / local
        if parent is None:
            # We check the global configuration of the user and groups
            prinper = self._global_permissions_for(principal, permission)
            if prinper is not None:
                cache_prin_per[permission] = prinper
                return prinper

            # If we did not found the permission for the user look at code
            prinper = SettingAsBoolean[code_principal_permission_setting(permission, principal, None)]
            # Now look for the group ids
            if prinper is None:
                for group in groups:
                    prinper = SettingAsBoolean[code_principal_permission_setting(permission, group, None)]
                    if prinper is not None:
                        continue
            cache_prin_per[permission] = prinper
            return prinper

        # Get the local map of the permissions
        # As we want to quit as soon as possible we check first locally
        prinper_map = IPrincipalPermissionMap(parent, None)
        if prinper_map is not None:
            prinper = level_setting_as_boolean(level, prinper_map.get_setting(permission, principal, None))
            if prinper is None:
                for group in groups:
                    prinper = level_setting_as_boolean(
                        level, prinper_map.get_setting(permission, group, None)
                    )
                    if prinper is not None:
                        # Once we conclude we exit
                        # May happen that first group Deny and second
                        # allows which will result on Deny for the first
                        break
            if prinper is not None:
                return prinper

        perminhe = query_adapter(parent, IInheritPermissionMap)
        if perminhe is None or perminhe.get_inheritance(permission) is Allow:
            parent = getattr(parent, "__parent__", None)
            prinper = self.cached_principal_permission(parent, principal, groups, permission, "p")
            cache_prin_per[permission] = prinper
            return prinper
        else:
            return None

    def global_principal_roles(self, principal, groups):
        roles = dict(
            [(role, SettingAsBoolean[setting]) for (role, setting) in code_roles_for_principal(principal)]
        )
        for group in groups:
            for role, settings in code_roles_for_principal(group):
                roles[role] = SettingAsBoolean[settings]
        roles["guillotina.Anonymous"] = True  # Everybody has Anonymous

        # First the global roles from user + group
        groles = self._global_roles_for(principal)
        roles.update(groles)
        return roles

    def cached_principal_roles(self, parent, principal, groups, level):
        # Redefine it to get global roles
        cache = self.cache(parent, level)
        try:
            cache_principal_roles = cache.principal_roles
        except AttributeError:
            cache_principal_roles = cache.principal_roles = {}
        try:
            return cache_principal_roles[principal]
        except KeyError:
            pass

        # We reached the end so we go to see the global ones
        if parent is None:
            # Then the code roles
            roles = self.global_principal_roles(principal, groups)

            cache_principal_roles[principal] = roles
            return roles

        roles = self.cached_principal_roles(getattr(parent, "__parent__", None), principal, groups, "p")

        # We check the local map of roles
        prinrole = IPrincipalRoleMap(parent, None)

        if prinrole:
            roles = roles.copy()
            for role, setting in prinrole.get_roles_for_principal(principal):
                roles[role] = level_setting_as_boolean(level, setting)
            for group in groups:
                for role, setting in prinrole.get_roles_for_principal(group):
                    roles[role] = level_setting_as_boolean(level, setting)

        cache_principal_roles[principal] = roles
        return roles

    def _global_roles_for(self, principal):
        """On a principal (user/group) get global roles."""
        roles = {}
        groups = get_utility(IGroups)
        if self.principal and principal == self.principal.id:
            # Its the actual user id
            # We return all the global roles (including group)
            roles = self.principal.roles.copy()

            for group in self.principal.groups:
                roles.update(groups.get_principal(group, self.principal).roles)
            return roles

        # We are asking for group id so only group roles
        if groups:
            group = groups.get_principal(principal)
            return group.roles.copy()

    def _global_permissions_for(self, principal, permission):
        """On a principal (user + group) get global permissions."""
        groups = get_utility(IGroups)
        if self.principal and principal == self.principal.id:
            # Its the actual user
            permissions = self.principal.permissions.copy()
            if permission in permissions:
                return level_setting_as_boolean("p", permissions[permission])

            for group in self.principal.groups:
                permissions = groups.get_principal(group, self.principal).permissions
                if permission in permissions:
                    return level_setting_as_boolean("p", permissions[permission])
        return None


def cached_roles(parent: Optional[IBaseObject], permission: str, level: str) -> Dict[str, int]:
    """
    Get the roles for a specific permission.
    Global + Local + Code
    """
    if parent is None:
        roles = dict(
            [(role, 1) for (role, setting) in code_roles_for_permission(permission) if setting is Allow]
        )
        return roles

    try:
        cache = parent.__volatile__.setdefault("security_cache", {})
    except AttributeError:
        cache = {}
    try:
        cache_roles = cache["roles"]
    except KeyError:
        cache_roles = cache["roles"] = {}
    try:
        return cache_roles[permission + level]
    except KeyError:
        pass

    perminhe = query_adapter(parent, IInheritPermissionMap)

    if perminhe is None or perminhe.get_inheritance(permission) is Allow:
        roles = cached_roles(getattr(parent, "__parent__", None), permission, "p")
    else:
        # We don't apply global permissions also
        # Its dangerous as may lead to an object who nobody can see
        roles = dict()

    roleper = query_adapter(parent, IRolePermissionMap)
    if roleper is not None:
        roles = roles.copy()
        for role, setting in roleper.get_roles_for_permission(permission):
            if setting is Allow:
                roles[role] = 1
            elif setting is AllowSingle and level == "o":
                roles[role] = 1
            elif setting is Deny and role in roles:
                del roles[role]

    cache_roles[permission + level] = roles
    return roles


def cached_principals(
    parent: Optional[IBaseObject], roles: List[str], permission: str, level: str
) -> Dict[str, int]:
    """Get the principals for a specific permission.

    Global + Local + Code
    """
    if parent is None:
        principals = dict(
            [(role, 1) for (role, setting) in code_principals_for_permission(permission) if setting is Allow]
        )
        return principals

    try:
        cache = parent.__volatile__.setdefault("security_cache", {})
    except AttributeError:
        cache = {}
    try:
        cache_principals = cache["principals"]
    except KeyError:
        cache_principals = cache["principals"] = {}
    try:
        return cache_principals[permission + level]
    except KeyError:
        pass

    perminhe = query_adapter(parent, IInheritPermissionMap)

    if perminhe is None or perminhe.get_inheritance(permission) is Allow:
        principals = cached_principals(getattr(parent, "__parent__", None), roles, permission, "p")
    else:
        # We don't apply global permissions also
        # Its dangerous as may lead to an object who nobody can see
        principals = dict()

    prinperm = IPrincipalPermissionMap(parent, None)
    if prinperm:
        principals = principals.copy()
        for principal, setting in prinperm.get_principals_for_permission(permission):
            if setting is Allow:
                principals[principal] = 1
            elif setting is AllowSingle and level == "o":
                principals[principal] = 1
            elif setting is Deny and principal in principals:
                del principals[principal]

    prinrole = IPrincipalRoleMap(parent, None)
    if prinrole:
        for role in roles:
            for principal, setting in prinrole.get_principals_for_role(role):
                if setting is Allow:
                    principals[principal] = 1
                elif setting is AllowSingle and level == "o":
                    principals[principal] = 1
                elif setting is Deny and principal in principals:
                    del principals[principal]

    cache_principals[permission + level] = principals
    return principals
