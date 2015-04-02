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
from botocore.exceptions import ParamValidationError
from botocore.signers import RequestSigner, generate_url
from botocore.signers import build_s3_post_form_args

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
            service_name='signing_name', expires=3600)
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
            service_name='signing_name', expires=3600)
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

    def test_generate_url_fixes_s3_host(self):
        self.signer = RequestSigner(
            'service_name', 'region_name', 'signing_name',
            's3', self.credentials, self.emitter)

        auth = mock.Mock()
        auth.REQUIRES_REGION = True

        request_dict = {
            'headers': {},
            'url': 'https://s3.amazonaws.com/mybucket/myobject',
            'body': '',
            'url_path': '/',
            'method': 'GET'
        }
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'s3-query': auth}):
            presigned_url = self.signer.generate_url(
                request_dict, expires_in=900)
        auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            expires=900, service_name='signing_name')
        self.assertEqual(presigned_url,
                         'https://mybucket.s3.amazonaws.com/myobject')


class TestSignerS3Post(BaseSignerTest):
    def setUp(self):
        super(TestSignerS3Post, self).setUp()
        self.signer = RequestSigner(
            'service_name', 'region_name', 'signing_name',
            's3v4', self.credentials, self.emitter)
        self.request_dict = {
            'headers': {},
            'url': 'https://s3.amazonaws.com/mybucket',
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
        super(TestSignerS3Post, self).tearDown()
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

        self.assertEqual(post_form_args['url'],
                         'https://s3.amazonaws.com/mybucket')
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

    def test_build_post_form_args_fixes_s3_host(self):
        self.signer = RequestSigner(
            'service_name', 'region_name', 'signing_name',
            's3', self.credentials, self.emitter)

        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'s3-presign-post': self.auth}):
            post_form_args = self.signer.build_post_form_args(
                self.request_dict)
        self.auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            service_name='signing_name')
        self.assertEqual(post_form_args['url'],
                         'https://mybucket.s3.amazonaws.com')


class TestGenerateUrl(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('s3', region_name='us-east-1')
        self.bucket = 'mybucket'
        self.key = 'mykey'
        self.client_kwargs = {'Bucket': self.bucket, 'Key': self.key}
        self.generate_url_patch = mock.patch(
            'botocore.signers.RequestSigner.generate_url')
        self.generate_url_mock = self.generate_url_patch.start()

    def tearDown(self):
        self.generate_url_patch.stop()

    def test_generate_url(self):
        generate_url(self.client, 'get_object', self.client_kwargs)

        ref_request_dict = {
            'body': '',
            'url': u'https://s3.amazonaws.com/mybucket/mykey',
            'headers': {},
            'query_string': {},
            'url_path': u'/mybucket/mykey',
            'method': u'GET'}
        self.generate_url_mock.assert_called_with(
            request_dict=ref_request_dict, expires_in=3600)

    def test_generate_url_missing_required_params(self):
        with self.assertRaises(ParamValidationError):
            generate_url(self.client, 'get_object')

    def test_generate_url_expires(self):
        generate_url(
            self.client, 'get_object', self.client_kwargs, expires_in=20)
        ref_request_dict = {
            'body': '',
            'url': u'https://s3.amazonaws.com/mybucket/mykey',
            'headers': {},
            'query_string': {},
            'url_path': u'/mybucket/mykey',
            'method': u'GET'}
        self.generate_url_mock.assert_called_with(
            request_dict=ref_request_dict, expires_in=20)


class TestBuildS3PostFormArgs(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('s3', region_name='us-east-1')
        self.bucket = 'mybucket'
        self.key = 'mykey'
        self.build_post_form_args_patch = mock.patch(
            'botocore.signers.RequestSigner.build_post_form_args')
        self.post_form_args_mock = self.build_post_form_args_patch.start()

    def tearDown(self):
        self.build_post_form_args_patch.stop()

    def test_build_s3_post_form_args(self):
        build_s3_post_form_args(
            self.client, self.bucket, self.key)

        _, post_form_kwargs = self.post_form_args_mock.call_args
        request_dict = post_form_kwargs['request_dict']
        fields = post_form_kwargs['fields']
        conditions = post_form_kwargs['conditions']
        self.assertEqual(
            request_dict['url'], 'https://s3.amazonaws.com/mybucket')
        self.assertEqual(post_form_kwargs['expires_in'], 3600)
        self.assertEqual(
            conditions,
            [{'bucket': 'mybucket'}, {'key': 'mykey'}])
        self.assertEqual(
            fields,
            {'key': 'mykey'})

    def test_build_s3_post_form_args_with_filename(self):
        self.key = 'myprefix/${filename}'
        build_s3_post_form_args(
            self.client, self.bucket, self.key)

        _, post_form_kwargs = self.post_form_args_mock.call_args
        request_dict = post_form_kwargs['request_dict']
        fields = post_form_kwargs['fields']
        conditions = post_form_kwargs['conditions']
        self.assertEqual(
            request_dict['url'], 'https://s3.amazonaws.com/mybucket')
        self.assertEqual(post_form_kwargs['expires_in'], 3600)
        self.assertEqual(
            conditions,
            [{'bucket': 'mybucket'}, ['starts-with', '$key', 'myprefix/']])
        self.assertEqual(
            fields,
            {'key': 'myprefix/${filename}'})

    def test_build_s3_post_form_args_expires(self):
        build_s3_post_form_args(
            self.client, self.bucket, self.key, expires_in=50)

        _, post_form_kwargs = self.post_form_args_mock.call_args
        request_dict = post_form_kwargs['request_dict']
        fields = post_form_kwargs['fields']
        conditions = post_form_kwargs['conditions']
        self.assertEqual(
            request_dict['url'], 'https://s3.amazonaws.com/mybucket')
        self.assertEqual(post_form_kwargs['expires_in'], 50)
        self.assertEqual(
            conditions,
            [{'bucket': 'mybucket'}, {'key': 'mykey'}])
        self.assertEqual(
            fields,
            {'key': 'mykey'})

    def test_build_s3_post_form_args_with_prefilled(self):
        conditions = [{'acl': 'public-read'}]
        fields = {'acl': 'public-read'}

        build_s3_post_form_args(
            self.client, self.bucket, self.key, fields=fields,
            conditions=conditions)

        _, post_form_kwargs = self.post_form_args_mock.call_args
        request_dict = post_form_kwargs['request_dict']
        fields = post_form_kwargs['fields']
        conditions = post_form_kwargs['conditions']
        self.assertEqual(
            request_dict['url'], 'https://s3.amazonaws.com/mybucket')
        self.assertEqual(
            conditions,
            [{'acl': 'public-read'}, {'bucket': 'mybucket'}, {'key': 'mykey'}])
        self.assertEqual(fields['acl'], 'public-read')
        self.assertEqual(
            fields, {'key': 'mykey', 'acl': 'public-read'})
