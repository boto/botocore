# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
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
import logging
import select
import functools

import six
from botocore.vendored.requests import models
from botocore.vendored.requests.sessions import REDIRECT_STATI
from botocore.compat import HTTPHeaders, file_type, HTTPResponse
from botocore.exceptions import UnseekableStreamError
from botocore.vendored.requests.packages.urllib3.connection import VerifiedHTTPSConnection
from botocore.vendored.requests.packages.urllib3.connectionpool import HTTPConnectionPool
from botocore.vendored.requests.packages.urllib3.connectionpool import HTTPSConnectionPool


logger = logging.getLogger(__name__)


class AWSHTTPResponse(HTTPResponse):
    def __init__(self, sock, debuglevel=0, strict=0, method=None,
                 buffering=False, status_tuple=None):
        HTTPResponse.__init__(self, sock, debuglevel, strict,
                                  method, buffering)
        self._status_tuple = status_tuple

    def _read_status(self):
        if self._status_tuple is not None:
            status_tuple = self._status_tuple
            self._status_tuple = None
            return status_tuple
        else:
            return HTTPResponse._read_status(self)


class AWSHTTPConnection(VerifiedHTTPSConnection):
    """HTTPConnection that supports Expect 100-continue.

    This is conceptually a subclass of httplib.HTTPConnection (though
    technically we subclass from urllib3, which subclasses
    httplib.HTTPConnection) and we only override this class to support Expect
    100-continue, which we need for S3.  As far as I can tell, this is
    general purpose enough to not be specific to S3, but I'm being
    tentative and keeping it in botocore because I've only tested
    this against AWS services.

    """
    def _send_request(self, method, url, body, headers):
        # We need to override _send_request to record
        # whether or not we see an Expect: 100-continue
        # header via the self._expect_header_set attribute.
        self._extra = {
            'method': method,
            'url': url,
            'body': body,
            'headers': headers,
        }
        if headers.get('Expect', '') == '100-continue':
            self._expect_header_set = True
        else:
            self._expect_header_set = False
        return VerifiedHTTPSConnection._send_request(
            self, method, url, body, headers)

    def _send_output(self, message_body=None):
        self._buffer.extend((b"", b""))
        msg = b"\r\n".join(self._buffer)
        del self._buffer[:]
        # If msg and message_body are sent in a single send() call,
        # it will avoid performance problems caused by the interaction
        # between delayed ack and the Nagle algorithm.
        if isinstance(message_body, bytes):
            msg += message_body
            message_body = None
        self.send(msg)
        if self._expect_header_set:
            # This is our custom behavior.  If the Expect header was
            # set, it will trigger this custom behavior.
            logger.debug("Waiting for 100 Continue response.")
            # Wait for 1 second for the server to send a response.
            read, write, exc = select.select([self.sock], [], [self.sock], 1)
            if read:
                self._handle_expect_response(message_body)
                return
            else:
                # From the RFC:
                # Because of the presence of older implementations, the
                # protocol allows ambiguous situations in which a client may
                # send "Expect: 100-continue" without receiving either a 417
                # (Expectation Failed) status or a 100 (Continue) status.
                # Therefore, when a client sends this header field to an origin
                # server (possibly via a proxy) from which it has never seen a
                # 100 (Continue) status, the client SHOULD NOT wait for an
                # indefinite period before sending the request body.
                logger.debug("No response seen from server, continuing to "
                             "send the response body.")
        if message_body is not None:
            # message_body was not a string (i.e. it is a file), and
            # we must run the risk of Nagle.
            self.send(message_body)

    def _handle_expect_response(self, message_body):
        # This is called when we sent the request headers containing
        # an Expect: 100-continue header and received a response.
        # We now need to figure out what to do.
        fp = self.sock.makefile('rb', 0)
        maybe_status_line = fp.readline()
        parts = maybe_status_line.split(None, 2)
        if self._is_100_continue_status(maybe_status_line):
            # Read an empty line as per the RFC.
            fp.readline()
            logger.debug("100 Continue response seen, now sending request body.")
            self._send_message_body(message_body)
            self._expect_header_set = False
        elif len(parts) == 3 and parts[0].startswith(b'HTTP/'):
            # From the RFC:
            # Requirements for HTTP/1.1 origin servers:
            #
            # - Upon receiving a request which includes an Expect
            #   request-header field with the "100-continue"
            #   expectation, an origin server MUST either respond with
            #   100 (Continue) status and continue to read from the
            #   input stream, or respond with a final status code.
            #
            # So if we don't get a 100 Continue response, then
            # whatever the server has sent back is the final response
            # and don't send the message_body.
            logger.debug("Received a non 100 Continue response "
                         "from the server, NOT sending request body.")
            status_tuple = (parts[0].decode('ascii'),
                            int(parts[1]), parts[2].decode('ascii'))
            response_class = functools.partial(
                AWSHTTPResponse, status_tuple=status_tuple)
            self.response_class = response_class
            self._expect_header_set = False

    def _send_message_body(self, message_body):
        if message_body is not None:
            self.send(message_body)

    def _is_100_continue_status(self, maybe_status_line):
        parts = maybe_status_line.split(None, 2)
        # Check for HTTP/<version> 100 Continue\r\n
        return (
            len(parts) == 3 and parts[0].startswith(b'HTTP/') and
            parts[1] == b'100' and parts[2].startswith(b'Continue'))


class AWSRequest(models.RequestEncodingMixin, models.Request):
    def __init__(self, *args, **kwargs):
        self.auth_path = None
        if 'auth_path' in kwargs:
            self.auth_path = kwargs['auth_path']
            del kwargs['auth_path']
        models.Request.__init__(self, *args, **kwargs)
        headers = HTTPHeaders()
        if self.headers is not None:
            for key, value in self.headers.items():
                headers[key] = value
        headers['Expect'] = '100-continue'
        self.headers = headers

    def prepare(self):
        """Constructs a :class:`AWSPreparedRequest <AWSPreparedRequest>`."""
        # Eventually I think it would be nice to add hooks into this process.
        p = AWSPreparedRequest(self)
        p.prepare_method(self.method)
        p.prepare_url(self.url, self.params)
        p.prepare_headers(self.headers)
        p.prepare_cookies(self.cookies)
        p.prepare_body(self.data, self.files)
        p.prepare_auth(self.auth)
        return p

    @property
    def body(self):
        p = models.PreparedRequest()
        p.prepare_headers({})
        p.prepare_body(self.data, self.files)
        return p.body


class AWSPreparedRequest(models.PreparedRequest):
    """Represents a prepared request.

    :ivar method: HTTP Method
    :ivar url: The full url
    :ivar headers: The HTTP headers to send.
    :ivar body: The HTTP body.
    :ivar hooks: The set of callback hooks.

    In addition to the above attributes, the following attributes are
    available:

    :ivar query_params: The original query parameters.
    :ivar post_param: The original POST params (dict).

    """
    def __init__(self, original_request):
        self.original = original_request
        super(AWSPreparedRequest, self).__init__()
        self.hooks.setdefault('response', []).append(
            self.reset_stream_on_redirect)

    def reset_stream_on_redirect(self, response, **kwargs):
        if response.status_code in REDIRECT_STATI and \
                self._looks_like_file(self.body):
            logger.debug("Redirect received, rewinding stream: %s", self.body)
            self.reset_stream()

    def _looks_like_file(self, body):
        return hasattr(body, 'read') and hasattr(body, 'seek')

    def reset_stream(self):
        # Trying to reset a stream when there is a no stream will
        # just immediately return.  It's not an error, it will produce
        # the same result as if we had actually reset the stream (we'll send
        # the entire body contents again if we need to).
        # Same case if the body is a string/bytes type.
        if self.body is None or isinstance(self.body, six.text_type) or \
                isinstance(self.body, six.binary_type):
            return
        try:
            logger.debug("Rewinding stream: %s", self.body)
            self.body.seek(0)
        except Exception as e:
            logger.debug("Unable to rewind stream: %s", e)
            raise UnseekableStreamError(stream_object=self.body)


HTTPSConnectionPool.ConnectionCls = AWSHTTPConnection
