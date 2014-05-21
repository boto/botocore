#!/usr/bin/env
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
from tests import unittest
import mock
import six

import botocore.auth
import botocore.credentials
from botocore.compat import HTTPHeaders


class TestSigV2(unittest.TestCase):

    def setUp(self):
        access_key = 'foo'
        secret_key = 'bar'
        self.credentials = botocore.credentials.Credentials(access_key,
                                                            secret_key)
        self.signer = botocore.auth.SigV2Auth(self.credentials)

    def test_put(self):
        request = mock.Mock()
        request.url = '/'
        request.method = 'POST'
        params = {'Foo': u'\u2713'}
        result = self.signer.calc_signature(request, params)
        self.assertEqual(
            result, ('Foo=%E2%9C%93',
                     u'VCtWuwaOL0yMffAT8W4y0AFW3W4KUykBqah9S40rB+Q='))
