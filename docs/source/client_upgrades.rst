.. _client-upgrades:

Upgrading to Clients
====================

Background
----------

Version 0.66.0 of botocore added support for clients (10/16/2014)
added initial support for clients.  This provided an alternate
interface to making AWS calls that provided a number of benefits over
the existing interface.  At the time, both interfaces were added
so that users could opt in to trying the new clients.

Below is an example of the old interface:

.. code-block:: python

    import botocore.session
    session = botocore.session.get_session()
    s3 = session.get_service('s3')
    endpoint = s3.get_endpoint('us-west-2')
    list_objects = s3.get_operation('ListObjects')
    http, response = list_objects.call(endpoint, Bucket='mybucket')
    if http.status_code == 200:
        print("Contents: %s" % response['Contents])
    else:
        print("API call failed, status code: %s, error: %s" % (
            http.status_code, http.content))


Here's an example of the newer (preferred) client interface:

.. code-block:: python

    import botocore.session
    session = botocore.session.get_session()
    s3 = session.create_client('s3', 'us-west-2')
    response = s3.list_objects(Bucket='mybucket')
    print("Contents: %s" % response['Contents'])


While there are many improvements with the new interface, here's
a few notable improvements:

* Less boilerplate.  With clients, the ``Endpoints`` are abstracted
  from the user.  The ``Operations`` are also abstracted.  The user
  only needs to deal with a single class, the client class.
* Exceptions.  With clients, exceptions are raised on failed requests.
  You do not have to check the error code of the http response object
* Return values.  The http response is abstracted from the user.  The
  client method makes an API call and returns a simple python dict.
* More granular context.  Clients allow you to have a context that's
  smaller than on a Service/Operation.  For example, you can now
  create a client and add specific customizations and event handlers
  that apply to only that specific client, instead of any S3 client.


Deprecation Timeline
--------------------

Botocore has not had a GA (1.0) release yet.  In version 1.0,
the Service/Operation object **will be removed**.  Leading
up to 1.0, we will be deprecating the old interface according
to this schedule:

* (**done**) Version 0.66.0 introduced client
* (**done**) Version 0.96.0 emitted a ``PendingDeprecationWarning`` when using
  the old interface.  By default, these warnings are not printed to
  stderr.  A developer will need to opt in to these warnings to
  see any emitted warnings.
* (**done**) Version 0.99.0 emitted a ``DeprecationWarning`` when using
  the old interface.  This has the same behavior as
  ``PendingDeprecationWarning``, in which by default nothing is
  printed to stderr.
* Version 0.104.0 emitted an ``ImminentRemovalWarning`` when using
  the old interface.  This warning is now printed to stderr by default.
  A user can still turn off these warnings via the ``warnings`` module.
* The ``develop`` branch on github will be updated to completely remove
  the old interface.  At this point the client interface will be the
  only interface available when using the ``develop`` branch on github.
* A 1.0 alpha version will be released.  By default, ``pip`` will not
  pick up any alpha/beta releases.
* A 1.0 beta version will be released.
* A GA (1.0) version of botocore will be released.


How To Upgrade
==============

Migrating to clients is straightforward.  This section outlines how
to upgrade and some common scenarios and how to upgrade.

Keyword Arg Casing
------------------

In botocore's old interface, kwargs could either be snake_cased or
CamelCased and botocore would map them to the correct version needed
by the service which is CamelCase.

Botocore's client interface accepts **only** CamelCased args.  More
specifically, botocore uses the same casing used by the respective
AWS service.  Most AWS services uses CamelCasing.  Some AWS services
use lowerCamelCase.

**Old**

.. code-block:: python

    list_objects.call(endpoint, bucket='foo', key='bar')

**New**

.. code-block:: python

    client.list_objects(Bucket='foo', Key='bar')


Connection Pooling
------------------

In the old interface, the connection pooling was tied to an endpoint
object.  To reuse existing HTTP connection, you needed to keep a reference
to the endpoint objects.  With clients, connection pooling is tied to a client.
Use a single client to make multiple API calls.

**Old**

.. code-block:: python

    service = session.get_service('s3')
    endpoint = service.get_endpoint('us-west-2')
    operation = service.get_operation('ListObjects')
    head_object = service.get_operation('HeadObject')
    parsed = operation.call(endpoint, Bucket='mybucket')[1]
    for obj in parsed['Contents']:
        name = obj['Key']
        # Use existing connection be passing in the same endpoint.
        print(head_object.call(endpoint, Bucket='mybucket', Key=name))

**New**

.. code-block:: python

    s3 = session.get_client('s3', 'us-west-2')
    for obj in s3.list_objects(Bucket='mybucket')['Contents']:
        name = obj['Key']
        # Using the same client will reuse any existing HTTP
        # connections the client was using.
        print(s3.head_object(Bucket='mybucket', Key=name))


Operation and Method Names
--------------------------

In the old interface, you would retrieve an API operation using the
casing defined by the service, which is typically CamelCase.  For example,
you'd use ``service.get_operation('ListObjects')``, not
``service.get_operation('list_objects')``.  With clients, method names,
which map 1 - 1 to operation names are snake_cased, as is common in python
code.


**Old**

.. code-block:: python

    service = session.get_service('s3')
    list_objects = service.get_operation('ListObjects')
    head_object = service.get_operation('HeadObject')
    get_object = service.get_operation('GetObject')

**New**

.. code-block:: python

    s3 = session.get_client('s3', 'us-west-2')
    list_objects = s3.list_objects
    head_object = s3.head_object
    get_object = s3.get_object



Return Values
-------------

In the old interface, the return value for an ``operation.call`` invocation is
a tuple of the HTTP response object, and the parsed dict that results from
parsing the HTTP object.  In the client interface, only the parsed
response is returned.  The HTTP response object is not returned.

**Old**

.. code-block:: python

    ec2 = session.get_service('ec2')
    endpoint = ec2.get_endpoint('ec2')
    describe_instances = ec2.get_operation('DescribeInstances')
    http, parsed = describe_instances.call(endpoint)

**New**

.. code-block:: python

    ec2 = session.get_client('ec2', 'us-west-2')
    parsed = ec2.describe_instances()

The main reason for returning the HTTP response was to check if an
error occurred via the HTTP response status code.  This is now no longer
required (discussed below).  Exception are automatically raised.

Note that if for some reason you do need to see the response status code,
it is available via the ``ResponseMetadata`` in the parsed dict that's
returned.

.. code-block:: python

    ec2 = session.get_client('ec2', 'us-west-2')
    parsed = ec2.describe_instances()
    print("The status code is:",
          parsed['ResponseMetadata']['HTTPStatusCode']))


Error Handling
--------------

With clients, exceptions are now raised on any non 2xx response.
A ``ClientError`` exception has both a ``.msg`` attribute as well
as the parsed error response (which is a dictionary).  There isn't
really equivalent functionality in the old interface, but below is
an example of how you can handle an error:

**New**

.. code-block:: python

    from botocore.exceptions import ClientError

    ec2 = session.get_client('ec2', 'us-west-2')
    try:
        parsed = ec2.describe_instances(InstanceIds=['i-badid'])
    except ClientError as e:
        logger.error("Received error: %s", e, exc_info=True)
        # Only worry about a specific service error code
        if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
            raise

If you run into any issues migrating from the old interface to the newer
client interface, please file an issue on github and let us know.  We'd
be happy to help.
