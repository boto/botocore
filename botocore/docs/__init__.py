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

import botocore.session
from botocore.compat import six
from botocore.docs.service import ServiceDocumenter


def generate_docs():
    services_doc_path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)))), 'docs', 'source',
        'reference', 'services')
    if not os.path.exists(services_doc_path):
        os.makedirs(services_doc_path)

    # Generate reference docs and write them out.
    session = botocore.session.get_session()
    for service_name in session.get_available_services():
        docs = ServiceDocumenter(service_name).document_service()
        service_doc_path = os.path.join(
            services_doc_path, service_name + '.rst')
        with open(service_doc_path, 'wb') as f:
            f.write(docs)
