# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import mock
from contextlib import contextmanager

import botocore.session
from tests import BaseSessionTest
from botocore.stub import Stubber
from tests import unittest


class TestNeptunePresignUrlInjection(BaseSessionTest):

    def setUp(self):
        super(TestNeptunePresignUrlInjection, self).setUp()
        self.client = self.session.create_client('neptune', 'us-west-2')

    @contextmanager
    def patch_http_layer(self, response, status_code=200):
        # TODO: fix with stubber / before send event
        with mock.patch('botocore.endpoint.Endpoint._send') as send:
            send.return_value = mock.Mock(status_code=status_code,
                                          headers={},
                                          content=response)
            yield send

    def assert_presigned_url_injected_in_request(self, body):
        self.assertIn('PreSignedUrl', body)
        self.assertNotIn('SourceRegion', body)

    def test_create_db_cluster(self):
        params = {
            'DBClusterIdentifier': 'my-cluster',
            'Engine': 'neptune',
            'SourceRegion': 'us-east-1'
        }
        response_body = (
            b'<CreateDBClusterResponse>'
            b'<CreateDBClusterResult>'
            b'</CreateDBClusterResult>'
            b'</CreateDBClusterResponse>'
        )
        with self.patch_http_layer(response_body) as send:
            self.client.create_db_cluster(**params)
            sent_request = send.call_args[0][0]
            self.assert_presigned_url_injected_in_request(sent_request.body)

    def test_copy_db_cluster_snapshot(self):
        params = {
            'SourceDBClusterSnapshotIdentifier': 'source-db',
            'TargetDBClusterSnapshotIdentifier': 'target-db',
            'SourceRegion': 'us-east-1'
        }
        response_body = (
            b'<CopyDBClusterSnapshotResponse>'
            b'<CopyDBClusterSnapshotResult>'
            b'</CopyDBClusterSnapshotResult>'
            b'</CopyDBClusterSnapshotResponse>'
        )
        with self.patch_http_layer(response_body) as send:
            self.client.copy_db_cluster_snapshot(**params)
            sent_request = send.call_args[0][0]
            self.assert_presigned_url_injected_in_request(sent_request.body)
