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

import requests
from botocore.compat import json

CODE_EXAMPLE_LINK = 'https://docs.aws.amazon.com/code-library/latest/ug/python_3_'
CODE_EXAMPLE_CATALOG_VERSION = '2025.0.0-alpha'
# Change this to the main repo and branch when PR is merged.
CODE_EXAMPLE_CATALOG_BASE = 'https://raw.githubusercontent.com/rlhagerm/aws-doc-sdk-examples/refs/tags/'


class CodeExamplesDocumenter:
    def __init__(self, client, root_docs_path):
        self._client = client
        self._client_class_name = self._client.__class__.__name__
        self._service_name = self._client.meta.service_model.service_name
        self._root_docs_path = root_docs_path

    def load_code_examples_catalog(self, service_id):
        """Loads the code library example catalog listing for the service.

        :param service_id: The code examples service id.
        :return: The list of examples.
        """
        git_service_url = f"{CODE_EXAMPLE_CATALOG_BASE}/{CODE_EXAMPLE_CATALOG_VERSION}/python/example_code/{service_id}/examples_catalog.json"

        response = requests.get(git_service_url)
        if response.status_code == 200:
            example_json = response.text
            if example_json:
                examples = json.loads(example_json)
                if len(examples) > 0:
                    return examples['examples']

        return []

    def document_code_examples(self, section, examples, service_id):
        """Documents the code library code examples for a service.

        :param section: The section to write to.
        :param examples: The list of examples.
        :param service_id: The code examples service id.
        """
        if examples:
            section.style.h2('AWS SDK Code Examples')
            self._add_overview(section)

        # Group the examples by category. Do not show a category if there are no examples.
        example_categories = {}
        for i in range(len(examples)):
            example_categories.setdefault(examples[i]['category'], []).append(examples[i])

        # Write a link item for each example in the category.
        for category in sorted(example_categories):
            section.style.new_line()
            section.style.h3(category)
            for i in range(len(example_categories[category])):
                section.style.start_li()
                title_text = example_categories[category][i]['title']
                if not title_text:
                    title_text = example_categories[category][i]['id'].rsplit('_', 1)[-1]
                service_page = example_categories[category][i]['doc_filenames']['service_pages'].get(
                    service_id,list(example_categories[category][i]['doc_filenames']['service_pages'].values())[0])
                section.style.external_link(
                    title=title_text,
                    link=service_page,
                )
                section.style.end_li()

    def _add_overview(self, section):
        """Write the overview section for code examples.

        :param section: The section to write to.
        """
        section.style.new_line()
        section.write(
            'Explore code examples in the '
        )
        section.style.external_link(
            title='AWS SDK Code Examples Code Library',
            link=CODE_EXAMPLE_LINK + self._service_name + '_code_examples.html',
        )
        section.write('.')
        section.style.new_line()


