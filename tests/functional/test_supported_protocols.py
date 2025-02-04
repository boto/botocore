# Copyright 2025 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

from botocore.args import PRIORITY_ORDERED_SUPPORTED_PROTOCOLS
from botocore.session import get_session


def _all_test_cases():
    session = get_session()
    loader = session.get_component('data_loader')

    services = loader.list_available_services('service-2')
    services_models_with_protocols = []
    services_models_without_protocols = []

    for service in services:
        service_model = session.get_service_model(service)
        if 'protocols' in service_model.metadata:
            services_models_with_protocols.append(service_model)
        else:
            services_models_without_protocols.append(service_model)
    return (services_models_with_protocols, services_models_without_protocols)


SERVICE_MODELS_WITH_PROTOCOLS, SERVICE_MODELS_WITHOUT_PROTOCOLS = (
    _all_test_cases()
)


@pytest.mark.validates_models
@pytest.mark.parametrize("service", SERVICE_MODELS_WITH_PROTOCOLS)
def test_services_with_protocols_trait_have_supported_protocol(service):
    service_supported_protocols = service.protocols
    message = f"No protocols supported for service {service.service_name}"
    assert any(
        protocol in PRIORITY_ORDERED_SUPPORTED_PROTOCOLS
        for protocol in service_supported_protocols
    ), message


@pytest.mark.validates_models
@pytest.mark.parametrize("service", SERVICE_MODELS_WITHOUT_PROTOCOLS)
def test_services_without_protocols_trait_have_supported_protocol(service):
    message = f"No protocols supported for service {service.service_name}"
    assert service.protocol in PRIORITY_ORDERED_SUPPORTED_PROTOCOLS, message
