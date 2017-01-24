# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import botocore.session
from tests import BaseSessionTest


class TestRDSPresign(BaseSessionTest):

    def test_inject_presigned_url(self):
        client = self.session.create_client('rds', 'us-west-2')
        params = {
            'SourceDBSnapshotIdentifier': 'source-db',
            'TargetDBSnapshotIdentifier': 'target-db',
            'SourceRegion': 'us-east-1'
        }
        with mock.patch('botocore.endpoint.Session.send') as _send:
            _send.return_value = mock.Mock(
                status_code=200, headers={}, content=(
                    b'<CopyDBSnapshotResponse>'
                    b'<CopyDBSnapshotResult></CopyDBSnapshotResult>'
                    b'</CopyDBSnapshotResponse>'
                ))
            client.copy_db_snapshot(**params)
            sent_request = _send.call_args[0][0]

        self.assertIn('PreSignedUrl', sent_request.body)
        self.assertNotIn('SourceRegion', sent_request.body)
