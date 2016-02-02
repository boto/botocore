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

from tests import unittest

import botocore
import botocore.session
from botocore.stub import Stubber
from botocore.exceptions import StubResponseError, ClientError
import botocore.client
import botocore.retryhandler
import botocore.translate


class TestStubber(unittest.TestCase):
    def setUp(self):
        session = botocore.session.get_session()
        config = botocore.client.Config(signature_version=botocore.UNSIGNED)
        self.client = session.create_client('s3', config=config)

        self.stubber = Stubber(self.client)

    def test_stubber_returns_response(self):
        service_response = {'ResponseMetadata': {'foo': 'bar'}}
        self.stubber.add_response('list_objects', service_response)
        self.stubber.activate()
        response = self.client.list_objects(Bucket='foo')
        self.assertEqual(response, service_response)

    def test_activated_stubber_errors_with_no_registered_stubs(self):
        self.stubber.activate()
        with self.assertRaises(StubResponseError):
            self.client.list_objects(Bucket='foo')

    def test_stubber_errors_when_stubs_are_used_up(self):
        self.stubber.add_response('list_objects', {})
        self.stubber.activate()
        self.client.list_objects(Bucket='foo')

        with self.assertRaises(StubResponseError):
            self.client.list_objects(Bucket='foo')

    def test_client_error_response(self):
        error_code = "AccessDenied"
        error_message = "Access Denied"
        self.stubber.add_client_error('list_objects', error_code, error_message)
        self.stubber.activate()

        with self.assertRaises(ClientError):
            self.client.list_objects(Bucket='foo')
