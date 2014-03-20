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

from tests import TestParamSerialization
import botocore.session


class TestCloudformationOperations(TestParamSerialization):

    def test_create_stack(self):
        result = {'StackName': 'foobar',
                  'TemplateURL': 'http://foo.com/bar.json',
                  'StackPolicyURL': 'http://fie.com/baz.json'}
        self.assert_params_serialize_to(
            'cloudformation.CreateStack',
            input_params={'StackName': 'foobar',
                          'TemplateURL': 'http://foo.com/bar.json',
                          'StackPolicyURL': 'http://fie.com/baz.json'},
            serialized_params=result)

    def test_update_stack(self):
        result = {'StackName': 'foobar',
                  'TemplateURL': 'http://foo.com/bar.json',
                  'StackPolicyURL': 'http://fie.com/baz.json'}
        self.assert_params_serialize_to(
            'cloudformation.UpdateStack',
            input_params={'StackName': 'foobar',
                          'TemplateURL': 'http://foo.com/bar.json',
                          'StackPolicyURL': 'http://fie.com/baz.json'},
            serialized_params=result)


if __name__ == "__main__":
    unittest.main()
