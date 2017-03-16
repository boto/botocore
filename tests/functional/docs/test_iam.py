# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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


class TestIamDocs(BaseDocsFunctionalTest):
    def test_get_role_assumerolepolicydocument_type(self):
        content = self.get_docstring_for_method('iam', 'get_role')
        self.assert_contains_line(
            '- **AssumeRolePolicyDocument** *(dict) --*',
            content)
        self.assert_contains_line(
            "'AssumeRolePolicyDocument': ...",
            content)
