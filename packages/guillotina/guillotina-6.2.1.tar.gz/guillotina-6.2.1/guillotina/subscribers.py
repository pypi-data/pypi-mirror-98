from datetime import datetime
from dateutil.tz import tzutc
from guillotina import configure
from guillotina.component._api import get_component_registry
from guillotina.component.interfaces import ComponentLookupError
from guillotina.component.interfaces import IObjectEvent
from guillotina.interfaces import IObjectModifiedEvent
from guillotina.interfaces import IResource


_zone = tzutc()


@configure.subscriber(for_=(IResource, IObjectModifiedEvent))
def modified_object(obj, event):
    """Set the modification date of an object."""
    now = datetime.now(tz=_zone)
    obj.modification_date = now


@configure.subscriber(for_=IObjectEvent)
async def object_event_notify(event):
    """Dispatch ObjectEvents to interested adapters."""
    try:
        sitemanager = get_component_registry()
    except ComponentLookupError:
        # Oh blast, no site manager. This should *never* happen!
        return []

    return await sitemanager.adapters.asubscribers((event.object, event), None)
