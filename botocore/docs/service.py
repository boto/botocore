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
from bcdoc.restdoc import DocumentStructure

from botocore import xform_name
import botocore.session
from botocore.exceptions import DataNotFoundError
from botocore.docs.utils import get_official_service_name
from botocore.docs.client import ClientDocumentor
from botocore.docs.waiter import WaiterDocumentor
from botocore.docs.paginator import PaginatorDocumentor


class ServiceDocumentor(object):
    def __init__(self, service_name):
        self._session = botocore.session.get_session()
        self._service_name = service_name

        self._client = self._session.create_client(
            service_name, region_name='us-east-1', aws_access_key_id='foo',
            aws_secret_access_key='bar')

        self.sections = [
            'title',
            'table-of-contents',
            'client_api',
            'paginator-api',
            'waiter_api'
        ]

    def document_service(self):
        """Documents an entire service.

        :returns: The reStructured text of the documented service.
        """ 
        self._register_sections()
        doc_structure = DocumentStructure(
            self._service_name, self._client.meta.events,
            section_names=self.sections)
        return doc_structure.flush_structure()

    def _register_sections(self):
        for section in self.sections:
            self._client.meta.events.register(
                'docs-adding-section.%s-%s' % (self._service_name, section),
                getattr(self, section.replace('-', '_')),
                unique_id='%s-%s' % (self._service_name, section))

    def title(self, section, **kwargs):
        official_service_name = get_official_service_name(
            self._client.meta.service_model)
        section.style.h1(official_service_name)

    def table_of_contents(self, section, **kwargs):
        section.style.table_of_contents(title='Table of Contents', depth=2)

    def client_api(self, section, **kwargs):
        ClientDocumentor(self._client).document_client(section)

    def paginator_api(self, section, **kwargs):
        try:
            service_paginator_model = self._session.get_paginator_model(
                self._service_name)
        except DataNotFoundError:
            return
        paginator_documentor = PaginatorDocumentor(
            self._client, service_paginator_model)
        paginator_documentor.document_paginators(section)

    def waiter_api(self, section, **kwargs):
        if self._client.waiter_names:
            service_waiter_model = self._session.get_waiter_model(
                self._service_name)
            waiter_documentor = WaiterDocumentor(
            self._client, service_waiter_model)
            waiter_documentor.document_waiters(section)

