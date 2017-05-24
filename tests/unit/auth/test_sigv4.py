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

"""Signature Version 4 test suite.

AWS provides a test suite for signature version 4:

    http://docs.aws.amazon.com/general/latest/gr/signature-v4-test-suite.html

This module contains logic to run these tests.  The test files were
placed in ./aws4_testsuite, and we're using nose's test generators to
dynamically generate testcases based on these files.

"""
import os
import logging
import io
import datetime
from botocore.compat import six

import nose.tools as t
from nose import with_setup
import mock

import botocore.auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials

try:
    from urllib.parse import urlsplit
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import urlsplit
    from urlparse import parse_qsl


CREDENTIAL_SCOPE = "KEYNAME/20110909/us-west-1/s3/aws4_request"
SECRET_KEY = "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"
ACCESS_KEY = 'AKIDEXAMPLE'
DATE_STRING = 'Mon, 09 Sep 2011 23:36:00 GMT'

TESTSUITE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'aws4_testsuite')

# The following tests are not run.  Each test has a comment as
# to why the test is being ignored.
TESTS_TO_IGNORE = [
    # Bad POST syntax, python's HTTP parser chokes on this.
    'post-vanilla-query-space',
    # Bad POST syntax, python's HTTP parser chokes on this.
    'post-vanilla-query-nonunreserved',
    # Multiple query params of the same key not supported by
    # the SDKs.
    'get-vanilla-query-order-key-case',
    # Multiple query params of the same key not supported by
    # the SDKs.
    'get-vanilla-query-order-value',
]
if not six.PY3:
    TESTS_TO_IGNORE += [
        # NO support
        'get-header-key-duplicate',
        'get-header-value-order',
    ]

log = logging.getLogger(__name__)


class RawHTTPRequest(six.moves.BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, raw_request):
        if isinstance(raw_request, six.text_type):
            raw_request = raw_request.encode('utf-8')
        self.rfile = six.BytesIO(raw_request)
        self.raw_requestline = self.rfile.readline()
        self.error_code = None
        self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


def test_generator():
    datetime_patcher = mock.patch.object(
        botocore.auth.datetime, 'datetime',
        mock.Mock(wraps=datetime.datetime)
    )
    mocked_datetime = datetime_patcher.start()
    mocked_datetime.utcnow.return_value = datetime.datetime(2011, 9, 9, 23, 36)
    formatdate_patcher = mock.patch('botocore.auth.formatdate')
    formatdate = formatdate_patcher.start()
    # We have to change this because Sep 9, 2011 was actually
    # a Friday, but the tests have this set to a Monday.
    formatdate.return_value = 'Mon, 09 Sep 2011 23:36:00 GMT'
    for test_case in set(os.path.splitext(i)[0]
                         for i in os.listdir(TESTSUITE_DIR)):
        if test_case in TESTS_TO_IGNORE:
            log.debug("Skipping test: %s", test_case)
            continue
        yield (_test_signature_version_4, test_case)
    datetime_patcher.stop()
    formatdate_patcher.stop()


def create_request_from_raw_request(raw_request):
    raw_request = raw_request.replace('http/1.1', 'HTTP/1.1')
    request = AWSRequest()
    raw = RawHTTPRequest(raw_request)
    if raw.error_code is not None:
        raise Exception(raw.error_message)
    request.method = raw.command
    datetime_now = datetime.datetime(2011, 9, 9, 23, 36)
    request.context['timestamp'] = datetime_now.strftime('%Y%m%dT%H%M%SZ')
    for key, val in raw.headers.items():
        request.headers[key] = val
    request.data = raw.rfile.read()
    host = raw.headers.get('host', '')
    # For whatever reason, the BaseHTTPRequestHandler encodes
    # the first line of the response as 'iso-8859-1',
    # so we need decode this into utf-8.
    if isinstance(raw.path, six.text_type):
        raw.path = raw.path.encode('iso-8859-1').decode('utf-8')
    url = 'https://%s%s' % (host, raw.path)
    if '?' in url:
        split_url = urlsplit(url)
        params = dict(parse_qsl(split_url.query))
        request.url = split_url.path
        request.params = params
    else:
        request.url = url
    return request


def _test_signature_version_4(test_case):
    test_case = _SignatureTestCase(test_case)
    request = create_request_from_raw_request(test_case.raw_request)

    auth = botocore.auth.SigV4Auth(test_case.credentials, 'host', 'us-east-1')

    actual_canonical_request = auth.canonical_request(request)
    assert_equal(actual_canonical_request, test_case.canonical_request,
                 test_case.raw_request, 'canonical_request')

    actual_string_to_sign = auth.string_to_sign(request,
                                                actual_canonical_request)
    assert_equal(actual_string_to_sign, test_case.string_to_sign,
                 test_case.raw_request, 'string_to_sign')

    auth.add_auth(request)
    actual_auth_header = request.headers['Authorization']
    assert_equal(actual_auth_header, test_case.authorization_header,
                 test_case.raw_request, 'authheader')


def assert_equal(actual, expected, raw_request, part):
    if actual != expected:
        message = "The %s did not match" % part
        message += "\nACTUAL:%r !=\nEXPECT:%r" % (actual, expected)
        message += '\nThe raw request was:\n%s' % raw_request
        raise AssertionError(message)


class _SignatureTestCase(object):
    def __init__(self, test_case):
        p = os.path.join
        # We're using io.open() because we need to open these files with
        # a specific encoding, and in 2.x io.open is the best way to do this.
        self.raw_request = io.open(p(TESTSUITE_DIR, test_case + '.req'),
                                   encoding='utf-8').read()
        self.canonical_request = io.open(
            p(TESTSUITE_DIR, test_case + '.creq'),
            encoding='utf-8').read().replace('\r', '')
        self.string_to_sign = io.open(
            p(TESTSUITE_DIR, test_case + '.sts'),
            encoding='utf-8').read().replace('\r', '')
        self.authorization_header = io.open(
            p(TESTSUITE_DIR, test_case + '.authz'),
            encoding='utf-8').read().replace('\r', '')
        self.signed_request = io.open(p(TESTSUITE_DIR, test_case + '.sreq'),
                                      encoding='utf-8').read()

        self.credentials = Credentials(ACCESS_KEY, SECRET_KEY)
