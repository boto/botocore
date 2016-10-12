from nose.tools import assert_true, assert_equals, assert_raises

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
                'members': {},
                'error': {
                    'code': 'NoSuchResource'
                }
            }
        }
    }
    factory = ServiceErrorFactory(ServiceModel(model))
    assert_equals(dir(factory), ['NoSuchResourceException'])
    assert_true(issubclass(factory.NoSuchResourceException, ClientError))
    assert_raises(AttributeError, getattr, factory, "Foo")
    assert_true(factory.ClientError is ClientError)
    assert_raises(AttributeError, getattr, factory, "_foo")
    assert_true(issubclass(factory._from_code("NoSuchResource"),
                           factory.NoSuchResourceException))
