#!/usr/bin/env python
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

import unittest
import logging

import mock

from tests import BaseSessionTest

import botocore.session
from botocore.exceptions import NoCredentialsError

LOG = logging.getLogger(__name__)


class TestSTSOperationsWithCreds(BaseSessionTest):

    def setUp(self):
        super(TestSTSOperationsWithCreds, self).setUp()
        self.sns = self.session.get_service('sts')
        self.called_params = {}
        self.session.register('before-auth.sts',
                              lambda **kwargs: self.called_params.update(kwargs))

    def reset_called_params(self):
        self.called_params = {}

    def get_mocked_endpoint(self):
        endpoint = self.sns.get_endpoint()
        endpoint._send_request = mock.Mock()
        return endpoint

    def test_get_session_token(self):
        op = self.sns.get_operation('GetSessionToken')
        params = {}
        endpoint = self.get_mocked_endpoint()
        endpoint.make_request(op, params)
        LOG.debug(self.called_params)
        self.assertIn('auth', self.called_params)
        self.reset_called_params()

    def test_assume_role_with_saml(self):
        op = self.sns.get_operation('AssumeRoleWithSAML')
        self.assertEqual(op.signature_version, None)
        endpoint = self.get_mocked_endpoint()
        params = op.build_parameters(principal_arn='principal_arn',
                                     role_arn='role_arn',
                                     saml_assertion='saml_assertion')
        endpoint.make_request(op, params)
        LOG.debug(self.called_params)
        self.assertNotIn('auth', self.called_params)
        self.reset_called_params()


class NoCredentialsTest(TestSTSOperationsWithCreds):

    def setUp(self):
        # Automatically patches out get_credentials to always
        # return None.
        super(NoCredentialsTest, self).setUp()
        self.get_credentials_patch = mock.patch(
            'botocore.credentials.get_credentials',
            self.mock_get_credentials)

    def mock_get_credentials(self, session, metadata=None):
        return None

    def test_get_session_token(self):
        with self.get_credentials_patch as mock_fn:
            session = botocore.session.get_session()
            sns = session.get_service('sts')
            op = sns.get_operation('GetSessionToken')
            params = {}
            endpoint = self.get_mocked_endpoint()
            self.assertRaises(NoCredentialsError,
                              endpoint.make_request,
                              op, params)

    def test_assume_role_with_saml(self):
        with self.get_credentials_patch as mock_fn:
            session = botocore.session.get_session()
            sns = session.get_service('sts')
            op = sns.get_operation('AssumeRoleWithSAML')
            self.assertEqual(op.signature_version, None)
            endpoint = self.get_mocked_endpoint()
            params = op.build_parameters(principal_arn='principal_arn',
                                         role_arn='role_arn',
                                         saml_assertion='saml_assertion')
            endpoint.make_request(op, params)
            self.assertNotIn('auth', self.called_params)
            self.reset_called_params()


if __name__ == "__main__":
    unittest.main()
