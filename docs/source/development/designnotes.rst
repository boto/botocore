Design Notes for Botocore
=========================

This document outlines the rationale behind various design
decisions in botocore.


Casing of Arguments
-------------------

One of the most noticeable differences between botocore and boto
is that the client objects 1) require parameters to be provided
as ``**kwargs`` and 2) require the arguments typically be provided as
``CamelCased`` values.

For example::

    ddb = session.create_client('dynamodb')
    ddb.describe_table(TableName='mytable')

In boto, the equivalent code would be::

    layer1.describe_table(table_name='mytable')

There are several reasons why this was changed in botocore.

The first reason was because we wanted to have the same casing for
inputs as well as outputs.  In both boto and botocore, the response
for the ``describe_table`` calls is::

    {'Table': {'CreationDateTime': 1393007077.387,
                'ItemCount': 0,
                'KeySchema': {'HashKeyElement': {'AttributeName': 'foo',
                                                 'AttributeType': 'S'}},
                'ProvisionedThroughput': {'ReadCapacityUnits': 5,
                                          'WriteCapacityUnits': 5},
                'TableName': 'testtable',
                'TableStatus': 'ACTIVE'}}

Notice that the response is ``CamelCased``.  This makes it more difficult
to round trip results.  In many cases you want to get the result of
a ``describe*`` call and use that value as input through a corresponding
``update*`` call.  If the input arguments require ``snake_casing`` but
the response data is ``CamelCased`` then you will need to manually convert
all the response elements back to ``snake_case`` in order to properly
round trip.

This makes the case for having consistent casing for both input and
output.  Why not use ``snake_casing`` for input as well as output?

We choose to use ``CamelCasing`` because this is the casing used by
AWS services.  As a result, we don't have to do any translation from
``CamelCasing`` to ``snake_casing``.  We can use the response values
exactly as they are returned from AWS services.

This also means that if you are reading the AWS API documentation
for services, the names and casing referenced there will match
what you would provide to botocore.  For example, here's the
corresponding API documentation for
`dynamodb.describe_table
<http://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DescribeTable.html>`__.
