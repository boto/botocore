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

import os
import mock

from botocore.session import Session
from tests import BaseEnvVar, temporary_file


class TestCredentialPrecedence(BaseEnvVar):
    def setUp(self):
        super(TestCredentialPrecedence, self).setUp()

        # Set the config file to something that doesn't exist so
        # that we don't accidentally load a config.
        os.environ['AWS_CONFIG_FILE'] = '~/.aws/config-missing'

    def create_session(self, *args, **kwargs):
        """
        Create a new session with the given arguments. Additionally,
        this method will set the credentials file to the test credentials
        used by the following test cases.
        """
        kwargs['session_vars'] = {
            'credentials_file': (
                None, None,
                os.path.join(os.path.dirname(__file__), 'test-credentials'),
                None)
        }

        return Session(*args, **kwargs)

    def test_access_secret_vs_profile_env(self):
        # If all three are given, then the access/secret keys should
        # take precedence.
        os.environ['AWS_ACCESS_KEY_ID'] = 'env'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'env-secret'
        os.environ['AWS_DEFAULT_PROFILE'] = 'test'

        s = self.create_session()
        credentials = s.get_credentials()

        self.assertEqual(credentials.access_key, 'env')
        self.assertEqual(credentials.secret_key, 'env-secret')

    @mock.patch('botocore.credentials.Credentials')
    def test_access_secret_vs_profile_code(self, credentials_cls):
        # If all three are given, then the access/secret keys should
        # take precedence.
        s = self.create_session(profile='test')

        client = s.create_client('s3', aws_access_key_id='code',
                                 aws_secret_access_key='code-secret')

        credentials_cls.assert_called_with(
            access_key='code', secret_key='code-secret', token=mock.ANY)

    def test_profile_env_vs_code(self):
        # If the profile is set both by the env var and by code,
        # then the one set by code should take precedence.
        os.environ['AWS_DEFAULT_PROFILE'] = 'test'
        s = self.create_session(profile='default')

        credentials = s.get_credentials()

        self.assertEqual(credentials.access_key, 'default')
        self.assertEqual(credentials.secret_key, 'default-secret')

    @mock.patch('botocore.credentials.Credentials')
    def test_access_secret_env_vs_code(self, credentials_cls):
        # If the access/secret keys are set both as env vars and via
        # code, then those set by code should take precedence.
        os.environ['AWS_ACCESS_KEY_ID'] = 'env'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'secret'
        s = self.create_session()

        client = s.create_client('s3', aws_access_key_id='code',
                                 aws_secret_access_key='code-secret')

        credentials_cls.assert_called_with(
            access_key='code', secret_key='code-secret', token=mock.ANY)

    def test_access_secret_env_vs_profile_code(self):
        # If access/secret keys are set in the environment, but then a
        # specific profile is passed via code, then the access/secret
        # keys defined in that profile should take precedence over
        # the environment variables. Example:
        #
        # ``aws --profile dev s3 ls``
        #
        os.environ['AWS_ACCESS_KEY_ID'] = 'env'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'env-secret'
        s = self.create_session(profile='test')

        credentials = s.get_credentials()

        self.assertEqual(credentials.access_key, 'test')
        self.assertEqual(credentials.secret_key, 'test-secret')

    def test_honors_aws_shared_credentials_file_env_var(self):
        with temporary_file('w') as f:
            f.write('[default]\n'
                    'aws_access_key_id=custom1\n'
                    'aws_secret_access_key=custom2\n')
            f.flush()
            os.environ['AWS_SHARED_CREDENTIALS_FILE'] = f.name
            s = Session()
            credentials = s.get_credentials()

            self.assertEqual(credentials.access_key, 'custom1')
            self.assertEqual(credentials.secret_key, 'custom2')
