# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from nose.tools import assert_equal
from botocore.session import get_session


# Several services have names that don't match for one reason or another.
SERVICE_RENAMES = {
    'application-autoscaling': 'autoscaling',
    'appstream': 'appstream2',
    'dynamodbstreams': 'streams.dynamodb',
    'cloudwatch': 'monitoring',
    'efs': 'elasticfilesystem',
    'elb': 'elasticloadbalancing',
    'elbv2': 'elasticloadbalancing',
    'emr': 'elasticmapreduce',
    'iot-data': 'data.iot',
    'meteringmarketplace': 'metering.marketplace',
    'opsworkscm': 'opsworks-cm',
    'ses': 'email',
    'stepfunctions': 'states'
}


def test_service_name_matches_endpoint_prefix():
    # Generates tests for each service to verify that the endpoint prefix
    # matches the service name unless there is an explicit exception.
    session = get_session()
    loader = session.get_component('data_loader')

    # Load the list of available services. The names here represent what
    # will become the client names.
    services = loader.list_available_services('service-2')

    for service in services:
        yield _assert_service_name_matches_endpoint_prefix, loader, service


def _assert_service_name_matches_endpoint_prefix(loader, service_name):
    # Load the service model and grab its endpoint prefix
    service_model = loader.load_service_model(service_name, 'service-2')
    endpoint_prefix = service_model['metadata']['endpointPrefix']

    # Handle known exceptions where we have renamed the service directory
    # for one reason or another.
    expected_endpoint_prefix = SERVICE_RENAMES.get(service_name, service_name)
    assert_equal(
        endpoint_prefix, expected_endpoint_prefix,
        "Service name `%s` does not match endpoint prefix `%s`." % (
            service_name, expected_endpoint_prefix))
