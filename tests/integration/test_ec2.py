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
from tests import unittest
import itertools

import botocore.session


class TestEC2(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()

    def test_can_make_request(self):
        # Basic smoke test to ensure we can talk to ec2.
        service = self.session.get_service('ec2')
        endpoint = service.get_endpoint('us-west-2')
        operation = service.get_operation('DescribeAvailabilityZones')
        http, result = operation.call(endpoint)
        zones = list(sorted(a['ZoneName'] for a in result['AvailabilityZones']))
        self.assertEqual(zones, ['us-west-2a', 'us-west-2b', 'us-west-2c'])


class TestEC2Pagination(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.service = self.session.get_service('ec2')
        self.endpoint = self.service.get_endpoint('us-west-2')

    def test_can_paginate(self):
        # Using an operation that we know will paginate.
        operation = self.service.get_operation('DescribeReservedInstancesOfferings')
        generator = operation.paginate(self.endpoint)
        results = list(itertools.islice(generator, 0, 3))
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0][1]['NextToken'] != results[1][1]['NextToken'])

    def test_can_paginate_with_page_size(self):
        # Using an operation that we know will paginate.
        operation = self.service.get_operation('DescribeReservedInstancesOfferings')
        generator = operation.paginate(self.endpoint, page_size=1)
        results = list(itertools.islice(generator, 0, 3))
        self.assertEqual(len(results), 3)
        for result in results:
            parsed = result[1]
            reserved_inst_offer = parsed['ReservedInstancesOfferings']
            # There should only be one reserved instance offering on each
            # page.
            self.assertEqual(len(reserved_inst_offer), 1)


class TestCopySnapshotCustomization(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        # Note, the EBS copy snapshot customization is not ported
        # over to the client interface so we have to use the
        # Service/Operation objects for the actual CopySnapshot
        # operation being tested.
        self.service = self.session.get_service('ec2')
        self.copy_snapshot = self.service.get_operation('CopySnapshot')
        # However, all the test fixture setup/cleanup can use
        # the client interface.
        self.client = self.session.create_client('ec2', 'us-west-2')
        self.us_east_1 = self.service.get_endpoint('us-east-1')
        self.us_west_2 = self.service.get_endpoint('us-west-2')

    def create_volume(self, encrypted=False):
        available_zones = self.client.describe_availability_zones()
        first_zone = available_zones['AvailabilityZones'][0]['ZoneName']
        response = self.client.create_volume(
            Size=1, AvailabilityZone=first_zone, Encrypted=encrypted)
        volume_id = response['VolumeId']
        self.addCleanup(self.client.delete_volume, VolumeId=volume_id)
        self.client.get_waiter('volume_available').wait(VolumeIds=[volume_id])
        return volume_id

    def create_snapshot(self, volume_id):
        response = self.client.create_snapshot(VolumeId=volume_id)
        snapshot_id = response['SnapshotId']
        self.client.get_waiter('snapshot_completed').wait(
            SnapshotIds=[snapshot_id])
        self.addCleanup(self.client.delete_snapshot, SnapshotId=snapshot_id)
        return snapshot_id

    def cleanup_copied_snapshot(self, snapshot_id):
        dest_client = self.session.create_client('ec2', 'us-east-1')
        self.addCleanup(dest_client.delete_snapshot,
                        SnapshotId=snapshot_id)
        dest_client.get_waiter('snapshot_completed').wait(
            SnapshotIds=[snapshot_id])

    def test_can_copy_snapshot(self):
        volume_id = self.create_volume()
        snapshot_id = self.create_snapshot(volume_id)

        http, parsed = self.copy_snapshot.call(
            self.us_east_1, SourceRegion='us-west-2',
            SourceSnapshotId=snapshot_id)
        self.assertEqual(http.status_code, 200)

        # Cleanup code.  We can wait for the snapshot to be complete
        # and then we can delete the snapshot.
        self.cleanup_copied_snapshot(parsed['SnapshotId'])

    def test_can_copy_encrypted_snapshot(self):
        # Note that we're creating an encrypted volume here.
        volume_id = self.create_volume(encrypted=True)
        snapshot_id = self.create_snapshot(volume_id)

        http, parsed = self.copy_snapshot.call(
            self.us_east_1, SourceRegion='us-west-2',
            SourceSnapshotId=snapshot_id)
        self.assertEqual(http.status_code, 200)
        self.cleanup_copied_snapshot(parsed['SnapshotId'])


if __name__ == '__main__':
    unittest.main()
