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
from tests.unit.docs import BaseDocsTest
from botocore.docs.example import ResponseExampleDocumenter
from botocore.docs.example import RequestExampleDocumenter
from botocore.docs.utils import DocumentedShape


class BaseExampleDocumenterTest(BaseDocsTest):
    def setUp(self):
        super(BaseExampleDocumenterTest, self).setUp()
        self.request_example = RequestExampleDocumenter()
        self.response_example = ResponseExampleDocumenter()


class TestDocumentDefaultValue(BaseExampleDocumenterTest):
    def setUp(self):
        super(TestDocumentDefaultValue, self).setUp()
        self.add_shape_to_params('Foo', 'String', 'This describes foo.')

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


class TestDocumentMultipleDefaultValues(BaseExampleDocumenterTest):
    def setUp(self):
        super(TestDocumentMultipleDefaultValues, self).setUp()
        self.add_shape_to_params('Foo', 'String', 'This describes foo.')
        self.add_shape_to_params('Bar', 'String', 'This describes bar.',
                                 is_required=True)

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


class TestDocumentInclude(BaseExampleDocumenterTest):
    def setUp(self):
        super(TestDocumentInclude, self).setUp()
        self.add_shape_to_params('Foo', 'String', 'This describes foo.')
        self.include_params = [
            DocumentedShape(
                name='Baz', type_name='integer',
                documentation='This describes baz.'
            )
        ]

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


class TestDocumentExclude(BaseExampleDocumenterTest):
    def setUp(self):
        super(TestDocumentExclude, self).setUp()
        self.add_shape_to_params('Foo', 'String', 'This describes foo.')
        self.add_shape_to_params('Bar', 'String', 'This describes bar.',
                                 is_required=True)
        self.exclude_params = ['Foo']

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


class TestDocumentList(BaseExampleDocumenterTest):
    def setUp(self):
        super(TestDocumentList, self).setUp()
        self.add_shape(
            {'List': {
                'type': 'list',
                'member': {'shape': 'String',
                           'documentation': 'A string element'}}})
        self.add_shape_to_params('Foo', 'List', 'This describes the list.')

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


class TestDocumentMap(BaseExampleDocumenterTest):
    def setUp(self):
        super(TestDocumentMap, self).setUp()
        self.add_shape(
            {'Map': {
                'type': 'map',
                'key': {'shape': 'String'},
                'value': {'shape': 'String'}}})
        self.add_shape_to_params('Foo', 'Map', 'This describes the map.')

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


class TestDocumentStructure(BaseExampleDocumenterTest):
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


class TestDocumentRecursiveShape(BaseExampleDocumenterTest):
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
