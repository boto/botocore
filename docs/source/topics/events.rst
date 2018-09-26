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
events are listed as ``event-name.<service>.<operations>``, in which
``<service>`` and ``<operation>`` are replaced with a specific service and
operation, for example ``event-name.s3.ListObjects``.

* ``'before-call.<service>.<operation>'``
* ``'before-send.<service>.<operation>'``
* ``'after-call.<service>.<operation>'``


before-call
~~~~~~~~~~~~~~~~~~~~~

:Full Event Name:
  ``'before-call.<service>.<operation>'``

:Description:
  This event is emitted when an operation is called and provides access to the
  parameters that will be passed when calling the operation.

:Keyword Arguments Emitted:

  :type params: dict
  :param params: A dictionary representing the keyword arguments that will be
                 used to invoke the operation call.

  :type context: dict
  :param context: A dictionary representing the operation context. Additional
                  information can be stored in this context to share state
                  between events for the operation call.

:Expected Return Value: A tuple of (http_response, parsed_response) where the
                        http_response is of type :class:`.AWSResponse` and
                        parsed_response is of type dict.


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


after-call
~~~~~~~~~~~~~~~~~~~~~

:Full Event Name:
  ``'after-call.<service>.<operation>'``

:Description:
  This event is emitted after an operation is called and provides access to the
  final HTTP response object as well as the parsed response for the operation.

:Keyword Arguments Emitted:

  :type http_response: :class:`.AWSResponse`
  :param http_response: An object representing the HTTP response.

  :type parsed: dict
  :param parsed: A dictionary representing the fully parsed result of calling
                 the operation.

  :type context: dict
  :param context: A dictionary representing the operation context. Additional
                  information can be stored in this context to share state
                  between events for the operation call.

:Expected Return Value: A tuple of (http_response, parsed_response) where the
                        http_response is of type :class:`.AWSResponse` and
                        parsed_response is of type dict.


Event Emission
--------------

When an event is emitted, the handlers are invoked in the order that they were
registered.
