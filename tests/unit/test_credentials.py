#!/usr/bin/env
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

from tests import unittest, BaseEnvVar
import json
import os
import datetime

import mock

import botocore.session
import botocore.exceptions
from botocore import credentials
from botocore.vendored.requests import ConnectionError, Response


# Passed to session to keep it from finding default config file
TESTENVVARS = {'config_file': (None, 'AWS_CONFIG_FILE', None)}


metadata = {'foobar': {'Code': 'Success', 'LastUpdated':
                       '2012-12-03T14:38:21Z', 'AccessKeyId': 'foo',
                       'SecretAccessKey': 'bar', 'Token': 'foobar',
                       'Expiration': '2012-12-03T20:48:03Z', 'Type':
                       'AWS-HMAC'}}


return1 = {
    'AssumedRoleUser':
        {
        'AssumedRoleId': 'AAAA:foobar',
        'Arn': 'arn:aws:sts::123456789012:assumed-role/FooBar/foobar'
        },
    'Credentials': {
        'SecretAccessKey': 'secret_key',
        'SessionToken': 'session_token',
        'Expiration': '2014-01-23T17:00:00Z',
        'AccessKeyId': 'access_key'},
    'ResponseMetadata': {'RequestId': '962be6e2-844b-11e3-93e3-9fcaebaba3bb'}}

return2 = {
    'AssumedRoleUser':
        {
        'AssumedRoleId': 'AAAA:foobar',
        'Arn': 'arn:aws:sts::123456789012:assumed-role/FooBar/foobar'
        },
    'Credentials': {
        'SecretAccessKey': 'secret_key2',
        'SessionToken': 'session_token2',
        'Expiration': '2014-01-23T18:00:00Z',
        'AccessKeyId': 'access_key2'},
    'ResponseMetadata': {'RequestId': '962be6e2-844b-11e3-93e3-9fcaebaba3bb'}}

json_body = ('{"AccessKeyId": "access_key3",'
             '"SecretAccessKey": "secret_key3",'
             '"Expiration": "2014-01-23T12:00:00Z",'
             '"CredentialOp": "AssumeRole",'
             '"SessionToken": "session_token3",'
             '"CredentialParams": {'
             '"role_session_name": "foobar",'
             '"role_arn": "arn:aws:iam::123456789012:role/FooBar"'
             '}}'
             )

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
    def test_session_config_timeout_var(self, retriever):
        retriever.return_value = metadata
        self.session.set_config_variable('metadata_service_timeout', '20.0')
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.method, 'iam-role')
        self.assertEqual(retriever.call_args[1]['timeout'], 20.0)

    @mock.patch('botocore.credentials.retrieve_iam_role_credentials')
    def test_session_config_num_attempts_var(self, retriever):
        retriever.return_value = metadata
        self.session.set_config_variable('metadata_service_num_attempts', '5')
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.method, 'iam-role')
        self.assertEqual(retriever.call_args[1]['num_attempts'], 5)

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
            num_attempts=2)
        self.assertEqual(retrieved['foobar']['AccessKeyId'], 'foo')


class TestTemporaryCredentials(BaseEnvVar):
    
    def setUp(self):
        super(TestTemporaryCredentials, self).setUp()
        self.session = botocore.session.get_session(env_vars=TESTENVVARS)
        self.environ['AWS_CONFIG_FILE'] = path('aws_config')
        self.http_response = Response()
        self.http_response.status_code = 200
        self.make_request_patch = mock.patch('botocore.endpoint.Endpoint.make_request')
        self.make_request_is_patched = False
        self.datetime_patch = mock.patch.object(
            botocore.credentials.datetime, 'datetime',
            mock.Mock(wraps=datetime.datetime))

    def tearDown(self):
        # This clears all the previous registrations.
        self.stop_make_request_patch()
        cache_path = credentials.get_temporary_credential_path(self.session)
        if cache_path:
            os.unlink(cache_path)
        super(TestTemporaryCredentials, self).setUp()

    def start_make_request_patch(self, parsed_data):
        make_request_patch = self.make_request_patch.start()
        make_request_patch.return_value = (self.http_response, parsed_data)
        self.make_request_is_patched = True

    def stop_make_request_patch(self):
        if self.make_request_is_patched:
            self.make_request_patch.stop()
            self.make_request_is_patched = False

    def test_create_and_refresh(self):
        # First delete any existing .sessions directory
        cache_path = credentials.get_temporary_credential_path(self.session)
        if os.path.exists(cache_path):
            os.unlink(cache_path)
        # Make sure there is no .sessions cache directory
        self.assertFalse(os.path.exists(cache_path))
        # Patch make_request
        self.start_make_request_patch(return1)
        # First try to check the credentials with a mocked datetime
        # that is prior to the expiration of the credentials.
        mocked_datetime = self.datetime_patch.start()
        mocked_datetime.utcnow.return_value = datetime.datetime(2014, 1, 23, 16, 0)
        # Create temporary credentials
        tc = credentials.create_temporary_credentials(
            self.session, 'sts', 'AssumeRole',
            role_arn='arn:aws:iam::123456789012:role/FooBar',
            role_session_name='foobar')
        self.stop_make_request_patch()
        # Now make sure the session file does exist now
        self.assertTrue(os.path.exists(cache_path))
        # Make sure we have the right values in our credential object.
        self.assertEqual(tc.access_key, return1['Credentials']['AccessKeyId'])
        self.assertEqual(tc.secret_key, return1['Credentials']['SecretAccessKey'])
        self.assertEqual(tc.token, return1['Credentials']['SessionToken'])
        self.datetime_patch.stop()
        self.start_make_request_patch(return2)
        # Now try to check the credentials with a mocked datetime
        # that is within 15 minutes of the expiration of the credentials.
        mocked_datetime = self.datetime_patch.start()
        mocked_datetime.utcnow.return_value = datetime.datetime(2014, 1, 23, 16, 46)
        # These attribute accesses should cause the TemporaryCredentials
        # object to check it's expiration date against the current time.
        # This should cause it to refetch credentials.
        self.assertEqual(tc.access_key, return2['Credentials']['AccessKeyId'])
        self.assertEqual(tc.secret_key, return2['Credentials']['SecretAccessKey'])
        self.assertEqual(tc.token, return2['Credentials']['SessionToken'])
        self.datetime_patch.stop()
        self.stop_make_request_patch()

    def test_use_existing(self):
        # Create a file containing credential data
        cache_path = credentials.get_temporary_credential_path(self.session)
        with open(cache_path, 'w') as fp:
            fp.write(json_body)
        # Patch make_request
        self.start_make_request_patch(return1)
        # Try to check the credentials with a mocked datetime
        # that is prior to the expiration of the credentials.
        # This should not require a fetch of new credentials
        # so we should end up with the data from the file we created.
        mocked_datetime = self.datetime_patch.start()
        mocked_datetime.utcnow.return_value = datetime.datetime(2014, 1, 23, 11, 30)
        # Create temporary credentials
        tc = credentials.create_temporary_credentials(self.session)
        # Now make sure the session file does exist now
        self.assertTrue(os.path.exists(cache_path))
        # Make sure we have the right values in our credential object.
        self.assertEqual(tc.access_key, 'access_key3')
        self.assertEqual(tc.secret_key, 'secret_key3')
        self.assertEqual(tc.token, 'session_token3')
        self.datetime_patch.stop()
        
if __name__ == "__main__":
    unittest.main()
