# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import pytest

from botocore.useragent import sanitize_user_agent_string_component


@pytest.mark.parametrize(
    'raw_str, allow_hash, expected_str',
    [
        ('foo', False, 'foo'),
        ('foo', True, 'foo'),
        ('ExampleFramework (1.2.3)', False, 'ExampleFramework--1.2.3-'),
        ('foo#1.2.3', False, 'foo-1.2.3'),
        ('foo#1.2.3', True, 'foo#1.2.3'),
        ('', False, ''),
        ('', True, ''),
        ('', False, ''),
        ('#', False, '-'),
        ('#', True, '#'),
        (' ', False, '-'),
        ('  ', False, '--'),
        ('@=[]{ }/\\øß©', True, '------------'),
        (
            'Java_HotSpot_(TM)_64-Bit_Server_VM/25.151-b12',
            True,
            'Java_HotSpot_-TM-_64-Bit_Server_VM-25.151-b12',
        ),
    ],
)
def test_sanitize_ua_string_component(raw_str, allow_hash, expected_str):
    actual_str = sanitize_user_agent_string_component(raw_str, allow_hash)
    assert actual_str == expected_str
