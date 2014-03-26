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

    def setUp(self):
        super(TestSNSOperations, self).setUp()
        self.sns = self.session.get_service('sns')
        self.http_response = Mock()
        self.http_response.status_code = 200
        self.parsed_response = {}

    def test_subscribe_with_endpoint(self):
        op = self.sns.get_operation('Subscribe')
        params = op.build_parameters(topic_arn='topic_arn',
                                     protocol='http',
                                     notification_endpoint='http://example.org')
        self.assertEqual(params['Endpoint'], 'http://example.org')

    def test_sns_pre_send_event(self):
        op = self.sns.get_operation('Subscribe')
        calls = []
        self.session.register('before-call.sns.Subscribe',
                              lambda **kwargs: calls.append(kwargs))
        endpoint = Mock()
        endpoint.make_request.return_value = (self.http_response,
                                              self.parsed_response)
        op.call(endpoint=endpoint, topic_arn='topic_arn', protocol='http',
                notification_endpoint='http://example.org')
        self.assertEqual(len(calls), 1)
        kwargs = calls[0]
        self.assertEqual(kwargs['operation'], op)
        self.assertEqual(kwargs['endpoint'], endpoint)
        self.assertEqual(kwargs['params']['TopicArn'], 'topic_arn')

    def test_sns_post_send_event_is_invoked(self):
        op = self.sns.get_operation('Subscribe')
        calls = []
        self.session.register('after-call.sns.Subscribe',
                              lambda **kwargs: calls.append(kwargs))
        endpoint = Mock()
        endpoint.make_request.return_value = (self.http_response,
                                              self.parsed_response)
        op.call(endpoint=endpoint, topic_arn='topic_arn', protocol='http',
                notification_endpoint='http://example.org')
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]['operation'], op)
        self.assertEqual(calls[0]['http_response'], self.http_response)
        self.assertEqual(calls[0]['parsed'], self.parsed_response)

    def test_create_platform_application(self):
        op = self.sns.get_operation('CreatePlatformApplication')
        attributes = OrderedDict()
        attributes['PlatformCredential'] = 'foo'
        attributes['PlatformPrincipal'] = 'bar'
        params = op.build_parameters(name='gcmpushapp', platform='GCM',
                                     attributes=attributes)
        result = {'Name': 'gcmpushapp',
                  'Platform': 'GCM',
                  'Attributes.entry.1.key': 'PlatformCredential',
                  'Attributes.entry.1.value': 'foo',
                  'Attributes.entry.2.key': 'PlatformPrincipal',
                  'Attributes.entry.2.value': 'bar'}
        self.assertEqual(params, result)
