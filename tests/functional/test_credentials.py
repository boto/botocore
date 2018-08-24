# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import threading
import os
import math
import time
import mock
import tempfile
import shutil
from datetime import datetime, timedelta
import sys

from dateutil.tz import tzlocal
from botocore.exceptions import CredentialRetrievalError

from tests import unittest, IntegerRefresher, BaseEnvVar, random_chars
from tests import temporary_file
from botocore.credentials import EnvProvider, ContainerProvider
from botocore.credentials import InstanceMetadataProvider
from botocore.credentials import Credentials, ReadOnlyCredentials
from botocore.credentials import AssumeRoleProvider
from botocore.credentials import CanonicalNameCredentialSourcer
from botocore.credentials import DeferredRefreshableCredentials
from botocore.session import Session
from botocore.exceptions import InvalidConfigError, InfiniteLoopConfigError
from botocore.stub import Stubber


class TestCredentialRefreshRaces(unittest.TestCase):
    def assert_consistent_credentials_seen(self, creds, func):
        collected = []
        self._run_threads(20, func, collected)
        for creds in collected:
            # During testing, the refresher uses it's current
            # refresh count as the values for the access, secret, and
            # token value.  This means that at any given point in time,
            # the credentials should be something like:
            #
            # ReadOnlyCredentials('1', '1', '1')
            # ReadOnlyCredentials('2', '2', '2')
            # ...
            # ReadOnlyCredentials('30', '30', '30')
            #
            # This makes it really easy to verify we see a consistent
            # set of credentials from the same time period.  We just
            # check if all the credential values are the same.  If
            # we ever see something like:
            #
            # ReadOnlyCredentials('1', '2', '1')
            #
            # We fail.  This is because we're using the access_key
            # from the first refresh ('1'), the secret key from
            # the second refresh ('2'), and the token from the
            # first refresh ('1').
            self.assertTrue(creds[0] == creds[1] == creds[2], creds)

    def assert_non_none_retrieved_credentials(self, func):
        collected = []
        self._run_threads(50, func, collected)
        for cred in collected:
            self.assertIsNotNone(cred)

    def _run_threads(self, num_threads, func, collected):
        threads = []
        for _ in range(num_threads):
            threads.append(threading.Thread(target=func, args=(collected,)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def test_has_no_race_conditions(self):
        creds = IntegerRefresher(
            creds_last_for=2,
            advisory_refresh=1,
            mandatory_refresh=0
        )
        def _run_in_thread(collected):
            for _ in range(4000):
                frozen = creds.get_frozen_credentials()
                collected.append((frozen.access_key,
                                  frozen.secret_key,
                                  frozen.token))
        start = time.time()
        self.assert_consistent_credentials_seen(creds, _run_in_thread)
        end = time.time()
        # creds_last_for = 2 seconds (from above)
        # So, for example, if execution time took 6.1 seconds, then
        # we should see a maximum number of refreshes being (6 / 2.0) + 1 = 4
        max_calls_allowed = math.ceil((end - start) / 2.0) + 1
        self.assertTrue(creds.refresh_counter <= max_calls_allowed,
                        "Too many cred refreshes, max: %s, actual: %s, "
                        "time_delta: %.4f" % (max_calls_allowed,
                                              creds.refresh_counter,
                                              (end - start)))

    def test_no_race_for_immediate_advisory_expiration(self):
        creds = IntegerRefresher(
            creds_last_for=1,
            advisory_refresh=1,
            mandatory_refresh=0
        )
        def _run_in_thread(collected):
            for _ in range(100):
                frozen = creds.get_frozen_credentials()
                collected.append((frozen.access_key,
                                  frozen.secret_key,
                                  frozen.token))
        self.assert_consistent_credentials_seen(creds, _run_in_thread)

    def test_no_race_for_initial_refresh_of_deferred_refreshable(self):
        def get_credentials():
            expiry_time = (
                datetime.now(tzlocal()) + timedelta(hours=24)).isoformat()
            return {
                'access_key': 'my-access-key',
                'secret_key': 'my-secret-key',
                'token': 'my-token',
                'expiry_time': expiry_time
            }

        deferred_creds = DeferredRefreshableCredentials(
            get_credentials, 'fixed')

        def _run_in_thread(collected):
            frozen = deferred_creds.get_frozen_credentials()
            collected.append(frozen)

        self.assert_non_none_retrieved_credentials(_run_in_thread)


class TestAssumeRole(BaseEnvVar):
    def setUp(self):
        super(TestAssumeRole, self).setUp()
        self.tempdir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.tempdir, 'config')
        self.environ['AWS_CONFIG_FILE'] = self.config_file
        self.environ['AWS_ACCESS_KEY_ID'] = 'access_key'
        self.environ['AWS_SECRET_ACCESS_KEY'] = 'secret_key'

        self.metadata_provider = self.mock_provider(InstanceMetadataProvider)
        self.env_provider = self.mock_provider(EnvProvider)
        self.container_provider = self.mock_provider(ContainerProvider)

    def mock_provider(self, provider_cls):
        mock_instance = mock.Mock(spec=provider_cls)
        mock_instance.load.return_value = None
        mock_instance.METHOD = provider_cls.METHOD
        mock_instance.CANONICAL_NAME = provider_cls.CANONICAL_NAME
        return mock_instance

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def create_session(self, profile=None):
        session = Session(profile=profile)

        # We have to set bogus credentials here or otherwise we'll trigger
        # an early credential chain resolution.
        sts = session.create_client(
            'sts',
            aws_access_key_id='spam',
            aws_secret_access_key='eggs',
        )
        stubber = Stubber(sts)
        stubber.activate()
        assume_role_provider = AssumeRoleProvider(
            load_config=lambda: session.full_config,
            client_creator=lambda *args, **kwargs: sts,
            cache={},
            profile_name=profile,
            credential_sourcer=CanonicalNameCredentialSourcer([
                self.env_provider, self.container_provider,
                self.metadata_provider
            ])
        )

        component_name = 'credential_provider'
        resolver = session.get_component(component_name)
        available_methods = [p.METHOD for p in resolver.providers]
        replacements = {
            'env': self.env_provider,
            'iam-role': self.metadata_provider,
            'container-role': self.container_provider,
            'assume-role': assume_role_provider
        }
        for name, provider in replacements.items():
            try:
                index = available_methods.index(name)
            except ValueError:
                # The provider isn't in the session
                continue

            resolver.providers[index] = provider

        session.register_component(
            'credential_provider', resolver
        )
        return session, stubber

    def create_assume_role_response(self, credentials, expiration=None):
        if expiration is None:
            expiration = self.some_future_time()

        response = {
            'Credentials': {
                'AccessKeyId': credentials.access_key,
                'SecretAccessKey': credentials.secret_key,
                'SessionToken': credentials.token,
                'Expiration': expiration
            },
            'AssumedRoleUser': {
                'AssumedRoleId': 'myroleid',
                'Arn': 'arn:aws:iam::1234567890:user/myuser'
            }
        }

        return response

    def create_random_credentials(self):
        return Credentials(
            'fake-%s' % random_chars(15),
            'fake-%s' % random_chars(35),
            'fake-%s' % random_chars(45)
        )

    def some_future_time(self):
        timeobj = datetime.now(tzlocal())
        return timeobj + timedelta(hours=24)

    def write_config(self, config):
        with open(self.config_file, 'w') as f:
            f.write(config)

    def assert_creds_equal(self, c1, c2):
        c1_frozen = c1
        if not isinstance(c1_frozen, ReadOnlyCredentials):
            c1_frozen = c1.get_frozen_credentials()
        c2_frozen = c2
        if not isinstance(c2_frozen, ReadOnlyCredentials):
            c2_frozen = c2.get_frozen_credentials()
        self.assertEqual(c1_frozen, c2_frozen)

    def test_assume_role(self):
        config = (
            '[profile A]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleA\n'
            'source_profile = B\n\n'
            '[profile B]\n'
            'aws_access_key_id = abc123\n'
            'aws_secret_access_key = def456\n'
        )
        self.write_config(config)

        expected_creds = self.create_random_credentials()
        response = self.create_assume_role_response(expected_creds)
        session, stubber = self.create_session(profile='A')
        stubber.add_response('assume_role', response)

        actual_creds = session.get_credentials()
        self.assert_creds_equal(actual_creds, expected_creds)
        stubber.assert_no_pending_responses()

    def test_environment_credential_source(self):
        config = (
            '[profile A]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleA\n'
            'credential_source = Environment\n'
        )
        self.write_config(config)

        environment_creds = self.create_random_credentials()
        self.env_provider.load.return_value = environment_creds

        expected_creds = self.create_random_credentials()
        response = self.create_assume_role_response(expected_creds)
        session, stubber = self.create_session(profile='A')
        stubber.add_response('assume_role', response)

        actual_creds = session.get_credentials()
        self.assert_creds_equal(actual_creds, expected_creds)

        stubber.assert_no_pending_responses()
        self.assertEqual(self.env_provider.load.call_count, 1)

    def test_instance_metadata_credential_source(self):
        config = (
            '[profile A]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleA\n'
            'credential_source = Ec2InstanceMetadata\n'
        )
        self.write_config(config)

        metadata_creds = self.create_random_credentials()
        self.metadata_provider.load.return_value = metadata_creds

        expected_creds = self.create_random_credentials()
        response = self.create_assume_role_response(expected_creds)
        session, stubber = self.create_session(profile='A')
        stubber.add_response('assume_role', response)

        actual_creds = session.get_credentials()
        self.assert_creds_equal(actual_creds, expected_creds)

        stubber.assert_no_pending_responses()
        self.assertEqual(self.metadata_provider.load.call_count, 1)

    def test_container_credential_source(self):
        config = (
            '[profile A]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleA\n'
            'credential_source = EcsContainer\n'
        )
        self.write_config(config)

        container_creds = self.create_random_credentials()
        self.container_provider.load.return_value = container_creds

        expected_creds = self.create_random_credentials()
        response = self.create_assume_role_response(expected_creds)
        session, stubber = self.create_session(profile='A')
        stubber.add_response('assume_role', response)

        actual_creds = session.get_credentials()
        self.assert_creds_equal(actual_creds, expected_creds)

        stubber.assert_no_pending_responses()
        self.assertEqual(self.container_provider.load.call_count, 1)

    def test_invalid_credential_source(self):
        config = (
            '[profile A]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleA\n'
            'credential_source = CustomInvalidProvider\n'
        )
        self.write_config(config)

        with self.assertRaises(InvalidConfigError):
            session, _ = self.create_session(profile='A')
            session.get_credentials()

    def test_misconfigured_source_profile(self):
        config = (
            '[profile A]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleA\n'
            'source_profile = B\n'
            '[profile B]\n'
            'credential_process = command\n'
        )
        self.write_config(config)

        with self.assertRaises(InvalidConfigError):
            session, _ = self.create_session(profile='A')
            session.get_credentials()

    def test_recursive_assume_role(self):
        config = (
            '[profile A]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleA\n'
            'source_profile = B\n\n'
            '[profile B]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleB\n'
            'source_profile = C\n\n'
            '[profile C]\n'
            'aws_access_key_id = abc123\n'
            'aws_secret_access_key = def456\n'
        )
        self.write_config(config)

        profile_b_creds = self.create_random_credentials()
        profile_b_response = self.create_assume_role_response(profile_b_creds)
        profile_a_creds = self.create_random_credentials()
        profile_a_response = self.create_assume_role_response(profile_a_creds)

        session, stubber = self.create_session(profile='A')
        stubber.add_response('assume_role', profile_b_response)
        stubber.add_response('assume_role', profile_a_response)

        actual_creds = session.get_credentials()
        self.assert_creds_equal(actual_creds, profile_a_creds)
        stubber.assert_no_pending_responses()

    def test_recursive_assume_role_stops_at_static_creds(self):
        config = (
            '[profile A]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleA\n'
            'source_profile = B\n\n'
            '[profile B]\n'
            'aws_access_key_id = abc123\n'
            'aws_secret_access_key = def456\n'
            'role_arn = arn:aws:iam::123456789:role/RoleB\n'
            'source_profile = C\n\n'
            '[profile C]\n'
            'aws_access_key_id = abc123\n'
            'aws_secret_access_key = def456\n'
        )
        self.write_config(config)

        profile_a_creds = self.create_random_credentials()
        profile_a_response = self.create_assume_role_response(profile_a_creds)
        session, stubber = self.create_session(profile='A')
        stubber.add_response('assume_role', profile_a_response)

        actual_creds = session.get_credentials()
        self.assert_creds_equal(actual_creds, profile_a_creds)
        stubber.assert_no_pending_responses()

    def test_infinitely_recursive_assume_role(self):
        config = (
            '[profile A]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleA\n'
            'source_profile = A\n'
        )
        self.write_config(config)

        with self.assertRaises(InfiniteLoopConfigError):
            session, _ = self.create_session(profile='A')
            session.get_credentials()

    def test_self_referential_profile(self):
        config = (
            '[profile A]\n'
            'role_arn = arn:aws:iam::123456789:role/RoleA\n'
            'source_profile = A\n'
            'aws_access_key_id = abc123\n'
            'aws_secret_access_key = def456\n'
        )
        self.write_config(config)

        expected_creds = self.create_random_credentials()
        response = self.create_assume_role_response(expected_creds)
        session, stubber = self.create_session(profile='A')
        stubber.add_response('assume_role', response)

        actual_creds = session.get_credentials()
        self.assert_creds_equal(actual_creds, expected_creds)
        stubber.assert_no_pending_responses()


class TestProcessProvider(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        credential_process = os.path.join(
            current_dir, 'utils', 'credentialprocess.py'
        )
        self.credential_process = '%s %s' % (
            sys.executable, credential_process
        )
        self.environ = os.environ.copy()
        self.environ_patch = mock.patch('os.environ', self.environ)
        self.environ_patch.start()

    def tearDown(self):
        self.environ_patch.stop()

    def test_credential_process(self):
        config = (
            '[profile processcreds]\n'
            'credential_process = %s\n'
        )
        config = config % self.credential_process
        with temporary_file('w') as f:
            f.write(config)
            f.flush()
            self.environ['AWS_CONFIG_FILE'] = f.name

            credentials = Session(profile='processcreds').get_credentials()
            self.assertEqual(credentials.access_key, 'spam')
            self.assertEqual(credentials.secret_key, 'eggs')

    def test_credential_process_returns_error(self):
        config = (
            '[profile processcreds]\n'
            'credential_process = %s --raise-error\n'
        )
        config = config % self.credential_process
        with temporary_file('w') as f:
            f.write(config)
            f.flush()
            self.environ['AWS_CONFIG_FILE'] = f.name

            session = Session(profile='processcreds')

            # This regex validates that there is no substring: b'
            # The reason why we want to validate that is that we want to
            # make sure that stderr is actually decoded so that in
            # exceptional cases the error is properly formatted.
            # As for how the regex works:
            # `(?!b').` is a negative lookahead, meaning that it will only
            # match if it is not followed by the pattern `b'`. Since it is
            # followed by a `.` it will match any character not followed by
            # that pattern. `((?!hede).)*` does that zero or more times. The
            # final pattern adds `^` and `$` to anchor the beginning and end
            # of the string so we can know the whole string is consumed.
            # Finally `(?s)` at the beginning makes dots match newlines so
            # we can handle a multi-line string.
            reg = r"(?s)^((?!b').)*$"
            with self.assertRaisesRegexp(CredentialRetrievalError, reg):
                session.get_credentials()
