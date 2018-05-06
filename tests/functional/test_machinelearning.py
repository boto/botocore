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
import mock

from tests import BaseSessionTest


class TestMachineLearning(BaseSessionTest):
    def setUp(self):
        super(TestMachineLearning, self).setUp()
        self.region = 'us-west-2'
        self.client = self.session.create_client(
            'machinelearning', self.region)

    def test_predict(self):
        with mock.patch('botocore.endpoint.Session.send') as \
                http_session_send_patch:
            http_response = mock.Mock()
            http_response.status_code = 200
            http_response.content = b'{}'
            http_response.headers = {}
            http_session_send_patch.return_value = http_response
            custom_endpoint = 'https://myendpoint.amazonaws.com/'
            self.client.predict(
                MLModelId='ml-foo',
                Record={'Foo': 'Bar'},
                PredictEndpoint=custom_endpoint
            )
            sent_request = http_session_send_patch.call_args[0][0]
            self.assertEqual(sent_request.url, custom_endpoint)
