# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

from botocore.session import get_session

# In the future, some services may have a list of credentials requirements where one signature may fail and others may
# succeed, for instance a service may want to use bearer by default but fall back to sigv4 if a token isn't found.
# There currently is not a way to do this in botocore, so we added this test to make sure that we handle this gracefully
# when the need arises.
AUTH_TYPE_REQUIREMENTS = {
    'aws.auth#sigv4': ['credentials'],
    'aws.auth#sigv4a': ['credentials'],
    'smithy.api#httpBearerAuth': ['bearer_token'],
    'smithy.api#noAuth': [],
}


def _all_test_cases():
    session = get_session()
    loader = session.get_component('data_loader')

    services = loader.list_available_services('service-2')
    auth_services = []
    auth_operations = []

    for service in services:
        service_model = session.get_service_model(service)
        auth_config = service_model.metadata.get('auth', {})
        if auth_config:
            auth_services.append([service, auth_config])
        for operation in service_model.operation_names:
            operation_model = service_model.operation_model(operation)
            if operation_model.auth:
                auth_operations.append([service, operation_model])
    return auth_services, auth_operations


AUTH_SERVICES, AUTH_OPERATIONS = _all_test_cases()


@pytest.mark.validates_models
@pytest.mark.parametrize("auth_service, auth_config", AUTH_SERVICES)
def test_all_requirements_match_for_service(auth_service, auth_config):
    # Validates that all service-level signature types have the same requirements
    message = f'Found mixed signer requirements for service: {auth_service}'
    assert_all_requirements_match(auth_config, message)


@pytest.mark.validates_models
@pytest.mark.parametrize("auth_service, operation_model", AUTH_OPERATIONS)
def test_all_requirements_match_for_operation(auth_service, operation_model):
    # Validates that all operation-level signature types have the same requirements
    message = f'Found mixed signer requirements for operation: {auth_service}.{operation_model.name}'
    auth_config = operation_model.auth
    assert_all_requirements_match(auth_config, message)


def assert_all_requirements_match(auth_config, message):
    if len(auth_config) > 1:
        first_auth = auth_config.pop()
        first_auth_reqs = AUTH_TYPE_REQUIREMENTS[first_auth]
        assert all(
            first_auth_reqs == AUTH_TYPE_REQUIREMENTS[req]
            for req in auth_config
        ), message