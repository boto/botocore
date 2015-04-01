#!/usr/bin/env python
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
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

import os

from tests import BaseSessionTest
from mock import patch, Mock

import botocore.session
from botocore import auth
from botocore import credentials
from botocore.exceptions import ServiceNotInRegionError
from botocore.handlers import fix_s3_host


class TestS3Addressing(BaseSessionTest):

    def setUp(self):
        super(TestS3Addressing, self).setUp()
        self.s3 = self.session.get_service('s3')
        self.signature_version = 's3'

    @patch('botocore.response.get_response', Mock())
    def get_prepared_request(self, op, param, force_hmacv1=False):
        request = []
        if force_hmacv1:
            self.endpoint.auth = auth.HmacV1Auth(
                credentials.Credentials('foo', 'bar'))
        def prepare_request(request, **kwargs):
            fix_s3_host(request, self.signature_version,
                        self.endpoint.region_name)
            return request
        self.endpoint.prepare_request = prepare_request
        return self.endpoint.create_request(param, op)

    def test_list_objects_dns_name(self):
        self.endpoint = self.s3.get_endpoint('us-east-1')
        op = self.s3.get_operation('ListObjects')
        params = op.build_parameters(bucket='safename')
        prepared_request = self.get_prepared_request(op, params,
                                                     force_hmacv1=True)
        self.assertEqual(prepared_request.url,
                         'https://safename.s3.amazonaws.com')

    def test_list_objects_non_dns_name(self):
        self.endpoint = self.s3.get_endpoint('us-east-1')
        op = self.s3.get_operation('ListObjects')
        params = op.build_parameters(bucket='un_safe_name')
        prepared_request = self.get_prepared_request(op, params)
        self.assertEqual(prepared_request.url,
                         'https://s3.amazonaws.com/un_safe_name')

    def test_list_objects_dns_name_non_classic(self):
        self.endpoint = self.s3.get_endpoint('us-west-2')
        op = self.s3.get_operation('ListObjects')
        params = op.build_parameters(bucket='safename')
        prepared_request = self.get_prepared_request(op, params,
                                                     force_hmacv1=True)
        self.assertEqual(prepared_request.url,
                         'https://safename.s3.amazonaws.com')

    def test_list_objects_unicode_query_string_eu_central_1(self):
        self.signature_version = 's3v4'
        self.endpoint = self.s3.get_endpoint('eu-central-1')
        op = self.s3.get_operation('ListObjects')
        params = op.build_parameters(bucket='safename',
                                     marker=u'\xe4\xf6\xfc-01.txt')
        prepared_request = self.get_prepared_request(op, params)
        self.assertEqual(
            prepared_request.url,
            ('https://s3.eu-central-1.amazonaws.com/safename'
             '?marker=%C3%A4%C3%B6%C3%BC-01.txt')
        )

    def test_list_objects_in_restricted_regions(self):
        self.endpoint = self.s3.get_endpoint('us-gov-west-1')
        op = self.s3.get_operation('ListObjects')
        params = op.build_parameters(bucket='safename')
        prepared_request = self.get_prepared_request(op, params)
        # Note how we keep the region specific endpoint here.
        self.assertEqual(prepared_request.url,
                         'https://s3-us-gov-west-1.amazonaws.com/safename')

    def test_list_objects_in_fips(self):
        self.endpoint = self.s3.get_endpoint('fips-us-gov-west-1')
        op = self.s3.get_operation('ListObjects')
        params = op.build_parameters(bucket='safename')
        prepared_request = self.get_prepared_request(op, params)
        # Note how we keep the region specific endpoint here.
        self.assertEqual(
            prepared_request.url,
            'https://s3-fips-us-gov-west-1.amazonaws.com/safename')

    def test_list_objects_non_dns_name_non_classic(self):
        self.endpoint = self.s3.get_endpoint('us-west-2')
        op = self.s3.get_operation('ListObjects')
        params = op.build_parameters(bucket='un_safe_name')
        prepared_request = self.get_prepared_request(op, params)
        self.assertEqual(prepared_request.url,
                         'https://s3-us-west-2.amazonaws.com/un_safe_name')

    def test_put_object_dns_name_non_classic(self):
        self.endpoint = self.s3.get_endpoint('us-west-2')
        op = self.s3.get_operation('PutObject')
        file_path = os.path.join(os.path.dirname(__file__),
                                 'put_object_data')
        fp = open(file_path, 'rb')
        params = op.build_parameters(bucket='my.valid.name',
                                     key='mykeyname',
                                     body=fp,
                                     acl='public-read',
                                     content_language='piglatin',
                                     content_type='text/plain')
        prepared_request = self.get_prepared_request(op, params)
        self.assertEqual(prepared_request.url,
                         'https://s3-us-west-2.amazonaws.com/my.valid.name/mykeyname')
        fp.close()

    def test_put_object_dns_name_classic(self):
        self.endpoint = self.s3.get_endpoint('us-east-1')
        op = self.s3.get_operation('PutObject')
        file_path = os.path.join(os.path.dirname(__file__),
                                 'put_object_data')
        fp = open(file_path, 'rb')
        params = op.build_parameters(bucket='my.valid.name',
                                     key='mykeyname',
                                     body=fp,
                                     acl='public-read',
                                     content_language='piglatin',
                                     content_type='text/plain')
        prepared_request = self.get_prepared_request(op, params)
        self.assertEqual(prepared_request.url,
                         'https://s3.amazonaws.com/my.valid.name/mykeyname')
        fp.close()

    def test_put_object_dns_name_single_letter_non_classic(self):
        self.endpoint = self.s3.get_endpoint('us-west-2')
        op = self.s3.get_operation('PutObject')
        file_path = os.path.join(os.path.dirname(__file__),
                                 'put_object_data')
        fp = open(file_path, 'rb')
        params = op.build_parameters(bucket='a.valid.name',
                                     key='mykeyname',
                                     body=fp,
                                     acl='public-read',
                                     content_language='piglatin',
                                     content_type='text/plain')
        prepared_request = self.get_prepared_request(op, params)
        self.assertEqual(prepared_request.url,
                         'https://s3-us-west-2.amazonaws.com/a.valid.name/mykeyname')
        fp.close()

    def test_get_object_non_dns_name_non_classic(self):
        self.endpoint = self.s3.get_endpoint('us-west-2')
        op = self.s3.get_operation('GetObject')
        params = op.build_parameters(bucket='AnInvalidName',
                                     key='mykeyname')
        prepared_request = self.get_prepared_request(op, params)
        self.assertEqual(prepared_request.url,
                         'https://s3-us-west-2.amazonaws.com/AnInvalidName/mykeyname')

    def test_get_object_non_dns_name_classic(self):
        self.endpoint = self.s3.get_endpoint('us-east-1')
        op = self.s3.get_operation('GetObject')
        params = op.build_parameters(bucket='AnInvalidName',
                                     key='mykeyname')
        prepared_request = self.get_prepared_request(op, params)
        self.assertEqual(prepared_request.url,
                         'https://s3.amazonaws.com/AnInvalidName/mykeyname')

    def test_get_object_ip_address_name_non_classic(self):
        self.endpoint = self.s3.get_endpoint('us-west-2')
        op = self.s3.get_operation('GetObject')
        params = op.build_parameters(bucket='192.168.5.4',
                                     key='mykeyname')
        prepared_request = self.get_prepared_request(op, params)
        self.assertEqual(
            prepared_request.url,
            'https://s3-us-west-2.amazonaws.com/192.168.5.4/mykeyname')

    def test_get_object_almost_an_ip_address_name_non_classic(self):
        self.endpoint = self.s3.get_endpoint('us-west-2')
        op = self.s3.get_operation('GetObject')
        params = op.build_parameters(bucket='192.168.5.256',
                                     key='mykeyname')
        prepared_request = self.get_prepared_request(op, params)
        self.assertEqual(
            prepared_request.url,
            'https://s3-us-west-2.amazonaws.com/192.168.5.256/mykeyname')

    def test_invalid_endpoint_raises_exception(self):
        with self.assertRaisesRegexp(ValueError, 'Invalid endpoint'):
            self.s3.get_endpoint('bad region name')

    def test_non_existent_region(self):
        # If I ask for a region that does not
        # exist on a global endpoint, such as:
        endpoint = self.s3.get_endpoint('REGION-DOES-NOT-EXIST')
        # Then the default endpoint heuristic will apply and we'll
        # get the region name as specified.
        self.assertEqual(endpoint.region_name, 'REGION-DOES-NOT-EXIST')
        # Why not fixed this?  Well backwards compatability for one thing.
        # The other reason is because it was intended to accomodate this
        # use case.  Let's say I have us-west-2 set as my default region,
        # possibly through an env var or config variable.  Well, by default,
        # we'd make a call like:
        iam_endpoint = self.session.get_service('iam').get_endpoint('us-west-2')
        # Instead of giving the user an error, we should instead give
        # them the global endpoint.
        self.assertEqual(iam_endpoint.region_name, 'us-east-1')
        # But if they request an endpoint that we *do* know about, we use
        # that specific endpoint.
        self.assertEqual(
            self.session.get_service('iam').get_endpoint(
                'us-gov-west-1').region_name,
            'us-gov-west-1')
