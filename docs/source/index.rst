Welcome to botocore
===================

Botocore is a low-level interface to a growing number of Amazon Web
Services.  Botocore serves as the foundation for the
`AWS-CLI <https://github.com/aws/aws-cli/>`_ command line utilities.
It will also play an important role in the boto3.x project.

The botocore package is compatible with Python versions Python 3.8
and higher.


Contents:

.. toctree::
   :maxdepth: 2
   :glob:

   tutorial/index
   reference/*
   topics/index
   development/index


Upgrade Notes
=============

Upgrading to 1.12.0
-------------------

What Changed
~~~~~~~~~~~~

The botocore event system was changed to emit events based on the service id
rather than the endpoint prefix or service name.

Why Was The Change Was Made
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This was done to handle several issues that were becoming increasingly
problematic:

* Services changing their endpoint prefix would cause some registered events to
  no longer fire (but not all).
* New services that launch using an endpoint that another service is using
  won't be able to be uniquely selected. There are a number of cases of this
  already.
* Services whose client name and endpoint prefix differed would require two
  different strings if you want to register against all events.

How Do I Know If I'm Impacted
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Any users relying on registering an event against one service impacting other
services are impacted. You can consult the following table to see if you are
impacted. If you are registering an event using one of the event parts in the
leftmost column with the intention of impacting an unintended target service
in the rightmost column, then you are impacted and will need to update.

+----------------------+-------------------------+---------------------------------------------------+
| Event Part           | Intended Target Service | Unintended Target Services                        |
+----------------------+-------------------------+---------------------------------------------------+
| rds                  | rds                     | neptune                                           |
+----------------------+-------------------------+---------------------------------------------------+
| autoscaling          | autoscaling             | application-autoscaling, autoscaling-plans        |
+----------------------+-------------------------+---------------------------------------------------+
| kinesisvideo         | kinesisvideo            | kinesis-video-media, kinesis-video-archived-media |
+----------------------+-------------------------+---------------------------------------------------+
| elasticloadbalancing | elb                     | elbv2                                             |
+----------------------+-------------------------+---------------------------------------------------+

For example, if you are registering an event against
``before-call.elasticloadbalancing`` expecting it to run when making calls with
an ``elbv2`` client, you will be impacted.

If you are registering an event against one of the services in the Unintended
Targets column, you may be impacted if you were relying on those events not
firing.

If you are registering events using ``*`` in the service place, or are
registering against any service not in this table, you will not need a code
change. In many cases the actual event name will have changed, but for services
without shared endpoints we do the work of translating the event name at
registration and emission time. In future versions of botocore we will remove
this translation, so you may wish to update your code anyway.

How Do I Update My Code
~~~~~~~~~~~~~~~~~~~~~~~

You will need to look at the events you are registering against and determine
which services you wish to impact with your handler. If you only wish to
impact the intended target service (as defined in the above table), then you
don't need to change the event. If you wish to impact another service in
addition to the intended target service, you will need to register a new event
using that service's event name. Similarly, if you wish to impact another
service instead you will simply need to change the event you are registered
against.

To get the new event name, consult this table:

+------------------------------+----------------------+------------------------------+
| Service                      | Old Event Name       | New Event Name               |
+------------------------------+----------------------+------------------------------+
| application-autoscaling      | autoscaling          | application-auto-scaling     |
+------------------------------+----------------------+------------------------------+
| autoscaling-plans            | autoscaling          | auto-scaling-plans           |
+------------------------------+----------------------+------------------------------+
| elbv2                        | elasticloadbalancing | elastic-load-balancing       |
+------------------------------+----------------------+------------------------------+
| kinesis-video-archived-media | kinesisvideo         | kinesis-video-archived-media |
+------------------------------+----------------------+------------------------------+
| kinesis-video-media          | kinesisvideo         | kinesis-video-media          |
+------------------------------+----------------------+------------------------------+
| neptune                      | rds                  | neptune                      |
+------------------------------+----------------------+------------------------------+

Additionally, you can get the new event name in code like so::

    from botocore.session import Session

    session = Session()
    client = session.create_client('elbv2')
    service_event_name = client.meta.service_model.service_id.hyphenize()

Armed with the service event name, simply replace the old service name in the
handler with the new service event name. If you were registering an event
against ``before-call.autoscaling`` intending to impact ``autoscaling-plans``
for example, you would instead register against
``before-call.auto-scaling-plans``.

If you are registering an event against one of the services in the Unintended
Targets column, you will now see those events getting fired where previously
they were not. While this is enabling that expected behavior, this still
represents a change in actual behavior. You should not need to update your
code, but you should test to ensure that you are seeing the behavior you want.

Upgrading to 1.11.0
---------------------
* The vendored versions of ``requests`` and ``urllib3`` are no longer being
  used and have been replaced with a direct dependency on upstream ``urllib3``
  and ``requests`` is no longer a dependency of ``botocore``.  While these
  vendored dependencies are still in the ``botocore`` package they should not
  be used as they will be removed in the future. Any code that imports from
  ``botocore.vendored.requests.*`` should be updated accordingly. Specifically,
  the use of ``botocore.vendored.requests.exceptions.*`` or
  ``botocore.vendored.requests.packages.urllib3.exceptions.*`` must be updated
  to the corresponding exception classes in ``botocore.exceptions``.
* The version of ``urllib3`` used to make HTTP requests has been updated from
  v1.10.4 to the range >=1.20,<1.24.

Upgrading to 1.0.0rc1
---------------------

* The ``default`` argument to ``session.get_config_variable()`` has been
  removed.  If you need this functionality you can use::

        value = session.get_config_variable() or 'default value'

Upgrading to 0.104.0
--------------------

* Warnings about imminent removal of service/operation objects are
  now printed to stderr by default.  It is highly encouraged that
  you switch to clients as soon as possible, as the deprecated
  service/operation object is going away.  See :ref:`client-upgrades`
  for more information.


Upgrading to 0.66.0
-------------------

* The ``before-call`` and ``after-call`` events have been changed
  such that their ``model`` for the operation is sent instead of the
  ``operation`` object itself.
* The interface to waiters via ``Service.get_waiter`` has changed.
  An endpoint is now required when creating the waiter via ``get_waiter()``
  instead of when calling the waiter ``waiter.wait(endpoint, **kwargs)``.


Upgrading to 0.65.0
-------------------

* ``get_scoped_config()`` will now include credentials from the
  shared credentials file (``~/.aws/credentials``) if present.

Upgrading to 0.64.0
-------------------

* ``botocore.parameters`` has been split into several different modules
  (``validate``, ``serialize``, and ``model``).  If you were using the
  ``Operation.call`` method, you are unaffected by this change.
* A ``botocore.client`` module has been added.  This is the preferred
  interface into botocore going forward.
* Response keys that are no longer in the HTTP response are not mapped
  to default values in the response dict.
* ``ResponseMetadata`` is now always added to any successful response
* ``Errors`` has been switch from a list of errors to a single ``Error``
  key.  Also consistently populate the ``Error`` dict on errors.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
