# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import datetime

import botocore
import botocore.auth

from botocore.credentials import Credentials
from botocore.exceptions import NoRegionError, UnknownSignatureVersionError
from botocore.signers import RequestSigner

from tests import unittest


class BaseSignerTest(unittest.TestCase):
    def setUp(self):
        self.credentials = Credentials('key', 'secret')
        self.emitter = mock.Mock()
        self.emitter.emit_until_response.return_value = (None, None)
        self.signer = RequestSigner(
            'service_name', 'region_name', 'signing_name',
            'v4', self.credentials, self.emitter)


class TestSigner(BaseSignerTest):

    def test_region_required_for_sigv4(self):
        self.signer = RequestSigner(
            'service_name', None, 'signing_name', 'v4', self.credentials,
            self.emitter)

        with self.assertRaises(NoRegionError):
            self.signer.sign('operation_name', mock.Mock())

    def test_get_auth(self):
        auth_cls = mock.Mock()
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4': auth_cls}):
            auth = self.signer.get_auth('service_name', 'region_name')

            self.assertEqual(auth, auth_cls.return_value)
            auth_cls.assert_called_with(
                credentials=self.credentials, service_name='service_name',
                region_name='region_name')

    def test_get_auth_cached(self):
        auth_cls = mock.Mock()
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4': auth_cls}):
            auth1 = self.signer.get_auth('service_name', 'region_name')
            auth2 = self.signer.get_auth('service_name', 'region_name')

        self.assertEqual(auth1, auth2)

    def test_get_auth_signature_override(self):
        auth_cls = mock.Mock()
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4-custom': auth_cls}):
            auth = self.signer.get_auth(
                'service_name', 'region_name', signature_version='v4-custom')

            self.assertEqual(auth, auth_cls.return_value)
            auth_cls.assert_called_with(
                credentials=self.credentials, service_name='service_name',
                region_name='region_name')

    def test_get_auth_bad_override(self):
        with self.assertRaises(UnknownSignatureVersionError):
            self.signer.get_auth('service_name', 'region_name',
                                 signature_version='bad')

    def test_emits_choose_signer(self):
        request = mock.Mock()

        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4': mock.Mock()}):
            self.signer.sign('operation_name', request)

        self.emitter.emit_until_response.assert_called_with(
            'choose-signer.service_name.operation_name',
            signing_name='signing_name', region_name='region_name',
            signature_version='v4')

    def test_choose_signer_override(self):
        request = mock.Mock()
        auth = mock.Mock()
        auth.REQUIRES_REGION = False
        self.emitter.emit_until_response.return_value = (None, 'custom')

        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'custom': auth}):
            self.signer.sign('operation_name', request)

        auth.assert_called_with(credentials=self.credentials)
        auth.return_value.add_auth.assert_called_with(request=request)

    def test_emits_before_sign(self):
        request = mock.Mock()

        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4': mock.Mock()}):
            self.signer.sign('operation_name', request)

        self.emitter.emit.assert_called_with(
            'before-sign.service_name.operation_name',
            request=mock.ANY, signing_name='signing_name',
            region_name='region_name', signature_version='v4',
            request_signer=self.signer)

    def test_disable_signing(self):
        # Returning botocore.UNSIGNED from choose-signer disables signing!
        request = mock.Mock()
        auth = mock.Mock()
        self.emitter.emit_until_response.return_value = (None,
                                                         botocore.UNSIGNED)

        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4': auth}):
            self.signer.sign('operation_name', request)

        auth.assert_not_called()

    def test_generate_url(self):
        auth = mock.Mock()
        auth.REQUIRES_REGION = True

        request_dict = {
            'headers': {},
            'url': 'https://foo.com',
            'body': '',
            'url_path': '/',
            'method': 'GET'
        }
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4-query': auth}):
            presigned_url = self.signer.generate_url(request_dict)
        auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            service_name='signing_name')
        self.assertEqual(presigned_url, 'https://foo.com')

    def test_generate_url_with_region_override(self):
        auth = mock.Mock()
        auth.REQUIRES_REGION = True

        request_dict = {
            'headers': {},
            'url': 'https://foo.com',
            'body': '',
            'url_path': '/',
            'method': 'GET'
        }
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4-query': auth}):
            presigned_url = self.signer.generate_url(
                request_dict, region_name='us-west-2')
        auth.assert_called_with(
            credentials=self.credentials, region_name='us-west-2',
            service_name='signing_name')
        self.assertEqual(presigned_url, 'https://foo.com')

    def test_generate_url_with_exipres_in(self):
        auth = mock.Mock()
        auth.REQUIRES_REGION = True

        request_dict = {
            'headers': {},
            'url': 'https://foo.com',
            'body': '',
            'url_path': '/',
            'method': 'GET'
        }
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4-query': auth}):
            presigned_url = self.signer.generate_url(
                request_dict, expires_in=900)
        auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            expires=900, service_name='signing_name')
        self.assertEqual(presigned_url, 'https://foo.com')


class TestPresignS3Post(BaseSignerTest):
    def setUp(self):
        super(TestPresignS3Post, self).setUp()
        self.signer = RequestSigner(
            'service_name', 'region_name', 'signing_name',
            's3v4', self.credentials, self.emitter)
        self.request_dict = {
            'headers': {},
            'url': 'https://foo.com/mybucket',
            'body': '',
            'url_path': '/',
            'method': 'POST'
        }
        self.auth = mock.Mock()
        self.auth.REQUIRES_REGION = True
        self.add_auth = mock.Mock()
        self.auth.return_value.add_auth = self.add_auth

        self.datetime_patch = mock.patch('botocore.signers.datetime')
        self.datetime_mock = self.datetime_patch.start()
        self.fixed_date = datetime.datetime(2014, 3, 10, 17, 2, 55, 0)
        self.fixed_delta = datetime.timedelta(seconds=3600)
        self.datetime_mock.datetime.utcnow.return_value = self.fixed_date
        self.datetime_mock.timedelta.return_value = self.fixed_delta

    def tearDown(self):
        super(TestPresignS3Post, self).tearDown()
        self.datetime_patch.stop()

    def test_build_post_form_args(self):
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'s3v4-presign-post': self.auth}):
            post_form_args = self.signer.build_post_form_args(
                self.request_dict)
        self.auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            service_name='signing_name')
        self.add_auth.assert_called_once()
        ref_request = self.add_auth.call_args[0][0]
        ref_policy = ref_request.context['s3-presign-post-policy']
        self.assertEqual(ref_policy['expiration'], '2014-03-10T18:02:55Z')
        self.assertEqual(ref_policy['conditions'], [])

        self.assertEqual(post_form_args['url'], 'https://foo.com/mybucket')
        self.assertEqual(post_form_args['fields'], {})

    def test_build_post_form_args_with_conditions(self):
        conditions = [
            {'bucket': 'mybucket'},
            ['starts-with', '$key', 'bar']
        ]
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'s3v4-presign-post': self.auth}):
            self.signer.build_post_form_args(
                self.request_dict, conditions=conditions)
        self.auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            service_name='signing_name')
        self.add_auth.assert_called_once()
        ref_request = self.add_auth.call_args[0][0]
        ref_policy = ref_request.context['s3-presign-post-policy']
        self.assertEqual(ref_policy['conditions'], conditions)

    def test_build_post_form_args_with_region_override(self):
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'s3v4-presign-post': self.auth}):
            self.signer.build_post_form_args(
                self.request_dict, region_name='foo')
        self.auth.assert_called_with(
            credentials=self.credentials, region_name='foo',
            service_name='signing_name')
