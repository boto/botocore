#!/usr/bin/env
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

from tests import unittest, create_session, temporary_file
import os
import logging
import tempfile
import shutil

import mock

import botocore.session
import botocore.exceptions
from botocore.model import ServiceModel
from botocore import client
from botocore.hooks import HierarchicalEmitter
from botocore.waiter import WaiterModel
from botocore.paginate import PaginatorModel


class BaseSessionTest(unittest.TestCase):

    def setUp(self):
        self.env_vars = {
            'profile': (None, 'FOO_PROFILE', None),
            'region': ('foo_region', 'FOO_REGION', None),
            'data_path': ('data_path', 'FOO_DATA_PATH', None),
            'config_file': (None, 'FOO_CONFIG_FILE', None),
            'credentials_file': (None, None, '/tmp/nowhere'),
        }
        self.environ = {}
        self.environ_patch = mock.patch('os.environ', self.environ)
        self.environ_patch.start()
        self.environ['FOO_PROFILE'] = 'foo'
        self.environ['FOO_REGION'] = 'moon-west-1'
        data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.environ['FOO_DATA_PATH'] = data_path
        config_path = os.path.join(os.path.dirname(__file__), 'cfg',
                                   'foo_config')
        self.environ['FOO_CONFIG_FILE'] = config_path
        self.session = create_session(session_vars=self.env_vars)

    def tearDown(self):
        self.environ_patch.stop()


class SessionTest(BaseSessionTest):

    def close_log_file_handler(self, tempdir, filename):
        logger = logging.getLogger('botocore')
        handlers = logger.handlers
        for handler in handlers[:]:
            if hasattr(handler, 'stream') and handler.stream.name == filename:
                handler.stream.close()
                logger.removeHandler(handler)
                os.remove(filename)
                # logging has an atexit handler that will try to flush/close
                # the file.  By setting this flag to False, we'll prevent it
                # from raising an exception, which is fine because we're
                # handling the closing of the file ourself.
                logging.raiseExceptions = False
        shutil.rmtree(tempdir)

    def test_profile(self):
        self.assertEqual(self.session.get_config_variable('profile'), 'foo')
        self.assertEqual(self.session.get_config_variable('region'),
                         'moon-west-1')
        self.session.get_config_variable('profile') == 'default'
        saved_region = self.environ['FOO_REGION']
        del self.environ['FOO_REGION']
        saved_profile = self.environ['FOO_PROFILE']
        del self.environ['FOO_PROFILE']
        session = create_session(session_vars=self.env_vars)
        self.assertEqual(session.get_config_variable('profile'), None)
        self.assertEqual(session.get_config_variable('region'), 'us-west-1')
        self.environ['FOO_REGION'] = saved_region
        self.environ['FOO_PROFILE'] = saved_profile

    def test_profile_does_not_exist_raises_exception(self):
        # Given we have no profile:
        self.environ['FOO_PROFILE'] = 'profile_that_does_not_exist'
        session = create_session(session_vars=self.env_vars)
        with self.assertRaises(botocore.exceptions.ProfileNotFound):
            session.get_scoped_config()

    def test_variable_does_not_exist(self):
        session = create_session(session_vars=self.env_vars)
        self.assertIsNone(session.get_config_variable('foo/bar'))

    def test_get_aws_services_in_alphabetical_order(self):
        session = create_session(session_vars=self.env_vars)
        services = session.get_available_services()
        self.assertEqual(sorted(services), services)

    def test_profile_does_not_exist_with_default_profile(self):
        session = create_session(session_vars=self.env_vars)
        config = session.get_scoped_config()
        # We should have loaded this properly, and we'll check
        # that foo_access_key which is defined in the config
        # file should be present in the loaded config dict.
        self.assertIn('aws_access_key_id', config)

    def test_default_profile_specified_raises_exception(self):
        # If you explicity set the default profile and you don't
        # have that in your config file, an exception is raised.
        config_path = os.path.join(os.path.dirname(__file__), 'cfg',
                                   'boto_config_empty')
        self.environ['FOO_CONFIG_FILE'] = config_path
        self.environ['FOO_PROFILE'] = 'default'
        session = create_session(session_vars=self.env_vars)
        # In this case, even though we specified default, because
        # the boto_config_empty config file does not have a default
        # profile, we should be raising an exception.
        with self.assertRaises(botocore.exceptions.ProfileNotFound):
            session.get_scoped_config()

    def test_file_logger(self):
        tempdir = tempfile.mkdtemp()
        temp_file = os.path.join(tempdir, 'file_logger')
        self.session.set_file_logger(logging.DEBUG, temp_file)
        self.addCleanup(self.close_log_file_handler, tempdir, temp_file)
        self.session.get_credentials()
        self.assertTrue(os.path.isfile(temp_file))
        with open(temp_file) as logfile:
            s = logfile.read()
        self.assertTrue('Looking for credentials' in s)

    def test_full_config_property(self):
        full_config = self.session.full_config
        self.assertTrue('foo' in full_config['profiles'])
        self.assertTrue('default' in full_config['profiles'])

    def test_full_config_merges_creds_file_data(self):
        with temporary_file('w') as f:
            self.session.set_config_variable('credentials_file', f.name)
            f.write('[newprofile]\n')
            f.write('aws_access_key_id=FROM_CREDS_FILE_1\n')
            f.write('aws_secret_access_key=FROM_CREDS_FILE_2\n')
            f.flush()

            self.session.profile = 'newprofile'
            full_config = self.session.full_config
            self.assertEqual(full_config['profiles']['newprofile'],
                             {'aws_access_key_id': 'FROM_CREDS_FILE_1',
                              'aws_secret_access_key': 'FROM_CREDS_FILE_2'})

    def test_path_not_in_available_profiles(self):
        with temporary_file('w') as f:
            self.session.set_config_variable('credentials_file', f.name)
            f.write('[newprofile]\n')
            f.write('aws_access_key_id=FROM_CREDS_FILE_1\n')
            f.write('aws_secret_access_key=FROM_CREDS_FILE_2\n')
            f.flush()

            profiles = self.session.available_profiles
            self.assertEqual(
                set(profiles),
                set(['foo', 'default', 'newprofile']))

    def test_emit_delegates_to_emitter(self):
        calls = []
        handler = lambda **kwargs: calls.append(kwargs)
        self.session.register('foo', handler)
        self.session.emit('foo')
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]['event_name'], 'foo')

    def test_emitter_can_be_passed_in(self):
        events = HierarchicalEmitter()
        session = create_session(session_vars=self.env_vars,
                                 event_hooks=events)
        calls = []
        handler = lambda **kwargs: calls.append(kwargs)
        events.register('foo', handler)

        session.emit('foo')
        self.assertEqual(len(calls), 1)

    def test_emit_first_non_none(self):
        session = create_session(session_vars=self.env_vars)
        session.register('foo', lambda **kwargs: None)
        session.register('foo', lambda **kwargs: 'first')
        session.register('foo', lambda **kwargs: 'second')
        response = session.emit_first_non_none_response('foo')
        self.assertEqual(response, 'first')

    def test_create_events(self):
        event = self.session.create_event('before-call', 'foo', 'bar')
        self.assertEqual(event, 'before-call.foo.bar')
        event = self.session.create_event('after-call', 'foo', 'bar')
        self.assertEqual(event, 'after-call.foo.bar')
        event = self.session.create_event('after-parsed', 'foo',
                                          'bar', 'fie', 'baz')
        self.assertEqual(event, 'after-parsed.foo.bar.fie.baz')
        event = self.session.create_event('service-created')
        self.assertEqual(event, 'service-created')
        self.assertRaises(botocore.exceptions.EventNotFound,
                          self.session.create_event, 'foo-bar')

    @mock.patch('logging.getLogger')
    @mock.patch('logging.FileHandler')
    def test_logger_name_can_be_passed_in(self, file_handler, get_logger):
        self.session.set_debug_logger('botocore.hooks')
        get_logger.assert_called_with('botocore.hooks')

        self.session.set_file_logger('DEBUG', 'debuglog', 'botocore.service')
        get_logger.assert_called_with('botocore.service')
        file_handler.assert_called_with('debuglog')

    @mock.patch('logging.getLogger')
    @mock.patch('logging.StreamHandler')
    @mock.patch('logging.Formatter')
    def test_general_purpose_logger(self, formatter, file_handler, get_logger):
        self.session.set_stream_logger('foo.bar', 'ERROR', format_string='foo')
        get_logger.assert_called_with('foo.bar')
        get_logger.return_value.setLevel.assert_called_with(logging.DEBUG)
        formatter.assert_called_with('foo')

    def test_register_with_unique_id(self):
        calls = []
        handler = lambda **kwargs: calls.append(kwargs)
        self.session.register('foo', handler, unique_id='bar')
        self.session.emit('foo')
        self.assertEqual(calls[0]['event_name'], 'foo')
        calls = []
        self.session.unregister('foo', unique_id='bar')
        self.session.emit('foo')
        self.assertEqual(calls, [])


class TestBuiltinEventHandlers(BaseSessionTest):
    def setUp(self):
        super(TestBuiltinEventHandlers, self).setUp()
        self.builtin_handlers = [
            ('foo', self.on_foo),
        ]
        self.foo_called = False
        self.handler_patch = mock.patch('botocore.handlers.BUILTIN_HANDLERS',
                                        self.builtin_handlers)
        self.handler_patch.start()

    def on_foo(self, **kwargs):
        self.foo_called = True

    def tearDown(self):
        super(TestBuiltinEventHandlers, self).setUp()
        self.handler_patch.stop()

    def test_registered_builtin_handlers(self):
        session = botocore.session.Session(self.env_vars, None,
                                           include_builtin_handlers=True)
        session.emit('foo')
        self.assertTrue(self.foo_called)


class TestSessionConfigurationVars(BaseSessionTest):
    def test_per_session_config_vars(self):
        self.session.session_var_map['foobar'] = (None, 'FOOBAR', 'default')
        # Default value.
        self.assertEqual(self.session.get_config_variable('foobar'), 'default')
        # Retrieve from os environment variable.
        self.environ['FOOBAR'] = 'fromenv'
        self.assertEqual(self.session.get_config_variable('foobar'), 'fromenv')

        # Explicit override.
        self.session.set_config_variable('foobar', 'session-instance')
        self.assertEqual(self.session.get_config_variable('foobar'),
                         'session-instance')

        # Can disable this check via the ``methods`` arg.
        del self.environ['FOOBAR']
        self.assertEqual(self.session.get_config_variable(
            'foobar', methods=('env', 'config')), 'default')

    def test_default_value_can_be_overriden(self):
        self.session.session_var_map['foobar'] = (None, 'FOOBAR', 'default')
        # Default value.
        self.assertEqual(self.session.get_config_variable('foobar'), 'default')
        self.assertEqual(
            self.session.get_config_variable('foobar',
                                             default='per-call-default'),
            'per-call-default')


class TestSessionUserAgent(BaseSessionTest):
    def test_can_change_user_agent_name(self):
        self.session.user_agent_name = 'something-else'
        self.assertTrue(self.session.user_agent().startswith('something-else'))

    def test_can_change_user_agent_version(self):
        self.session.user_agent_version = '24.0'
        self.assertTrue(self.session.user_agent().startswith('Botocore/24.0'))

    def test_can_append_to_user_agent(self):
        self.session.user_agent_extra = 'custom-thing/other'
        self.assertTrue(
            self.session.user_agent().endswith('custom-thing/other'))


class TestConfigLoaderObject(BaseSessionTest):
    def test_config_loader_delegation(self):
        with temporary_file('w') as f:
            f.write('[credfile-profile]\naws_access_key_id=a\n')
            f.write('aws_secret_access_key=b\n')
            f.flush()
            self.session.set_config_variable('credentials_file', f.name)
            self.session.profile = 'credfile-profile'
            # Now trying to retrieve the scoped config should pull in
            # values from the shared credentials file.
            self.assertEqual(self.session.get_scoped_config(),
                             {'aws_access_key_id': 'a',
                              'aws_secret_access_key': 'b'})


class TestGetServiceModel(BaseSessionTest):
    def test_get_service_model(self):
        loader = mock.Mock()
        loader.load_service_model.return_value = {}
        self.session.register_component('data_loader', loader)
        model = self.session.get_service_model('made_up')
        self.assertIsInstance(model, ServiceModel)
        self.assertEqual(model.service_name, 'made_up')


class TestGetPaginatorModel(BaseSessionTest):
    def test_get_paginator_model(self):
        loader = mock.Mock()
        loader.determine_latest.return_value = 'aws/foo/2014-01-01.normal.json'
        loader.load_data.return_value = {"pagination": {}}
        self.session.register_component('data_loader', loader)

        model = self.session.get_paginator_model('foo')

        # Verify we get a PaginatorModel back
        self.assertIsInstance(model, PaginatorModel)
        # Verify we called the loader correctly.
        loader.load_data.assert_called_with(
            'aws/foo/2014-01-01.paginators.json')


class TestGetWaiterModel(BaseSessionTest):
    def test_get_waiter_model(self):
        loader = mock.Mock()
        loader.determine_latest.return_value = 'aws/foo/2014-01-01.normal.json'
        loader.load_data.return_value = {"version": 2, "waiters": {}}
        self.session.register_component('data_loader', loader)

        model = self.session.get_waiter_model('foo')

        # Verify we (1) get the expected return data,
        self.assertIsInstance(model, WaiterModel)
        self.assertEqual(model.waiter_names, [])
        # and (2) call the loader correctly.
        loader.load_data.assert_called_with('aws/foo/2014-01-01.waiters.json')


class TestCreateClient(BaseSessionTest):
    def test_can_create_client(self):
        sts_client = self.session.create_client('sts', 'us-west-2')
        self.assertIsInstance(sts_client, client.BaseClient)

    def test_credential_provider_not_called_when_creds_provided(self):
        cred_provider = mock.Mock()
        self.session.register_component(
            'credential_provider', cred_provider)
        self.session.create_client(
            'sts', 'us-west-2',
            aws_access_key_id='foo',
            aws_secret_access_key='bar',
            aws_session_token='baz')
        self.assertFalse(cred_provider.load_credentials.called,
                         "Credential provider was called even though "
                         "explicit credentials were provided to the "
                         "create_client call.")

    @mock.patch('botocore.client.ClientCreator')
    def test_config_passed_to_client_creator(self, client_creator):
        config = client.Config()
        self.session.create_client('sts', config=config)

        client_creator.return_value.create_client.assert_called_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY,
            scoped_config=mock.ANY, client_config=config)


if __name__ == "__main__":
    unittest.main()
