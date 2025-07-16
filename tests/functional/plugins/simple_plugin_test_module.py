class TestPluginModule:
    """A mock plugin module for testing client plugin loading."""

    def __init__(self):
        self.events_seen = []

    def register_event(self, client):
        client.meta.events.register('before-call', self.increment_calls)

    def increment_calls(self, **kwargs):
        self.events_seen.append(kwargs)


plugin_instance = TestPluginModule()


def initialize_client_plugin(client):
    plugin_instance.register_event(client)
    return plugin_instance
