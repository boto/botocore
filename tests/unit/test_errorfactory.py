import sys

from nose.tools import assert_equals, assert_true

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
    members = dir(factory)
    if sys.version_info >= (2, 7):
        assert_equals(members, ['NoSuchResourceException'])
    assert_true(issubclass(factory.NoSuchResourceException, ClientError))
    assert_true(issubclass(factory.Foo, ClientError))
