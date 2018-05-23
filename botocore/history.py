# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import logging


HISTORY_RECORDER = None
logger = logging.getLogger(__name__)


class BaseHistoryHandler(object):
    """Handler to respond to events that are recorded from a HistoryRecorder

    All handlers that get added to a HistoryRecorder must subclass
    and implement the ``emit()`` method.
    """
    def emit(self, event_type, payload, source):
        """Emit a recorded event to the handler

        :type event_type: string
        :param event_type: The name of event to be emitted

        :type payload: any
        :param payload: The data associated to the event. This typically
            should be a dictionary with information relevant to the event

        :type source: string
        :param source: The source of the event. This is typically the name
            of the library (i.e. BOTOCORE, CLI, etc.)
        """
        raise NotImplementedError('emit()')


class HistoryRecorder(object):
    """Records events pertinent to a workflow"""
    def __init__(self):
        self._enabled = False
        self._handlers = []
        self._scopes = []

    def enable(self):
        """Enables the recorder to emit events to registered handlers

        By default, the record is **not** enabled.
        """
        self._enabled = True

    def disable(self):
        """Disables the recorder from emitting events to registered handlers

        By default, the record is **not** enabled.
        """
        self._enabled = False

    def add_handler(self, handler):
        """Adds a handler to listen to events from the recorder

        :type handler: BaseHistoryHandler
        :param handler: The handler to add to the history recorder. Even if the
            handler is added to the recorder, the recorder must be enabled
            for the handler's ``emit()`` to actually be called.
        """
        self._handlers.append(handler)

    def add_scope(self, scope):
        """Adds a scope to a history recorder

        :type scope: HistoryRecorderScope
        :param scope: The scope to add to the history recorder. Handlers that
            are added to the registered scope will only be called if the event
            came from a client registered to that scope
        """
        self._scopes.append(scope)

    def record(self, event_type, payload, source='BOTOCORE', scope_id=None):
        """Record an event and emit the event to attached handlers

        :type event_type: string
        :param event_type: The name of event to be emitted

        :type payload: any
        :param payload: The data associated to the event. This typically
            should be a dictionary with information relevant to the event

        :type source: string
        :param source: The source of the event. This is typically the name
            of the library (i.e. BOTOCORE, CLI, etc.)

        :type scope_id: string
        :param scope_id: An identifier used to determine if an event should
            be passed to a registered scope. If the identifier matches one
            of the registered idenitfiers of a registered scope. The event
            will be emitted to the handlers attached to that registered scope.
            If the value is None, no handlers of any of the registered scopes
            will have the event emitted to them.
        """
        if self._enabled:
            for handler in self._handlers:
                self._emit_event(handler, event_type, payload, source)
            if scope_id is not None:
                scopes = self._get_scopes_for_scope_id(scope_id)
                for scope in scopes:
                    for handler in scope.handlers:
                        self._emit_event(handler, event_type, payload, source)

    def _emit_event(self, handler, event_type, payload, source):
        try:
            handler.emit(event_type, payload, source)
        except Exception:
            # Never let the process die because we had a failure in
            # a record collection handler.
            logger.debug("Exception raised in %s.", handler,
                         exc_info=True)

    def _get_scopes_for_scope_id(self, scope_id):
        return [
            scope for scope in self._scopes
            if scope_id in scope.registered_scope_ids
        ]


class HistoryRecorderScope(object):
    """Scopes events from the history recorder

    This allows handlers to only be fired if the recorded event is associated
    to a particular scope instead of having the handler fired for all events
    generated from a history recorder
    """
    def __init__(self):
        self._registered_scope_ids = []
        self._handlers = []

    @property
    def handlers(self):
        """The handlers registered to the scope"""
        return self._handlers

    @property
    def registered_scope_ids(self):
        """The idenitifiers for which the scope's handlers will be fired for"""
        return self._registered_scope_ids

    def register_client(self, client):
        """Registers a client to the scope

        It will use the client's id as the scope identifier. So if the client
        id is passed in as the `scope_id` to a `HistoryRecoreder.record()`
        call, all handlers registered to this scope will be fired.
        """
        self._registered_scope_ids.append(id(client))

    def add_handler(self, handler):
        """Adds a handler to listen for events associated to this scope

        :type handler: BaseHistoryHandler
        :param handler: The handler to add to the scope. Handlers that
            are registered will only be called if the event recorded included
            an identifier registered to the scope
        """
        self._handlers.append(handler)


def get_global_history_recorder():
    """Retrieves a global history recorder to record events"""
    global HISTORY_RECORDER
    if HISTORY_RECORDER is None:
        HISTORY_RECORDER = HistoryRecorder()
    return HISTORY_RECORDER
