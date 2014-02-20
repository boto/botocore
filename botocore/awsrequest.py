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

import six
from botocore.vendored.requests import models
from botocore.vendored.requests.sessions import REDIRECT_STATI

from botocore.compat import HTTPHeaders, file_type
from botocore.exceptions import UnseekableStreamError


logger = logging.getLogger(__name__)


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
