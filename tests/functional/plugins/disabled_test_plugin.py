class DisabledPluginModule:
    def __init__(self):
        self.invocations = 0

    def register_event(self, client):
        # Intentionally does nothing
        pass


plugin_instance = DisabledPluginModule()


def initialize_client_plugin(client):
    plugin_instance.register_event(client)
    return plugin_instance
