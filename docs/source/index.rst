Welcome to botocore
===================

Botocore is a low-level interface to a growing number of Amazon Web
Services.  Botocore serves as the foundation for the
`AWS-CLI <https://github.com/aws/aws-cli/>`_ command line utilities.
It will also play an important role in the boto3.x project.

The botocore package is compatible with Python versions 2.6.5, Python 2.7.x,
and Python 3.3.x and higher.


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
