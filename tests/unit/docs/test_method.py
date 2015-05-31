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
from tests import unittest
from tests.unit.docs import BaseDocsTest
from botocore.docs.method import document_model_driven_signature
from botocore.docs.method import document_custom_signature
from botocore.docs.method import document_model_driven_method
from botocore.docs.method import get_instance_public_methods
from botocore.docs.utils import DocumentedShape


class TestGetInstanceMethods(unittest.TestCase):
    class MySampleClass(object):
        def _internal_method(self):
            pass

        def public_method(self):
            pass

    def test_get_instance_methods(self):
        instance = self.MySampleClass()
        instance_methods = get_instance_public_methods(instance)
        self.assertEqual(len(instance_methods), 1)
        self.assertIn('public_method', instance_methods)
        self.assertEqual(
            instance.public_method, instance_methods['public_method'])


class TestDocumentModelDrivenSignature(BaseDocsTest):
    def setUp(self):
        super(TestDocumentModelDrivenSignature, self).setUp()
        self.add_shape_to_params('Foo', 'String')
        self.add_shape_to_params('Bar', 'String', is_required=True)
        self.add_shape_to_params('Baz', 'String')

    def test_document_signature(self):
        document_model_driven_signature(
            self.doc_structure, 'my_method', self.operation_model)
        self.assert_contains_line(
            '.. py:method:: my_method(Bar=None, Foo=None, Baz=None)')

    def test_document_signature_include(self):
        include_params = [
            DocumentedShape(
                name='Biz', type_name='integer', documentation='biz docs')
        ]
        document_model_driven_signature(
            self.doc_structure, 'my_method', self.operation_model,
            include=include_params)
        self.assert_contains_line(
            '.. py:method:: my_method(Bar=None, Foo=None, Baz=None, Biz=None)')

    def test_document_signature_exclude(self):
        exclude_params = ['Baz']
        document_model_driven_signature(
            self.doc_structure, 'my_method', self.operation_model,
            exclude=exclude_params)
        self.assert_contains_line(
            '.. py:method:: my_method(Bar=None, Foo=None)')


class TestDocumentCustomSignature(BaseDocsTest):
    def sample_method(self, foo, bar='bar', baz=None):
        pass

    def test_document_signature(self):
        document_custom_signature(
            self.doc_structure, 'my_method', self.sample_method)
        self.assert_contains_line(
            '.. py:method:: my_method(foo, bar=\'bar\', baz=None)')


class TestDocumentModelDrivenMethod(BaseDocsTest):
    def setUp(self):
        super(TestDocumentModelDrivenMethod, self).setUp()
        self.add_shape_to_params('Bar', 'String')

    def test_default(self):
        document_model_driven_method(
            self.doc_structure, 'foo', self.operation_model,
            method_description='This describes the foo method.',
            example_prefix='response = client.foo'
        )
        self.assert_contains_lines([
            '.. py:method:: foo(Bar=None)',
            '  This describes the foo method.',
            '  **Example**',
            '  ::',
            '    response = client.foo(',
            '        Bar=\'string\'',
            '    )',
            '  :type Bar: string',
            '  :param Bar:',
            '  :rtype: dict',
            '  :returns:',
            '    **Response Example**',
            '    ::',
            '      {',
            '          \'Bar\': \'string\'',
            '      }',
            '    **Response Structure**',
            '    - *(dict) --*',
            '      - **Bar** *(string) --*'
        ])

    def test_no_input_output_shape(self):
        del self.json_model['operations']['SampleOperation']['input']
        del self.json_model['operations']['SampleOperation']['output']
        document_model_driven_method(
            self.doc_structure, 'foo', self.operation_model,
            method_description='This describes the foo method.',
            example_prefix='response = client.foo'
        )
        self.assert_contains_lines([
            '.. py:method:: foo()',
            '  This describes the foo method.',
            '  **Example**',
            '  ::',
            '    response = client.foo()',
            '  :returns: None',
        ])

    def test_include_input(self):
        include_params = [
            DocumentedShape(
                name='Biz', type_name='string', documentation='biz docs')
        ]
        document_model_driven_method(
            self.doc_structure, 'foo', self.operation_model,
            method_description='This describes the foo method.',
            example_prefix='response = client.foo',
            include_input=include_params
        )
        self.assert_contains_lines([
            '.. py:method:: foo(Bar=None, Biz=None)',
            '  This describes the foo method.',
            '  **Example**',
            '  ::',
            '    response = client.foo(',
            '        Bar=\'string\',',
            '        Biz=\'string\'',
            '    )',
            '  :type Bar: string',
            '  :param Bar:',
            '  :type Biz: string',
            '  :param Biz: biz docs',
            '  :rtype: dict',
            '  :returns:',
            '    **Response Example**',
            '    ::',
            '      {',
            '          \'Bar\': \'string\'',
            '      }',
            '    **Response Structure**',
            '    - *(dict) --*',
            '      - **Bar** *(string) --*'
        ])

    def test_include_output(self):
        include_params = [
            DocumentedShape(
                name='Biz', type_name='string', documentation='biz docs')
        ]
        document_model_driven_method(
            self.doc_structure, 'foo', self.operation_model,
            method_description='This describes the foo method.',
            example_prefix='response = client.foo',
            include_output=include_params
        )
        self.assert_contains_lines([
            '.. py:method:: foo(Bar=None)',
            '  This describes the foo method.',
            '  **Example**',
            '  ::',
            '    response = client.foo(',
            '        Bar=\'string\'',
            '    )',
            '  :type Bar: string',
            '  :param Bar:',
            '  :rtype: dict',
            '  :returns:',
            '    **Response Example**',
            '    ::',
            '      {',
            '          \'Bar\': \'string\'',
            '          \'Biz\': \'string\'',
            '      }',
            '    **Response Structure**',
            '    - *(dict) --*',
            '      - **Bar** *(string) --*',
            '      - **Biz** *(string) --*'
        ])

    def test_exclude_input(self):
        self.add_shape_to_params('Biz', 'String')
        document_model_driven_method(
            self.doc_structure, 'foo', self.operation_model,
            method_description='This describes the foo method.',
            example_prefix='response = client.foo',
            exclude_input=['Bar']
        )
        self.assert_contains_lines([
            '.. py:method:: foo(Biz=None)',
            '  This describes the foo method.',
            '  **Example**',
            '  ::',
            '    response = client.foo(',
            '        Biz=\'string\'',
            '    )',
            '  :type Biz: string',
            '  :param Biz:',
            '  :rtype: dict',
            '  :returns:',
            '    **Response Example**',
            '    ::',
            '      {',
            '          \'Bar\': \'string\'',
            '          \'Biz\': \'string\'',
            '      }',
            '    **Response Structure**',
            '    - *(dict) --*',
            '      - **Bar** *(string) --*',
            '      - **Biz** *(string) --*'
        ])
        self.assert_not_contains_lines([
            ':param Bar: string',
            'Bar=\'string\''
        ])

    def test_exclude_output(self):
        self.add_shape_to_params('Biz', 'String')
        document_model_driven_method(
            self.doc_structure, 'foo', self.operation_model,
            method_description='This describes the foo method.',
            example_prefix='response = client.foo',
            exclude_output=['Bar']
        )
        self.assert_contains_lines([
            '.. py:method:: foo(Bar=None, Biz=None)',
            '  This describes the foo method.',
            '  **Example**',
            '  ::',
            '    response = client.foo(',
            '        Bar=\'string\'',
            '        Biz=\'string\'',
            '    )',
            '  :type Biz: string',
            '  :param Biz:',
            '  :rtype: dict',
            '  :returns:',
            '    **Response Example**',
            '    ::',
            '      {',
            '          \'Biz\': \'string\'',
            '      }',
            '    **Response Structure**',
            '    - *(dict) --*',
            '      - **Biz** *(string) --*'
        ])
        self.assert_not_contains_lines([
            '\'Bar\': \'string\'',
            '- **Bar** *(string) --*',
        ])
