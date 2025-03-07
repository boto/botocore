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
import os

from botocore import xform_name
from botocore.compat import OrderedDict
from botocore.docs.bcdoc.restdoc import DocumentStructure
from botocore.docs.method import document_model_driven_method
from botocore.docs.utils import DocumentedShape
from botocore.utils import get_service_module_name


class CodeExamplesDocumenter:
    def __init__(self, client, root_docs_path):
        self._client = client
        self._client_class_name = self._client.__class__.__name__
        self._service_name = self._client.meta.service_model.service_name
        self._root_docs_path = root_docs_path
        self._USER_GUIDE_LINK = (
            'https://boto3.amazonaws.com/'
            'v1/documentation/api/latest/guide/clients.html#waiters'
        )
        self._CODE_EXAMPLE_LINK = (
            'https://docs.aws.amazon.com/code-library/latest/ug/python_3_'
        )

    def document_code_examples(self, section, examples):
        """Documents the code library code examples for a service.

        :param section: The section to write to.
        :param examples: The list of examples.
        """
        section.style.h2('AWS SDK Code Examples')
        self._add_overview(section)

        # List the available Code Library examples with a link.
        # TODO: fix service name
        for example in examples:
            section.style.start_li()
            title_text = examples[example]['title']
            plain_title = title_text.replace('<code>', '').replace('</code>', '')
            section.style.external_link(
                title=plain_title,
                link=examples[example]['doc_filenames']['service_pages']['lookoutvision'],
                # link=self._CODE_EXAMPLE_LINK + self._service_name + '_code_examples.html',
            )
            section.style.end_li()

    def _add_overview(self, section):
        section.style.new_line()
        section.write(
            'Explore more examples for this service in the '
        )
        section.style.external_link(
            title='AWS SDK Code Examples Code Library',
            link=self._CODE_EXAMPLE_LINK + self._service_name + '_code_examples.html',
        )
        section.write('.')
        section.style.new_line()


