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
