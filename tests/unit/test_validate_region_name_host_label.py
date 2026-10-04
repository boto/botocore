# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
"""Regression tests for ``validate_region_name``.

The docstring promises "must be a valid host label", but the regex used
``{,63}`` (which means ``{0,63}``, so the empty string matched) and ``$``
(which in Python matches just before a trailing newline). Both the empty
string and a region ending in ``\\n`` were therefore accepted.

The region reaches this validator from the server-controlled
``x-amz-bucket-region`` response header on the S3 cross-region redirect path.
"""

import pytest

from botocore.exceptions import InvalidRegionError
from botocore.utils import validate_region_name


@pytest.mark.parametrize(
    'region_name',
    [
        '',
        'us-east-1\n',
        '\n',
        'us-east-1\n\n',
        ' us-east-1',
        'us-east-1 ',
        'us-east-1\r',
    ],
)
def test_invalid_host_labels_are_rejected(region_name):
    with pytest.raises(InvalidRegionError):
        validate_region_name(region_name)


@pytest.mark.parametrize(
    'region_name',
    [
        'us-east-1',
        'us-gov-west-1',
        'cn-north-1',
        'a',
        'eu-central-1',
        'us-iso-east-1',
    ],
)
def test_valid_regions_are_still_accepted(region_name):
    validate_region_name(region_name)


def test_none_is_still_a_no_op():
    # Pre-existing contract: None means "no region supplied", not "invalid".
    validate_region_name(None)


def test_numeric_only_region_is_rejected():
    # Pre-existing guard: a bare number is not a valid region.
    with pytest.raises(InvalidRegionError):
        validate_region_name('12345')


def test_leading_or_trailing_hyphen_is_rejected():
    with pytest.raises(InvalidRegionError):
        validate_region_name('-us-east-1')
    with pytest.raises(InvalidRegionError):
        validate_region_name('us-east-1-')


def test_exactly_63_characters_is_accepted():
    region_name = 'a' * 63
    assert len(region_name) == 63
    validate_region_name(region_name)


def test_64_characters_is_rejected():
    with pytest.raises(InvalidRegionError):
        validate_region_name('a' * 64)