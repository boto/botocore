# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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


class TestSMSVoiceDocs(BaseDocsFunctionalTest):

    def test_warning_at_top(self):
        docs = self.get_title_section_for('sms-voice')
        self.assert_contains_lines_in_order([
            '.. warning:',
            ('This service client is deprecated. Please use '
             ':doc:`pinpoint-sms-voice <pinpoint-sms-voice>` instead.'),
        ], docs)
