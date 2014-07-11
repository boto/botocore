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

import copy
import datetime
import six
import sys
import inspect


if six.PY3:
    from six.moves import http_client
    class HTTPHeaders(http_client.HTTPMessage):
        pass
    from urllib.parse import quote
    from urllib.parse import unquote
    from urllib.parse import unquote_plus
    from urllib.parse import urlsplit
    from urllib.parse import urlunsplit
    from urllib.parse import urljoin
    from urllib.parse import parse_qsl
    from urllib.parse import parse_qs
    from urllib.parse import urlencode
    from http.client import HTTPResponse
    from io import IOBase as _IOBase
    from base64 import encodebytes
    file_type = _IOBase
    zip = zip

    # In python3, unquote takes a str() object, url decodes it,
    # then takes the bytestring and decodes it to utf-8.
    # Python2 we'll have to do this ourself (see below).
    unquote_str = unquote_plus

    def set_socket_timeout(http_response, timeout):
        """Set the timeout of the socket from an HTTPResponse.

        :param http_response: An instance of ``httplib.HTTPResponse``

        """
        http_response._fp.fp.raw._sock.settimeout(timeout)

    def accepts_kwargs(func):
        # In python3.4.1, there's backwards incompatible
        # changes when using getargspec with functools.partials.
        return inspect.getfullargspec(func)[2]


else:
    from urllib import quote
    from urllib import unquote
    from urllib import unquote_plus
    from urllib import urlencode
    from urlparse import urlsplit
    from urlparse import urlunsplit
    from urlparse import urljoin
    from urlparse import parse_qsl
    from urlparse import parse_qs
    from email.message import Message
    file_type = file
    from itertools import izip as zip
    from httplib import HTTPResponse
    from base64 import encodestring as encodebytes

    class HTTPHeaders(Message):

        # The __iter__ method is not available in python2.x, so we have
        # to port the py3 version.
        def __iter__(self):
            for field, value in self._headers:
                yield field

    def unquote_str(value, encoding='utf-8'):
        # In python2, unquote() gives us a string back that has the urldecoded
        # bits, but not the unicode parts.  We need to decode this manually.
        # unquote has special logic in which if it receives a unicode object it
        # will decode it to latin1.  This is hard coded.  To avoid this, we'll
        # encode the string with the passed in encoding before trying to
        # unquote it.
        byte_string = value.encode(encoding)
        return unquote_plus(byte_string).decode(encoding)

    def set_socket_timeout(http_response, timeout):
        """Set the timeout of the socket from an HTTPResponse.

        :param http_response: An instance of ``httplib.HTTPResponse``

        """
        http_response._fp.fp._sock.settimeout(timeout)

    def accepts_kwargs(func):
        return inspect.getargspec(func)[2]

try:
    from collections import OrderedDict
except ImportError:
    # Python2.6 we use the 3rd party back port.
    from ordereddict import OrderedDict


if sys.version_info[:2] == (2, 6):
    import simplejson as json
    # In py26, invalid xml parsed by element tree
    # will raise a plain old SyntaxError instead of
    # a real exception, so we need to abstract this change.
    XMLParseError = SyntaxError
else:
    import xml.etree.cElementTree
    XMLParseError = xml.etree.cElementTree.ParseError
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


def total_seconds(delta):
    """
    Returns the total seconds in a ``datetime.timedelta``.

    Python 2.6 does not have ``timedelta.total_seconds()``, so we have
    to calculate this ourselves. On 2.7 or better, we'll take advantage of the
    built-in method.

    The math was pulled from the ``datetime`` docs
    (http://docs.python.org/2.7/library/datetime.html#datetime.timedelta.total_seconds).

    :param delta: The timedelta object
    :type delta: ``datetime.timedelta``
    """
    if sys.version_info[:2] != (2, 6):
        return delta.total_seconds()

    day_in_seconds = delta.days * 24 * 3600.0
    micro_in_seconds = delta.microseconds / 10.0**6
    return day_in_seconds + delta.seconds + micro_in_seconds
