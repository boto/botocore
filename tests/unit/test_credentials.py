# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from datetime import datetime, timedelta
import mock
import os

from dateutil.tz import tzlocal, tzutc

from botocore import credentials
from botocore.credentials import EnvProvider, create_assume_role_refresher
import botocore.exceptions
import botocore.session
from tests import unittest, BaseEnvVar, IntegerRefresher


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


class TestCredentials(BaseEnvVar):
    def _ensure_credential_is_normalized_as_unicode(self, access, secret):
        c = credentials.Credentials(access, secret)
        self.assertTrue(isinstance(c.access_key, type(u'u')))
        self.assertTrue(isinstance(c.secret_key, type(u'u')))

    def test_detect_nonascii_character(self):
        self._ensure_credential_is_normalized_as_unicode(
            'foo\xe2\x80\x99', 'bar\xe2\x80\x99')

    def test_unicode_input(self):
        self._ensure_credential_is_normalized_as_unicode(
            u'foo', u'bar')


class TestRefreshableCredentials(TestCredentials):
    def setUp(self):
        super(TestRefreshableCredentials, self).setUp()
        self.refresher = mock.Mock()
        self.future_time = datetime.now(tzlocal()) + timedelta(hours=24)
        self.expiry_time = \
            datetime.now(tzlocal()) - timedelta(minutes=30)
        self.metadata = {
            'access_key': 'NEW-ACCESS',
            'secret_key': 'NEW-SECRET',
            'token': 'NEW-TOKEN',
            'expiry_time': self.future_time.isoformat(),
            'role_name': 'rolename',
        }
        self.refresher.return_value = self.metadata
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
        self.mock_time.return_value = datetime.now(tzlocal())
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
            datetime.now(tzlocal()) - timedelta(minutes=60))
        self.assertTrue(not self.creds.refresh_needed())

        self.assertEqual(self.creds.access_key, 'ORIGINAL-ACCESS')
        self.assertEqual(self.creds.secret_key, 'ORIGINAL-SECRET')
        self.assertEqual(self.creds.token, 'ORIGINAL-TOKEN')

    def test_get_credentials_set(self):
        # We need to return a consistent set of credentials to use during the
        # signing process.
        self.mock_time.return_value = (
            datetime.now(tzlocal()) - timedelta(minutes=60))
        self.assertTrue(not self.creds.refresh_needed())
        credential_set = self.creds.get_frozen_credentials()
        self.assertEqual(credential_set.access_key, 'ORIGINAL-ACCESS')
        self.assertEqual(credential_set.secret_key, 'ORIGINAL-SECRET')
        self.assertEqual(credential_set.token, 'ORIGINAL-TOKEN')


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
        timeobj = datetime.now(tzlocal())
        timestamp = (timeobj + timedelta(hours=24)).isoformat()
        fetcher = mock.Mock()
        fetcher.retrieve_iam_role_credentials.return_value = {
            'access_key': 'a',
            'secret_key': 'b',
            'token': 'c',
            'expiry_time': timestamp,
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

    def test_get_provider_by_name(self):
        resolver = credentials.CredentialResolver(providers=[self.provider1])
        result = resolver.get_provider('provider1')
        self.assertIs(result, self.provider1)

    def test_get_unknown_provider_raises_error(self):
        resolver = credentials.CredentialResolver(providers=[self.provider1])
        with self.assertRaises(botocore.exceptions.UnknownCredentialError):
            resolver.get_provider('unknown-foo')

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
        self.session_instance_vars = {
            'credentials_file': 'a',
            'legacy_config_file': 'b',
            'config_file': 'c',
            'metadata_service_timeout': 'd',
            'metadata_service_num_attempts': 'e',
        }
        self.fake_env_vars = {}
        self.session.get_config_variable = self.fake_get_config_variable

    def fake_get_config_variable(self, name, methods=None):
        if methods == ('instance',):
            return self.session_instance_vars.get(name)
        elif methods is not None and 'env' in methods:
            return self.fake_env_vars.get(name)

    def test_create_credential_resolver(self):
        resolver = credentials.create_credential_resolver(self.session)
        self.assertIsInstance(resolver, credentials.CredentialResolver)

    def test_explicit_profile_ignores_env_provider(self):
        self.session_instance_vars['profile'] = 'dev'
        resolver = credentials.create_credential_resolver(self.session)

        self.assertTrue(
            all(not isinstance(p, EnvProvider) for p in resolver.providers))

    def test_no_profile_checks_env_provider(self):
        # If no profile is provided,
        self.session_instance_vars.pop('profile', None)
        resolver = credentials.create_credential_resolver(self.session)
        # Then an EnvProvider should be part of our credential lookup chain.
        self.assertTrue(
            any(isinstance(p, EnvProvider) for p in resolver.providers))

    def test_env_provider_added_if_profile_from_env_set(self):
        self.fake_env_vars['profile'] = 'profile-from-env'
        resolver = credentials.create_credential_resolver(self.session)
        self.assertTrue(
            any(isinstance(p, EnvProvider) for p in resolver.providers))


class TestAssumeRoleCredentialProvider(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.fake_config = {
            'profiles': {
                'development': {
                    'role_arn': 'myrole',
                    'source_profile': 'longterm',
                },
                'longterm': {
                    'aws_access_key_id': 'akid',
                    'aws_secret_access_key': 'skid',
                }
            }
        }

    def create_config_loader(self, with_config=None):
        if with_config is None:
            with_config = self.fake_config
        load_config = mock.Mock()
        load_config.return_value = with_config
        return load_config

    def create_client_creator(self, with_response):
        # Create a mock sts client that returns a specific response
        # for assume_role.
        client = mock.Mock()
        if isinstance(with_response, list):
            client.assume_role.side_effect = with_response
        else:
            client.assume_role.return_value = with_response
        return mock.Mock(return_value=client)

    def some_future_time(self):
        timeobj = datetime.now(tzlocal())
        return timeobj + timedelta(hours=24)

    def test_assume_role_with_no_cache(self):
        response = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                'Expiration': self.some_future_time().isoformat()
            },
        }
        client_creator = self.create_client_creator(with_response=response)
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(),
            client_creator, cache={}, profile_name='development')

        creds = provider.load()

        self.assertEqual(creds.access_key, 'foo')
        self.assertEqual(creds.secret_key, 'bar')
        self.assertEqual(creds.token, 'baz')

    def test_assume_role_with_datetime(self):
        response = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                # Note the lack of isoformat(), we're using
                # a datetime.datetime type.  This will ensure
                # we test both parsing as well as serializing
                # from a given datetime because the credentials
                # are immediately expired.
                'Expiration': datetime.now(tzlocal()) + timedelta(hours=20)
            },
        }
        client_creator = self.create_client_creator(with_response=response)
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(),
            client_creator, cache={}, profile_name='development')

        creds = provider.load()

        self.assertEqual(creds.access_key, 'foo')
        self.assertEqual(creds.secret_key, 'bar')
        self.assertEqual(creds.token, 'baz')

    def test_assume_role_refresher_serializes_datetime(self):
        client = mock.Mock()
        time_zone = tzutc()
        expiration = datetime(
            year=2016, month=11, day=6, hour=1, minute=30, tzinfo=time_zone)
        client.assume_role.return_value = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                'Expiration': expiration,
            }
        }
        refresh = create_assume_role_refresher(client, {})
        expiry_time = refresh()['expiry_time']
        self.assertEqual(expiry_time, '2016-11-06T01:30:00UTC')

    def test_assume_role_retrieves_from_cache(self):
        date_in_future = datetime.utcnow() + timedelta(seconds=1000)
        utc_timestamp = date_in_future.isoformat() + 'Z'
        self.fake_config['profiles']['development']['role_arn'] = 'myrole'
        cache = {
            'development--myrole': {
                'Credentials': {
                    'AccessKeyId': 'foo-cached',
                    'SecretAccessKey': 'bar-cached',
                    'SessionToken': 'baz-cached',
                    'Expiration': utc_timestamp,
                }
            }
        }
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(), mock.Mock(),
            cache=cache, profile_name='development')

        creds = provider.load()

        self.assertEqual(creds.access_key, 'foo-cached')
        self.assertEqual(creds.secret_key, 'bar-cached')
        self.assertEqual(creds.token, 'baz-cached')

    def test_cache_key_is_windows_safe(self):
        response = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                'Expiration': datetime.now(tzlocal()).isoformat()
            },
        }
        cache = {}
        self.fake_config['profiles']['development']['role_arn'] = (
            'arn:aws:iam::foo-role')

        client_creator = self.create_client_creator(with_response=response)
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(),
            client_creator, cache=cache, profile_name='development')

        provider.load()
        # On windows, you cannot use a a ':' in the filename, so
        # we need to do some small transformations on the filename
        # to replace any ':' that come up.
        self.assertEqual(cache['development--arn_aws_iam__foo-role'],
                         response)

    def test_cache_key_with_role_session_name(self):
        response = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                'Expiration': datetime.now(tzlocal()).isoformat()
            },
        }
        cache = {}
        self.fake_config['profiles']['development']['role_arn'] = (
            'arn:aws:iam::foo-role')
        self.fake_config['profiles']['development']['role_session_name'] = (
            'foo_role_session_name')

        client_creator = self.create_client_creator(with_response=response)
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(),
            client_creator, cache=cache, profile_name='development')

        provider.load()
        self.assertEqual(
            cache['development--arn_aws_iam__foo-role--foo_role_session_name'],
            response)

    def test_assume_role_in_cache_but_expired(self):
        expired_creds = datetime.utcnow()
        valid_creds = expired_creds + timedelta(seconds=60)
        utc_timestamp = expired_creds.isoformat() + 'Z'
        response = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                'Expiration': valid_creds.isoformat() + 'Z',
            },
        }
        client_creator = self.create_client_creator(with_response=response)
        cache = {
            'development--myrole': {
                'Credentials': {
                    'AccessKeyId': 'foo-cached',
                    'SecretAccessKey': 'bar-cached',
                    'SessionToken': 'baz-cached',
                    'Expiration': utc_timestamp,
                }
            }
        }
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(), client_creator,
            cache=cache, profile_name='development')

        creds = provider.load()

        self.assertEqual(creds.access_key, 'foo')
        self.assertEqual(creds.secret_key, 'bar')
        self.assertEqual(creds.token, 'baz')

    def test_role_session_name_provided(self):
        dev_profile = self.fake_config['profiles']['development']
        dev_profile['role_session_name'] = 'myname'
        response = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                'Expiration': datetime.now(tzlocal()).isoformat(),
            },
        }
        client_creator = self.create_client_creator(with_response=response)
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(),
            client_creator, cache={}, profile_name='development')

        provider.load()

        client = client_creator.return_value
        client.assume_role.assert_called_with(
            RoleArn='myrole', RoleSessionName='myname')

    def test_external_id_provided(self):
        self.fake_config['profiles']['development']['external_id'] = 'myid'
        response = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                'Expiration': datetime.now(tzlocal()).isoformat(),
            },
        }
        client_creator = self.create_client_creator(with_response=response)
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(),
            client_creator, cache={}, profile_name='development')

        provider.load()

        client = client_creator.return_value
        client.assume_role.assert_called_with(
            RoleArn='myrole', ExternalId='myid', RoleSessionName=mock.ANY)

    def test_assume_role_with_mfa(self):
        self.fake_config['profiles']['development']['mfa_serial'] = 'mfa'
        response = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                'Expiration': datetime.now(tzlocal()).isoformat(),
            },
        }
        client_creator = self.create_client_creator(with_response=response)
        prompter = mock.Mock(return_value='token-code')
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(), client_creator,
            cache={}, profile_name='development', prompter=prompter)

        provider.load()

        client = client_creator.return_value
        # In addition to the normal assume role args, we should also
        # inject the serial number from the config as well as the
        # token code that comes from prompting the user (the prompter
        # object).
        client.assume_role.assert_called_with(
            RoleArn='myrole', RoleSessionName=mock.ANY, SerialNumber='mfa',
            TokenCode='token-code')

    def test_assume_role_populates_session_name_on_refresh(self):
        responses = [{
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                # We're creating an expiry time in the past so as
                # soon as we try to access the credentials, the
                # refresh behavior will be triggered.
                'Expiration': (
                    datetime.now(tzlocal()) -
                    timedelta(seconds=100)).isoformat(),
            },
        }, {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                'Expiration': (
                    datetime.now(tzlocal()) + timedelta(seconds=100)
                ).isoformat(),
            }
        }]
        client_creator = self.create_client_creator(with_response=responses)
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(), client_creator,
            cache={}, profile_name='development',
            prompter=mock.Mock(return_value='token-code'))

        # This will trigger the first assume_role() call.  It returns
        # credentials that are expired and will trigger a refresh.
        creds = provider.load()
        # This will trigger the second assume_role() call because
        # a refresh is needed.
        creds.get_frozen_credentials()
        client = client_creator.return_value
        assume_role_calls = client.assume_role.call_args_list
        self.assertEqual(len(assume_role_calls), 2, assume_role_calls)
        # The args should be identical.  That is, the second
        # assume_role call should have the exact same args as the
        # initial assume_role call.
        self.assertEqual(assume_role_calls[0], assume_role_calls[1])

    def test_assume_role_mfa_cannot_refresh_credentials(self):
        # Note: we should look into supporting optional behavior
        # in the future that allows for reprompting for credentials.
        # But for now, if we get temp creds with MFA then when those
        # creds expire, we can't refresh the credentials.
        self.fake_config['profiles']['development']['mfa_serial'] = 'mfa'
        response = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
                # We're creating an expiry time in the past so as
                # soon as we try to access the credentials, the
                # refresh behavior will be triggered.
                'Expiration': (
                    datetime.now(tzlocal()) -
                    timedelta(seconds=100)).isoformat(),
            },
        }
        client_creator = self.create_client_creator(with_response=response)
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(), client_creator,
            cache={}, profile_name='development',
            prompter=mock.Mock(return_value='token-code'))

        creds = provider.load()
        with self.assertRaises(credentials.RefreshWithMFAUnsupportedError):
            # access_key is a property that will refresh credentials
            # if they're expired.  Because we set the expiry time to
            # something in the past, this will trigger the refresh
            # behavior, with with MFA will currently raise an exception.
            creds.access_key

    def test_no_config_is_noop(self):
        self.fake_config['profiles']['development'] = {
            'aws_access_key_id': 'foo',
            'aws_secret_access_key': 'bar',
        }
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(),
            mock.Mock(), cache={}, profile_name='development')

        # Because a role_arn was not specified, the AssumeRoleProvider
        # is a noop and will not return credentials (which means we
        # move on to the next provider).
        creds = provider.load()
        self.assertIsNone(creds)

    def test_source_profile_not_provided(self):
        del self.fake_config['profiles']['development']['source_profile']
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(),
            mock.Mock(), cache={}, profile_name='development')

        # source_profile is required, we shoudl get an error.
        with self.assertRaises(botocore.exceptions.PartialCredentialsError):
            provider.load()

    def test_source_profile_does_not_exist(self):
        dev_profile = self.fake_config['profiles']['development']
        dev_profile['source_profile'] = 'does-not-exist'
        provider = credentials.AssumeRoleProvider(
            self.create_config_loader(),
            mock.Mock(), cache={}, profile_name='development')

        # source_profile is required, we shoudl get an error.
        with self.assertRaises(botocore.exceptions.InvalidConfigError):
            provider.load()


class TestRefreshLogic(unittest.TestCase):
    def test_mandatory_refresh_needed(self):
        creds = IntegerRefresher(
            # These values will immediately trigger
            # a manadatory refresh.
            creds_last_for=2,
            mandatory_refresh=3,
            advisory_refresh=3)
        temp = creds.get_frozen_credentials()
        self.assertEqual(
            temp, credentials.ReadOnlyCredentials('1', '1', '1'))

    def test_advisory_refresh_needed(self):
        creds = IntegerRefresher(
            # These values will immediately trigger
            # a manadatory refresh.
            creds_last_for=4,
            mandatory_refresh=2,
            advisory_refresh=5)
        temp = creds.get_frozen_credentials()
        self.assertEqual(
            temp, credentials.ReadOnlyCredentials('1', '1', '1'))

    def test_refresh_fails_is_not_an_error_during_advisory_period(self):
        fail_refresh = mock.Mock(side_effect=Exception("refresh failed"))
        creds = IntegerRefresher(
            creds_last_for=5,
            advisory_refresh=7,
            mandatory_refresh=3,
            refresh_function=fail_refresh
        )
        temp = creds.get_frozen_credentials()
        # We should have called the refresh function.
        self.assertTrue(fail_refresh.called)
        # The fail_refresh function will raise an exception.
        # Because we're in the advisory period we'll not propogate
        # the exception and return the current set of credentials
        # (generation '1').
        self.assertEqual(
            temp, credentials.ReadOnlyCredentials('0', '0', '0'))

    def test_exception_propogated_on_error_during_mandatory_period(self):
        fail_refresh = mock.Mock(side_effect=Exception("refresh failed"))
        creds = IntegerRefresher(
            creds_last_for=5,
            advisory_refresh=10,
            # Note we're in the mandatory period now (5 < 7< 10).
            mandatory_refresh=7,
            refresh_function=fail_refresh
        )
        with self.assertRaisesRegexp(Exception, 'refresh failed'):
            creds.get_frozen_credentials()

    def test_exception_propogated_on_expired_credentials(self):
        fail_refresh = mock.Mock(side_effect=Exception("refresh failed"))
        creds = IntegerRefresher(
            # Setting this to 0 mean the credentials are immediately
            # expired.
            creds_last_for=0,
            advisory_refresh=10,
            mandatory_refresh=7,
            refresh_function=fail_refresh
        )
        with self.assertRaisesRegexp(Exception, 'refresh failed'):
            # Because credentials are actually expired, any
            # failure to refresh should be propagated.
            creds.get_frozen_credentials()

    def test_refresh_giving_expired_credentials_raises_exception(self):
        # This verifies an edge cases where refreshed credentials
        # still give expired credentials:
        # 1. We see credentials are expired.
        # 2. We try to refresh the credentials.
        # 3. The "refreshed" credentials are still expired.
        #
        # In this case, we hard fail and let the user know what
        # happened.
        creds = IntegerRefresher(
            # Negative number indicates that the credentials
            # have already been expired for 2 seconds, even
            # on refresh.
            creds_last_for=-2,
        )
        err_msg = 'refreshed credentials are still expired'
        with self.assertRaisesRegexp(RuntimeError, err_msg):
            # Because credentials are actually expired, any
            # failure to refresh should be propagated.
            creds.get_frozen_credentials()
