class SecondPluginModule:
    def __init__(self):
        self.invocations = 0

    def register_event(self, client):
        client.meta.events.register('before-call', self.increment_invocations)

    def increment_invocations(self, **kwargs):
        self.invocations += 1


plugin_instance = SecondPluginModule()


def initialize_client_plugin(client):
    plugin_instance.register_event(client)
    return plugin_instance
