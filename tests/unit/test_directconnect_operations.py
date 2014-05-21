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


class TestDirectconnectOperations(BaseSessionTest):

    def setUp(self):
        super(TestDirectconnectOperations, self).setUp()
        self.dc = self.session.get_service('directconnect')

    def test_create_connection(self):
        op = self.dc.get_operation('CreateConnection')
        params = op.build_parameters(connection_name='foobarconn',
                                     location='location', bandwidth='bandwidth')
        result = {'location': 'location', 'bandwidth': 'bandwidth',
                  'connectionName': 'foobarconn'}
        self.assertEqual(params, result)

    def test_describe_virtual_gateways(self):
        new_int = {'amazonAddress': 'amzaddress',
                   'customerAddress': 'custaddress',
                   'asn': 42,
                   'vlan': 43,
                   'authKey': 'my_auth_key',
                   'virtualInterfaceName': 'viname',
                   'routeFilterPrefixes': [{'cidr': '1.2.3.4/5'},
                                           {'cidr': '6.7.8.9/10'}]}
        op = self.dc.get_operation('CreatePublicVirtualInterface')
        params = op.build_parameters(connection_id='dxcon-fg5678gh',
                                     new_public_virtual_interface=new_int)
        result = {'connectionId': 'dxcon-fg5678gh',
                  'newPublicVirtualInterface': {
                      'amazonAddress': 'amzaddress',
                      'customerAddress': 'custaddress',
                      'asn': 42,
                      'vlan': 43,
                      'authKey': 'my_auth_key',
                      'virtualInterfaceName': 'viname',
                      'routeFilterPrefixes': [{'cidr': '1.2.3.4/5'},
                                              {'cidr': '6.7.8.9/10'}]}}
        self.maxDiff = None
        self.assertEqual(params, result)
