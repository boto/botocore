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
import mock

from tests.unit.docs import BaseDocsTest
from botocore.docs.service import ServiceDocumenter


class TestServiceDocumenter(BaseDocsTest):
    def setUp(self):
        super(TestServiceDocumenter, self).setUp()
        self.add_shape_to_params('Biz', 'String')
        self.setup_client()
        with mock.patch('botocore.session.create_loader',
                        return_value=self.loader):
            self.service_documenter = ServiceDocumenter('myservice')

    def test_document_service(self):
        # Note that not everything will be included as it is just
        # a smoke test to make sure all of the main parts are inluded.
        contents = self.service_documenter.document_service().decode('utf-8')
        lines = [
            '*************',
            'AWS MyService',
            '*************',
            '.. contents:: Table of Contents',
            '   :depth: 2',
            '======',
            'Client',
            '======',
            '.. py:class:: myservice.Client',
            '  A low-level client representing AWS MyService::',
            '    client = session.create_client(\'myservice\')',
            '  These are the available methods:',
            '  *   :py:meth:`myservice.Client.sample_operation`',
            '  .. py:method:: sample_operation(Biz=None)',
            '==========',
            'Paginators',
            '==========',
            '.. py:class:: myservice.Paginator.sample_operation',
            ('  .. py:method:: paginate(Biz=None, max_items=None, '
             'page_size=None, starting_token=None)'),
            '=======',
            'Waiters',
            '=======',
            '.. py:class:: myservice.Waiter.sample_operation_complete',
            '  .. py:method:: wait(Biz=None)'
        ]
        for line in lines:
            self.assertIn(line, contents)
