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

import datetime
import json
import mock
import os

from botocore import credentials
import botocore.exceptions
import botocore.session
from botocore.vendored.requests import ConnectionError

from tests import unittest, BaseEnvVar, create_session


# Passed to session to keep it from finding default config file
TESTENVVARS = {'config_file': (None, 'AWS_CONFIG_FILE', None)}


raw_metadata = {
    'foobar': {
        'Code': 'Success',
        'LastUpdated': '2012-12-03T14:38:21Z',
        'AccessKeyId': 'foo',
        'SecretAccessKey': 'bar',
        'Token': 'foobar',
        'Expiration': '2012-12-03T20:48:03Z',
        'Type': 'AWS-HMAC'
    }
}
post_processed_metadata = {
    'role_name': 'foobar',
    'access_key': raw_metadata['foobar']['AccessKeyId'],
    'secret_key': raw_metadata['foobar']['SecretAccessKey'],
    'token': raw_metadata['foobar']['Token'],
    'expiry_time': raw_metadata['foobar']['Expiration'],
}


def path(filename):
    return os.path.join(os.path.dirname(__file__), 'cfg', filename)


class RefreshableCredentialsTest(BaseEnvVar):
    def setUp(self):
        super(RefreshableCredentialsTest, self).setUp()
        self.creds = credentials.RefreshableCredentials()

    def test_refresh_needed(self):
        self.creds.expiry_time = None
        self.assertFalse(self.creds.refresh_needed())

        # With a current expiry.
        self.creds.expiry_time = datetime.datetime.utcnow() + \
                                  datetime.timedelta(days=1)
        self.assertFalse(self.creds.refresh_needed())

        # With an outdated expiry.
        self.creds.expiry_time = datetime.datetime.utcnow() + \
                                  datetime.timedelta(seconds=30)
        self.assertTrue(self.creds.refresh_needed())

    def test_create_from_metadata(self):
        new_metadata = {
            'role_name': 'foobaz',
            'access_key': 'abcdef123456',
            'secret_key': '123456abcdef',
            'expiry_time': '2014-03-07T15:24:46Z',
        }
        creds = credentials.RefreshableCredentials.create_from_metadata(
            post_processed_metadata,
            method='testing',
            refresh_using=lambda: new_metadata
        )
        # Test the internals, so as not to kick off a refresh.
        self.assertEqual(creds._access_key, 'foo')
        self.assertEqual(creds._secret_key, 'bar')
        self.assertEqual(creds._token, 'foobar')
        self.assertEqual(
            creds.expiry_time,
            datetime.datetime(2012, 12, 3, 20, 48, 3)
        )
        self.assertEqual(creds.method, 'testing')
        self.assertTrue(self.creds.refresh_needed())

        # Kick a refresh.
        self.assertEqual(creds.access_key, 'abcdef123456')
        self.assertEqual(
            creds.expiry_time,
            datetime.datetime(2014, 3, 7, 15, 24, 46)
        )


class EnvVarTest(BaseEnvVar):

    def setUp(self):
        super(EnvVarTest, self).setUp()
        self.environ['AWS_CONFIG_FILE'] = path('aws_config_nocreds')
        self.environ['BOTO_CONFIG'] = ''
        self.environ['AWS_ACCESS_KEY_ID'] = 'foo'
        self.environ['AWS_SECRET_ACCESS_KEY'] = 'bar'
        self.session = create_session(session_vars=TESTENVVARS)

    def test_envvar(self):
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.access_key, 'foo')
        self.assertEqual(credentials.secret_key, 'bar')
        self.assertEqual(credentials.method, 'env')


class CredentialsFileTest(BaseEnvVar):

    def setUp(self):
        super(CredentialsFileTest, self).setUp()
        self.environ['BOTO_CONFIG'] = ''
        self.session = create_session(session_vars=TESTENVVARS)

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
        self.session = create_session(session_vars=TESTENVVARS)

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
        session = create_session()
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
        self.session = create_session(session_vars=TESTENVVARS)

    def test_boto_config(self):
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.access_key, 'foo')
        self.assertEqual(credentials.secret_key, 'bar')
        self.assertEqual(credentials.method, 'boto')


class IamRoleTest(BaseEnvVar):
    def setUp(self):
        super(IamRoleTest, self).setUp()
        self.session = create_session(session_vars=TESTENVVARS)
        self.environ['BOTO_CONFIG'] = ''

    @mock.patch('botocore.utils.InstanceMetadataFetcher.retrieve_iam_role_credentials')
    def test_iam_role(self, retriever):
        retriever.return_value = post_processed_metadata
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.method, 'iam-role')
        self.assertEqual(credentials.access_key, 'foo')
        self.assertEqual(credentials.secret_key, 'bar')

    @mock.patch('botocore.utils.InstanceMetadataFetcher.retrieve_iam_role_credentials')
    def test_session_config_timeout_var(self, retriever):
        retriever.return_value = post_processed_metadata
        self.session.set_config_variable('metadata_service_timeout', '20.0')
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.method, 'iam-role')
        self.assertEqual(retriever.call_args[1]['timeout'], 20.0)

    @mock.patch('botocore.utils.InstanceMetadataFetcher.retrieve_iam_role_credentials')
    def test_session_config_num_attempts_var(self, retriever):
        retriever.return_value = post_processed_metadata
        self.session.set_config_variable('metadata_service_num_attempts', '5')
        credentials = self.session.get_credentials()
        self.assertEqual(credentials.method, 'iam-role')
        self.assertEqual(retriever.call_args[1]['num_attempts'], 5)

    @mock.patch('botocore.utils.InstanceMetadataFetcher.retrieve_iam_role_credentials')
    def test_empty_boto_config_is_ignored(self, retriever):
        retriever.return_value = post_processed_metadata
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
        second.content = json.dumps(raw_metadata['foobar']).encode('utf-8')
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
        second.content = json.dumps(raw_metadata['foobar']).encode('utf-8')
        get.side_effect = [first, second]

        self.session.set_config_variable('metadata_service_timeout', 10)
        iam_creds = credentials.InstanceMetadataProvider(session=self.session)
        iam_creds.load()
        self.assertEqual(get.call_args[1]['timeout'], 10)

    @mock.patch('botocore.vendored.requests.get')
    def test_request_timeout_occurs(self, get):
        first = mock.Mock()
        first.side_effect = ConnectionError

        self.session.set_config_variable('metadata_service_timeout', 10)
        iam_creds = credentials.InstanceMetadataProvider(session=self.session)
        d = iam_creds.load()
        self.assertEqual(d, None)

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
        third.content = json.dumps(raw_metadata['foobar']).encode('utf-8')
        get.side_effect = [first, second, third]

        self.session.set_config_variable('metadata_service_num_attempts', 2)
        iam_creds = credentials.InstanceMetadataProvider(session=self.session)
        retrieved = iam_creds.load()
        # Using the property would see an expired set of credentials (old
        # hardcoded expiry in the response) & try to refresh again, which isn't
        # what we're testing here.
        # So we're going to check the private variable here instead of the
        # public property.
        self.assertEqual(retrieved._access_key, 'foo')


class CredentialResolverTest(BaseEnvVar):
    def setUp(self):
        super(CredentialResolverTest, self).setUp()
        self.environ['AWS_CONFIG_FILE'] = path('aws_config_nocreds')
        self.environ['BOTO_CONFIG'] = ''
        self.environ['AWS_ACCESS_KEY_ID'] = 'foo'
        self.environ['AWS_SECRET_ACCESS_KEY'] = 'bar'
        self.session = create_session(session_vars=TESTENVVARS)
        self.default_resolver = credentials.CredentialResolver(
            session=self.session
        )
        self.small_resolver = credentials.CredentialResolver(
            session=self.session,
            methods=[
                credentials.BotoProvider(),
                credentials.ConfigProvider()
            ]
        )

    def test_default_init(self):
        self.assertEqual(self.default_resolver.available_methods, [
            'env',
            'config',
            'credentials-file',
            'boto',
            'iam-role',
        ])
        self.assertEqual(len(self.default_resolver.methods), 5)

    def test_custom_init(self):
        resolver = credentials.CredentialResolver(methods=[
            credentials.BotoProvider(),
            credentials.ConfigProvider()
        ])
        self.assertEqual(resolver.available_methods, [
            'boto',
            'config',
        ])
        self.assertEqual(len(resolver.methods), 2)

    def test_insert_before(self):
        # Sanity check.
        self.assertEqual(self.small_resolver.available_methods, [
            'boto',
            'config',
        ])

        self.small_resolver.insert_before('boto', credentials.EnvProvider())
        self.assertEqual(self.small_resolver.available_methods, [
            'env',
            'boto',
            'config',
        ])

        self.small_resolver.insert_before(
            'config',
            credentials.OriginalEC2Provider()
        )
        self.assertEqual(self.small_resolver.available_methods, [
            'env',
            'boto',
            'credentials-file',
            'config',
        ])

        # Test a failed insert.
        with self.assertRaises(botocore.exceptions.UnknownCredentialError):
            self.small_resolver.insert_before(
                'foobar',
                credentials.InstanceMetadataProvider()
            )

    def test_insert_after(self):
        # Sanity check.
        self.assertEqual(self.small_resolver.available_methods, [
            'boto',
            'config',
        ])

        self.small_resolver.insert_after('boto', credentials.EnvProvider())
        self.assertEqual(self.small_resolver.available_methods, [
            'boto',
            'env',
            'config',
        ])

        self.small_resolver.insert_after(
            'config',
            credentials.OriginalEC2Provider()
        )
        self.assertEqual(self.small_resolver.available_methods, [
            'boto',
            'env',
            'config',
            'credentials-file',
        ])

        # Test a failed insert.
        with self.assertRaises(botocore.exceptions.UnknownCredentialError):
            self.small_resolver.insert_after(
                'foobar',
                credentials.InstanceMetadataProvider()
            )

    def test_remove(self):
        # Sanity check.
        self.assertEqual(self.small_resolver.available_methods, [
            'boto',
            'config',
        ])

        # Should work.
        self.small_resolver.remove('boto')
        self.assertEqual(self.small_resolver.available_methods, [
            'config',
        ])

        # Should silently fail.
        self.small_resolver.remove('boto')
        self.assertEqual(self.small_resolver.available_methods, [
            'config',
        ])

        # Should silently fail.
        self.small_resolver.remove('foobar')
        self.assertEqual(self.small_resolver.available_methods, [
            'config',
        ])

    def test_get_credentials(self):
        # Should return the environment ones (from the ``setUp``).
        creds = self.default_resolver.get_credentials()
        self.assertEqual(creds.method, 'env')
        self.assertEqual(creds.access_key, 'foo')


class AlternateCredentialResolverTest(BaseEnvVar):
    def setUp(self):
        super(AlternateCredentialResolverTest, self).setUp()
        self.environ['AWS_CONFIG_FILE'] = path('aws_config')
        self.environ['BOTO_CONFIG'] = ''
        self.session = create_session(session_vars=TESTENVVARS)
        self.small_resolver = credentials.CredentialResolver(
            session=self.session,
            methods=[
                credentials.BotoProvider(),
                credentials.ConfigProvider(session=self.session)
            ]
        )

    def test_get_credentials(self):
        # Sanity check.
        self.assertEqual(self.small_resolver.available_methods, [
            'boto',
            'config',
        ])

        # Now with something custom.
        creds = self.small_resolver.get_credentials()
        self.assertEqual(creds.method, 'config')
        self.assertEqual(creds.access_key, 'foo')


if __name__ == "__main__":
    unittest.main()
