# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under thimport mock
import contextlib
import copy
import json
import os
import socket
import threading

import mock
from nose.tools import assert_equal

from tests import temporary_file
from tests import ClientHTTPStubber
from botocore import xform_name
import botocore.session
import botocore.exceptions


CASES_FILE = os.path.join(os.path.dirname(__file__), 'cases.json')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data/')


class RetryableException(botocore.exceptions.EndpointConnectionError):
    fmt = '{message}'


class NonRetryableException(Exception):
    pass


def test_client_monitoring():
    test_cases = _load_test_cases()
    for case in test_cases:
        yield _run_test_case, case


def _load_test_cases():
    with open(CASES_FILE) as f:
        loaded_tests = json.loads(f.read())
    test_cases = _get_cases_with_defaults(loaded_tests)
    _replace_expected_anys(test_cases)
    return test_cases


def _get_cases_with_defaults(loaded_tests):
    cases = []
    defaults = loaded_tests['defaults']
    for case in loaded_tests['cases']:
        base = copy.deepcopy(defaults)
        base.update(case)
        cases.append(base)
    return cases


def _replace_expected_anys(test_cases):
    for case in test_cases:
        for expected_event in case['expectedMonitoringEvents']:
            for entry, value in expected_event.items():
                if value in ['ANY_STR', 'ANY_INT']:
                    expected_event[entry] = mock.ANY


@contextlib.contextmanager
def _configured_session(case_configuration, listener_port):
    environ = {
        'AWS_ACCESS_KEY_ID': case_configuration['accessKey'],
        'AWS_SECRET_ACCESS_KEY': 'secret-key',
        'AWS_DEFAULT_REGION': case_configuration['region'],
        'AWS_DATA_PATH': DATA_DIR,
        'AWS_CSM_PORT': listener_port
    }
    environ.update(case_configuration['environmentVariables'])
    if 'sessionToken' in case_configuration:
        environ['AWS_SESSION_TOKEN'] = case_configuration['sessionToken']
    with temporary_file('w') as f:
        f.write('[default]\n')
        for key, value in case_configuration['sharedConfigFile'].items():
            f.write('%s = %s\n' % (key, value))
        f.flush()
        environ['AWS_CONFIG_FILE'] = f.name
        with mock.patch('os.environ', environ):
            yield botocore.session.Session()


def _run_test_case(case):
    with MonitoringListener() as listener:
        with _configured_session(
                case['configuration'], listener.port) as session:
            for api_call in case['apiCalls']:
                _make_api_call(session, api_call)
        assert_equal(
            listener.received_events, case['expectedMonitoringEvents'])


def _make_api_call(session, api_call):
    client = session.create_client(
        api_call['serviceId'].lower().replace(' ', ''))
    operation_name = api_call['operationName']
    client_method = getattr(client, xform_name(operation_name))
    with _stubbed_http_layer(client, api_call['attemptResponses']):
        try:
            client_method(**api_call['params'])
        except (botocore.exceptions.ClientError, NonRetryableException):
            pass


@contextlib.contextmanager
def _stubbed_http_layer(client, attempt_responses):
    with ClientHTTPStubber(client) as stubber:
        _add_stubbed_responses(stubber, attempt_responses)
        yield


def _add_stubbed_responses(stubber, attempt_responses):
    for attempt_response in attempt_responses:
        if 'sdkException' in attempt_response:
            sdk_exception = attempt_response['sdkException']
            _add_sdk_exception(
                stubber, sdk_exception['message'],
                sdk_exception['isRetryable']
            )
        else:
            _add_stubbed_response(stubber, attempt_response)


def _add_sdk_exception(stubber, message, is_retryable):
    if is_retryable:
        stubber.responses.append(RetryableException(message=message))
    else:
        stubber.responses.append(NonRetryableException(message))


def _add_stubbed_response(stubber, attempt_response):
    headers = attempt_response['responseHeaders']
    status_code = attempt_response['httpStatus']
    if 'errorCode' in attempt_response:
        error = {
            '__type': attempt_response['errorCode'],
            'message': attempt_response['errorMessage']
        }
        content = json.dumps(error).encode('utf-8')
    else:
        content = b'{}'
    stubber.add_response(status=status_code, headers=headers, body=content)


class MonitoringListener(threading.Thread):
    _PACKET_SIZE = 1024 * 8

    def __init__(self, port=0):
        threading.Thread.__init__(self)
        self._socket = None
        self.port = port
        self.received_events = []

    def __enter__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(('127.0.0.1', self.port))
        # The socket may have been assigned to an unused port so we
        # reset the port member after binding.
        self.port = self._socket.getsockname()[1]
        self.start()
        return self

    def __exit__(self, *args):
        self._socket.sendto(b'', ('127.0.0.1', self.port))
        self.join()
        self._socket.close()

    def run(self):
        while True:
            data = self._socket.recv(self._PACKET_SIZE)
            if not data:
                return
            self.received_events.append(json.loads(data.decode('utf-8')))
