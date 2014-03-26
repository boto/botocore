#!/usr/bin/env python
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

from tests import BaseSessionTest
import botocore.session
from botocore.compat import json


class TestElasticTranscoderOperations(BaseSessionTest):

    maxDiff = None

    def setUp(self):
        super(TestElasticTranscoderOperations, self).setUp()
        self.dc = self.session.get_service('elastictranscoder')

    def test_create_connection(self):
        op = self.dc.get_operation('CreatePipeline')
        params = op.build_parameters(name='testpipeline',
                                     input_bucket='etc-input',
                                     output_bucket='etc-output',
                                     role='etc-role',
                                     notifications={'Completed': 'etc-topic',
                                                    'Progressing': 'etc-topic',
                                                    'Warning': 'etc-topic',
                                                    'Error': 'etc-topic'})
        result = {"OutputBucket": "etc-output",
                  "Notifications": {"Completed": "etc-topic",
                                    "Warning": "etc-topic",
                                    "Progressing": "etc-topic",
                                    "Error": "etc-topic"},
                  "Role": "etc-role",
                  "Name": "testpipeline",
                  "InputBucket": "etc-input"}
        json_body = json.loads(params['payload'].getvalue())
        self.assertEqual(json_body, result)
