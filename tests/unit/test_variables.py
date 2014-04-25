# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from tests import unittest
import mock

from botocore import variables
import botocore.exceptions


class TestVariableResolver(unittest.TestCase):
    def test_resolve_variables_in_process(self):
        in_memory_dict = variables.InMemoryVars({
            'foo': 'foo-value',
            'bar': 'bar-value',
        })
        resolver = variables.VariableResolver(('inmem', in_memory_dict))
        self.assertEqual(resolver.resolve_variable('foo'), 'foo-value')
        self.assertEqual(resolver.resolve_variable('bar'), 'bar-value')
        # None of the resolvers know how how to look up this variable.
        self.assertEqual(resolver.resolve_variable('baz'), None)

    def test_resolve_variables_unknown(self):
        in_memory_dict = variables.InMemoryVars({
            'foo': 'foo-value',
            'bar': 'bar-value',
        })
        resolver = variables.VariableResolver(('inmem', in_memory_dict))
        self.assertEqual(resolver.resolve_variable('baz'), None)

        # Now declare a variable with a default.
        resolver.declare_variable('baz', default='baz-default')
        self.assertEqual(resolver.resolve_variable('baz'), 'baz-default')

    def test_resolver_interface(self):
        in_mem = variables.InMemoryVars({'foo': 'foo-value'})
        self.assertEqual(in_mem.resolve('foo'), 'foo-value')
        self.assertEqual(in_mem.resolve('bar'), None)
        in_mem.add_variable('bar', 'bar-value')
        self.assertEqual(in_mem.resolve('bar'), 'bar-value')

    def test_env_var_resolver(self):
        environ = {}
        var = variables.DictMapping(
            environ, {'foo': 'AWS_FOO', 'bar': 'BAR_FOO'})
        self.assertEqual(var.resolve('foo'), None)

        environ['AWS_FOO'] = 'FOO-VALUE'
        self.assertEqual(var.resolve('foo'), 'FOO-VALUE')

        # Now add a new mapping, this says that the 'baz'
        # var is resolved through the AWS_BAZ env var.
        self.assertEqual(var.resolve('baz'), None)
        var.add_mapping('baz', 'AWS_BAZ')
        # It doesn't exist in the environ, so it initially returns None.
        self.assertEqual(var.resolve('baz'), None)
        # Now if it's in the environ it should resolve.
        environ['AWS_BAZ'] = 'baz-value'
        self.assertEqual(var.resolve('baz'), 'baz-value')

    def test_add_envvar_support_through_resolver_interface(self):
        # Basically, test_env_var_resolver but through the
        # VariableResolver interface.
        environ = {'AWS_FOO': 'bar'}
        resolver = variables.VariableResolver(
            ('env-vars', variables.DictMapping(environ, {})))
        resolver.get_resolver('env-vars').add_mapping('foo', 'AWS_FOO')
        self.assertEqual(resolver.resolve_variable('foo'), 'bar')

    def test_insert_new_var_resolver_into_chain(self):
        original = mock.Mock()
        original.resolve.return_value = None

        resolver = variables.VariableResolver(('original', original))
        self.assertIsNone(resolver.resolve_variable('foo'))

        new_resolver = mock.Mock()
        new_resolver.resolve.return_value = 'NEW-RESOLVER'
        resolver.insert_after('original', ('new-resolver', new_resolver))

        self.assertEqual(resolver.resolve_variable('foo'), 'NEW-RESOLVER')

    def test_insert_references_unknown_resolver(self):
        original = mock.Mock()
        original.resolve.return_value = None
        resolver = variables.VariableResolver(('original', original))
        with self.assertRaises(ValueError):
            resolver.insert_after('unknown-name', ('foo', None))

    def test_config_var_resolves_var(self):
        parser = mock.Mock()
        parser.return_value = {'profiles': {'myprofile': {'foo': 'bar'}}}
        config = variables.ConfigVars(['myconfig'], 'myprofile', parser)
        self.assertEqual(config.resolve('foo'), 'bar')

    def test_config_var_does_not_exist(self):
        parser = mock.Mock()
        parser.return_value = {'profiles': {'myprofile': {}}}
        config = variables.ConfigVars(['myconfig'], 'myprofile', parser)
        self.assertIsNone(config.resolve('foo'))

    def test_config_var_profile_does_not_exist(self):
        parser = mock.Mock()
        bad_profile = 'badprofile'
        parser.return_value = {'profiles': {'myprofile': {}}}
        config = variables.ConfigVars(['myconfig'], bad_profile, parser)
        with self.assertRaises(botocore.exceptions.ProfileNotFound):
            config.resolve('foo')

    def test_config_file_does_not_exist(self):
        parser = mock.Mock()
        parser.side_effect = botocore.exceptions.ConfigNotFound(path='myconfig')
        config = variables.ConfigVars(['myconfig'], 'myprofile', parser)
        self.assertIsNone(config.resolve('foo'))

    def test_use_default_profile(self):
        # If not profile name is explicity given, then use the default profile.
        parser = mock.Mock()
        parser.return_value = {'profiles': {'default': {'foo': 'bar'}}}
        config = variables.ConfigVars(['myconfig'], profile_name=None, parser=parser)
        self.assertEqual(config.resolve('foo'), 'bar')

    def test_use_default_profile_but_dont_raise_exception(self):
        # If no profile name is used, we'll try the default profile, but it's
        # not an error if the profile does not exists (a config file is not
        # required).
        parser = mock.Mock()
        # This is what the response would look like if a user does not have a
        # config file.
        parser.return_value = {'profiles': {}}
        config = variables.ConfigVars(['myconfig'], profile_name=None, parser=parser)
        self.assertIsNone(config.resolve('foo'))

    def test_get_entire_config(self):
        parser = mock.Mock()
        parser.return_value = {'profiles': {'myprofile': {'a': 'b', 'c': 'd'}}}
        config = variables.ConfigVars(['myconfig'], profile_name='myprofile', parser=parser)
        self.assertEqual(config.get_scoped_config(), {'a': 'b', 'c': 'd'})

    def test_get_full_config(self):
        parser = mock.Mock()
        parser.return_value = {'profiles': {'myprofile': {'a': 'b', 'c': 'd'}}, 'preview': 'foo'}
        config = variables.ConfigVars(['myconfig'], profile_name='myprofile', parser=parser)
        self.assertEqual(
            config.get_full_config(),
            {'profiles': {'myprofile': {'a': 'b', 'c': 'd'}},
             'preview': 'foo'})

    def test_add_config_file(self):
        parser = mock.Mock()
        parser.return_value = {'profiles': {'myprofile': {'foo': 'bar'}}}
        config = variables.ConfigVars(['myconfig'], 'myprofile', parser)
        self.assertEqual(config.resolve('foo'), 'bar')
        config.add_config_file('newconfig')
        self.assertEqual(config.resolve('foo'), 'bar')

        # We should call the parser twice, once for the initial resolve()
        # call, then the add_config_file should trigger a reload.
        self.assertEqual(parser.call_count, 2)
        # The last call should be called with both filenames, with the second
        # name last.
        parser.assert_called_with('myconfig', 'newconfig')

    def test_create_config_resolver(self):
        pass
