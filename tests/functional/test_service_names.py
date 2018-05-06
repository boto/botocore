# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import re

from nose.tools import assert_true
from botocore.session import get_session

BLACKLIST = [
]


# Service names are limited here to 50 characters here as that seems like a
# reasonable limit in the general case. Services can be added to the
# blacklist above to be given an exception.
VALID_NAME_REGEX = re.compile(
    (
        '[a-z]'           # Starts with a letter
        '[a-z0-9]*'       # Followed by any number of letters or digits
        '(-[a-z0-9]+)*$'  # Dashes are allowed as long as they aren't
                          # consecutive or at the end
    ), re.M)
VALID_NAME_EXPLANATION = (
    'Service names must be made up entirely of lowercase alphanumeric '
    'characters and dashes. The name must start with a letter and may not end '
    'with a dash'
)
MIN_SERVICE_NAME_LENGTH = 2
MAX_SERVICE_NAME_LENGTH = 50


def _assert_name_length(service_name):
    if service_name not in BLACKLIST:
        service_name_length = len(service_name)
        assert_true(service_name_length >= MIN_SERVICE_NAME_LENGTH,
                    'Service name must be greater than or equal to 2 '
                    'characters in length.')
        assert_true(service_name_length <= MAX_SERVICE_NAME_LENGTH,
                    'Service name must be less than or equal to 50 '
                    'characters in length.')


def _assert_name_pattern(service_name):
    if service_name not in BLACKLIST:
        valid = VALID_NAME_REGEX.match(service_name) is not None
        assert_true(valid, VALID_NAME_EXPLANATION)


def test_service_names_are_valid():
    session = get_session()
    loader = session.get_component('data_loader')
    service_names = loader.list_available_services('service-2')
    for service_name in service_names:
        yield _assert_name_length, service_name
        yield _assert_name_pattern, service_name
