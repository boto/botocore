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
from botocore.docs.utils import py_type_name
from botocore.docs.utils import py_default
from botocore.docs.utils import get_official_service_name
from botocore.docs.utils import get_instance_methods
from botocore.docs.utils import ModelDrivenMethodSignatureDocumentor
from botocore.docs.utils import CustomMethodSignatureDocumentor
from botocore.docs.utils import RequestParamsDocumentor
from botocore.docs.utils import ResponseParamsDocumentor
from botocore.docs.utils import ResponseExampleDocumentor
from botocore.docs.utils import RequestExampleDocumentor
from botocore.docs.utils import ModelDrivenMethodDocumentor
from botocore.docs.utils import DocumentedShape


class TestPythonTypeName(unittest.TestCase):
    def test_structure(self):
        self.assertEqual('dict', py_type_name('structure'))

    def test_list(self):
        self.assertEqual('list', py_type_name('list'))

    def test_map(self):
        self.assertEqual('dict', py_type_name('map'))

    def test_string(self):
        self.assertEqual('string', py_type_name('string'))

    def test_character(self):
        self.assertEqual('string', py_type_name('character'))

    def test_blob(self):
        self.assertEqual('bytes', py_type_name('blob'))

    def test_timestamp(self):
        self.assertEqual('datetime', py_type_name('timestamp'))

    def test_integer(self):
        self.assertEqual('integer', py_type_name('integer'))

    def test_long(self):
        self.assertEqual('integer', py_type_name('long'))

    def test_float(self):
        self.assertEqual('float', py_type_name('float'))

    def test_double(self):
        self.assertEqual('float', py_type_name('double'))


class TestPythonDefault(unittest.TestCase):
    def test_structure(self):
        self.assertEqual('{...}', py_default('structure'))

    def test_list(self):
        self.assertEqual('[...]', py_default('list'))

    def test_map(self):
        self.assertEqual('{...}', py_default('map'))

    def test_string(self):
        self.assertEqual('\'string\'', py_default('string'))

    def test_blob(self):
        self.assertEqual('b\'bytes\'', py_default('blob'))

    def test_timestamp(self):
        self.assertEqual('datetime(2015, 1, 1)', py_default('timestamp'))

    def test_integer(self):
        self.assertEqual('123', py_default('integer'))

    def test_long(self):
        self.assertEqual('123', py_default('long'))

    def test_double(self):
        self.assertEqual('123.0', py_default('double'))


class TestGetOfficialServiceName(BaseDocsTest):
    def setUp(self):
        super(TestGetOfficialServiceName, self).setUp()
        self.service_model.metadata = {
            'serviceFullName': 'Official Name'
        }

    def test_no_short_name(self):
        self.assertEqual('Official Name',
                         get_official_service_name(self.service_model))

    def test_aws_short_name(self):
        self.service_model.metadata['serviceAbbreviation'] = 'AWS Foo'
        self.assertEqual('Official Name (Foo)',
                         get_official_service_name(self.service_model))

    def test_amazon_short_name(self):
        self.service_model.metadata['serviceAbbreviation'] = 'Amazon Foo'
        self.assertEqual('Official Name (Foo)',
                         get_official_service_name(self.service_model))

    def test_short_name_in_official_name(self):
        self.service_model.metadata['serviceFullName'] = 'The Foo Service'
        self.service_model.metadata['serviceAbbreviation'] = 'Amazon Foo'
        self.assertEqual('The Foo Service',
                         get_official_service_name(self.service_model))


class TestGetInstanceMethods(unittest.TestCase):
    class MySampleClass(object):
        def _internal_method(self):
            pass

        def public_method(self):
            pass

    def test_get_instance_methods(self):
        instance = self.MySampleClass()
        instance_methods = get_instance_methods(instance)
        self.assertEqual(len(instance_methods), 1)
        self.assertIn('public_method', instance_methods)
        self.assertEqual(
            instance.public_method, instance_methods['public_method'])


class TestModelDrivenMethodSignatureDocumentor(BaseDocsTest):
    def setUp(self):
        super(TestModelDrivenMethodSignatureDocumentor, self).setUp()
        self.sig_documentor = ModelDrivenMethodSignatureDocumentor()
        self.add_shape_to_params('Foo', 'String')
        self.add_shape_to_params('Bar', 'String', is_required=True)
        self.add_shape_to_params('Baz', 'String')

    def test_document_signature(self):
        self.sig_documentor.document_signature(
            self.doc_structure, 'my_method', self.operation_model)
        self.assert_contains_line(
            '.. py:method:: my_method(Bar=None, Baz=None, Foo=None)')

    def test_document_signature_include(self):
        include_params = [
            DocumentedShape(
                name='Biz', type_name='integer', documentation='biz docs')
        ]
        self.sig_documentor.document_signature(
            self.doc_structure, 'my_method', self.operation_model,
            include=include_params)
        self.assert_contains_line(
            '.. py:method:: my_method(Bar=None, Baz=None, Foo=None, Biz=None)')

    def test_document_signature_exclude(self):
        exclude_params = ['Baz']
        self.sig_documentor.document_signature(
            self.doc_structure, 'my_method', self.operation_model,
            exclude=exclude_params)
        self.assert_contains_line(
            '.. py:method:: my_method(Bar=None, Foo=None)')


class TestCustomMethodSignatureDocumentor(BaseDocsTest):
    def setUp(self):
        super(TestCustomMethodSignatureDocumentor, self).setUp()
        self.sig_documentor = CustomMethodSignatureDocumentor()

    def sample_method(self, foo, bar='bar', baz=None):
        pass

    def test_document_signature(self):
        self.sig_documentor.document_signature(
            self.doc_structure, 'my_method', self.sample_method)
        self.assert_contains_line(
            '.. py:method:: my_method(foo, bar=\'bar\', baz=None)')


class BaseUtilsDocumentorTest(BaseDocsTest):
    def setUp(self):
        super(BaseUtilsDocumentorTest, self).setUp()
        self.request_params = RequestParamsDocumentor()
        self.response_params = ResponseParamsDocumentor()
        self.request_example = RequestExampleDocumentor()
        self.response_example = ResponseExampleDocumentor()


class TestDocumentDefaultValue(BaseUtilsDocumentorTest):
    def setUp(self):
        super(TestDocumentDefaultValue, self).setUp()
        self.add_shape_to_params('Foo', 'String', 'This describes foo.')

    def test_request_params(self):
        self.request_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            ':type Foo: string',
            ':param Foo: This describes foo.'
        ])

    def test_response_params(self):
        self.response_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            '- *(dict) --*',
            '  - **Foo** *(string) --* This describes foo.'
        ])

    def test_request_example(self):
        self.request_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
            prefix='response = myclient.call'
        )
        self.assert_contains_lines([
            '::',
            '  response = myclient.call(',
            '      Foo=\'string\'',
            '  )'
        ])

    def test_response_example(self):
        self.response_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
        )
        self.assert_contains_lines([
            '::',
            '  {',
            '      \'Foo\': \'string\'',
            '  }'
        ])


class TestDocumentMultipleDefaultValues(BaseUtilsDocumentorTest):
    def setUp(self):
        super(TestDocumentMultipleDefaultValues, self).setUp()
        self.add_shape_to_params('Foo', 'String', 'This describes foo.')
        self.add_shape_to_params('Bar', 'String', 'This describes bar.',
                                 is_required=True)

    def test_request_params(self):
        self.request_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            ':type Foo: string',
            ':param Foo: This describes foo.',
            ':type Bar: string',
            ':param Bar: **[REQUIRED]** This describes bar.'
        ])

    def test_response_params(self):
        self.response_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            '- *(dict) --*',
            '  - **Foo** *(string) --* This describes foo.',
            '  - **Bar** *(string) --* This describes bar.'
        ])

    def test_request_example(self):
        self.request_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
            prefix='response = myclient.call'
        )
        self.assert_contains_lines([
            '::',
            '  response = myclient.call(',
            '      Foo=\'string\',',
            '      Bar=\'string\'',
            '  )'
        ])

    def test_response_example(self):
        self.response_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
        )
        self.assert_contains_lines([
            '::',
            '  {',
            '      \'Foo\': \'string\',',
            '      \'Bar\': \'string\'',
            '  }'
        ])


class TestDocumentInclude(BaseUtilsDocumentorTest):
    def setUp(self):
        super(TestDocumentInclude, self).setUp()
        self.add_shape_to_params('Foo', 'String', 'This describes foo.')
        self.include_params = [
            DocumentedShape(
                name='Baz', type_name='integer',
                documentation='This describes baz.'
            )
        ]

    def test_request_params(self):
        self.request_params.document_params(
            self.doc_structure, self.operation_model.input_shape,
            include=self.include_params
        )
        self.assert_contains_lines([
            ':type Foo: string',
            ':param Foo: This describes foo.',
            ':type Baz: int',
            ':param Baz: This describes baz.'
        ])

    def test_response_params(self):
        self.response_params.document_params(
            self.doc_structure, self.operation_model.input_shape,
            include=self.include_params
        )
        self.assert_contains_lines([
            '- *(dict) --*',
            '  - **Foo** *(string) --* This describes foo.',
            '  - **Baz** *(integer) --* This describes baz.'
        ])

    def test_request_example(self):
        self.request_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
            prefix='response = myclient.call',
            include=self.include_params
        )
        self.assert_contains_lines([
            '::',
            '  response = myclient.call(',
            '      Foo=\'string\',',
            '      Baz=123',
            '  )'
        ])

    def test_response_example(self):
        self.response_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
            include=self.include_params
        )
        self.assert_contains_lines([
            '::',
            '  {',
            '      \'Foo\': \'string\',',
            '      \'Baz\': 123',
            '  }'
        ])


class TestDocumentExclude(BaseUtilsDocumentorTest):
    def setUp(self):
        super(TestDocumentExclude, self).setUp()
        self.add_shape_to_params('Foo', 'String', 'This describes foo.')
        self.add_shape_to_params('Bar', 'String', 'This describes bar.',
                                 is_required=True)
        self.exclude_params = ['Foo']

    def test_request_params(self):
        self.request_params.document_params(
            self.doc_structure, self.operation_model.input_shape,
            exclude=self.exclude_params)
        self.assert_contains_lines([
            ':type Bar: string',
            ':param Bar: **[REQUIRED]** This describes bar.'
        ])
        self.assert_not_contains_lines([
            ':type Foo: string',
            ':param Foo: This describes foo.'
        ])

    def test_response_params(self):
        self.response_params.document_params(
            self.doc_structure, self.operation_model.input_shape,
            exclude=self.exclude_params)
        self.assert_contains_lines([
            '- *(dict) --*',
            '  - **Bar** *(string) --* This describes bar.'
        ])
        self.assert_not_contains_line(
            '  - **Foo** *(string) --* This describes foo.')

    def test_request_example(self):
        self.request_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
            prefix='response = myclient.call',
            exclude=self.exclude_params
        )
        self.assert_contains_lines([
            '::',
            '  response = myclient.call(',
            '      Bar=\'string\'',
            '  )'
        ])
        self.assert_not_contains_line('      Foo=\'string\'')

    def test_response_example(self):
        self.response_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
            exclude=self.exclude_params
        )
        self.assert_contains_lines([
            '::',
            '  {',
            '      \'Bar\': \'string\'',
            '  }'
        ])
        self.assert_not_contains_line('\'Foo\': \'string\',')


class TestDocumentList(BaseUtilsDocumentorTest):
    def setUp(self):
        super(TestDocumentList, self).setUp()
        self.add_shape(
            {'List': {
                'type': 'list',
                'member': {'shape': 'String',
                           'documentation': 'A string element'}}})
        self.add_shape_to_params('Foo', 'List', 'This describes the list.')

    def test_request_params(self):
        self.request_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            ':type Foo: list',
            ':param Foo: This describes the list.',
            '  - *(string) --* A string element'
        ])

    def test_response_params(self):
        self.response_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            '- *(dict) --*',
            '  - **Foo** *(list) --* This describes the list.',
            '    - *(string) --* A string element'
        ])

    def test_request_example(self):
        self.request_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
            prefix='response = myclient.call')
        self.assert_contains_lines([
            '::',
            '  response = myclient.call(',
            '      Foo=[',
            '          \'string\',',
            '      ]',
            '  )'
        ])

    def test_response_example(self):
        self.response_example.document_example(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            '::',
            '  {',
            '      \'Foo\': [',
            '          \'string\',',
            '      ]',
            '  }'
        ])


class TestDocumentMap(BaseUtilsDocumentorTest):
    def setUp(self):
        super(TestDocumentMap, self).setUp()
        self.add_shape(
            {'Map': {
                'type': 'map',
                'key': {'shape': 'String'},
                'value': {'shape': 'String'}}})
        self.add_shape_to_params('Foo', 'Map', 'This describes the map.')

    def test_request_params(self):
        self.request_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            ':type Foo: dict',
            ':param Foo: This describes the map.',
            '  - *(string) --*',
            '    - *(string) --*'
        ])

    def test_response_params(self):
        self.response_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            '- *(dict) --*',
            '  - **Foo** *(dict) --* This describes the map.',
            '    - *(string) --*',
            '      - *(string) --*'
        ])

    def test_request_example(self):
        self.request_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
            prefix='response = myclient.call')
        self.assert_contains_lines([
            '::',
            '  response = myclient.call(',
            '      Foo={',
            '          \'string\': \'string\'',
            '      }',
            '  )'
        ])

    def test_response_example(self):
        self.response_example.document_example(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            '::',
            '  {',
            '      \'Foo\': {',
            '          \'string\': \'string\'',
            '      }',
            '  }'
        ])


class TestDocumentStructure(BaseUtilsDocumentorTest):
    def setUp(self):
        super(TestDocumentStructure, self).setUp()
        self.add_shape(
            {'Structure': {
                'type': 'structure',
                'members': {
                    'Member': {'shape': 'String',
                               'documentation': 'This is its member.'}}}})
        self.add_shape_to_params(
            'Foo', 'Structure', 'This describes the structure.')

    def test_request_params(self):
        self.request_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            ':type Foo: dict',
            ':param Foo: This describes the structure.',
            '  - **Member** *(string) --* This is its member.'
        ])

    def test_response_params(self):
        self.response_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            '- *(dict) --*',
            '  - **Foo** *(dict) --* This describes the structure.',
            '    - **Member** *(string) --* This is its member.'
        ])

    def test_request_example(self):
        self.request_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
            prefix='response = myclient.call')
        self.assert_contains_lines([
            '::',
            '  response = myclient.call(',
            '      Foo={',
            '          \'Member\': \'string\'',
            '      }',
            '  )'
        ])

    def test_response_example(self):
        self.response_example.document_example(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            '::',
            '  {',
            '      \'Foo\': {',
            '          \'Member\': \'string\'',
            '      }',
            '  }'
        ])


class TestDocumentRecursiveShape(BaseUtilsDocumentorTest):
    def setUp(self):
        super(TestDocumentRecursiveShape, self).setUp()
        self.add_shape(
            {'Structure': {
                'type': 'structure',
                'members': {
                    'Foo': {
                        'shape': 'Structure',
                        'documentation': 'This is a recursive structure.'}}}})
        self.add_shape_to_params(
            'Foo', 'Structure', 'This describes the structure.')

    def test_request_params(self):
        self.request_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            ':type Foo: dict',
            ':param Foo: This describes the structure.',
            '  - **Foo** *(dict) --* This is a recursive structure.'
        ])

    def test_response_params(self):
        self.response_params.document_params(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            '- *(dict) --*',
            '  - **Foo** *(dict) --* This is a recursive structure.',
        ])

    def test_request_example(self):
        self.request_example.document_example(
            self.doc_structure, self.operation_model.input_shape,
            prefix='response = myclient.call')
        self.assert_contains_lines([
            '::',
            '  response = myclient.call(',
            '      Foo={',
            '          \'Foo\': {\'... recursive ...\'}',
            '      }',
            '  )'
        ])

    def test_response_example(self):
        self.response_example.document_example(
            self.doc_structure, self.operation_model.input_shape)
        self.assert_contains_lines([
            '::',
            '  {',
            '      \'Foo\': {',
            '          \'Foo\': {\'... recursive ...\'}',
            '      }',
            '  }'
        ])


class TestModelDrivenMethodDocumentor(BaseDocsTest):
    def setUp(self):
        super(TestModelDrivenMethodDocumentor, self).setUp()
        self.method_documentor = ModelDrivenMethodDocumentor()
        self.add_shape_to_params('Bar', 'String')

    def test_default(self):
        self.method_documentor.document_method(
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
        self.method_documentor.document_method(
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
        self.method_documentor.document_method(
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
        self.method_documentor.document_method(
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
        self.method_documentor.document_method(
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
        self.method_documentor.document_method(
            self.doc_structure, 'foo', self.operation_model,
            method_description='This describes the foo method.',
            example_prefix='response = client.foo',
            exclude_output=['Bar']
        )
        self.assert_contains_lines([
            '.. py:method:: foo(Biz=None, Bar=None)',
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
