#!/usr/bin/env
# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from nose.tools import assert_equals

from botocore import exceptions


def test_client_error_can_handle_missing_code_or_message():
    response = {'Error': {}}
    expect = 'An error occurred (Unknown) when calling the blackhole operation: Unknown'
    assert_equals(str(exceptions.ClientError(response, 'blackhole')), expect)


def test_client_error_has_operation_name_set():
    response = {'Error': {}}
    exception = exceptions.ClientError(response, 'blackhole')
    assert hasattr(exception, 'operation_name')


def test_client_error_set_correct_operation_name():
    response = {'Error': {}}
    exception = exceptions.ClientError(response, 'blackhole')
    assert_equals(exception.operation_name, 'blackhole')


def test_retry_info_added_when_present():
    response = {
        'Error': {},
        'ResponseMetadata': {
            'MaxAttemptsReached': True,
            'RetryAttempts': 3,
        }
    }
    error_msg = str(exceptions.ClientError(response, 'operation'))
    if '(reached max retries: 3)' not in error_msg:
        raise AssertionError("retry information not inject into error "
                             "message: %s" % error_msg)


def test_retry_info_not_added_if_retry_attempts_not_present():
    response = {
        'Error': {},
        'ResponseMetadata': {
            'MaxAttemptsReached': True,
        }
    }
    # Because RetryAttempts is missing, retry info is not
    # in the error message.
    error_msg = str(exceptions.ClientError(response, 'operation'))
    if 'max retries' in error_msg:
        raise AssertionError("Retry information should not be in exception "
                             "message when retry attempts not in response "
                             "metadata: %s" % error_msg)
