#!/usr/bin/env python
# Copyright 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
from tests import BaseSessionTest

import botocore.exceptions


class TestService(BaseSessionTest):

    def test_get_endpoint_with_no_region(self):
        # Test global endpoint service such as iam.
        service = self.session.get_service('iam')
        endpoint = service.get_endpoint()
        self.assertEqual(endpoint.host, 'https://iam.amazonaws.com/')

    def test_endpoint_arg_overrides_everything(self):
        service = self.session.get_service('iam')
        endpoint = service.get_endpoint(
            region_name='us-east-1',
            endpoint_url='https://wherever.i.want.com')
        self.assertEqual(endpoint.host, 'https://wherever.i.want.com')
        self.assertEqual(endpoint.region_name, 'us-east-1')

    def test_service_metadata_not_required_for_region(self):
        service = self.session.get_service('iam')
        # Empty out the service metadata.  This contains info
        # about supported protocools and region/endpoints.
        # Even if this info is not present, if the user
        # passes in an endpoint_url, we should be able to use
        # this value.
        service.metadata = {}
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
        service = self.session.get_service('ec2')
        service.metadata = {}
        endpoint = service.get_endpoint(
            endpoint_url='https://wherever.i.want.com')
        self.assertEqual(endpoint.host, 'https://wherever.i.want.com')
        self.assertIsNone(endpoint.region_name)

    def test_region_required_for_sigv4(self):
        # However, if the service uses siv4 auth, then an exception
        # is raised if we call get_endpoint without a region name.
        service = self.session.get_service('cloudformation')
        service.metadata = {}
        with self.assertRaises(botocore.exceptions.NoRegionError):
            service.get_endpoint(endpoint_url='https://wherever.i.want.com')

    def test_region_required_for_non_global_endpoint(self):
        # If you don't provide an endpoint_url, than you need to
        # provide a region_name.
        service = self.session.get_service('ec2')
        with self.assertRaises(botocore.exceptions.NoRegionError):
            service.get_endpoint()


if __name__ == "__main__":
    unittest.main()
