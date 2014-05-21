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
import botocore.session


class TestELBOperations(BaseSessionTest):

    def setUp(self):
        super(TestELBOperations, self).setUp()
        self.elb = self.session.get_service('elb')

    def test_describe_load_balancers_no_params(self):
        op = self.elb.get_operation('DescribeLoadBalancers')
        params = op.build_parameters()
        result = {}
        self.assertEqual(params, result)

    def test_describe_load_balancers_name(self):
        op = self.elb.get_operation('DescribeLoadBalancers')
        params = op.build_parameters(load_balancer_names=['foo'])
        result = {'LoadBalancerNames.member.1': 'foo'}
        self.assertEqual(params, result)

    def test_describe_load_balancers_names(self):
        op = self.elb.get_operation('DescribeLoadBalancers')
        params = op.build_parameters(load_balancer_names=['foo', 'bar'])
        result = {'LoadBalancerNames.member.1': 'foo',
                  'LoadBalancerNames.member.2': 'bar'}
        self.assertEqual(params, result)

    def test_create_load_balancer_listeners(self):
        op = self.elb.get_operation('CreateLoadBalancerListeners')
        params = op.build_parameters(listeners=[{'InstancePort':80,
                                                 'SSLCertificateId': 'foobar',
                                                 'LoadBalancerPort':81,
                                                 'Protocol':'HTTPS',
                                                 'InstanceProtocol':'HTTP'}],
                                     load_balancer_name='foobar')
        result = {'Listeners.member.1.LoadBalancerPort': '81',
                  'Listeners.member.1.InstancePort': '80',
                  'Listeners.member.1.Protocol': 'HTTPS',
                  'Listeners.member.1.InstanceProtocol': 'HTTP',
                  'Listeners.member.1.SSLCertificateId': 'foobar',
                  'LoadBalancerName': 'foobar'}
        self.assertEqual(params, result)

    def test_register_instances_with_load_balancer(self):
        op = self.elb.get_operation('RegisterInstancesWithLoadBalancer')
        params = op.build_parameters(load_balancer_name='foobar',
                                     instances=[{'InstanceId': 'i-12345678'},
                                                {'InstanceId': 'i-87654321'}])
        result = {'LoadBalancerName': 'foobar',
                  'Instances.member.1.InstanceId': 'i-12345678',
                  'Instances.member.2.InstanceId': 'i-87654321'}
        self.assertEqual(params, result)

    def test_set_lb_policies_for_backend_server(self):
        op = self.elb.get_operation('SetLoadBalancerPoliciesForBackendServer')
        params = op.build_parameters(load_balancer_name='foobar',
                                     instance_port=443,
                                     policy_names=['fie', 'baz'])
        result = {'LoadBalancerName': 'foobar',
                  'InstancePort': '443',
                  'PolicyNames.member.1': 'fie',
                  'PolicyNames.member.2': 'baz'}
        self.assertEqual(params, result)

    def test_clear_lb_policies_for_backend_server(self):
        op = self.elb.get_operation('SetLoadBalancerPoliciesForBackendServer')
        params = op.build_parameters(load_balancer_name='foobar',
                                     instance_port=443,
                                     policy_names=[])
        result = {'LoadBalancerName': 'foobar',
                  'InstancePort': '443',
                  'PolicyNames': ''}
        self.assertEqual(params, result)


if __name__ == "__main__":
    unittest.main()
