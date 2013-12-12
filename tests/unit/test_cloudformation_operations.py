#!/usr/bin/env python
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
import unittest
import base64
import six
import botocore.session


class TestCloudformationOperations(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
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
