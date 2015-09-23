# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import os
from tests import BaseClientDriverTest, random_chars, temporary_file

import botocore.session


def random_content(num_megabytes, filename):
    with open(filename, 'wb') as f:
        # Write out a 50MB file.
        for _ in range(num_megabytes):
            f.write(os.urandom(1024 * 1024))
        f.flush()


class TestAPICallsDontLeakMemory(BaseClientDriverTest):
    # We're making up numbers here, but let's say arbitrarily
    # that the memory can't increase by more than 10MB.
    MAX_GROWTH_BYTES = 5 * 1024 * 1024

    def setUp(self):
        self.session = botocore.session.get_session()
        super(TestAPICallsDontLeakMemory, self).setUp()

    def collect_memory_until_finished(self):
        while not self.driver.is_cmd_finished():
            time.sleep(1)
            self.record_memory()

    def create_bucket(self):
        bucket_name = random_chars(12)
        client = self.session.create_client('s3')
        client.create_bucket(Bucket=bucket_name)
        self.addCleanup(client.delete_bucket, Bucket=bucket_name)
        return bucket_name

    def test_create_single_client_memory_constant(self):
        self.cmd('make_aws_request', '10', 'ec2', 'describe_instances')
        self.record_memory()
        self.cmd('make_aws_request', '100', 'ec2', 'describe_instances')
        self.record_memory()
        start, end = self.memory_samples
        self.assertTrue((end - start) < self.MAX_GROWTH_BYTES, (end - start))

    def test_streaming_upload_have_constant_memory(self):
        bucket_name = self.create_bucket()
        client = self.session.create_client('s3')
        with temporary_file('wb') as f:
            random_content(num_megabytes=50, filename=f.name)
            self.send_cmd('stream_s3_upload', bucket_name, 'foo',
                                 f.name)
            self.collect_memory_until_finished()
            client.delete_object(Bucket=bucket_name, Key='foo')
        memory = self.memory_samples
        mem_range = max(memory) - min(memory)
        # We should have O(1) memory growth, but we'll allow
        # up to a 1MB range.
        self.assertTrue(mem_range < self.MAX_GROWTH_BYTES, mem_range)

    def test_streaming_downloads_have_constant_memory(self):
        bucket_name = self.create_bucket()
        client = self.session.create_client('s3')
        with temporary_file('wb') as f:
            random_content(num_megabytes=50, filename=f.name)
            with open(f.name, 'rb') as upload_file:
                client.put_object(Bucket=bucket_name, Key='foo',
                                  Body=upload_file)
                self.addCleanup(client.delete_object, Bucket=bucket_name,
                                Key='foo')
            download_filename = f.name + '.download'
            self.send_cmd('stream_s3_download', bucket_name,
                                 'foo', download_filename)
            self.collect_memory_until_finished()
        memory = self.memory_samples
        mem_range = max(memory) - min(memory)
        self.assertTrue(mem_range < self.MAX_GROWTH_BYTES, mem_range)
