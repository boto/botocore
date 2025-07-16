from botocore import utils
from botocore.session import get_session
from tests import ClientHTTPStubber


class RecursivePluginModule:
    """A mock recursive plugin for testing nested client creation."""

    def __init__(self):
        self.called = False

    def register_event(self, client):
        client.meta.events.register(
            'before-call.dynamodb.*', self.create_client
        )

    def create_client(self, **kwargs):
        self.called = True
        session = get_session()
        client = utils.create_nested_client(
            session, "dynamodb", region_name="us-west-2"
        )
        with ClientHTTPStubber(client) as http_stubber:
            http_stubber.add_response(status=200, body=b'')
            client.list_tables()


plugin_instance = RecursivePluginModule()


def initialize_client_plugin(client):
    plugin_instance.register_event(client)
    return plugin_instance
