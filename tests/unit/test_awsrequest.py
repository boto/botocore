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
import io
import socket
import sys

from mock import Mock, patch

from botocore.exceptions import UnseekableStreamError
from botocore.awsrequest import AWSRequest
from botocore.awsrequest import AWSHTTPConnection
from botocore.compat import file_type, six


class IgnoreCloseBytesIO(io.BytesIO):
    def close(self):
        pass


class FakeSocket(object):
    def __init__(self, read_data, fileclass=IgnoreCloseBytesIO):
        self.sent_data = b''
        self.read_data = read_data
        self.fileclass = fileclass
        self._fp_object = None

    def sendall(self, data):
        self.sent_data += data

    def makefile(self, mode, bufsize=None):
        if self._fp_object is None:
            self._fp_object = self.fileclass(self.read_data)
        return self._fp_object

    def close(self):
        pass


class BytesIOWithLen(six.BytesIO):
    def __len__(self):
        return len(self.getvalue())


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


class TestAWSHTTPConnection(unittest.TestCase):
    def create_tunneled_connection(self, url, port, response):
        s = FakeSocket(response)
        conn = AWSHTTPConnection(url, port)
        conn.sock = s
        conn._tunnel_host = url
        conn._tunnel_port = port
        conn._tunnel_headers = {'key': 'value'}

        # Create a mock response.
        self.mock_response = Mock()
        self.mock_response.fp = Mock()

        # Imitate readline function by creating a list to be sent as
        # a side effect of the mocked readline to be able to track how the
        # response is processed in ``_tunnel()``.
        delimeter = b'\r\n'
        side_effect = []
        response_components = response.split(delimeter)
        for i in range(len(response_components)):
            new_component = response_components[i]
            # Only add the delimeter on if it is not the last component
            # which should be an empty string.
            if i != len(response_components) - 1:
                new_component += delimeter
            side_effect.append(new_component)

        self.mock_response.fp.readline.side_effect = side_effect

        response_components = response.split(b' ')
        self.mock_response._read_status.return_value = (
            response_components[0], int(response_components[1]),
            response_components[2]
        )
        conn.response_class = Mock()
        conn.response_class.return_value = self.mock_response
        return conn

    def test_expect_100_continue_returned(self):
        with patch('select.select') as select_mock:
            # Shows the server first sending a 100 continue response
            # then a 200 ok response.
            s = FakeSocket(b'HTTP/1.1 100 Continue\r\n\r\nHTTP/1.1 200 OK\r\n')
            conn = AWSHTTPConnection('s3.amazonaws.com', 443)
            conn.sock = s
            select_mock.return_value = ([s], [], [])
            conn.request('GET', '/bucket/foo', b'body',
                         {'Expect': '100-continue'})
            response = conn.getresponse()
            # Now we should verify that our final response is the 200 OK
            self.assertEqual(response.status, 200)

    def test_expect_100_sends_connection_header(self):
        # When using squid as an HTTP proxy, it will also send
        # a Connection: keep-alive header back with the 100 continue
        # response.  We need to ensure we handle this case.
        with patch('select.select') as select_mock:
            # Shows the server first sending a 100 continue response
            # then a 500 response.  We're picking 500 to confirm we
            # actually parse the response instead of getting the
            # default status of 200 which happens when we can't parse
            # the response.
            s = FakeSocket(b'HTTP/1.1 100 Continue\r\n'
                           b'Connection: keep-alive\r\n'
                           b'\r\n'
                           b'HTTP/1.1 500 Internal Service Error\r\n')
            conn = AWSHTTPConnection('s3.amazonaws.com', 443)
            conn.sock = s
            select_mock.return_value = ([s], [], [])
            conn.request('GET', '/bucket/foo', b'body',
                         {'Expect': '100-continue'})
            response = conn.getresponse()
            self.assertEqual(response.status, 500)

    def test_expect_100_continue_sends_307(self):
        # This is the case where we send a 100 continue and the server
        # immediately sends a 307
        with patch('select.select') as select_mock:
            # Shows the server first sending a 100 continue response
            # then a 200 ok response.
            s = FakeSocket(
                b'HTTP/1.1 307 Temporary Redirect\r\n'
                b'Location: http://example.org\r\n')
            conn = AWSHTTPConnection('s3.amazonaws.com', 443)
            conn.sock = s
            select_mock.return_value = ([s], [], [])
            conn.request('GET', '/bucket/foo', b'body',
                         {'Expect': '100-continue'})
            response = conn.getresponse()
            # Now we should verify that our final response is the 307.
            self.assertEqual(response.status, 307)

    def test_expect_100_continue_no_response_from_server(self):
        with patch('select.select') as select_mock:
            # Shows the server first sending a 100 continue response
            # then a 200 ok response.
            s = FakeSocket(
                b'HTTP/1.1 307 Temporary Redirect\r\n'
                b'Location: http://example.org\r\n')
            conn = AWSHTTPConnection('s3.amazonaws.com', 443)
            conn.sock = s
            # By settings select_mock to return empty lists, this indicates
            # that the server did not send any response.  In this situation
            # we should just send the request anyways.
            select_mock.return_value = ([], [], [])
            conn.request('GET', '/bucket/foo', b'body',
                         {'Expect': '100-continue'})
            response = conn.getresponse()
            self.assertEqual(response.status, 307)

    def test_message_body_is_file_like_object(self):
        # Shows the server first sending a 100 continue response
        # then a 200 ok response.
        body = BytesIOWithLen(b'body contents')
        s = FakeSocket(b'HTTP/1.1 200 OK\r\n')
        conn = AWSHTTPConnection('s3.amazonaws.com', 443)
        conn.sock = s
        conn.request('GET', '/bucket/foo', body)
        response = conn.getresponse()
        self.assertEqual(response.status, 200)

    def test_no_expect_header_set(self):
        # Shows the server first sending a 100 continue response
        # then a 200 ok response.
        s = FakeSocket(b'HTTP/1.1 200 OK\r\n')
        conn = AWSHTTPConnection('s3.amazonaws.com', 443)
        conn.sock = s
        conn.request('GET', '/bucket/foo', b'body')
        response = conn.getresponse()
        self.assertEqual(response.status, 200)

    def test_tunnel_readline_none_bugfix(self):
        # Tests whether ``_tunnel`` function is able to work around the
        # py26 bug of avoiding infinite while loop if nothing is returned.
        conn = self.create_tunneled_connection(
            url='s3.amazonaws.com',
            port=443,
            response=b'HTTP/1.1 200 OK\r\n',
        )
        conn._tunnel()
        # Ensure proper amount of readline calls were made.
        self.assertEqual(self.mock_response.fp.readline.call_count, 2)

    def test_tunnel_readline_normal(self):
        # Tests that ``_tunnel`` function behaves normally when it comes
        # across the usual http ending.
        conn = self.create_tunneled_connection(
            url='s3.amazonaws.com',
            port=443,
            response=b'HTTP/1.1 200 OK\r\n\r\n',
        )
        conn._tunnel()
        # Ensure proper amount of readline calls were made.
        self.assertEqual(self.mock_response.fp.readline.call_count, 2)

    def test_tunnel_raises_socket_error(self):
        # Tests that ``_tunnel`` function throws appropriate error when
        # not 200 status.
        conn = self.create_tunneled_connection(
            url='s3.amazonaws.com',
            port=443,
            response=b'HTTP/1.1 404 Not Found\r\n\r\n',
        )
        with self.assertRaises(socket.error):
            conn._tunnel()

    @unittest.skipIf(sys.version_info[:2] == (2, 6),
                     ("``_tunnel()`` function defaults to standard "
                      "http library function when not py26."))
    def test_tunnel_uses_std_lib(self):
        s = FakeSocket(b'HTTP/1.1 200 OK\r\n')
        conn = AWSHTTPConnection('s3.amazonaws.com', 443)
        conn.sock = s
        # Test that the standard library method was used by patching out
        # the ``_tunnel`` method and seeing if the std lib method was called.
        with patch('botocore.vendored.requests.packages.urllib3.connection.'
                   'HTTPConnection._tunnel') as mock_tunnel:
            conn._tunnel()
            self.assertTrue(mock_tunnel.called)

    def test_encodes_unicode_method_line(self):
        s = FakeSocket(b'HTTP/1.1 200 OK\r\n')
        conn = AWSHTTPConnection('s3.amazonaws.com', 443)
        conn.sock = s
        # Note the combination of unicode 'GET' and
        # bytes 'Utf8-Header' value.
        conn.request(u'GET', '/bucket/foo', b'body',
                     headers={"Utf8-Header": b"\xe5\xb0\x8f"})
        response = conn.getresponse()
        self.assertEqual(response.status, 200)


if __name__ == "__main__":
    unittest.main()
