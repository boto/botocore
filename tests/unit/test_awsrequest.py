#!/usr/bin/env
# Copyright 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import os
import tempfile
import shutil

from mock import Mock

from botocore.exceptions import UnseekableStreamError
from botocore.awsrequest import AWSRequest
from botocore.compat import file_type


class Unseekable(file_type):
    def __init__(self, stream):
        self._stream = stream

    def read(self):
        return self._stream.read()

    def seek(self, offset, whence):
        # This is a case where seek() exists as part of the object's interface,
        # but it doesn't actually work (for example socket.makefile(), which
        # will raise an io.* error on python3).
        raise ValueError("Underlying stream does not support seeking.")


class TestAWSRequest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.request = AWSRequest(url='http://example.com')
        self.prepared_request = self.request.prepare()
        self.filename = os.path.join(self.tempdir, 'foo')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_should_reset_stream(self):
        with open(self.filename, 'wb') as f:
            f.write(b'foobarbaz')
        with open(self.filename, 'rb') as body:
            self.prepared_request.body = body

            # Now pretend we try to send the request.
            # This means that we read the body:
            body.read()
            # And create a response object that indicates
            # a redirect.
            fake_response = Mock()
            fake_response.status_code = 307

            # Then requests calls our reset_stream hook.
            self.prepared_request.reset_stream(fake_response)

            # The stream should now be reset.
            self.assertEqual(body.tell(), 0)

    def test_cannot_reset_stream_raises_error(self):
        with open(self.filename, 'wb') as f:
            f.write(b'foobarbaz')
        with open(self.filename, 'rb') as body:
            self.prepared_request.body = Unseekable(body)

            # Now pretend we try to send the request.
            # This means that we read the body:
            body.read()
            # And create a response object that indicates
            # a redirect.
            fake_response = Mock()
            fake_response.status_code = 307

            # Then requests calls our reset_stream hook.
            with self.assertRaises(UnseekableStreamError):
                self.prepared_request.reset_stream(fake_response)


if __name__ == "__main__":
    unittest.main()
