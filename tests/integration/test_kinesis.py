# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from uuid import uuid4
from tests import unittest, random_chars

from nose.plugins.attrib import attr

import botocore.session


class TestKinesisListStreams(unittest.TestCase):

    REGION = 'us-east-1'

    def setUp(self):
        self.client = self.session.create_client('kinesis', self.REGION)

    @classmethod
    def setUpClass(cls):
        cls.session = botocore.session.get_session()
        cls.stream_name = 'botocore-test-%s' % random_chars(10)
        client = cls.session.create_client('kinesis', cls.REGION)
        client.create_stream(StreamName=cls.stream_name,
                             ShardCount=1)
        waiter = client.get_waiter('stream_exists')
        waiter.wait(StreamName=cls.stream_name)

    @classmethod
    def tearDownClass(cls):
        client = cls.session.create_client('kinesis', cls.REGION)
        client.delete_stream(StreamName=cls.stream_name)

    def test_list_streams(self):
        parsed = self.client.list_streams()
        self.assertIn('StreamNames', parsed)

    @attr('slow')
    def test_can_put_stream_blob(self):
        unique_data = str(uuid4())
        self.client.put_record(
            StreamName=self.stream_name, PartitionKey='foo', Data=unique_data)
        # Give it a few seconds for the record to get into the stream.
        records = self.wait_for_stream_data()
        self.assert_record_data_contains(records, unique_data.encode('ascii'))
        self.assertTrue(len(records['Records']) > 0)
        self.assertEqual(records['Records'][0]['Data'], b'foobar')

    @attr('slow')
    def test_can_put_records_single_blob(self):
        unique_data = str(uuid4())
        self.client.put_records(
            StreamName=self.stream_name,
            Records=[{
                'Data': unique_data,
                'PartitionKey': 'foo'
            }]
        )
        records = self.wait_for_stream_data()
        self.assert_record_data_contains(records, unique_data.encode('ascii'))

    @attr('slow')
    def test_can_put_records_multiple_blob(self):
        self.client.put_records(
            StreamName=self.stream_name,
            Records=[{
                'Data': 'foobar',
                'PartitionKey': 'foo'
            }, {
                'Data': 'barfoo',
                'PartitionKey': 'foo'
            }]
        )
        records = self.wait_for_stream_data()
        self.assert_record_data_contains(records, b'foobar', b'barfoo')

    def wait_for_stream_data(self, num_attempts=6, poll_time=10):
        # Poll until we get records returned from get_records().
        for i in range(num_attempts):
            time.sleep(poll_time)
            stream = self.client.describe_stream(StreamName=self.stream_name)
            shard = stream['StreamDescription']['Shards'][0]
            shard_iterator = self.client.get_shard_iterator(
                StreamName=self.stream_name, ShardId=shard['ShardId'],
                ShardIteratorType='TRIM_HORIZON')
            records = self.client.get_records(
                ShardIterator=shard_iterator['ShardIterator'])
            if records['Records']:
                return records
        raise RuntimeError("Unable to retrieve data from kinesis stream after "
                           "%s attempts with delay of %s seconds."
                           % (num_attempts, poll_time))

    def assert_record_data_contains(self, records, *expected):
        record_data = [r['Data'] for r in records['Records']]
        for item in expected:
            self.assertIn(item, record_data)


if __name__ == '__main__':
    unittest.main()
