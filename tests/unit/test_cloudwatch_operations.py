#!/usr/bin/env python
# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

from decimal import Decimal
from tests import TestParamSerialization

import botocore.session
from botocore.exceptions import ValidationError


class TestCloudwatchOperations(TestParamSerialization):

    def assert_is_valid_float_value(self, value):
        # We don't really care about the specific operation,
        # just that an operation that has a float param
        # can accept the specified value passed in.
        # We're using put-metric-data as the operation here.
        input_metric_data = [
            {"MetricName": "FreeMemoryBytes", "Dimensions": [],
             "Unit": "Bytes",
             "Timestamp": "2013-07-30T00:58:11.284Z",
             # The "Value" param is specified as type "float"
             # in the model.
             "Value": value}]
        serialized_params = {
            'MetricData.member.1.MetricName':
            'FreeMemoryBytes',
            'MetricData.member.1.Timestamp':
                '2013-07-30T00:58:11.284000+00:00',
            'MetricData.member.1.Unit': 'Bytes',
            'MetricData.member.1.Value': str(value),
            'Namespace': 'System/Linux'
        }
        self.assert_params_serialize_to(
            'cloudwatch.PutMetricData',
            input_params={'namespace': 'System/Linux',
                          'metric_data': input_metric_data},
            serialized_params=serialized_params)

    def test_float_validation(self):
        self.assert_is_valid_float_value(9130160128.0)

    def test_integers_allowed_for_floats(self):
        self.assert_is_valid_float_value(9130160128)

    def test_string_type_is_allowed(self):
        self.assert_is_valid_float_value("9130160128.123")

    def test_decimal_type_is_allowed(self):
        self.assert_is_valid_float_value(Decimal("9130160128.123"))

    def test_bad_float_value(self):
        bad_value = 'notafloat'
        input_metric_data = [
            {"MetricName": "FreeMemoryBytes", "Dimensions": [],
             "Unit": "Bytes",
             "Timestamp": "2013-07-30T00:58:11.284Z",
             "Value": bad_value}]
        op = self.session.get_service(
            'cloudwatch').get_operation('PutMetricData')
        with self.assertRaises(ValidationError):
            op.build_parameters(namespace='System/Linux',
                                metric_data=input_metric_data)
        # Empty dict is also a bad value for a float param.
        input_metric_data[0]['Value'] = {}
        with self.assertRaises(ValidationError):
            op.build_parameters(namespace='System/Linux',
                                metric_data=input_metric_data)
