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


class TestCloudformationOperations(BaseSessionTest):

    def setUp(self):
        super(TestCloudformationOperations, self).setUp()
        self.cf = self.session.get_service('cloudformation')

    def test_create_stack(self):
        op = self.cf.get_operation('CreateStack')
        params = op.build_parameters(stack_name='foobar',
                                     template_url='http://foo.com/bar.json',
                                     stack_policy_url='http://fie.com/baz.json')
        result = {'StackName': 'foobar',
                  'TemplateURL': 'http://foo.com/bar.json',
                  'StackPolicyURL': 'http://fie.com/baz.json'}
        self.assertEqual(params, result)

    def test_update_stack(self):
        op = self.cf.get_operation('UpdateStack')
        params = op.build_parameters(stack_name='foobar',
                                     template_url='http://foo.com/bar.json',
                                     stack_policy_url='http://fie.com/baz.json')
        result = {'StackName': 'foobar',
                  'TemplateURL': 'http://foo.com/bar.json',
                  'StackPolicyURL': 'http://fie.com/baz.json'}
        self.assertEqual(params, result)


if __name__ == "__main__":
    unittest.main()
