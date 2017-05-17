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
from botocore.docs.client import ClientDocumenter


class TestClientDocumenter(BaseDocsTest):
    def setUp(self):
        super(TestClientDocumenter, self).setUp()
        self.add_shape_to_params('Biz', 'String')
        self.setup_client()
        self.client_documenter = ClientDocumenter(self.client)

    def test_document_client(self):
        self.client_documenter.document_client(self.doc_structure)
        self.assert_contains_lines_in_order([
            '======',
            'Client',
            '======',
            '.. py:class:: MyService.Client',
            '  A low-level client representing AWS MyService::',
            '    client = session.create_client(\'myservice\')',
            '  These are the available methods:',
            '  *   :py:meth:`~MyService.Client.can_paginate`',
            '  *   :py:meth:`~MyService.Client.get_paginator`',
            '  *   :py:meth:`~MyService.Client.get_waiter`',
            '  *   :py:meth:`~MyService.Client.sample_operation`',
            '  .. py:method:: can_paginate(operation_name)',
            '  .. py:method:: get_paginator(operation_name)',
            '  .. py:method:: get_waiter(waiter_name)',
            '  .. py:method:: sample_operation(**kwargs)',
            '    **Request Syntax**',
            '    ::',
            '      response = client.sample_operation(',
            '          Biz=\'string\'',
            '      )',
            '    :type Biz: string',
            '    :param Biz:',
            '    :rtype: dict',
            '    :returns:',
            '      **Response Syntax**',
            '      ::',
            '        {',
            '            \'Biz\': \'string\'',
            '        }',
            '      **Response Structure**',
            '      - *(dict) --*',
            '        - **Biz** *(string) --*'
        ])
