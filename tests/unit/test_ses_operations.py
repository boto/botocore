#!/usr/bin/env python
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

from mock import Mock, sentinel

import botocore.session
from botocore.exceptions import MissingParametersError, ValidationError
from botocore.exceptions import UnknownParameterError
from botocore.exceptions import UnknownKeyError


class TestSESOperations(BaseSessionTest):

    def setUp(self):
        super(TestSESOperations, self).setUp()
        self.ses = self.session.get_service('ses')
        self.op = self.ses.get_operation('SendEmail')

    def test_send_email_missing_required_parameters(self):
        with self.assertRaisesRegexp(
                MissingParametersError,
                ('The following required parameters are missing '
                 'for Operation:SendEmail: source, destination, message')):
            self.op.build_parameters()

    def test_send_email_validates_structure(self):
        with self.assertRaises(ValidationError):
            self.op.build_parameters(
                source='foo@example.com',
                destination={'ToAddresses': ['bar@examplecom']},
                message='bar')

    def test_send_email_with_required_inner_member(self):
        with self.assertRaises(MissingParametersError):
            self.op.build_parameters(
                source='foo@example.com',
                destination={'ToAddresses': ['bar@examplecom']},
                message={})

    def test_send_email_with_unknown_params(self):
        with self.assertRaises(UnknownParameterError):
            self.op.build_parameters(
                source='foo@example.com',
                to={'ToAddresses': ['bar@examplecom']},
                message={})


    def test_send_email_with_missing_inner_member(self):
        with self.assertRaises(MissingParametersError):
            self.op.build_parameters(source='foo@example.com',
                                     destination={'ToAddresses': ['bar@examplecom']},
                                     message={'Subject': {'Data': 'foo'},
                                              # 'Text' is missing the 'Data'
                                              # param.
                                              'Body': {'Text': {}}})

    def test_send_email_with_unknown_inner_member(self):
        with self.assertRaises(UnknownKeyError):
            self.op.build_parameters(
                source='foo@example.com',
                destination={'ToAddresses': ['bar@examplecom']},
                message={'Subject': {'Data': 'foo'},
                         'Body': {'Text': {'BADKEY': 'foo'}}})
