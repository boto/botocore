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
from tests import BaseClientDriverTest


class TestDoesNotLeakMemory(BaseClientDriverTest):
    # We're making up numbers here, but let's say arbitrarily
    # that the memory can't increase by more than 10MB.
    MAX_GROWTH_BYTES = 10 * 1024 * 1024

    def test_create_single_client_memory_constant(self):
        self.cmd('create_client', 's3')
        self.cmd('free_clients')
        self.record_memory()
        for _ in range(100):
            self.cmd('create_client', 's3')
            self.cmd('free_clients')
        self.record_memory()
        start, end = self.runner.memory_samples
        self.assertTrue((end - start) < self.MAX_GROWTH_BYTES, (end - start))

    def test_create_memory_clients_in_loop(self):
        self.cmd('create_multiple_clients', '200', 's3')
        self.cmd('free_clients')
        self.record_memory()
        # 500 clients in batches of 50.
        for _ in range(10):
            self.cmd('create_multiple_clients', '50', 's3')
            self.cmd('free_clients')
        self.record_memory()
        start, end = self.runner.memory_samples
        self.assertTrue((end - start) < self.MAX_GROWTH_BYTES, (end - start))
