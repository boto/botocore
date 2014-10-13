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
import time
import random
from tests import unittest

import botocore.session
from botocore.client import ClientError


class TestWaiterLegacy(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.service = self.session.get_service('dynamodb')
        self.endpoint = self.service.get_endpoint('us-west-2')

    def test_create_table_and_wait(self):
        table_name = 'botocoretestddb-%s' % random.randint(1, 10000)
        operation = self.service.get_operation('CreateTable')
        http, parsed = operation.call(
            self.endpoint, TableName=table_name,
            ProvisionedThroughput={"ReadCapacityUnits": 5,
                                   "WriteCapacityUnits": 5},
            KeySchema=[{"AttributeName": "foo", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "foo",
                                   "AttributeType": "S"}])
        if http.status_code != 200:
            self.fail("Could not create table.")
        self.addCleanup(self.service.get_operation("DeleteTable").call,
                        self.endpoint, TableName=table_name)
        waiter = self.service.get_waiter('TableExists', self.endpoint)
        waiter.wait(TableName=table_name)
        parsed = self.service.get_operation('DescribeTable').call(
            self.endpoint, TableName=table_name)[1]
        self.assertEqual(parsed['Table']['TableStatus'], 'ACTIVE')


# This is the same test as above, except using the client interface.
class TestWaiterForDynamoDB(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('dynamodb', 'us-west-2')

    def test_create_table_and_wait(self):
        table_name = 'botocoretestddb-%s' % random.randint(1, 10000)
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
