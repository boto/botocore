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
from tests import unittest


class TestCredentialPrecedence(unittest.TestCase):
    def setUp(self):
        # Clean up any existing environment
        for name in ['AWS_ACCESS_KEY_ID',
                     'AWS_SECRET_ACCESS_KEY',
                     'BOTO_DEFAULT_PROFILE']:
            if name in os.environ:
                del os.environ[name]

        # Set the config file to something that doesn't exist, then
        # set the shared credential file to our test config.
        os.environ['AWS_CONFIG_FILE'] = '~/.aws/config-missing'
        Session.SessionVariables['credentials_file'] = (
            None, None,
            os.path.join(os.path.dirname(__file__), 'test-credentials'))

    def test_access_secret_vs_profile_env(self):
        # If all three are given, then the access/secret keys should
        # take precedence.
        os.environ['AWS_ACCESS_KEY_ID'] = 'env'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'env-secret'
        os.environ['BOTO_DEFAULT_PROFILE'] = 'test'

        s = Session()
        credentials = s.get_credentials()

        self.assertEqual(credentials.access_key, 'env')
        self.assertEqual(credentials.secret_key, 'env-secret')

    @mock.patch('botocore.credentials.Credentials')
    def test_access_secret_vs_profile_code(self, credentials_cls):
        # If all three are given, then the access/secret keys should
        # take precedence.
        s = Session()
        s.profile = 'test'

        client = s.create_client('s3', aws_access_key_id='code',
                                 aws_secret_access_key='code-secret')

        credentials_cls.assert_called_with(
            access_key='code', secret_key='code-secret', token=mock.ANY)

    def test_profile_env_vs_code(self):
        # If the profile is set both by the env var and by code,
        # then the one set by code should take precedence.
        os.environ['BOTO_DEFAULT_PROFILE'] = 'test'
        s = Session()
        s.profile = 'default'

        credentials = s.get_credentials()

        self.assertEqual(credentials.access_key, 'default')
        self.assertEqual(credentials.secret_key, 'default-secret')

    @mock.patch('botocore.credentials.Credentials')
    def test_access_secret_env_vs_code(self, credentials_cls):
        # If the access/secret keys are set both as env vars and via
        # code, then those set by code should take precedence.
        os.environ['AWS_ACCESS_KEY_ID'] = 'env'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'secret'
        s = Session()

        client = s.create_client('s3', aws_access_key_id='code',
                                 aws_secret_access_key='code-secret')

        credentials_cls.assert_called_with(
            access_key='code', secret_key='code-secret', token=mock.ANY)

    @mock.patch('botocore.credentials.Credentials')
    def test_access_secret_env_vs_profile_code(self, credentials_cls):
        # If access/secret keys are set in the environment, but then a
        # specific profile is passed via code, then the access/secret
        # keys defined in that profile should take precedence over
        # the environment variables. Example:
        #
        # ``aws --profile dev s3 ls``
        #
        os.environ['AWS_ACCESS_KEY_ID'] = 'env'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'env-secret'
        s = Session()
        s.profile = 'test'

        client = s.create_client('s3')

        credentials_cls.assert_called_with(
            'test', 'test-secret', None, method='shared-credentials-file')
