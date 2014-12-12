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
import random
from tests import unittest

import botocore.session


class TestKinesisListStreams(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('kinesis', 'us-east-1')
        self.stream_name = 'botocore-test-%s-%s' % (int(time.time()),
                                                    random.randint(1, 100))

    def test_list_streams(self):
        parsed = self.client.list_streams()
        self.assertIn('StreamNames', parsed)

    def test_can_put_stream_blob(self):
        self.client.create_stream(StreamName=self.stream_name,
                                  ShardCount=1)
        waiter = self.client.get_waiter('stream_exists')
        waiter.wait(StreamName=self.stream_name)
        self.addCleanup(self.client.delete_stream,
                        StreamName=self.stream_name)

        self.client.put_record(
            StreamName=self.stream_name, PartitionKey='foo', Data='foobar')
        # Give it a few seconds for the record to get into the stream.
        time.sleep(10)

        stream = self.client.describe_stream(StreamName=self.stream_name)
        shard = stream['StreamDescription']['Shards'][0]
        shard_iterator = self.client.get_shard_iterator(
            StreamName=self.stream_name, ShardId=shard['ShardId'],
            ShardIteratorType='TRIM_HORIZON')

        records = self.client.get_records(
            ShardIterator=shard_iterator['ShardIterator'])
        self.assertTrue(len(records['Records']) > 0)
        self.assertEqual(records['Records'][0]['Data'], b'foobar')

    def test_can_put_records_single_blob(self):
        self.client.create_stream(StreamName=self.stream_name,
                                  ShardCount=1)
        waiter = self.client.get_waiter('stream_exists')
        waiter.wait(StreamName=self.stream_name)
        self.addCleanup(self.client.delete_stream,
                        StreamName=self.stream_name)

        self.client.put_records(
            StreamName=self.stream_name,
            Records=[{
                'Data': 'foobar',
                'PartitionKey': 'foo'
            }]
        )
        # Give it a few seconds for the record to get into the stream.
        time.sleep(10)

        stream = self.client.describe_stream(StreamName=self.stream_name)
        shard = stream['StreamDescription']['Shards'][0]
        shard_iterator = self.client.get_shard_iterator(
            StreamName=self.stream_name, ShardId=shard['ShardId'],
            ShardIteratorType='TRIM_HORIZON')

        records = self.client.get_records(
            ShardIterator=shard_iterator['ShardIterator'])
        self.assertTrue(len(records['Records']) > 0)
        self.assertEqual(records['Records'][0]['Data'], b'foobar')

    def test_can_put_records_multiple_blob(self):
        self.client.create_stream(StreamName=self.stream_name,
                                  ShardCount=1)
        waiter = self.client.get_waiter('stream_exists')
        waiter.wait(StreamName=self.stream_name)
        self.addCleanup(self.client.delete_stream,
                        StreamName=self.stream_name)

        self.client.put_records(
            StreamName=self.stream_name,
            Records=[{
                'Data': 'foobar',
                'PartitionKey': 'foo'
            },{
                'Data': 'barfoo',
                'PartitionKey': 'foo'
            }]
        )
        # Give it a few seconds for the record to get into the stream.
        time.sleep(10)

        stream = self.client.describe_stream(StreamName=self.stream_name)
        shard = stream['StreamDescription']['Shards'][0]
        shard_iterator = self.client.get_shard_iterator(
            StreamName=self.stream_name, ShardId=shard['ShardId'],
            ShardIteratorType='TRIM_HORIZON')

        records = self.client.get_records(
            ShardIterator=shard_iterator['ShardIterator'])
        self.assertTrue(len(records['Records']) == 2)
        #verify that both made it through
        record_data = [r['Data'] for r in records['Records']]
        self.assertItemsEqual(['foobar', 'barfoo'], record_data)

if __name__ == '__main__':
    unittest.main()
