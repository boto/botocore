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
import pytest

from botocore.exceptions import DataNotFoundError
from botocore.loaders import Loader
from botocore.session import Session


def _paginators_and_waiters_test_cases():
    for service_name in Session().get_available_services():
        versions = Loader().list_api_versions(service_name, 'service-2')
        if len(versions) > 1:
            for type_name in ['paginators-1', 'waiters-2']:
                yield service_name, type_name, versions[-2], versions[-1]


@pytest.mark.parametrize(
    "service_name, type_name, previous_version, latest_version",
    _paginators_and_waiters_test_cases(),
)
def test_paginators_and_waiters_are_not_lost_in_new_version(
    service_name, type_name, previous_version, latest_version
):
    # Make sure if a paginator and/or waiter exists in previous version,
    # there will be a successor existing in latest version.
    loader = Loader()
    try:
        loader.load_service_model(service_name, type_name, previous_version)
    except DataNotFoundError:
        pass
    else:
        try:
            loader.load_service_model(service_name, type_name, latest_version)
        except DataNotFoundError as e:
            raise AssertionError(
                f"{type_name} must exist for {service_name}: {e}"
            )
