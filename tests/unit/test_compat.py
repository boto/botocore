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

import datetime
import mock

from botocore.exceptions import MD5UnavailableError
from botocore.compat import (
    total_seconds, unquote_str, six, ensure_bytes, get_md5
)

from tests import BaseEnvVar, unittest


class TotalSecondsTest(BaseEnvVar):
    def test_total_seconds(self):
        delta = datetime.timedelta(days=1, seconds=45)
        remaining = total_seconds(delta)
        self.assertEqual(remaining, 86445.0)

        delta = datetime.timedelta(seconds=33, microseconds=772)
        remaining = total_seconds(delta)
        self.assertEqual(remaining, 33.000772)


class TestUnquoteStr(unittest.TestCase):
    def test_unquote_str(self):
        value = u'%E2%9C%93'
        # Note: decoded to unicode and utf-8 decoded as well.
        # This would work in python2 and python3.
        self.assertEqual(unquote_str(value), u'\u2713')

    def test_unquote_normal(self):
        value = u'foo'
        # Note: decoded to unicode and utf-8 decoded as well.
        # This would work in python2 and python3.
        self.assertEqual(unquote_str(value), u'foo')

    def test_unquote_with_spaces(self):
        value = u'foo+bar'
        # Note: decoded to unicode and utf-8 decoded as well.
        # This would work in python2 and python3.
        self.assertEqual(unquote_str(value), 'foo bar')


class TestEnsureBytes(unittest.TestCase):
    def test_string(self):
        value = 'foo'
        response = ensure_bytes(value)
        self.assertIsInstance(response, six.binary_type)
        self.assertEqual(response, b'foo')

    def test_binary(self):
        value = b'bar'
        response = ensure_bytes(value)
        self.assertIsInstance(response, six.binary_type)
        self.assertEqual(response, b'bar')

    def test_unicode(self):
        value = u'baz'
        response = ensure_bytes(value)
        self.assertIsInstance(response, six.binary_type)
        self.assertEqual(response, b'baz')

    def test_non_ascii(self):
        value = u'\u2713'
        response = ensure_bytes(value)
        self.assertIsInstance(response, six.binary_type)
        self.assertEqual(response, b'\xe2\x9c\x93')

    def test_non_string_or_bytes_raises_error(self):
        value = 500
        with self.assertRaises(ValueError):
            ensure_bytes(value)


class TestGetMD5(unittest.TestCase):
    def test_available(self):
        md5 = mock.Mock()
        with mock.patch('botocore.compat.MD5_AVAILABLE', True):
            with mock.patch('hashlib.md5', mock.Mock(return_value=md5)):
                self.assertEqual(get_md5(), md5)

    def test_unavailable_raises_error(self):
        with mock.patch('botocore.compat.MD5_AVAILABLE', False):
            with self.assertRaises(MD5UnavailableError):
                get_md5()
