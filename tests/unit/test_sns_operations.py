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

from mock import Mock

from botocore.compat import OrderedDict


class TestSNSOperations(BaseSessionTest):

    maxDiff = None

    def setUp(self):
        super(TestSNSOperations, self).setUp()
        self.sns = self.session.get_service('sns')
        self.http_response = Mock()
        self.http_response.status_code = 200
        self.parsed_response = {}

    def test_subscribe_with_endpoint(self):
        # XXX: Deal with this.  Can we move the "notification_endpoint"
        # customization up to the CLI?
        # op = self.sns.get_operation('Subscribe')
        # params = op.build_parameters(
        #     topic_arn='topic_arn',
        #     protocol='http',
        #     notification_endpoint='http://example.org')['body']
        # self.assertEqual(params['Endpoint'], 'http://example.org')
        pass

    def test_create_platform_application(self):
        op = self.sns.get_operation('CreatePlatformApplication')
        attributes = OrderedDict()
        attributes['PlatformCredential'] = 'foo'
        attributes['PlatformPrincipal'] = 'bar'
        params = op.build_parameters(name='gcmpushapp', platform='GCM',
                                     attributes=attributes)['body']
        del params['Action']
        del params['Version']
        result = {'Name': 'gcmpushapp',
                  'Platform': 'GCM',
                  'Attributes.entry.1.key': 'PlatformCredential',
                  'Attributes.entry.1.value': 'foo',
                  'Attributes.entry.2.key': 'PlatformPrincipal',
                  'Attributes.entry.2.value': 'bar'}
        self.assertEqual(params, result)
