from nose.tools import assert_true, assert_equals

from botocore.exceptions import ClientError
from botocore.errorfactory import ServiceErrorFactory
from botocore.model import ServiceModel


def test_errorfactory():
    model = {
        'operations': {
            'OperationName': {
                'name': 'OperationName',
                'errors': [{'shape': 'NoSuchResourceException'}],
            }
        },
        'shapes': {
            'NoSuchResourceException': {
                'type': 'structure',
                'members': {}
            }
        }
    }
    factory = ServiceErrorFactory(ServiceModel(model))
    assert_equals(dir(factory), ['NoSuchResourceException'])
    assert_true(issubclass(factory.NoSuchResourceException, ClientError))
    assert_true(issubclass(factory.Foo, ClientError))
    assert_true(factory.ClientError is ClientError)
