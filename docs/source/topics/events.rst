Botocore Events
===============

Botocore will emit events during various parts of its execution.  Users of the
library can register handlers (callables) for these events, such that whenever
an event is emitted, all registered handlers for the event will be called.
This allows you to customize and extend the behavior of botocore without having
to modify the internals.  This document covers this event system in detail.

Session Events
--------------

The main interface for events is through the :class:`botocore.session.Session`
class.  The ``Session`` object allows you to register and unregister handlers
to events.


Event Types
-----------

The list below shows all of the events emitted by botocore.  In some cases, the
events are listed as ``event-name.<service-id>.<operations>``, in which
``<service-id>`` and ``<operation>`` are replaced with a specific service
identifier operation, for example ``event-name.s3.ListObjects``.

* ``'before-send.<service-id>.<operation>'``


before-send
~~~~~~~~~~~~~~~~~~~~~

:Full Event Name:
  ``'before-send.<service>.<operation>'``

:Description:
  This event is emitted when the operation has been fully serialized, signed,
  and is ready to be sent across the wire. This event allows the finalized
  request to be inspected and allows a response to be returned that fufills
  the request. If no response is returned botocore will fulfill the request
  as normal.

:Keyword Arguments Emitted:

  :type request: :class:`.AWSPreparedRequest`
  :param params: An object representing the properties of an HTTP request.

:Expected Return Value: None or an instance of :class:`.AWSResponse`


Event Emission
--------------

When an event is emitted, the handlers are invoked in the order that they were
registered.


Service ID
----------
To get the service id from a service client use the following::

    import botocore
    import botocore.session

    session = botocore.session.Session()
    client = session.create_client('elbv2')
    service_event_name = client.meta.service_model.service_id.hyphenize()
