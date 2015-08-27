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
from botocore.exceptions import UnknownClientMethodError, ParamValidationError
from botocore.exceptions import UnsupportedSignatureVersionError
from botocore.signers import RequestSigner, S3PostPresigner, CloudFrontSigner

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

    def test_region_name(self):
        self.assertEqual(self.signer.region_name, 'region_name')

    def test_signature_version(self):
        self.assertEqual(self.signer.signature_version, 'v4')

    def test_signing_name(self):
        self.assertEqual(self.signer.signing_name, 'signing_name')

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
        def side_effect(*args, **kwargs):
            return mock.Mock()
        auth_cls = mock.Mock(side_effect=side_effect)
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4': auth_cls}):
            auth1 = self.signer.get_auth('service_name', 'region_name')
            auth2 = self.signer.get_auth('service_name', 'region_name')

        self.assertEqual(auth1, auth2)

    def test_get_auth_cached_expires(self):
        def side_effect(*args, **kwargs):
            return mock.Mock()
        auth_cls = mock.Mock(side_effect=side_effect)
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4': auth_cls}):
            auth1 = self.signer.get_auth('service_name', 'region_name',
                                         expires=60)
            auth2 = self.signer.get_auth('service_name', 'region_name',
                                         expires=90)

        self.assertNotEqual(auth1, auth2)

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

    def test_generate_presigned_url(self):
        auth = mock.Mock()
        auth.REQUIRES_REGION = True

        request_dict = {
            'headers': {},
            'url': 'https://foo.com',
            'body': b'',
            'url_path': '/',
            'method': 'GET'
        }
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4-query': auth}):
            presigned_url = self.signer.generate_presigned_url(request_dict)
        auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            service_name='signing_name', expires=3600)
        self.assertEqual(presigned_url, 'https://foo.com')

    def test_generate_presigned_url_with_region_override(self):
        auth = mock.Mock()
        auth.REQUIRES_REGION = True

        request_dict = {
            'headers': {},
            'url': 'https://foo.com',
            'body': b'',
            'url_path': '/',
            'method': 'GET'
        }
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4-query': auth}):
            presigned_url = self.signer.generate_presigned_url(
                request_dict, region_name='us-west-2')
        auth.assert_called_with(
            credentials=self.credentials, region_name='us-west-2',
            service_name='signing_name', expires=3600)
        self.assertEqual(presigned_url, 'https://foo.com')

    def test_generate_presigned_url_with_exipres_in(self):
        auth = mock.Mock()
        auth.REQUIRES_REGION = True

        request_dict = {
            'headers': {},
            'url': 'https://foo.com',
            'body': b'',
            'url_path': '/',
            'method': 'GET'
        }
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'v4-query': auth}):
            presigned_url = self.signer.generate_presigned_url(
                request_dict, expires_in=900)
        auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            expires=900, service_name='signing_name')
        self.assertEqual(presigned_url, 'https://foo.com')

    def test_generate_presigned_url_fixes_s3_host(self):
        self.signer = RequestSigner(
            'service_name', 'region_name', 'signing_name',
            's3', self.credentials, self.emitter)

        auth = mock.Mock()
        auth.REQUIRES_REGION = True

        request_dict = {
            'headers': {},
            'url': 'https://s3.amazonaws.com/mybucket/myobject',
            'body': b'',
            'url_path': '/',
            'method': 'GET'
        }
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'s3-query': auth}):
            presigned_url = self.signer.generate_presigned_url(
                request_dict, expires_in=900)
        auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            expires=900, service_name='signing_name')
        self.assertEqual(presigned_url,
                         'https://mybucket.s3.amazonaws.com/myobject')

    def test_presigned_url_throws_unsupported_signature_error(self):
        self.signer = RequestSigner(
            'service_name', 'region_name', 'signing_name',
            'foo', self.credentials, self.emitter)
        with self.assertRaises(UnsupportedSignatureVersionError):
            self.signer.generate_presigned_url({})


class TestCloudfrontSigner(unittest.TestCase):
    def setUp(self):
        # The private key, its id, and the domain name used in this class,
        # are all based on a real CloudFront distribution as test environment.
        # That distribution and the key will probably not last for long,
        # but the test case(s) will remain valid.
        key_id = "APKAJW2UAWQ7F2BI3OHA"
        private_key = """
            -----BEGIN RSA PRIVATE KEY-----
            MIIEowIBAAKCAQEAu6o2+Jc8UINw2P/w2l7A1xXu3emQEZQ9diA3bmog8r9Dg+65
            fZgAqmuNWPqBivv7j3DGnLUdt8uCIr7PYUbK7wDa6n7U3ryOWtO2ZTc3StiJVcqT
            sokZ0qxGFtDRafjBuydXtcxh52vVTcHqH33nubyyZIzuhTwfmrIOnUXnLwbMrBBP
            bg/8mlgQooyo1XbrN1eO4XMs+UgQ9Mqc7KRJRinUJ+KYuCnM8f/nN4RjYdjTcghk
            xCPEHCeSt2luywWyYmfguWCBS2Mu1q0250wKyNazlgiiTJtAuuSeweb4NKPOJL9X
            hR6Ce6UuU4WYlli8gvQh3FAV3N3C1Rxo20k28QIDAQABAoIBAQCUEkP5dWrzpCJg
            NeHWizjg/L9SfT1dgXfVQqo6BqckoeElsjDNdifgT6hhcpbQEO52SWeMsiNWp85w
            l9mNSYxJdIVGzPgtHt27sJyT1DNebOg/tu0+y4qCfcd3rR/u24YQo4RDP5ZoQN82
            0TBn1LIIDWk8iS6SFdRh/OgnE8bLhNbK9IfZQFEEJrFkArrn/le/ro2mfJkC/imo
            QvqKmM0dGBXt5SCDSbUQAzKtEcR/4gf/qSjFe2YAwAvSA05WXMH6szdtx6/H/VbK
            Uck/WwTHvGObQDFEWmICxPK9AWT0qaFNjlUsi3bjQRdIlYYrXe+6nVMB/Jp1awq7
            tGBqIcWBAoGBAPtXCNuoQhKXqkjJgteQpB+wFav12XRZgpOciYdeviJrgWydpOOu
            O9wkiRUctUijRJbUuWCJF7SgYGoT2xTTp/COiOReqs7qXLMuuXCZcPKkMRJj5wmo
            Uc2AwUV/o3+PNz1NFK+2RgciXplac7qugIyuxIvBKuVFTBlCg0+if/0pAoGBAL8k
            845wKqOeiawwle/o9lKLGPy1T11GrE6l1A5jRuE1WTVM77jRrb0Hmo0mdfHaf5A0
            EjXGIX/fjcmQzBrEd78eCUsvI2Bgn6xXwhd4TTyWHGZfoQjFqAGkixuLN1oo2h1g
            bRreFKfAubFP8MC93z23vnH6tdY2VIA4h5ehUFyJAoGAJqxJrKLDJ+E2TmTTQR/8
            YPPTIdZ+UyzCrrvTXYTydJFeJLxM9suEYmcswJbePgMBNsQckgIGJ8DVlPzhJN88
            ZANKhPkcByKAiQGTfwPdITiqZE4C6rV/gMNi+bKeEa6TrVcC69Z8B/T94VLNo9fd
            58esbmSWmRiEkQ5u7f3u+6ECgYA8+6ANCLJB43nPCu07TpsP+LrvHTWF799XdEa0
            lG3vuiKNA8/TqmoAziU79VJZ6Dkcm9BXga/8aSmGboD/5UDDI+UZLJ/fxtQKmzEc
            ZdBWjRnge5AYCV+xrnqHPiJZzIDSMIp+sO3sG2vjKzsHc0x/F1lWagOLpWfORLrV
            4KyP6QKBgAafeSrfK3LM7idiCBuxckLCgFoHa7uXLUNJRS5iIU+bbZLPj2ozu/tk
            U0jp7sNk1CyMWI36lR3sujkSyH3lPIXVgrXMuGY3PJRGntN8WlWEsw4VUMGRj3h4
            5rB+y/UOS+nlEwQ6eOS09GByJDEXOXpcwjFcTr/f7V8mi0jH+gY/
            -----END RSA PRIVATE KEY-----
            """
        self.signer = CloudFrontSigner(key_id, private_key)

    def test_b64encode(self):
        self.assertEqual(
            b'aGVsbG8gd29ybGQ_', CloudFrontSigner.b64encode(b'hello world'))

    def test_sign_expire_start_ip(self):
        expected_url = "http://d2ragvjhlngfb6.cloudfront.net/index.html?foo=bar&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlR3JlYXRlclRoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTQyMDA3MDQwMH0sIkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzY3MTM5MjAwfSwiSXBBZGRyZXNzIjp7IkFXUzpTb3VyY2VJcCI6IjU0LjI0MC4xOTYuMTY5LzMyIn19LCJSZXNvdXJjZSI6Imh0dHA6Ly9kMnJhZ3ZqaGxuZ2ZiNi5jbG91ZGZyb250Lm5ldC9pbmRleC5odG1sP2Zvbz1iYXIifV19&Signature=ggae69gtUM1c8Av6wWyqlkZWk1sSmUgzPSNn0tUwKwmuEeaDZEy8HqLu~iHYXjHw7uyQomB8O8kg4UozKn~RjIgg4rPo3SjFlcDHB4E-CK8F69w2-bFifLBYb92lhW~qIPtP1HLdc8jXnY3-vp3pj8Lpxl3m7z5UTDZPSAX~u9ZTFZvDo2HEdXWj86EKwXXLqdZlsFBoxC1kVo9hRJPG~zovp0xxz8MdgeidFrHJm-iyiW07A7AJ52mbSZ0KgLOa0TPNgcu-v1jZqUJKDIOtSGU10jh0DM3jpKqcT7gTZW3sQwmApw9Yklf6t0a0pnAE7TDYlLZ6ulnJeQMMKXN8FQ__&Key-Pair-Id=APKAJW2UAWQ7F2BI3OHA"
        self.assertEqual(expected_url, self.signer.sign(
            "http://d2ragvjhlngfb6.cloudfront.net/index.html?foo=bar",
            expires=1767139200, starts=1420070400,
            ip_address="54.240.196.169"))

    def test_sign_expire_start(self):
        expected_url = "http://d2ragvjhlngfb6.cloudfront.net/index.html?Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlR3JlYXRlclRoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTQyMDA3MDQwMH0sIkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzY3MTM5MjAwfX0sIlJlc291cmNlIjoiaHR0cDovL2QycmFndmpobG5nZmI2LmNsb3VkZnJvbnQubmV0L2luZGV4Lmh0bWwifV19&Signature=DRQ8dBO5SNfoPtFHwmbMFp5MOve8WU5-IkUBm1EMX2xi1tHY1aAiQMlbMtWFel8vHCeYcgcd-aVHRYlwAsG3Fq28HivqGNKBGvhVXUzkM9Jd-BUIWifmpuvH6hw3g7Q6C~3txZ709jxqMBONNSLgBVjL4QXNEycHIgCq43uA9n9Vc3gVOcHf-SVTXpmRl0nt2ZdgjZaN2Dg06sLmE1xEWBbXPrKi455ykZtpsbUXALPHxbnfIOiCi~uF8qrxNvS~nxwQ1zf-kz3avVjd4ruf4Q4QTB8nuGtERBlMCTske8X5-7gzrDejrZW7FMhNiaGdG~QErX0FGMC80XxN-qe0Jw__&Key-Pair-Id=APKAJW2UAWQ7F2BI3OHA"
        self.assertEqual(expected_url, self.signer.sign(
            "http://d2ragvjhlngfb6.cloudfront.net/index.html",
            expires=1767139200, starts=1420070400))

    def test_sign_expire_ip(self):
        expected_url = "http://d2ragvjhlngfb6.cloudfront.net/index.html?Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzEzOTIwMH0sIklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiI1NC4yNDAuMTk2LjAvMSJ9fSwiUmVzb3VyY2UiOiJodHRwOi8vZDJyYWd2amhsbmdmYjYuY2xvdWRmcm9udC5uZXQvaW5kZXguaHRtbCJ9XX0_&Signature=JQy1XUUal8fM50FYfVWtu4po0AfzXqN0YwImv0yLbZkYg7~J~ZeESznOdIG8lLyzRLIDXYmrP0Lz4PW-L7UYPkpCiqDI9mHHMBJUF7rMlleR4vSfdyeSqPAPq-R0SarelXNUYN9yaXkVWbgtalcaoC3jNBUwZun7Fhb6PI1~1oKIYIKRIGo~1mfqwOjzBS5B1oHlXO5SmW9yXE9MjkfYYcVlJrGizpwIgj0L6qe8eBCbSQNTq7BpyNc5~4YaiFS-tBv~GpQoJdUey1CSZJrYGfkqySAOZIeWphrNVInfxCy8Hai06UYs7QPszhTuK~hlPEJab2~sZJQ6Ce6hufXx9A__&Key-Pair-Id=APKAJW2UAWQ7F2BI3OHA"
        self.assertEqual(expected_url, self.signer.sign(
            "http://d2ragvjhlngfb6.cloudfront.net/index.html",
            expires=1767139200,
            ip_address="54.240.196.0/1"))  # Note: VPN can not fool CloudFront


class TestS3PostPresigner(BaseSignerTest):
    def setUp(self):
        super(TestS3PostPresigner, self).setUp()
        self.request_signer = RequestSigner(
            'service_name', 'region_name', 'signing_name',
            's3v4', self.credentials, self.emitter)
        self.signer = S3PostPresigner(self.request_signer)
        self.request_dict = {
            'headers': {},
            'url': 'https://s3.amazonaws.com/mybucket',
            'body': b'',
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
        super(TestS3PostPresigner, self).tearDown()
        self.datetime_patch.stop()

    def test_generate_presigned_post(self):
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'s3v4-presign-post': self.auth}):
            post_form_args = self.signer.generate_presigned_post(
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

    def test_generate_presigned_post_with_conditions(self):
        conditions = [
            {'bucket': 'mybucket'},
            ['starts-with', '$key', 'bar']
        ]
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'s3v4-presign-post': self.auth}):
            self.signer.generate_presigned_post(
                self.request_dict, conditions=conditions)
        self.auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            service_name='signing_name')
        self.add_auth.assert_called_once()
        ref_request = self.add_auth.call_args[0][0]
        ref_policy = ref_request.context['s3-presign-post-policy']
        self.assertEqual(ref_policy['conditions'], conditions)

    def test_generate_presigned_post_with_region_override(self):
        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'s3v4-presign-post': self.auth}):
            self.signer.generate_presigned_post(
                self.request_dict, region_name='foo')
        self.auth.assert_called_with(
            credentials=self.credentials, region_name='foo',
            service_name='signing_name')

    def test_generate_presigned_post_fixes_s3_host(self):
        self.request_signer = RequestSigner(
            'service_name', 'region_name', 'signing_name',
            's3', self.credentials, self.emitter)
        self.signer = S3PostPresigner(self.request_signer)

        with mock.patch.dict(botocore.auth.AUTH_TYPE_MAPS,
                             {'s3-presign-post': self.auth}):
            post_form_args = self.signer.generate_presigned_post(
                self.request_dict)
        self.auth.assert_called_with(
            credentials=self.credentials, region_name='region_name',
            service_name='signing_name')
        self.assertEqual(post_form_args['url'],
                         'https://mybucket.s3.amazonaws.com/')

    def test_presigned_post_throws_unsupported_signature_error(self):
        self.request_signer = RequestSigner(
            'service_name', 'region_name', 'signing_name',
            'foo', self.credentials, self.emitter)
        self.signer = S3PostPresigner(self.request_signer)
        with self.assertRaises(UnsupportedSignatureVersionError):
            self.signer.generate_presigned_post({})


class TestGenerateUrl(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('s3', region_name='us-east-1')
        self.bucket = 'mybucket'
        self.key = 'mykey'
        self.client_kwargs = {'Bucket': self.bucket, 'Key': self.key}
        self.generate_url_patch = mock.patch(
            'botocore.signers.RequestSigner.generate_presigned_url')
        self.generate_url_mock = self.generate_url_patch.start()

    def tearDown(self):
        self.generate_url_patch.stop()

    def test_generate_presigned_url(self):
        self.client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket, 'Key': self.key})

        ref_request_dict = {
            'body': b'',
            'url': u'https://s3.amazonaws.com/mybucket/mykey',
            'headers': {},
            'query_string': {},
            'url_path': u'/mybucket/mykey',
            'method': u'GET'}
        self.generate_url_mock.assert_called_with(
            request_dict=ref_request_dict, expires_in=3600)

    def test_generate_presigned_url_with_query_string(self):
        disposition = 'attachment; filename="download.jpg"'
        self.client.generate_presigned_url(
            'get_object', Params={
                'Bucket': self.bucket,
                'Key': self.key,
                'ResponseContentDisposition': disposition})
        ref_request_dict = {
            'body': b'',
            'url': (u'https://s3.amazonaws.com/mybucket/mykey'
                    '?response-content-disposition='
                    'attachment%3B%20filename%3D%22download.jpg%22'),
            'headers': {},
            'query_string': {u'response-content-disposition': disposition},
            'url_path': u'/mybucket/mykey',
            'method': u'GET'}
        self.generate_url_mock.assert_called_with(
            request_dict=ref_request_dict, expires_in=3600)

    def test_generate_presigned_url_unknown_method_name(self):
        with self.assertRaises(UnknownClientMethodError):
            self.client.generate_presigned_url('getobject')

    def test_generate_presigned_url_missing_required_params(self):
        with self.assertRaises(ParamValidationError):
            self.client.generate_presigned_url('get_object')

    def test_generate_presigned_url_expires(self):
        self.client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket, 'Key': self.key},
            ExpiresIn=20)
        ref_request_dict = {
            'body': b'',
            'url': u'https://s3.amazonaws.com/mybucket/mykey',
            'headers': {},
            'query_string': {},
            'url_path': u'/mybucket/mykey',
            'method': u'GET'}
        self.generate_url_mock.assert_called_with(
            request_dict=ref_request_dict, expires_in=20)

    def test_generate_presigned_url_override_http_method(self):
        self.client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket, 'Key': self.key},
            HttpMethod='PUT')
        ref_request_dict = {
            'body': b'',
            'url': u'https://s3.amazonaws.com/mybucket/mykey',
            'headers': {},
            'query_string': {},
            'url_path': u'/mybucket/mykey',
            'method': u'PUT'}
        self.generate_url_mock.assert_called_with(
            request_dict=ref_request_dict, expires_in=3600)


class TestGeneratePresignedPost(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('s3', region_name='us-east-1')
        self.bucket = 'mybucket'
        self.key = 'mykey'
        self.presign_post_patch = mock.patch(
            'botocore.signers.S3PostPresigner.generate_presigned_post')
        self.presign_post_mock = self.presign_post_patch.start()

    def tearDown(self):
        self.presign_post_patch.stop()

    def test_generate_presigned_post(self):
        self.client.generate_presigned_post(self.bucket, self.key)

        _, post_kwargs = self.presign_post_mock.call_args
        request_dict = post_kwargs['request_dict']
        fields = post_kwargs['fields']
        conditions = post_kwargs['conditions']
        self.assertEqual(
            request_dict['url'], 'https://s3.amazonaws.com/mybucket')
        self.assertEqual(post_kwargs['expires_in'], 3600)
        self.assertEqual(
            conditions,
            [{'bucket': 'mybucket'}, {'key': 'mykey'}])
        self.assertEqual(
            fields,
            {'key': 'mykey'})

    def test_generate_presigned_post_with_filename(self):
        self.key = 'myprefix/${filename}'
        self.client.generate_presigned_post(self.bucket, self.key)

        _, post_kwargs = self.presign_post_mock.call_args
        request_dict = post_kwargs['request_dict']
        fields = post_kwargs['fields']
        conditions = post_kwargs['conditions']
        self.assertEqual(
            request_dict['url'], 'https://s3.amazonaws.com/mybucket')
        self.assertEqual(post_kwargs['expires_in'], 3600)
        self.assertEqual(
            conditions,
            [{'bucket': 'mybucket'}, ['starts-with', '$key', 'myprefix/']])
        self.assertEqual(
            fields,
            {'key': 'myprefix/${filename}'})

    def test_generate_presigned_post_expires(self):
        self.client.generate_presigned_post(
            self.bucket, self.key, ExpiresIn=50)
        _, post_kwargs = self.presign_post_mock.call_args
        request_dict = post_kwargs['request_dict']
        fields = post_kwargs['fields']
        conditions = post_kwargs['conditions']
        self.assertEqual(
            request_dict['url'], 'https://s3.amazonaws.com/mybucket')
        self.assertEqual(post_kwargs['expires_in'], 50)
        self.assertEqual(
            conditions,
            [{'bucket': 'mybucket'}, {'key': 'mykey'}])
        self.assertEqual(
            fields,
            {'key': 'mykey'})

    def test_generate_presigned_post_with_prefilled(self):
        conditions = [{'acl': 'public-read'}]
        fields = {'acl': 'public-read'}

        self.client.generate_presigned_post(
            self.bucket, self.key, Fields=fields, Conditions=conditions)

        _, post_kwargs = self.presign_post_mock.call_args
        request_dict = post_kwargs['request_dict']
        fields = post_kwargs['fields']
        conditions = post_kwargs['conditions']
        self.assertEqual(
            request_dict['url'], 'https://s3.amazonaws.com/mybucket')
        self.assertEqual(
            conditions,
            [{'acl': 'public-read'}, {'bucket': 'mybucket'}, {'key': 'mykey'}])
        self.assertEqual(fields['acl'], 'public-read')
        self.assertEqual(
            fields, {'key': 'mykey', 'acl': 'public-read'})

    def test_generate_presigned_post_non_s3_client(self):
        self.client = self.session.create_client('ec2', 'us-west-2')
        with self.assertRaises(AttributeError):
            self.client.generate_presigned_post()
