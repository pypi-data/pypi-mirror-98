# Interfaces

Guillotina uses interfaces to abstract and define various things including
content. Interfaces are useful when defining API contracts, using inheritance,
defining schema/behaviors and being able to define which content your services
are used for.

In the services example, you'll notice the use of `context=IContainer` for the service
decorator configuration. In that case, it is used to tell Guillotina that the
service is only defined for a container object.

Read the [zope.interface documentation](https://zopeinterface.readthedocs.io/en/latest/)
for more details about the power of designing around around interfaces
and to learn more about how to use it.
