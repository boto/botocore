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
import mock

from tests import BaseSessionTest


class TestCloudsearchdomain(BaseSessionTest):
    def setUp(self):
        super(TestCloudsearchdomain, self).setUp()
        self.region = 'us-west-2'
        self.client = self.session.create_client(
            'cloudsearchdomain', self.region)

    def test_search(self):
        with mock.patch('botocore.endpoint.Session.send') as _send:
            _send.return_value = mock.Mock(
                status_code=200, headers={}, content=b'{}')
            self.client.search(query='foo')
            sent_request = _send.call_args[0][0]
            self.assertEqual(sent_request.method, 'POST')
            self.assertEqual(
                sent_request.headers.get('Content-Type'),
                b'application/x-www-form-urlencoded')
            self.assertIn('q=foo', sent_request.body)
