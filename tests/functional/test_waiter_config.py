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
from nose.tools import assert_equals

import botocore.session


def test_lint_waiter_configs():
    session = botocore.session.get_session()
    for service_name in session.get_available_services():
        client = session.create_client(service_name, 'us-east-1')
        service_model = client.meta.service_model
        for waiter_name in client.waiter_names:
            waiter = client.get_waiter(waiter_name)
            yield _lint_single_waiter, waiter, service_model


def _lint_single_waiter(waiter, service_model):
    operation_name = waiter.config.operation
    # Needs to reference an existing operation name.
    if operation_name not in service_model.operation_names:
        raise AssertionError("Waiter config references unknown "
                             "operation: %s" % operation_name)
    # Needs to have at least one acceptor.
    if not waiter.config.acceptors:
        raise AssertionError("Waiter config must have at least "
                             "one acceptor state: %s" % waiter.name)
    # Additional things to add:
    # 1. Verify the error acceptors correspond to a 'code' in the model
    # 2. Verify JMESPath expressions can resolve to something in
    #    the response.

