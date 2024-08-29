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

# This test verifies that S3 is the only service that uses the 'expires' header
# in their response. If any other service is found to target this header in any
# of their output shapes, the test will fail and alert us of the change.


@pytest.mark.validates_models
def test_only_s3_targets_expires_header():
    session = get_session()
    loader = session.get_component('data_loader')
    services = loader.list_available_services('service-2')
    services_that_target_expires_header = set()

    for service in services:
        service_model = session.get_service_model(service)
        for operation in service_model.operation_names:
            operation_model = service_model.operation_model(operation)
            if output_shape := operation_model.output_shape:
                if _shape_targets_expires_header(output_shape):
                    services_that_target_expires_header.add(service)
    assert services_that_target_expires_header == {'s3'}, (
        f"Expected only 's3' to target the 'Expires' header.\n"
        f"Actual services that target the 'Expires' header: {services_that_target_expires_header}\n"
        f"Please review the service models to verify this change."
    )


def _shape_targets_expires_header(shape):
    for member_shape in shape.members.values():
        location = member_shape.serialization.get('location')
        location_name = member_shape.serialization.get('name')
        if (
            location
            and location.lower() == 'header'
            and location_name
            and location_name.lower() == 'expires'
        ):
            return True
    return False
