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
from botocore.docs.codeexamples import CodeExamplesDocumenter
from botocore.compat import json
from tests.unit.docs import BaseDocsTest
from tests import mock


class TestCodeExamplesDocumenter(BaseDocsTest):
    def setUp(self):
        super().setUp()
        self.add_shape_to_params('Biz', 'String')
        self.extra_setup()

    def extra_setup(self):
        self.setup_client()
        self.examples_documenter = CodeExamplesDocumenter(
            client=self.client,
            root_docs_path=self.root_services_path,
        )

    def mock_response(
            self,
            status=200,
            content="CONTENT",
            json_data=None):

        mock_resp = mock.Mock()
        # Aet status code and content.
        mock_resp.status_code = status
        mock_resp.content = content
        # Add json data if provided.
        if json_data:
            mock_resp.text = json_data
        return mock_resp

    def test_load_catalog(self):
        mock_json = '''
                {
                    "examples": [
                        {
                            "id": "service1_actions1"
                        }
                    ]
                }
                '''
        examples_result = json.loads(mock_json)
        mock_resp = self.mock_response(status=200, json_data=mock_json)
        self.request_patch = mock.patch('requests.get', return_value=mock_resp)
        self.request_patch.start()
        examples = self.examples_documenter.load_code_examples_catalog('service1')
        self.request_patch.stop()
        self.assertEqual(examples, examples_result['examples'])

    def test_document_codeexamples(self):
        examples_json = '''
        {
            "examples": [
                {
                    "id": "service1_actions1",
                    "file": "service1_metadata.yaml",
                    "languages": [],
                    "title": "Action1",
                    "category": "Api",
                    "doc_filenames": {
                        "service_pages": {
                            "service1": "https://docs.aws.amazon.com/code-library/latest/ug/service1_example_service1_Action1_section.html"
                        },
                        "sdk_pages": []
                    },
                    "synopsis_list": [],
                    "source_key": null
                },
                {
                    "id": "service1_basics",
                    "file": "service1_metadata.yaml",
                    "title": "Learn the Basics",
                    "category": "Basics",
                    "doc_filenames": {
                        "service_pages": {
                            "service1": "https://docs.aws.amazon.com/code-library/latest/ug/service_example_service1_Basics_section.html"
                        },
                        "sdk_pages": []
                    },
                    "synopsis_list": [],
                    "source_key": null
                },
                {
                    "id": "service1_Scenario1",
                    "file": "service1_metadata.yaml",
                    "title": "Scenario1",
                    "category": "Scenarios",
                    "doc_filenames": {
                        "service_pages": {
                            "service1": "https://docs.aws.amazon.com/code-library/latest/ug/service_example_service1_Scenario1_section.html"
                        },
                        "sdk_pages": []
                    },
                    "synopsis_list": [],
                    "source_key": null
                }
            ]
        }
        '''
        examples = json.loads(examples_json)
        self.examples_documenter.document_code_examples(self.doc_structure, examples['examples'], 'service1')
        self.assert_contains_line('AWS SDK Code Examples')
        self.assert_contains_line(
            'Explore code examples in the `AWS SDK Code Examples Code Library <https://docs.aws.amazon.com/code-library/latest/ug/python_3_myservice_code_examples.html>`_')
        self.assert_contains_line('Api')
        self.assert_contains_line('* `Action1 <https://docs.aws.amazon.com/code-library/latest/ug/service1_example_service1_Action1_section.html>`_')
        self.assert_contains_line('Basics')
        self.assert_contains_line(
            '* `Learn the Basics <https://docs.aws.amazon.com/code-library/latest/ug/service_example_service1_Basics_section.html>`_')
        self.assert_contains_line('Scenarios')
        self.assert_contains_line(
            '* `Scenario1 <https://docs.aws.amazon.com/code-library/latest/ug/service_example_service1_Scenario1_section.html>`_')

    def test_no_empty_examples_section(self):
        examples = []

        self.examples_documenter.document_code_examples(self.doc_structure, examples, 'service1')
        self.assert_not_contains_line('AWS SDK Code Examples')
