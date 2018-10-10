#!/usr/bin/env
# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import socket

import botocore.config
from tests import unittest
import mock

from botocore import args
from botocore.client import ClientEndpointBridge
from botocore.config import Config
from botocore.hooks import HierarchicalEmitter
from botocore.model import ServiceModel


class TestCreateClientArgs(unittest.TestCase):
    def setUp(self):
        self.event_emitter = mock.Mock(HierarchicalEmitter)
        self.args_create = args.ClientArgsCreator(
            self.event_emitter, None, None, None, None)
        self.region = 'us-west-2'
        self.endpoint_url = 'https://ec2/'
        self.service_model = mock.Mock(ServiceModel)
        self.service_model.metadata = {
            'serviceFullName': 'MyService',
            'protocol': 'query'
        }
        self.service_model.operation_names = []
        self.bridge = mock.Mock(ClientEndpointBridge)
        self.bridge.resolve.return_value = {
            'region_name': self.region, 'signature_version': 'v4',
            'endpoint_url': self.endpoint_url,
            'signing_name': 'ec2', 'signing_region': self.region,
            'metadata': {}}
        self.default_socket_options = [
            (socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        ]

    def call_get_client_args(self, **override_kwargs):
        call_kwargs = {
            'service_model': self.service_model,
            'region_name': self.region,
            'is_secure': True,
            'endpoint_url': self.endpoint_url,
            'verify': True,
            'credentials': None,
            'scoped_config': {},
            'client_config': None,
            'endpoint_bridge': self.bridge
        }
        call_kwargs.update(**override_kwargs)
        return self.args_create.get_client_args(**call_kwargs)

    def assert_create_endpoint_call(self, mock_endpoint, **override_kwargs):
        call_kwargs = {
            'endpoint_url': self.endpoint_url,
            'region_name': self.region,
            'response_parser_factory': None,
            'timeout': (60, 60),
            'verify': True,
            'max_pool_connections': 10,
            'proxies': None,
            'socket_options': self.default_socket_options,
            'client_cert': None,
        }
        call_kwargs.update(**override_kwargs)
        mock_endpoint.return_value.create_endpoint.assert_called_with(
            self.service_model, **call_kwargs
        )

    def test_compute_s3_configuration(self):
        scoped_config = {}
        client_config = None
        self.assertIsNone(
            self.args_create.compute_s3_config(
                scoped_config, client_config))

    def test_compute_s3_config_only_scoped_config(self):
        scoped_config = {
            's3': {'use_accelerate_endpoint': True},
        }
        client_config = None
        self.assertEqual(
            self.args_create.compute_s3_config(scoped_config, client_config),
            {'use_accelerate_endpoint': True}
        )

    def test_client_s3_accelerate_from_varying_forms_of_true(self):
        scoped_config= {'s3': {'use_accelerate_endpoint': 'True'}}
        client_config = None

        self.assertEqual(
            self.args_create.compute_s3_config(
                {'s3': {'use_accelerate_endpoint': 'True'}},
                client_config=None),
            {'use_accelerate_endpoint': True}
        )
        self.assertEqual(
            self.args_create.compute_s3_config(
                {'s3': {'use_accelerate_endpoint': 'true'}},
                client_config=None),
            {'use_accelerate_endpoint': True}
        )
        self.assertEqual(
            self.args_create.compute_s3_config(
                {'s3': {'use_accelerate_endpoint': True}},
                client_config=None),
            {'use_accelerate_endpoint': True}
        )

    def test_client_s3_accelerate_from_client_config(self):
        self.assertEqual(
            self.args_create.compute_s3_config(
                scoped_config=None,
                client_config=Config(s3={'use_accelerate_endpoint': True})
            ),
            {'use_accelerate_endpoint': True}
        )

    def test_client_s3_accelerate_client_config_overrides_scoped(self):
        self.assertEqual(
            self.args_create.compute_s3_config(
                scoped_config={'s3': {'use_accelerate_endpoint': False}},
                client_config=Config(s3={'use_accelerate_endpoint': True})
            ),
            # client_config beats scoped_config
            {'use_accelerate_endpoint': True}
        )

    def test_client_s3_dualstack_handles_varying_forms_of_true(self):
        scoped_config= {'s3': {'use_dualstack_endpoint': 'True'}}
        client_config = None

        self.assertEqual(
            self.args_create.compute_s3_config(
                {'s3': {'use_dualstack_endpoint': 'True'}},
                client_config=None),
            {'use_dualstack_endpoint': True}
        )
        self.assertEqual(
            self.args_create.compute_s3_config(
                {'s3': {'use_dualstack_endpoint': 'true'}},
                client_config=None),
            {'use_dualstack_endpoint': True}
        )
        self.assertEqual(
            self.args_create.compute_s3_config(
                {'s3': {'use_dualstack_endpoint': True}},
                client_config=None),
            {'use_dualstack_endpoint': True}
        )

    def test_max_pool_from_client_config_forwarded_to_endpoint_creator(self):
        config = botocore.config.Config(max_pool_connections=20)
        with mock.patch('botocore.args.EndpointCreator') as m:
            self.call_get_client_args(client_config=config)
            self.assert_create_endpoint_call(m, max_pool_connections=20)

    def test_proxies_from_client_config_forwarded_to_endpoint_creator(self):
        proxies = {'http': 'http://foo.bar:1234',
                   'https': 'https://foo.bar:4321'}
        config = botocore.config.Config(proxies=proxies)
        with mock.patch('botocore.args.EndpointCreator') as m:
            self.call_get_client_args(client_config=config)
            self.assert_create_endpoint_call(m, proxies=proxies)

    def test_s3_with_endpoint_url_still_resolves_region(self):
        self.service_model.endpoint_prefix = 's3'
        self.service_model.metadata = {'protocol': 'rest-xml'}
        self.bridge.resolve.side_effect = [
            {
                'region_name': None, 'signature_version': 's3v4',
                'endpoint_url': 'http://other.com/', 'signing_name': 's3',
                'signing_region': None, 'metadata': {}
            },
            {
                'region_name': 'us-west-2', 'signature_version': 's3v4',
                'enpoint_url': 'https://s3-us-west-2.amazonaws.com',
                'signing_name': 's3', 'signing_region': 'us-west-2',
                'metadata': {}
            }
        ]
        client_args = self.call_get_client_args(
            endpoint_url='http://other.com/')
        self.assertEqual(
            client_args['client_config'].region_name, 'us-west-2')

    def test_region_does_not_resolve_if_not_s3_and_endpoint_url_provided(self):
        self.service_model.endpoint_prefix = 'ec2'
        self.service_model.metadata = {'protocol': 'query'}
        self.bridge.resolve.side_effect = [{
            'region_name': None, 'signature_version': 'v4',
            'endpoint_url': 'http://other.com/', 'signing_name': 'ec2',
            'signing_region': None, 'metadata': {}
        }]
        client_args = self.call_get_client_args(
            endpoint_url='http://other.com/')
        self.assertEqual(client_args['client_config'].region_name, None)

    def test_provide_retry_config(self):
        config = botocore.config.Config(retries={'max_attempts': 10})
        client_args = self.call_get_client_args(client_config=config)
        self.assertEqual(
            client_args['client_config'].retries, {'max_attempts': 10})

    def test_tcp_keepalive_enabled(self):
        scoped_config = {'tcp_keepalive': 'true'}
        with mock.patch('botocore.args.EndpointCreator') as m:
            self.call_get_client_args(scoped_config=scoped_config)
            self.assert_create_endpoint_call(
                m, socket_options=self.default_socket_options + [
                    (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                ]
            )

    def test_tcp_keepalive_not_specified(self):
        scoped_config = {}
        with mock.patch('botocore.args.EndpointCreator') as m:
            self.call_get_client_args(scoped_config=scoped_config)
            self.assert_create_endpoint_call(
                m, socket_options=self.default_socket_options)

    def test_tcp_keepalive_explicitly_disabled(self):
        scoped_config = {'tcp_keepalive': 'false'}
        with mock.patch('botocore.args.EndpointCreator') as m:
            self.call_get_client_args(scoped_config=scoped_config)
            self.assert_create_endpoint_call(
                m, socket_options=self.default_socket_options)

    def test_tcp_keepalive_enabled_case_insensitive(self):
        scoped_config = {'tcp_keepalive': 'True'}
        with mock.patch('botocore.args.EndpointCreator') as m:
            self.call_get_client_args(scoped_config=scoped_config)
            self.assert_create_endpoint_call(
                m, socket_options=self.default_socket_options + [
                    (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                ]
            )
