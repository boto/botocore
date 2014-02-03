#!/usr/bin/env
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

from tests import unittest
import botocore.parameters
import botocore.payload
from botocore.compat import json

XML_BODY1 = """<foobar xmlns="http://foobar.com/"><foo>value1</foo><bar>value2</bar></foobar>"""
XML_BODY2 = """<foo>value1</foo>"""


class TestPayloads(unittest.TestCase):

    def test_json_payload_scalar(self):
        payload = botocore.payload.JSONPayload()
        p = botocore.parameters.StringParameter(None, name='foo')
        payload.add_param(p, 'value1')
        p = botocore.parameters.StringParameter(None, name='bar')
        payload.add_param(p, 'value2')
        json_body = json.loads(payload.getvalue())
        params = {"foo": "value1", "bar": "value2"}
        self.assertEqual(json_body, params)

    def test_json_payload_list(self):
        payload = botocore.payload.JSONPayload()
        p = botocore.parameters.ListParameter(None, name='foo',
                                              members={'type': 'string'})
        value = ['This', 'is', 'a', 'test']
        payload.add_param(p, value)
        json_body = json.loads(payload.getvalue())
        params = {"foo": ["This", "is", "a", "test"]}
        self.assertEqual(json_body, params)

    def test_xml_payload_scalar(self):
        payload = botocore.payload.XMLPayload(root_element_name='foobar',
                                              namespace='http://foobar.com/')
        p = botocore.parameters.StringParameter(None, name='foo')
        payload.add_param(p, 'value1')
        p = botocore.parameters.StringParameter(None, name='bar')
        payload.add_param(p, 'value2')
        xml_body = payload.getvalue()
        self.assertEqual(xml_body, XML_BODY1)

    def test_xml_payload_scalar_no_root(self):
        payload = botocore.payload.XMLPayload(root_element_name=None)
        p = botocore.parameters.StringParameter(None, name='foo')
        payload.add_param(p, 'value1')
        p = botocore.parameters.StringParameter(None, name='bar')
        payload.add_param(p, 'value2')
        xml_body = payload.getvalue()
        self.assertEqual(xml_body, XML_BODY2)


if __name__ == "__main__":
    unittest.main()
