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

from botocore.stub import Stubber
from tests import BaseSessionTest


class TestApiGateway(BaseSessionTest):
    def setUp(self):
        super(TestApiGateway, self).setUp()
        self.region = 'us-west-2'
        self.client = self.session.create_client(
            'apigateway', self.region)
        self.stubber = Stubber(self.client)

    def test_get_export(self):
        params = {
            'restApiId': 'foo',
            'stageName': 'bar',
            'exportType': 'swagger',
            'accepts': 'application/yaml'
        }

        with mock.patch('botocore.endpoint.Session.send') as _send:
            _send.return_value = mock.Mock(
                status_code=200, headers={}, content=b'{}')
            self.client.get_export(**params)
            sent_request = _send.call_args[0][0]
            self.assertEqual(sent_request.method, 'GET')
            self.assertEqual(
                sent_request.headers.get('Accept'), b'application/yaml')
