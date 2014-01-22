# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
from tests import unittest

import mock
import six
from botocore import response
from botocore.exceptions import IncompleteReadError


class TestStreamWrapper(unittest.TestCase):
    def test_streaming_wrapper_validates_content_length(self):
        body = six.BytesIO(b'1234567890')
        stream = response.StreamingBody(body, content_length=10)
        self.assertEqual(stream.read(), b'1234567890')

    def test_streaming_body_with_invalid_length(self):
        body = six.BytesIO(b'123456789')
        stream = response.StreamingBody(body, content_length=10)
        with self.assertRaises(IncompleteReadError):
            self.assertEqual(stream.read(9), b'123456789')
            # The next read will have nothing returned and raise
            # an IncompleteReadError because we were expectd 10 bytes, not 9.
            stream.read()

    def test_streaming_body_with_single_read(self):
        body = six.BytesIO(b'123456789')
        stream = response.StreamingBody(body, content_length=10)
        with self.assertRaises(IncompleteReadError):
            stream.read()
