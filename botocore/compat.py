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

import sys
import copy
import six
if six.PY3:
    from six.moves import http_client
    class HTTPHeaders(http_client.HTTPMessage):
        pass
    from urllib.parse import quote
    from urllib.parse import unquote
    from urllib.parse import urlsplit
    from urllib.parse import urlunsplit
    from urllib.parse import urljoin
    from urllib.parse import parse_qsl
    from io import IOBase as _IOBase
    file_type = _IOBase

    def set_socket_timeout(http_response, timeout):
        """Set the timeout of the socket from an HTTPResponse.

        :param http_response: An instance of ``httplib.HTTPResponse``

        """
        http_response._fp.fp.raw._sock.settimeout(timeout)

else:
    from urllib import quote
    from urllib import unquote
    from urlparse import urlsplit
    from urlparse import urlunsplit
    from urlparse import urljoin
    from urlparse import parse_qsl
    from email.message import Message
    file_type = file
    class HTTPHeaders(Message):

        # The __iter__ method is not available in python2.x, so we have
        # to port the py3 version.
        def __iter__(self):
            for field, value in self._headers:
                yield field

    def set_socket_timeout(http_response, timeout):
        """Set the timeout of the socket from an HTTPResponse.

        :param http_response: An instance of ``httplib.HTTPResponse``

        """
        http_response._fp.fp._sock.settimeout(timeout)

try:
    from collections import OrderedDict
except ImportError:
    # Python2.6 we use the 3rd party back port.
    from ordereddict import OrderedDict


if sys.version_info[:2] == (2, 6):
    import simplejson as json
else:
    import json


@classmethod
def from_dict(cls, d):
    new_instance = cls()
    for key, value in d.items():
        new_instance[key] = value
    return new_instance


@classmethod
def from_pairs(cls, pairs):
    new_instance = cls()
    for key, value in pairs:
        new_instance[key] = value
    return new_instance

HTTPHeaders.from_dict = from_dict
HTTPHeaders.from_pairs = from_pairs


def copy_kwargs(kwargs):
    """
    There is a bug in Python versions < 2.6.5 that prevents you
    from passing unicode keyword args (#4978).  This function
    takes a dictionary of kwargs and returns a copy.  If you are
    using Python < 2.6.5, it also encodes the keys to avoid this bug.
    Oh, and version_info wasn't a namedtuple back then, either!
    """
    vi = sys.version_info
    if vi[0] == 2 and vi[1] <= 6 and vi[3] < 5:
        copy_kwargs = {}
        for key in kwargs:
            copy_kwargs[key.encode('utf-8')] = kwargs[key]
    else:
        copy_kwargs = copy.copy(kwargs)
    return copy_kwargs
