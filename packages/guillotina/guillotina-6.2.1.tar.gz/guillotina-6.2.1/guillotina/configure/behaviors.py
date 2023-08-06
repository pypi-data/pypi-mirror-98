from guillotina.interfaces import IBehavior
from guillotina.interfaces import IBehaviorAdapterFactory
from zope.interface import implementer
from zope.interface import Interface


REGISTRATION_REPR = """\
<{class} {name} at {id}
  schema: {identifier}
  marker: {marker}
  factory: {factory}
  title: {title}
  {description}
>"""


@implementer(IBehavior)
class BehaviorRegistration(object):
    def __init__(self, title, description, interface, marker, factory, name=None, for_=Interface):
        self.title = title
        self.description = description
        self.interface = interface
        self.marker = marker
        self.factory = factory
        self.name = name
        self.for_ = for_

    def __repr__(self):
        if self.marker is not None:
            marker_info = self.marker.__identifier__
        elif self.marker is not self.interface:
            marker_info = "(uses schema as marker)"
        else:
            marker_info = "(no marker is set)"
        info = {
            "class": self.__class__.__name__,
            "id": id(self),
            "name": self.name or "(unique name not set)",
            "identifier": self.interface.__identifier__,
            "marker": marker_info,
            "factory": str(self.factory),
            "title": self.title or "(no title)",
            "description": self.description or "(no description)",
        }
        return REGISTRATION_REPR.format(**info)


@implementer(IBehaviorAdapterFactory)
class BehaviorAdapterFactory(object):
    def __init__(self, behavior):
        self.behavior = behavior

    def __call__(self, context):
        if self.behavior.factory is not None:
            adapted = self.behavior.factory(context)
        else:
            # When no factory is specified the object should provide the
            # behavior directly
            adapted = context
        return adapted
