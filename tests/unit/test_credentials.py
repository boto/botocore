#!/usr/bin/env
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from tests import unittest, BaseEnvVar
import json
import os

import mock

import botocore.session
import botocore.exceptions
from botocore import credentials
from botocore.vendored.requests import ConnectionError

# Passed to session to keep it from finding default config file
TESTENVVARS = {'config_file': (None, 'AWS_CONFIG_FILE', None)}


metadata = {'foobar': {'Code': 'Success', 'LastUpdated':
                       '2012-12-03T14:38:21Z', 'AccessKeyId': 'foo',
                       'SecretAccessKey': 'bar', 'Token': 'foobar',
                       'Expiration': '2012-12-03T20:48:03Z', 'Type':
                       'AWS-HMAC'}}


def path(filename):
    return os.path.join(os.path.dirname(__file__), 'cfg', filename)


class EnvVarTest(BaseEnvVar):

    def setUp(self):
        super(EnvVarTest, self).setUp()
        self.environ['AWS_CONFIG_FILE'] = path('aws_config_nocreds')
        self.environ['BOTO_CONFIG'] = ''
        self.environ['AWS_ACCESS_KEY_ID'] = 'foo'
        self.environ['AWS_SECRET_ACCESS_KEY'] = 'bar'
        self.session = botocore.session.get_session(env_vars=TESTENVVARS)

    def test_envvar(self):
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.access_key, 'foo')
        self.assertEqual(credentials.secret_key, 'bar')
        self.assertEqual(credentials.method, 'env')


class CredentialsFileTest(BaseEnvVar):

    def setUp(self):
        super(CredentialsFileTest, self).setUp()
        self.environ['BOTO_CONFIG'] = ''
        self.session = botocore.session.get_session(env_vars=TESTENVVARS)

    def test_credentials_file(self):
        self.environ['AWS_CREDENTIAL_FILE'] = path('aws_credentials')
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.access_key, 'foo')
        self.assertEqual(credentials.secret_key, 'bar')
        self.assertEqual(credentials.method, 'credentials-file')

    @mock.patch('botocore.vendored.requests.get')
    def test_bad_file(self, get):
        self.environ['AWS_CREDENTIAL_FILE'] = path('no_aws_credentials')
        credentials = self.session.get_credentials()
        self.assertIsNone(credentials)


class ConfigTest(BaseEnvVar):

    def setUp(self):
        super(ConfigTest, self).setUp()
        self.environ['AWS_CONFIG_FILE'] = path('aws_config')
        self.environ['BOTO_CONFIG'] = ''
        self.session = botocore.session.get_session(env_vars=TESTENVVARS)

    def test_config(self):
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.access_key, 'foo')
        self.assertEqual(credentials.secret_key, 'bar')
        self.assertEqual(credentials.method, 'config')
        self.assertEqual(len(self.session.available_profiles), 2)
        self.assertIn('default', self.session.available_profiles)
        self.assertIn('personal', self.session.available_profiles)

    def test_default_profile_is_obeyed(self):
        self.environ['BOTO_DEFAULT_PROFILE'] = 'personal'
        session = botocore.session.get_session()
        credentials = session.get_credentials()
        self.assertEqual(credentials.access_key, 'fie')
        self.assertEqual(credentials.secret_key, 'baz')
        self.assertEqual(credentials.token, 'fiebaz')
        self.assertEqual(credentials.method, 'config')
        self.assertEqual(len(session.available_profiles), 2)
        self.assertIn('default', session.available_profiles)
        self.assertIn('personal', session.available_profiles)


class BotoConfigTest(BaseEnvVar):

    def setUp(self):
        super(BotoConfigTest, self).setUp()
        self.environ['BOTO_CONFIG'] = path('boto_config')
        self.session = botocore.session.get_session(env_vars=TESTENVVARS)

    def test_boto_config(self):
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.access_key, 'foo')
        self.assertEqual(credentials.secret_key, 'bar')
        self.assertEqual(credentials.method, 'boto')


class IamRoleTest(BaseEnvVar):
    def setUp(self):
        super(IamRoleTest, self).setUp()
        self.session = botocore.session.get_session(env_vars=TESTENVVARS)
        self.environ['BOTO_CONFIG'] = ''

    @mock.patch('botocore.credentials.retrieve_iam_role_credentials')
    def test_iam_role(self, retriever):
        retriever.return_value = metadata
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.method, 'iam-role')
        self.assertEqual(credentials.access_key, 'foo')
        self.assertEqual(credentials.secret_key, 'bar')

    @mock.patch('botocore.credentials.retrieve_iam_role_credentials')
    def test_empty_boto_config_is_ignored(self, retriever):
        retriever.return_value = metadata
        self.environ['BOTO_CONFIG'] = path('boto_config_empty')
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.method, 'iam-role')
        self.assertEqual(credentials.access_key, 'foo')
        self.assertEqual(credentials.secret_key, 'bar')

    @mock.patch('botocore.vendored.requests.get')
    def test_get_credentials_with_metadata_mock(self, get):
        first = mock.Mock()
        first.status_code = 200
        first.content = 'foobar'.encode('utf-8')

        second = mock.Mock()
        second.status_code = 200
        second.content = json.dumps(metadata['foobar']).encode('utf-8')
        get.side_effect = [first, second]

        credentials = self.session.get_credentials()
        self.assertEqual(credentials.method, 'iam-role')

    @mock.patch('botocore.vendored.requests.get')
    def test_timeout_argument_forwarded_to_requests(self, get):
        first = mock.Mock()
        first.status_code = 200
        first.content = 'foobar'.encode('utf-8')

        second = mock.Mock()
        second.status_code = 200
        second.content = json.dumps(metadata['foobar']).encode('utf-8')
        get.side_effect = [first, second]

        credentials.retrieve_iam_role_credentials(timeout=10)
        self.assertEqual(get.call_args[1]['timeout'], 10)

    @mock.patch('botocore.vendored.requests.get')
    def test_request_timeout_occurs(self, get):
        first = mock.Mock()
        first.side_effect = ConnectionError

        d = credentials.retrieve_iam_role_credentials(timeout=10)
        self.assertEqual(d, {})

    @mock.patch('botocore.vendored.requests.get')
    def test_retry_errors(self, get):
        # First attempt we get a connection error.
        first = mock.Mock()
        first.side_effect = ConnectionError

        # Next attempt we get a response with the foobar key.
        second = mock.Mock()
        second.status_code = 200
        second.content = 'foobar'.encode('utf-8')

        # Next attempt we get a response with the foobar creds.
        third = mock.Mock()
        third.status_code = 200
        third.content = json.dumps(metadata['foobar']).encode('utf-8')
        get.side_effect = [first, second, third]

        retrieved = credentials.retrieve_iam_role_credentials(
            num_retries=1)
        self.assertEqual(retrieved['foobar']['AccessKeyId'], 'foo')


if __name__ == "__main__":
    unittest.main()
