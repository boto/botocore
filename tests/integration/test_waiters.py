# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from tests import unittest, random_chars
from tests.integration.test_s3 import random_bucketname, clear_out_bucket

from nose.plugins.attrib import attr

import botocore.session
from botocore.exceptions import WaiterError

import logging
LOG = logging.getLogger('botocore.tests.integration')

# This is the same test as above, except using the client interface.
@attr('slow')
class TestWaiterForDynamoDB(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('dynamodb', 'us-west-2')

    def test_create_table_and_wait(self):
        table_name = 'botocoretest-%s' % random_chars(10)
        self.client.create_table(
            TableName=table_name,
            ProvisionedThroughput={"ReadCapacityUnits": 5,
                                   "WriteCapacityUnits": 5},
            KeySchema=[{"AttributeName": "foo", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "foo",
                                   "AttributeType": "S"}])
        self.addCleanup(self.client.delete_table, TableName=table_name)
        waiter = self.client.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        parsed = self.client.describe_table(TableName=table_name)
        self.assertEqual(parsed['Table']['TableStatus'], 'ACTIVE')


class TestCanGetWaitersThroughClientInterface(unittest.TestCase):
    def test_get_ses_waiter(self):
        # We're checking this because ses is not the endpoint prefix
        # for the service, it's email.  We want to make sure this does
        # not affect the lookup process.
        session = botocore.session.get_session()
        client = session.create_client('ses', 'us-east-1')
        # If we have at least one waiter in the list, we know that we have
        # actually loaded the waiters and this test has passed.
        self.assertTrue(len(client.waiter_names) > 0)


class TestMatchersWithErrors(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client(
            'ec2', region_name='us-west-2')

    def test_dont_search_on_error_responses(self):
        """Test that InstanceExists can handle a nonexistent instance."""
        waiter = self.client.get_waiter('instance_exists')
        waiter.config.max_attempts = 1
        with self.assertRaises(WaiterError):
            waiter.wait(InstanceIds=['i-12345'])


@attr('slow')
class TestWaiterForAthena(unittest.TestCase):
    REGION = 'us-west-2'

    @classmethod
    def setUpClass(cls):
        cls.output_bucket = random_bucketname()
        cls.output_location = 's3://{}/'.format(cls.output_bucket)
        cls.session = botocore.session.get_session()
        s3 = cls.session.create_client('s3')
        waiter = s3.get_waiter('bucket_exists')
        try:
            s3.create_bucket(Bucket=cls.output_bucket,
                             CreateBucketConfiguration={
                                 'LocationConstraint': cls.REGION
                             })
        except Exception as e:
            # A create_bucket can fail for a number of reasons.
            # We're going to defer to the waiter below to make the
            # final call as to whether or not the bucket exists.
            LOG.debug("create_bucket() raised an exception: %s", e, exc_info=True)
        waiter.wait(Bucket=cls.output_bucket)

    @classmethod
    def tearDownClass(cls):
        clear_out_bucket(cls.output_bucket, cls.REGION, True)

    def setUp(self):
        self.client = self.session.create_client(
            'athena', region_name=self.REGION)

    def test_waiter_query_succeeded(self):
        """Test query_succeeded waiter"""
        query = self.client.start_query_execution(
            QueryString='SELECT current_date',
            ResultConfiguration={
                'OutputLocation': self.output_location
            }
        )
        query_id = query['QueryExecutionId']
        waiter = self.client.get_waiter('query_succeeded')
        waiter.wait(QueryExecutionId=query_id)
        execution = self.client.get_query_execution(QueryExecutionId=query_id)
        self.assertEqual(execution['QueryExecution']['Status']['State'], 'SUCCEEDED')

    def test_waiter_query_succeeded_error(self):
        """Test query_succeeded waiter failed case"""
        # Without QueryExecutionContext["Database"], this query is doomed to fail
        query = self.client.start_query_execution(
            QueryString='SELECT * FROM non_existent_table',
            ResultConfiguration={
                'OutputLocation': self.output_location
            }
        )
        query_id = query['QueryExecutionId']
        waiter = self.client.get_waiter('query_succeeded')
        with self.assertRaises(WaiterError):
            waiter.wait(QueryExecutionId=query_id)

    def test_waiter_queries_finished(self):
        """Test queries_finished waiter."""
        query_1 = self.client.start_query_execution(
            QueryString='SELECT current_date',
            ResultConfiguration={
                'OutputLocation': self.output_location
            }
        )
        # Without QueryExecutionContext["Database"], this query is doomed to fail
        query_2 = self.client.start_query_execution(
            QueryString='SELECT * FROM non_existent_table',
            ResultConfiguration={
                'OutputLocation': self.output_location
            }
        )
        query_ids = [query_1['QueryExecutionId'], query_2['QueryExecutionId']]
        waiter = self.client.get_waiter('queries_finished')
        # It comes back after all queries either processed or can't be processed.
        waiter.wait(QueryExecutionIds=query_ids)
        execution = self.client.batch_get_query_execution(QueryExecutionIds=query_ids)
        self.assertNotEqual(execution['QueryExecutions'][0]['Status']['State'], 'RUNNING')
        self.assertNotEqual(execution['QueryExecutions'][1]['Status']['State'], 'RUNNING')


