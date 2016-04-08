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
from tests import unittest
from botocore.hooks import HierarchicalEmitter
from botocore.utils import ScopedEventHandler


class TestScopedEventHandler(unittest.TestCase):
    def setUp(self):
        self.event_emitter = HierarchicalEmitter()
        self.handlers_called = []

    def create_handler(self, handler_name):
        def handler(event_name, **kwargs):
            self.handlers_called.append(handler_name)
        return handler

    def test_scoped_event_handler_only_registered_in_scope(self):
        event_name = 'foo'
        handler_name = 'foo.bar'
        handler = self.create_handler(handler_name)
        scoped_handler = ScopedEventHandler(
            self.event_emitter, event_name, handler, 'bar')
        self.event_emitter.emit(event_name)

        with scoped_handler:
            self.event_emitter.emit(event_name)
        self.event_emitter.emit(event_name)

        self.assertEqual(len(self.handlers_called), 1)
        self.assertEqual(self.handlers_called[0], handler_name)

    def test_scoped_event_handler_registers_first(self):
        event_name = 'foo'

        # Register a normal event
        normal_handler = self.create_handler('normal')
        self.event_emitter.register(event_name, normal_handler, 'baz')

        handler = self.create_handler('first')
        scoped_handler = ScopedEventHandler(
            self.event_emitter, event_name, handler, 'bar', 'first')

        with scoped_handler:
            self.event_emitter.emit(event_name)

        self.assertEqual(len(self.handlers_called), 2)
        self.assertEqual(self.handlers_called[0], 'first')

    def test_scoped_event_handler_registers_last(self):
        event_name = 'foo'

        # Register a normal event
        normal_handler = self.create_handler('normal')
        self.event_emitter.register(event_name, normal_handler, 'baz', 'last')

        handler = self.create_handler('last')
        scoped_handler = ScopedEventHandler(
            self.event_emitter, event_name, handler, 'bar')

        with scoped_handler:
            self.event_emitter.emit(event_name)

        self.assertEqual(len(self.handlers_called), 2)
        self.assertEqual(self.handlers_called[1], 'last')


