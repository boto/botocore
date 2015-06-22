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
import mock
import os

from dateutil.tz import tzlocal

from botocore import credentials
from botocore.credentials import EnvProvider
import botocore.exceptions
import botocore.session
from tests import unittest, BaseEnvVar


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


class TestRefreshableCredentials(BaseEnvVar):
    def setUp(self):
        super(TestRefreshableCredentials, self).setUp()
        self.refresher = mock.Mock()
        self.metadata = {
            'access_key': 'NEW-ACCESS',
            'secret_key': 'NEW-SECRET',
            'token': 'NEW-TOKEN',
            'expiry_time': '2015-03-07T15:24:46Z',
            'role_name': 'rolename',
        }
        self.refresher.return_value = self.metadata
        self.expiry_time = \
            datetime.datetime.now(tzlocal()) - datetime.timedelta(minutes=30)
        self.mock_time = mock.Mock()
        self.creds = credentials.RefreshableCredentials(
            'ORIGINAL-ACCESS', 'ORIGINAL-SECRET', 'ORIGINAL-TOKEN',
            self.expiry_time, self.refresher, 'iam-role',
            time_fetcher=self.mock_time
        )

    def test_refresh_needed(self):
        # The expiry time was set for 30 minutes ago, so if we
        # say the current time is utcnow(), then we should need
        # a refresh.
        self.mock_time.return_value = datetime.datetime.now(tzlocal())
        self.assertTrue(self.creds.refresh_needed())
        # We should refresh creds, if we try to access "access_key"
        # or any of the cred vars.
        self.assertEqual(self.creds.access_key, 'NEW-ACCESS')
        self.assertEqual(self.creds.secret_key, 'NEW-SECRET')
        self.assertEqual(self.creds.token, 'NEW-TOKEN')

    def test_no_refresh_needed(self):
        # The expiry time was 30 minutes ago, let's say it's an hour
        # ago currently.  That would mean we don't need a refresh.
        self.mock_time.return_value = (
            datetime.datetime.now(tzlocal()) - datetime.timedelta(minutes=60))
        self.assertTrue(not self.creds.refresh_needed())

        self.assertEqual(self.creds.access_key, 'ORIGINAL-ACCESS')
        self.assertEqual(self.creds.secret_key, 'ORIGINAL-SECRET')
        self.assertEqual(self.creds.token, 'ORIGINAL-TOKEN')


class TestEnvVar(BaseEnvVar):

    def test_envvars_are_found_no_token(self):
        environ = {
            'AWS_ACCESS_KEY_ID': 'foo',
            'AWS_SECRET_ACCESS_KEY': 'bar',
        }
        provider = credentials.EnvProvider(environ)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'foo')
        self.assertEqual(creds.secret_key, 'bar')
        self.assertEqual(creds.method, 'env')

    def test_envvars_found_with_security_token(self):
        environ = {
            'AWS_ACCESS_KEY_ID': 'foo',
            'AWS_SECRET_ACCESS_KEY': 'bar',
            'AWS_SECURITY_TOKEN': 'baz',
        }
        provider = credentials.EnvProvider(environ)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'foo')
        self.assertEqual(creds.secret_key, 'bar')
        self.assertEqual(creds.token, 'baz')
        self.assertEqual(creds.method, 'env')

    def test_envvars_found_with_session_token(self):
        environ = {
            'AWS_ACCESS_KEY_ID': 'foo',
            'AWS_SECRET_ACCESS_KEY': 'bar',
            'AWS_SESSION_TOKEN': 'baz',
        }
        provider = credentials.EnvProvider(environ)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'foo')
        self.assertEqual(creds.secret_key, 'bar')
        self.assertEqual(creds.token, 'baz')
        self.assertEqual(creds.method, 'env')

    def test_envvars_not_found(self):
        provider = credentials.EnvProvider(environ={})
        creds = provider.load()
        self.assertIsNone(creds)

    def test_can_override_env_var_mapping(self):
        # We can change the env var provider to
        # use our specified env var names.
        environ = {
            'FOO_ACCESS_KEY': 'foo',
            'FOO_SECRET_KEY': 'bar',
            'FOO_SESSION_TOKEN': 'baz',
        }
        mapping = {
            'access_key': 'FOO_ACCESS_KEY',
            'secret_key': 'FOO_SECRET_KEY',
            'token': 'FOO_SESSION_TOKEN',
        }
        provider = credentials.EnvProvider(
            environ, mapping
        )
        creds = provider.load()
        self.assertEqual(creds.access_key, 'foo')
        self.assertEqual(creds.secret_key, 'bar')
        self.assertEqual(creds.token, 'baz')

    def test_can_override_partial_env_var_mapping(self):
        # Only changing the access key mapping.
        # The other 2 use the default values of
        # AWS_SECRET_ACCESS_KEY and AWS_SESSION_TOKEN
        # use our specified env var names.
        environ = {
            'FOO_ACCESS_KEY': 'foo',
            'AWS_SECRET_ACCESS_KEY': 'bar',
            'AWS_SESSION_TOKEN': 'baz',
        }
        provider = credentials.EnvProvider(
            environ, {'access_key': 'FOO_ACCESS_KEY'}
        )
        creds = provider.load()
        self.assertEqual(creds.access_key, 'foo')
        self.assertEqual(creds.secret_key, 'bar')
        self.assertEqual(creds.token, 'baz')

    def test_partial_creds_is_an_error(self):
        # If the user provides an access key, they must also
        # provide a secret key.  Not doing so will generate an
        # error.
        environ = {
            'AWS_ACCESS_KEY_ID': 'foo',
            # Missing the AWS_SECRET_ACCESS_KEY
        }
        provider = credentials.EnvProvider(environ)
        with self.assertRaises(botocore.exceptions.PartialCredentialsError):
            provider.load()

class TestSharedCredentialsProvider(BaseEnvVar):
    def setUp(self):
        super(TestSharedCredentialsProvider, self).setUp()
        self.ini_parser = mock.Mock()

    def test_credential_file_exists_default_profile(self):
        self.ini_parser.return_value = {
            'default': {
                'aws_access_key_id': 'foo',
                'aws_secret_access_key': 'bar',
            }
        }
        provider = credentials.SharedCredentialProvider(
            creds_filename='~/.aws/creds', profile_name='default',
            ini_parser=self.ini_parser)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'foo')
        self.assertEqual(creds.secret_key, 'bar')
        self.assertIsNone(creds.token)
        self.assertEqual(creds.method, 'shared-credentials-file')

    def test_partial_creds_raise_error(self):
        self.ini_parser.return_value = {
            'default': {
                'aws_access_key_id': 'foo',
                # Missing 'aws_secret_access_key'.
            }
        }
        provider = credentials.SharedCredentialProvider(
            creds_filename='~/.aws/creds', profile_name='default',
            ini_parser=self.ini_parser)
        with self.assertRaises(botocore.exceptions.PartialCredentialsError):
            provider.load()

    def test_credentials_file_exists_with_session_token(self):
        self.ini_parser.return_value = {
            'default': {
                'aws_access_key_id': 'foo',
                'aws_secret_access_key': 'bar',
                'aws_session_token': 'baz',
            }
        }
        provider = credentials.SharedCredentialProvider(
            creds_filename='~/.aws/creds', profile_name='default',
            ini_parser=self.ini_parser)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'foo')
        self.assertEqual(creds.secret_key, 'bar')
        self.assertEqual(creds.token, 'baz')
        self.assertEqual(creds.method, 'shared-credentials-file')

    def test_credentials_file_with_multiple_profiles(self):
        self.ini_parser.return_value = {
            # Here the user has a 'default' and a 'dev' profile.
            'default': {
                'aws_access_key_id': 'a',
                'aws_secret_access_key': 'b',
                'aws_session_token': 'c',
            },
            'dev': {
                'aws_access_key_id': 'd',
                'aws_secret_access_key': 'e',
                'aws_session_token': 'f',
            },
        }
        # And we specify a profile_name of 'dev'.
        provider = credentials.SharedCredentialProvider(
            creds_filename='~/.aws/creds', profile_name='dev',
            ini_parser=self.ini_parser)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'd')
        self.assertEqual(creds.secret_key, 'e')
        self.assertEqual(creds.token, 'f')
        self.assertEqual(creds.method, 'shared-credentials-file')

    def test_credentials_file_does_not_exist_returns_none(self):
        # It's ok if the credentials file does not exist, we should
        # just catch the appropriate errors and return None.
        self.ini_parser.side_effect = botocore.exceptions.ConfigNotFound(
            path='foo')
        provider = credentials.SharedCredentialProvider(
            creds_filename='~/.aws/creds', profile_name='dev',
            ini_parser=self.ini_parser)
        creds = provider.load()
        self.assertIsNone(creds)


class TestConfigFileProvider(BaseEnvVar):

    def setUp(self):
        super(TestConfigFileProvider, self).setUp()
        profile_config = {
            'aws_access_key_id': 'a',
            'aws_secret_access_key': 'b',
            'aws_session_token': 'c',
            # Non creds related configs can be in a session's # config.
            'region': 'us-west-2',
            'output': 'json',
        }
        parsed = {'profiles': {'default': profile_config}}
        parser = mock.Mock()
        parser.return_value = parsed
        self.parser = parser

    def test_config_file_exists(self):
        provider = credentials.ConfigProvider('cli.cfg', 'default',
                                              self.parser)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'a')
        self.assertEqual(creds.secret_key, 'b')
        self.assertEqual(creds.token, 'c')
        self.assertEqual(creds.method, 'config-file')

    def test_config_file_missing_profile_config(self):
        # Referring to a profile that's not in the config file
        # will result in session.config returning an empty dict.
        profile_name = 'NOT-default'
        provider = credentials.ConfigProvider('cli.cfg', profile_name,
                                              self.parser)
        creds = provider.load()
        self.assertIsNone(creds)

    def test_config_file_errors_ignored(self):
        # We should move on to the next provider if the config file
        # can't be found.
        self.parser.side_effect = botocore.exceptions.ConfigNotFound(
            path='cli.cfg')
        provider = credentials.ConfigProvider('cli.cfg', 'default',
                                              self.parser)
        creds = provider.load()
        self.assertIsNone(creds)

    def test_partial_creds_is_error(self):
        profile_config = {
            'aws_access_key_id': 'a',
            # Missing aws_secret_access_key
        }
        parsed = {'profiles': {'default': profile_config}}
        parser = mock.Mock()
        parser.return_value = parsed
        provider = credentials.ConfigProvider('cli.cfg', 'default', parser)
        with self.assertRaises(botocore.exceptions.PartialCredentialsError):
            provider.load()


class TestBotoProvider(BaseEnvVar):
    def setUp(self):
        super(TestBotoProvider, self).setUp()
        self.ini_parser = mock.Mock()

    def test_boto_config_file_exists_in_home_dir(self):
        environ = {}
        self.ini_parser.return_value = {
            'Credentials': {
                # boto's config file does not support a session token
                # so we only test for access_key/secret_key.
                'aws_access_key_id': 'a',
                'aws_secret_access_key': 'b',
            }
        }
        provider = credentials.BotoProvider(environ=environ,
                                            ini_parser=self.ini_parser)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'a')
        self.assertEqual(creds.secret_key, 'b')
        self.assertIsNone(creds.token)
        self.assertEqual(creds.method, 'boto-config')

    def test_env_var_set_for_boto_location(self):
        environ = {
            'BOTO_CONFIG': 'alternate-config.cfg'
        }
        self.ini_parser.return_value = {
            'Credentials': {
                # boto's config file does not support a session token
                # so we only test for access_key/secret_key.
                'aws_access_key_id': 'a',
                'aws_secret_access_key': 'b',
            }
        }
        provider = credentials.BotoProvider(environ=environ,
                                            ini_parser=self.ini_parser)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'a')
        self.assertEqual(creds.secret_key, 'b')
        self.assertIsNone(creds.token)
        self.assertEqual(creds.method, 'boto-config')

        # Assert that the parser was called with the filename specified
        # in the env var.
        self.ini_parser.assert_called_with('alternate-config.cfg')

    def test_no_boto_config_file_exists(self):
        self.ini_parser.side_effect = botocore.exceptions.ConfigNotFound(
            path='foo')
        provider = credentials.BotoProvider(environ={},
                                            ini_parser=self.ini_parser)
        creds = provider.load()
        self.assertIsNone(creds)

    def test_partial_creds_is_error(self):
        ini_parser = mock.Mock()
        ini_parser.return_value = {
            'Credentials': {
                'aws_access_key_id': 'a',
                # Missing aws_secret_access_key.
            }
        }
        provider = credentials.BotoProvider(environ={},
                                            ini_parser=ini_parser)
        with self.assertRaises(botocore.exceptions.PartialCredentialsError):
            provider.load()


class TestOriginalEC2Provider(BaseEnvVar):

    def test_load_ec2_credentials_file_not_exist(self):
        provider = credentials.OriginalEC2Provider(environ={})
        creds = provider.load()
        self.assertIsNone(creds)

    def test_load_ec2_credentials_file_exists(self):
        environ = {
            'AWS_CREDENTIAL_FILE': 'foo.cfg',
        }
        parser = mock.Mock()
        parser.return_value = {
            'AWSAccessKeyId': 'a',
            'AWSSecretKey': 'b',
        }
        provider = credentials.OriginalEC2Provider(environ=environ,
                                                   parser=parser)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'a')
        self.assertEqual(creds.secret_key, 'b')
        self.assertIsNone(creds.token)
        self.assertEqual(creds.method, 'ec2-credentials-file')


class TestInstanceMetadataProvider(BaseEnvVar):
    def test_load_from_instance_metadata(self):
        fetcher = mock.Mock()
        fetcher.retrieve_iam_role_credentials.return_value = {
            'access_key': 'a',
            'secret_key': 'b',
            'token': 'c',
            'expiry_time': '2014-04-23T15:24:46Z',
            'role_name': 'myrole',
        }
        provider = credentials.InstanceMetadataProvider(
            iam_role_fetcher=fetcher)
        creds = provider.load()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'a')
        self.assertEqual(creds.secret_key, 'b')
        self.assertEqual(creds.token, 'c')
        self.assertEqual(creds.method, 'iam-role')

    def test_no_role_creds_exist(self):
        fetcher = mock.Mock()
        fetcher.retrieve_iam_role_credentials.return_value = {}
        provider = credentials.InstanceMetadataProvider(
            iam_role_fetcher=fetcher)
        creds = provider.load()
        self.assertIsNone(creds)
        fetcher.retrieve_iam_role_credentials.assert_called_with()


class CredentialResolverTest(BaseEnvVar):
    def setUp(self):
        super(CredentialResolverTest, self).setUp()
        self.provider1 = mock.Mock()
        self.provider1.METHOD = 'provider1'
        self.provider2 = mock.Mock()
        self.provider2.METHOD = 'provider2'
        self.fake_creds = credentials.Credentials('a', 'b', 'c')

    def test_load_credentials_single_provider(self):
        self.provider1.load.return_value = self.fake_creds
        resolver = credentials.CredentialResolver(providers=[self.provider1])
        creds = resolver.load_credentials()
        self.assertEqual(creds.access_key, 'a')
        self.assertEqual(creds.secret_key, 'b')
        self.assertEqual(creds.token, 'c')

    def test_first_credential_non_none_wins(self):
        self.provider1.load.return_value = None
        self.provider2.load.return_value = self.fake_creds
        resolver = credentials.CredentialResolver(providers=[self.provider1,
                                                             self.provider2])
        creds = resolver.load_credentials()
        self.assertEqual(creds.access_key, 'a')
        self.assertEqual(creds.secret_key, 'b')
        self.assertEqual(creds.token, 'c')
        self.provider1.load.assert_called_with()
        self.provider2.load.assert_called_with()

    def test_no_creds_loaded(self):
        self.provider1.load.return_value = None
        self.provider2.load.return_value = None
        resolver = credentials.CredentialResolver(providers=[self.provider1,
                                                             self.provider2])
        creds = resolver.load_credentials()
        self.assertIsNone(creds)

    def test_inject_additional_providers_after_existing(self):
        self.provider1.load.return_value = None
        self.provider2.load.return_value = self.fake_creds
        resolver = credentials.CredentialResolver(providers=[self.provider1,
                                                             self.provider2])
        # Now, if we were to call resolver.load() now, provider2 would
        # win because it's returning a non None response.
        # However we can inject a new provider before provider2 to
        # override this process.
        # Providers can be added by the METHOD name of each provider.
        new_provider = mock.Mock()
        new_provider.METHOD = 'new_provider'
        new_provider.load.return_value = credentials.Credentials('d', 'e', 'f')

        resolver.insert_after('provider1', new_provider)

        creds = resolver.load_credentials()
        self.assertIsNotNone(creds)

        self.assertEqual(creds.access_key, 'd')
        self.assertEqual(creds.secret_key, 'e')
        self.assertEqual(creds.token, 'f')
        # Provider 1 should have been called, but provider2 should
        # *not* have been called because new_provider already returned
        # a non-None response.
        self.provider1.load.assert_called_with()
        self.assertTrue(not self.provider2.called)

    def test_inject_provider_before_existing(self):
        new_provider = mock.Mock()
        new_provider.METHOD = 'override'
        new_provider.load.return_value = credentials.Credentials('x', 'y', 'z')

        resolver = credentials.CredentialResolver(providers=[self.provider1,
                                                             self.provider2])
        resolver.insert_before(self.provider1.METHOD, new_provider)
        creds = resolver.load_credentials()
        self.assertEqual(creds.access_key, 'x')
        self.assertEqual(creds.secret_key, 'y')
        self.assertEqual(creds.token, 'z')

    def test_can_remove_providers(self):
        self.provider1.load.return_value = credentials.Credentials(
            'a', 'b', 'c')
        self.provider2.load.return_value = credentials.Credentials(
            'd', 'e', 'f')
        resolver = credentials.CredentialResolver(providers=[self.provider1,
                                                             self.provider2])
        resolver.remove('provider1')
        creds = resolver.load_credentials()
        self.assertIsNotNone(creds)
        self.assertEqual(creds.access_key, 'd')
        self.assertEqual(creds.secret_key, 'e')
        self.assertEqual(creds.token, 'f')
        self.assertTrue(not self.provider1.load.called)
        self.provider2.load.assert_called_with()

    def test_provider_unknown(self):
        resolver = credentials.CredentialResolver(providers=[self.provider1,
                                                             self.provider2])
        # No error is raised if you try to remove an unknown provider.
        resolver.remove('providerFOO')
        # But an error IS raised if you try to insert after an unknown
        # provider.
        with self.assertRaises(botocore.exceptions.UnknownCredentialError):
            resolver.insert_after('providerFoo', None)


class TestCreateCredentialResolver(BaseEnvVar):
    def setUp(self):
        super(TestCreateCredentialResolver, self).setUp()

        self.session = mock.Mock()
        self.config = {
            'credentials_file': 'a',
            'legacy_config_file': 'b',
            'config_file': 'c',
            'metadata_service_timeout': 'd',
            'metadata_service_num_attempts': 'e',
            'profile': 'profilename',
        }
        self.session.get_config_variable = lambda x: self.config[x]

    def test_create_credential_resolver(self):
        resolver = credentials.create_credential_resolver(self.session)
        self.assertIsInstance(resolver, credentials.CredentialResolver)

    def test_explicit_profile_ignores_env_provider(self):
        self.config['profile'] = 'dev'
        resolver = credentials.create_credential_resolver(self.session)

        self.assertTrue(
            all(not isinstance(p, EnvProvider) for p in resolver.providers))

    def test_no_profile_checks_env_provider(self):
        self.config['profile'] = None
        self.session._profile = None
        resolver = credentials.create_credential_resolver(self.session)

        self.assertTrue(
            any(isinstance(p, EnvProvider) for p in resolver.providers))

    def test_no_profile_env_provider_is_first(self):
        self.config['profile'] = None
        self.session._profile = None
        resolver = credentials.create_credential_resolver(self.session)

        self.assertIsInstance(resolver.providers[0], credentials.EnvProvider)


if __name__ == "__main__":
    unittest.main()
