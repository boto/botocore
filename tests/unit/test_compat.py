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

from botocore.compat import total_seconds, unquote_str

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
