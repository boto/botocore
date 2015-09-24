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
from tests.functional.docs import BaseDocsFunctionalTest
from botocore.docs.service import ServiceDocumenter


class TestIAMDocs(BaseDocsFunctionalTest):
    def test_changes_policy_doc_to_dict(self):
        modified_methods = ['create_policy', 'get_role_policy']
        service_contents = ServiceDocumenter('iam', self._session)\
            .document_service()
        for method_name in modified_methods:
            method_contents = self.get_method_document_block(
                method_name, service_contents)
            self.assertNotIn(b"Document': 'string'", method_contents)
            self.assertNotIn(b"Document='string", method_contents)
            self.assertTrue(
                (b"Document': {}" in method_contents) or
                (b"Document={}" in method_contents))
            self.assertNotIn(b"Document** *(string)", method_contents)
            self.assertNotIn(b"Document: string", method_contents)
            self.assertTrue(
                (b"Document** *(dict)" in method_contents) or
                (b"Document: dict" in method_contents))

    def test_changes_policy_doc_list_to_dict(self):
        modified_methods = ['get_context_keys_for_custom_policy',
                            'simulate_custom_policy']
        service_contents = ServiceDocumenter('iam', self._session)\
            .document_service()
        for method_name in modified_methods:
            method_contents = self.get_method_document_block(
                method_name, service_contents)
            lines = [
                "PolicyInputList=[",
                "              {},",
                "          ]"
            ]
            self.assert_contains_lines_in_order(lines, method_contents)
