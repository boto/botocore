#!/usr/bin/env python
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

import botocore.exceptions


class TestService(BaseSessionTest):
    def setUp(self):
        super(TestService, self).setUp()
        self.environ['AWS_CONFIG_FILE'] = 'nowhere-foobar'

    def test_get_endpoint_with_no_region(self):
        # Test global endpoint service such as iam.
        service = self.session.get_service('iam')
        endpoint = service.get_endpoint()
        self.assertEqual(endpoint.host, 'https://iam.amazonaws.com')

    def test_get_endpoint_forwards_verify_args(self):
        service = self.session.get_service('iam')
        endpoint = service.get_endpoint(verify='/path/cacerts.pem')
        self.assertEqual(endpoint.verify, '/path/cacerts.pem')

    def test_endpoint_arg_overrides_everything(self):
        service = self.session.get_service('iam')
        endpoint = service.get_endpoint(
            region_name='us-east-1',
            endpoint_url='https://wherever.i.want.com')
        self.assertEqual(endpoint.host, 'https://wherever.i.want.com')
        self.assertEqual(endpoint.region_name, 'us-east-1')

    def test_service_metadata_not_required_for_region(self):
        service = self.session.get_service('iam')
        endpoint = service.get_endpoint(
            region_name='us-east-1',
            endpoint_url='https://wherever.i.want.com')
        self.assertEqual(endpoint.host, 'https://wherever.i.want.com')
        self.assertEqual(endpoint.region_name, 'us-east-1')

    def test_region_not_required_if_endpoint_url_given(self):
        # Only services that require the region_name (sigv4)
        # should require this param.  If we're talking to
        # a service that doesn't need this info, there's no
        # reason to require this param in botocore.
        service = self.session.get_service('importexport')
        endpoint = service.get_endpoint(
            endpoint_url='https://wherever.i.want.com')
        self.assertEqual(endpoint.host, 'https://wherever.i.want.com')
        self.assertIsNone(endpoint.region_name)

    def test_region_required_for_sigv4(self):
        # However, if the service uses siv4 auth, then an exception
        # is raised if we call get_endpoint without a region name.
        service = self.session.get_service('cloudformation')
        with self.assertRaises(botocore.exceptions.NoRegionError):
            service.get_endpoint(endpoint_url='https://wherever.i.want.com')

    def test_region_required_for_non_global_endpoint(self):
        # If you don't provide an endpoint_url, than you need to
        # provide a region_name.
        service = self.session.get_service('ec2')
        with self.assertRaises(botocore.exceptions.UnknownEndpointError):
            service.get_endpoint()

    def test_region_not_required_if_endpoint_url_given(self):
        # Even if we're not a global service, if an endpoint_url is given
        # then we still construct an endpoint even if the heuristics fail.
        service = self.session.get_service('sdb')
        endpoint = service.get_endpoint(
            region_name=None,
            endpoint_url='http://custom-endpoint/')
        self.assertEqual(endpoint.host, 'http://custom-endpoint/')

    def test_turnoff_signing(self):
        service = self.session.get_service('ec2')
        service.signature_version = None
        with mock.patch('botocore.endpoint.EndpointCreator.create_endpoint') \
                as mock_create_endpoint:
            service.get_endpoint('us-east-1')
            self.assertEqual(
                mock_create_endpoint.call_args[1]['signature_version'],
                None
            )


if __name__ == "__main__":
    unittest.main()
