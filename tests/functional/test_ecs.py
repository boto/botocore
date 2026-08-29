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
import botocore.session
from botocore.stub import Stubber


def _create_ecs_client():
    session = botocore.session.get_session()
    return session.create_client('ecs', region_name='us-east-1')


def test_services_stable_waiter_with_missing_deployments():
    """ServicesStable waiter should not raise when deployments key is absent.

    When a service is deployed using CodeDeploy Blue/Green, the
    DescribeServices response may not include a ``deployments`` field.
    The waiter must handle this gracefully instead of raising a
    JMESPathTypeError.
    """
    client = _create_ecs_client()
    stubber = Stubber(client)

    # First response: service without deployments key — the waiter should
    # treat this as "not yet stable" and retry rather than crashing.
    response_missing_deployments = {
        'services': [
            {
                'serviceName': 'my-service',
                'clusterArn': 'arn:aws:ecs:us-east-1:123456789012:cluster/my-cluster',
                'serviceArn': 'arn:aws:ecs:us-east-1:123456789012:service/my-cluster/my-service',
                'status': 'ACTIVE',
                'desiredCount': 1,
                'runningCount': 1,
                'launchType': 'FARGATE',
            }
        ],
        'failures': [],
    }

    # Second response: service with a single deployment and matching counts —
    # this should satisfy the waiter's success condition.
    response_stable = {
        'services': [
            {
                'serviceName': 'my-service',
                'clusterArn': 'arn:aws:ecs:us-east-1:123456789012:cluster/my-cluster',
                'serviceArn': 'arn:aws:ecs:us-east-1:123456789012:service/my-cluster/my-service',
                'status': 'ACTIVE',
                'desiredCount': 1,
                'runningCount': 1,
                'deployments': [
                    {
                        'id': 'ecs-svc/1234567890123456789',
                        'status': 'PRIMARY',
                        'desiredCount': 1,
                        'runningCount': 1,
                    }
                ],
                'launchType': 'FARGATE',
            }
        ],
        'failures': [],
    }

    expected_params = {
        'cluster': 'my-cluster',
        'services': ['my-service'],
    }

    stubber.add_response('describe_services', response_missing_deployments, expected_params)
    stubber.add_response('describe_services', response_stable, expected_params)

    waiter = client.get_waiter('services_stable')
    waiter.config.delay = 0  # No delay for tests

    with stubber:
        # This should not raise a JMESPathTypeError
        waiter.wait(
            cluster='my-cluster',
            services=['my-service'],
        )


def test_services_stable_waiter_with_deployments_present():
    """ServicesStable waiter succeeds when deployments is present and stable."""
    client = _create_ecs_client()
    stubber = Stubber(client)

    response_stable = {
        'services': [
            {
                'serviceName': 'my-service',
                'clusterArn': 'arn:aws:ecs:us-east-1:123456789012:cluster/my-cluster',
                'serviceArn': 'arn:aws:ecs:us-east-1:123456789012:service/my-cluster/my-service',
                'status': 'ACTIVE',
                'desiredCount': 2,
                'runningCount': 2,
                'deployments': [
                    {
                        'id': 'ecs-svc/1234567890123456789',
                        'status': 'PRIMARY',
                        'desiredCount': 2,
                        'runningCount': 2,
                    }
                ],
                'launchType': 'FARGATE',
            }
        ],
        'failures': [],
    }

    expected_params = {
        'cluster': 'my-cluster',
        'services': ['my-service'],
    }

    stubber.add_response('describe_services', response_stable, expected_params)

    waiter = client.get_waiter('services_stable')
    waiter.config.delay = 0

    with stubber:
        waiter.wait(
            cluster='my-cluster',
            services=['my-service'],
        )
