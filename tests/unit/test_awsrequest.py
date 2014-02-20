#!/usr/bin/env
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
            self.prepared_request.reset_stream_on_redirect(fake_response)

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
            # a redirect
            fake_response = Mock()
            fake_response.status_code = 307

            # Then requests calls our reset_stream hook.
            with self.assertRaises(UnseekableStreamError):
                self.prepared_request.reset_stream_on_redirect(fake_response)

    def test_duck_type_for_file_check(self):
        # As part of determining whether or not we can rewind a stream
        # we first need to determine if the thing is a file like object.
        # We should not be using an isinstance check.  Instead, we should
        # be using duck type checks.
        class LooksLikeFile(object):
            def __init__(self):
                self.seek_called = False

            def read(self, amount=None):
                pass

            def seek(self, where):
                self.seek_called = True

        looks_like_file = LooksLikeFile()
        self.prepared_request.body = looks_like_file

        fake_response = Mock()
        fake_response.status_code = 307

        # Then requests calls our reset_stream hook.
        self.prepared_request.reset_stream_on_redirect(fake_response)

        # The stream should now be reset.
        self.assertTrue(looks_like_file.seek_called)



if __name__ == "__main__":
    unittest.main()
