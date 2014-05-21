#!/usr/bin/env python
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
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
from tests import BaseSessionTest


attributes = {
    "MysqlRootPasswordUbiquitous": None,
    "RubygemsVersion": "1.8.24",
    "RailsStack": "apache_passenger",
    "HaproxyHealthCheckMethod": None,
    "RubyVersion": "1.9.3",
    "BundlerVersion": "1.2.3",
    "HaproxyStatsPassword": None,
    "PassengerVersion": "3.0.17",
    "MemcachedMemory": None,
    "EnableHaproxyStats": None,
    "ManageBundler": "true",
    "NodejsVersion": None,
    "HaproxyHealthCheckUrl": None,
    "MysqlRootPassword": None,
    "GangliaPassword": None,
    "GangliaUser": None,
    "HaproxyStatsUrl": None,
    "GangliaUrl": None,
    "HaproxyStatsUser": None
}

class TestOpsworksOperations(BaseSessionTest):

    def setUp(self):
        super(TestOpsworksOperations, self).setUp()
        self.environ['BOTO_DATA_PATH'] = '~/.aws_data'
        self.opsworks = self.session.get_service('opsworks')
        self.stack_id = '35959772-cd1e-4082-8346-79096d4179f2'

    def test_describe_layers(self):
        op = self.opsworks.get_operation('DescribeLayers')
        params = op.build_parameters(stack_id=self.stack_id,
                                     layer_ids=['3e9a9949-a85e-4687-bf95-25c5dab11205'])
        result = {'StackId': self.stack_id,
                  'LayerIds': ['3e9a9949-a85e-4687-bf95-25c5dab11205']}
        self.assertEqual(params, result)

    def test_create_layers(self):
        op = self.opsworks.get_operation('CreateLayer')
        params = op.build_parameters(name='Test CLI',
                                     stack_id=self.stack_id,
                                     auto_assign_elastic_ips=True,
                                     attributes=attributes,
                                     type='rails-app',
                                     shortname='a')
        result = {'StackId': self.stack_id,
                  'Name': 'Test CLI',
                  'AutoAssignElasticIps': True,
                  'Attributes': attributes,
                  'Type': 'rails-app',
                  'Shortname': 'a'}
        self.maxDiff = None
        self.assertEqual(params, result)
