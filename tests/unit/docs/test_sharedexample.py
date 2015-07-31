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
from botocore.docs.sharedexample import SharedExampleBuilder, \
    document_shared_examples


class TestDocumentSharedExample(BaseDocsTest):
    def setUp(self):
        super(TestDocumentSharedExample, self).setUp()
        self._examples = [
            {
                "id": "sample-id",
                "title": "sample-title",
                "description": "Sample Description.",
                "input": {
                    "foo": "bar"
                },
                "output": {
                    "bar": "baz"
                },
                "comments": {
                    "output": {
                        "bar": "Sample Comment"
                    }
                }
            }
        ]

    def test_default(self):
        document_shared_examples(
            self.doc_structure, self.operation_model,
            'response = client.foo', self._examples)
        self.assert_contains_lines_in_order([
            "**Examples**",
            "Sample Description.",
            "::",
            "  response = client.foo(",
            "      foo='bar', ",
            "  )",
            "  print(response)",
            "Expected Output:",
            "::",
            "  {",
            "      'bar': 'baz', # Sample Comment",
            "  }"
        ])


class TestSharedExampleBuilder(BaseDocsTest):
    def test_is_input(self):
        builder = SharedExampleBuilder(
            params={'foo': 'bar'},
            operation_name='SampleOperation',
            is_input=True
        )
        example = builder.build_example_code()
        self.assertIn("(\n    foo='bar', \n)", example)

        example = builder.build_example_code(prefix='sample_operation')
        self.assertIn("sample_operation(\n    foo='bar', \n)", example)

    def test_dict_example(self):
        builder = SharedExampleBuilder(
            params={'foo': {'bar': 'baz'}},
            operation_name='SampleOperation',
            is_input=False
        )
        example = builder.build_example_code()
        self.assertIn("'foo': {\n        'bar': 'baz', \n    },", example)

    def test_list_example(self):
        builder = SharedExampleBuilder(
            params={'foo': ['bar']},
            operation_name='SampleOperation',
            is_input=False
        )
        example = builder.build_example_code()
        self.assertIn("'foo': [\n        'bar', \n    ],", example)

    def test_string_example(self):
        builder = SharedExampleBuilder(
            params={'foo': 'bar'},
            operation_name='SampleOperation',
            is_input=False
        )
        example = builder.build_example_code()
        self.assertIn("'foo': 'bar'", example)

        # test unicode string
        builder = SharedExampleBuilder(
            params={'foo': u'bar'},
            operation_name='SampleOperation',
            is_input=False
        )
        example = builder.build_example_code()
        self.assertIn("'foo': 'bar'", example)

    def test_add_comment(self):
        builder = SharedExampleBuilder(
            params={'foo': 'bar'},
            operation_name='SampleOperation',
            comments={'foo': 'baz'},
            is_input=False
        )
        example = builder.build_example_code()
        self.assertIn("'foo': 'bar'", example)
        self.assertIn("# baz", example)
