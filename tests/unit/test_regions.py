# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from tests import unittest

from botocore import regions
from botocore.exceptions import UnknownEndpointError


class TestEndpointHeuristics(unittest.TestCase):

    def create_endpoint_resolver(self, rules):
        return regions.EndpointResolver(rules)

    def test_matches_exact_rule(self):
        resolver = self.create_endpoint_resolver({
            'iam': [
                {'uri': 'https://{service}.us-gov.amazonaws.com',
                 'constraints': [['region', 'startsWith', 'us-gov']]}
            ]
        })
        endpoint = resolver.construct_endpoint(
            service_name='iam', region_name='us-gov-1')
        self.assertEqual(endpoint['uri'], 'https://iam.us-gov.amazonaws.com')
        self.assertEqual(endpoint['properties'], {})

    def test_no_match_throws_exception(self):
        resolver = self.create_endpoint_resolver({
            'iam': [
                {'uri': 'https://{service}.us-gov.amazonaws.com',
                 'constraints': [['region', 'startsWith', 'us-gov']]}
            ]
        })
        with self.assertRaises(UnknownEndpointError):
            resolver.construct_endpoint(service_name='iam',
                                        region_name='not-us-gov-2')

    def test_use_default_section_if_no_service_name(self):
        resolver = self.create_endpoint_resolver({
            '_default': [
                {'uri': 'https://{service}.us-gov.amazonaws.com',
                 'constraints': [['region', 'startsWith', 'us-gov']]}
            ]
        })
        self.assertEqual(
            resolver.construct_endpoint(service_name='iam',
                                        region_name='us-gov-1')['uri'],
            'https://iam.us-gov.amazonaws.com')

    def test_use_default_section_if_no_service_rule_matches(self):
        resolver = self.create_endpoint_resolver({
            '_default': [
                {"uri":"{scheme}://{service}.{region}.amazonaws.com",
                 "constraints": [
                    ["region", "notEquals", None]
                ]}
            ],
            'iam': [
                {'uri': 'https://{service}.us-gov.amazonaws.com',
                 'constraints': [['region', 'startsWith', 'us-gov']]}
            ]
        })
        self.assertEqual(
            resolver.construct_endpoint(service_name='iam',
                                        region_name='other-region')['uri'],
            'https://iam.other-region.amazonaws.com')

    def test_matches_last_rule(self):
        resolver = self.create_endpoint_resolver({
            "s3":[
                {
                    "uri":"{scheme}://s3.amazonaws.com",
                    "constraints":[
                        ["region", "oneOf", ["us-east-1", None]]
                    ]
                },
                {
                    "uri":"{scheme}://{service}-{region}.amazonaws.com.cn",
                    "constraints":[
                        ["region", "startsWith", "cn-"]
                    ]
                },
                {
                    "uri":"{scheme}://{service}-{region}.amazonaws.com",
                    "constraints": [
                        ["region", "notEquals", None]
                    ]
                }
            ],
        })
        self.assertEqual(
            resolver.construct_endpoint(service_name='s3',
                                        region_name='us-east-1')['uri'],
            'https://s3.amazonaws.com')
        self.assertEqual(
            resolver.construct_endpoint(service_name='s3',
                                        region_name=None)['uri'],
            'https://s3.amazonaws.com')
        self.assertEqual(
            resolver.construct_endpoint(service_name='s3',
                                        region_name='us-west-2')['uri'],
            'https://s3-us-west-2.amazonaws.com')
        self.assertEqual(
            resolver.construct_endpoint(service_name='s3',
                                        region_name='cn-north-1')['uri'],
            'https://s3-cn-north-1.amazonaws.com.cn')

    def test_not_starts_with(self):
        resolver = self.create_endpoint_resolver({
            'iam': [
                {'uri': 'https://route53.amazonaws.com',
                 'constraints': [['region', 'notStartsWith', 'cn-']]}
            ]
        })
        self.assertEqual(
            resolver.construct_endpoint(service_name='iam',
                                        region_name='us-east-1')['uri'],
            'https://route53.amazonaws.com')

    def test_can_add_rule(self):
        # This shows how a customer could add their own rules.
        resolver = self.create_endpoint_resolver({
            'iam': [
                {'uri': 'https://{service}.us-gov.amazonaws.com',
                 'constraints': [['region', 'startsWith', 'us-gov']]}
            ]
        })
        resolver.get_rules_for_service('iam').insert(
            0, {'uri': 'https://my.custom.location',
                'constraints': [['region', 'equals', 'custom-region']]})
        self.assertEqual(
            resolver.construct_endpoint(service_name='iam',
                                        region_name='custom-region')['uri'],
            'https://my.custom.location')

    def test_property_bags_returned(self):
        resolver = self.create_endpoint_resolver({
            'iam': [
                {'uri': 'https://{service}.us-gov.amazonaws.com',
                 'constraints': [['region', 'startsWith', 'us-gov']],
                 'properties': {
                     'credentialScope': {
                         'region': 'us-east-1'
                     }
                 }}
            ]
        })
        endpoint = resolver.construct_endpoint(
            service_name='iam', region_name='us-gov-1')
        self.assertEqual(endpoint['properties'],
                         {'credentialScope': {'region': 'us-east-1'}})
