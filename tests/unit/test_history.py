from tests import unittest

import mock

from botocore.history import HistoryRecorder
from botocore.history import BaseHistoryHandler
from botocore.history import HistoryRecorderScope
from botocore.history import get_global_history_recorder


class TerribleError(Exception):
    pass


class ExceptionThrowingHandler(BaseHistoryHandler):
    def emit(self, event_type, payload, source):
        raise TerribleError('Bad behaving handler')


class TestHistoryRecorder(unittest.TestCase):
    def get_enabled_history_recorder(self):
        history_recorder = HistoryRecorder()
        history_recorder.enable()
        return history_recorder

    def test_can_attach_and_call_handler_emit(self):
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        recorder = HistoryRecorder()
        recorder.enable()
        recorder.add_handler(mock_handler)
        recorder.record('foo', 'bar', source='source')

        mock_handler.emit.assert_called_with('foo', 'bar', 'source')

    def test_can_call_multiple_handlers(self):
        first_handler = mock.Mock(spec=BaseHistoryHandler)
        second_handler = mock.Mock(spec=BaseHistoryHandler)
        recorder = HistoryRecorder()
        recorder.enable()
        recorder.add_handler(first_handler)
        recorder.add_handler(second_handler)
        recorder.record('foo', 'bar', source='source')

        first_handler.emit.assert_called_with('foo', 'bar', 'source')
        second_handler.emit.assert_called_with('foo', 'bar', 'source')

    def test_does_use_botocore_source_by_default(self):
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        recorder = HistoryRecorder()
        recorder.enable()
        recorder.add_handler(mock_handler)
        recorder.record('foo', 'bar')

        mock_handler.emit.assert_called_with('foo', 'bar', 'BOTOCORE')

    def test_does_not_call_handlers_when_never_enabled(self):
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        recorder = HistoryRecorder()
        recorder.add_handler(mock_handler)
        recorder.record('foo', 'bar')

        mock_handler.emit.assert_not_called()

    def test_does_not_call_handlers_when_disabled(self):
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        recorder = HistoryRecorder()
        recorder.enable()
        recorder.disable()
        recorder.add_handler(mock_handler)
        recorder.record('foo', 'bar')

        mock_handler.emit.assert_not_called()

    def test_can_ignore_handler_exceptions(self):
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        recorder = HistoryRecorder()
        recorder.enable()
        bad_handler = ExceptionThrowingHandler()
        recorder.add_handler(bad_handler)
        recorder.add_handler(mock_handler)
        try:
            recorder.record('foo', 'bar')
        except TerribleError:
            self.fail('Should not have raised a TerribleError')
        mock_handler.emit.assert_called_with('foo', 'bar', 'BOTOCORE')

    def test_add_scope_and_emit_handlers_for_scope(self):
        history_scope = HistoryRecorderScope()
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        history_scope.add_handler(mock_handler)
        mock_client = object()
        history_scope.register_client(mock_client)

        recorder = self.get_enabled_history_recorder()
        recorder.add_scope(history_scope)

        recorder.record('myevent', {}, scope_id=id(mock_client))
        mock_handler.emit.assert_called_with('myevent', {}, 'BOTOCORE')

    def test_add_scope_and_emit_all_handlers_for_scope(self):
        history_scope = HistoryRecorderScope()
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        other_mock_hanlder = mock.Mock(spec=BaseHistoryHandler)
        history_scope.add_handler(mock_handler)
        history_scope.add_handler(other_mock_hanlder)
        mock_client = object()
        history_scope.register_client(mock_client)

        recorder = self.get_enabled_history_recorder()
        recorder.add_scope(history_scope)

        recorder.record('myevent', {}, scope_id=id(mock_client))
        mock_handler.emit.assert_called_with('myevent', {}, 'BOTOCORE')
        other_mock_hanlder.emit.assert_called_with('myevent', {}, 'BOTOCORE')

    def test_emits_scoped_and_not_scoped_handlders(self):
        history_scope = HistoryRecorderScope()
        scoped_handler = mock.Mock(spec=BaseHistoryHandler)
        history_scope.add_handler(scoped_handler)
        mock_client = object()
        history_scope.register_client(mock_client)

        recorder = self.get_enabled_history_recorder()
        recorder.add_scope(history_scope)

        global_handler = mock.Mock(spec=BaseHistoryHandler)
        recorder.add_handler(global_handler)

        recorder.record('myevent', {}, scope_id=id(mock_client))
        scoped_handler.emit.assert_called_with('myevent', {}, 'BOTOCORE')
        global_handler.emit.assert_called_with('myevent', {}, 'BOTOCORE')

    def test_does_not_call_scoped_handler_with_wrong_scope_id(self):
        history_scope = HistoryRecorderScope()
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        history_scope.add_handler(mock_handler)
        mock_client = object()
        other_mock_client = object()
        history_scope.register_client(mock_client)

        recorder = self.get_enabled_history_recorder()
        recorder.add_scope(history_scope)

        recorder.record('myevent', {}, scope_id=id(other_mock_client))
        mock_handler.emit.assert_not_called()

    def test_does_not_called_scoped_handler_with_no_scope_id(self):
        history_scope = HistoryRecorderScope()
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        history_scope.add_handler(mock_handler)
        mock_client = object()
        history_scope.register_client(mock_client)

        recorder = self.get_enabled_history_recorder()
        recorder.add_scope(history_scope)

        recorder.record('myevent', {})
        mock_handler.emit.assert_not_called()

    def test_calls_handlers_for_all_scopes_registered_to_same_id(self):
        history_scope = HistoryRecorderScope()
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        history_scope.add_handler(mock_handler)

        other_history_scope = HistoryRecorderScope()
        other_mock_handler = mock.Mock(spec=BaseHistoryHandler)
        other_history_scope.add_handler(other_mock_handler)

        mock_client = object()
        history_scope.register_client(mock_client)
        other_history_scope.register_client(mock_client)

        recorder = self.get_enabled_history_recorder()
        recorder.add_scope(history_scope)
        recorder.add_scope(other_history_scope)

        recorder.record('myevent', {}, scope_id=id(mock_client))
        mock_handler.emit.assert_called_with('myevent', {}, 'BOTOCORE')
        other_mock_handler.emit.assert_called_with('myevent', {}, 'BOTOCORE')

    def test_does_not_call_scoped_handlers_when_not_enabled(self):
        history_scope = HistoryRecorderScope()
        mock_handler = mock.Mock(spec=BaseHistoryHandler)
        history_scope.add_handler(mock_handler)
        mock_client = object()
        history_scope.register_client(mock_client)

        recorder = HistoryRecorder()
        recorder.add_scope(history_scope)

        recorder.record('myevent', {}, scope_id=id(mock_client))
        mock_handler.emit.assert_not_called()

    def test_can_ignore_scoped_handler_exceptions(self):
        history_scope = HistoryRecorderScope()
        bad_handler = ExceptionThrowingHandler()
        history_scope.add_handler(bad_handler)
        mock_client = object()
        history_scope.register_client(mock_client)

        recorder = self.get_enabled_history_recorder()
        recorder.add_scope(history_scope)

        try:
            recorder.record('myevent', {}, scope_id=id(mock_client))
        except TerribleError:
            self.fail('Should not have raised a TerribleError')


class TestHistoryRecorderScope(unittest.TestCase):
    def test_add_handlers(self):
        history_scope = HistoryRecorderScope()
        handler = mock.Mock(spec=BaseHistoryHandler)
        history_scope.add_handler(handler)
        self.assertEqual(history_scope.handlers, [handler])

    def test_add_multiple_handlers(self):
        history_scope = HistoryRecorderScope()
        handler = mock.Mock(spec=BaseHistoryHandler)
        other_handler = mock.Mock(spec=BaseHistoryHandler)
        history_scope.add_handler(handler)
        history_scope.add_handler(other_handler)
        self.assertEqual(history_scope.handlers, [handler, other_handler])

    def test_register_clients(self):
        history_scope = HistoryRecorderScope()
        client = object()
        history_scope.register_client(client)
        self.assertEqual(history_scope.registered_scope_ids, [id(client)])

    def test_register_multiple_clients(self):
        history_scope = HistoryRecorderScope()
        client = object()
        other_client = object()
        history_scope.register_client(client)
        history_scope.register_client(other_client)
        self.assertEqual(
            history_scope.registered_scope_ids, [id(client), id(other_client)])


class TestGetHistoryRecorder(unittest.TestCase):
    def test_can_get_history_recorder(self):
        recorder = get_global_history_recorder()
        self.assertTrue(isinstance(recorder, HistoryRecorder))

    def test_does_reuse_history_recorder(self):
        recorder_1 = get_global_history_recorder()
        recorder_2 = get_global_history_recorder()
        self.assertIs(recorder_1, recorder_2)
