from tests import unittest
import pytest

from botocore import model
from botocore.compat import OrderedDict
from botocore.compat import six


def test_missing_model_attribute_raises_exception():
    # We're using a test generator here to cut down
    # on the duplication.  The property names below
    # all have the same test logic.
    service_model = model.ServiceModel({'metadata': {'endpointPrefix': 'foo'}})
    property_names = ['api_version', 'protocol']

    def _test_attribute_raise_exception(attr_name):
        try:
            getattr(service_model, attr_name)
        except model.UndefinedModelAttributeError:
            # This is what we expect, so the test passes.
            pass
        except Exception as e:
            raise AssertionError("Expected UndefinedModelAttributeError to "
                                 "be raised, but %s was raised instead" %
                                 (e.__class__))
        else:
            raise AssertionError(
                "Expected UndefinedModelAttributeError to "
                "be raised, but no exception was raised for: %s" % attr_name)

    for name in property_names:
        _test_attribute_raise_exception(name)


class TestServiceId(unittest.TestCase):
    def test_hypenize_replaces_spaces(self):
        assert model.ServiceId('my service').hyphenize() == 'my-service'

    def test_hyphenize_lower_cases(self):
        assert model.ServiceId('MyService').hyphenize() == 'myservice'


class TestServiceModel(unittest.TestCase):

    def setUp(self):
        self.model = {
            'metadata': {'protocol': 'query',
                         'endpointPrefix': 'endpoint-prefix',
                         'serviceId': 'MyService'},
            'documentation': 'Documentation value',
            'operations': {},
            'shapes': {
                'StringShape': {'type': 'string'}
            }
        }
        self.error_shapes = {
            'ExceptionOne': {
                'exception': True,
                'type': 'structure',
                'members': {},
            },
            'ExceptionTwo': {
                'exception': True,
                'type': 'structure',
                'members': {},
                'error': {
                    'code': 'FooCode'
                }
            },
        }
        self.service_model = model.ServiceModel(self.model)

    def test_metadata_available(self):
        # You should be able to access the metadata in a service description
        # through the service model object.
        assert self.service_model.metadata.get('protocol') == 'query'

    def test_service_name_can_be_overriden(self):
        service_model = model.ServiceModel(self.model,
                                           service_name='myservice')
        assert service_model.service_name == 'myservice'

    def test_service_name_defaults_to_endpoint_prefix(self):
        assert self.service_model.service_name == 'endpoint-prefix'

    def test_service_id(self):
        assert self.service_model.service_id == 'MyService'

    def test_hyphenize_service_id(self):
        assert self.service_model.service_id.hyphenize() == 'myservice'

    def test_service_id_does_not_exist(self):
        service_model = {
            'metadata': {
                'protocol': 'query',
                'endpointPrefix': 'endpoint-prefix',
            },
            'documentation': 'Documentation value',
            'operations': {},
            'shapes': {
                'StringShape': {'type': 'string'}
            }
        }
        service_name = 'myservice'
        service_model = model.ServiceModel(service_model, service_name)
        with pytest.raises(model.UndefinedModelAttributeError, match=service_name):
            service_model.service_id()

    def test_operation_does_not_exist(self):
        with self.assertRaises(model.OperationNotFoundError):
            self.service_model.operation_model('NoExistOperation')

    def test_signing_name_defaults_to_endpoint_prefix(self):
        assert self.service_model.signing_name == 'endpoint-prefix'

    def test_documentation_exposed_as_property(self):
        assert self.service_model.documentation == 'Documentation value'

    def test_shape_names(self):
        assert self.service_model.shape_names == ['StringShape']

    def test_repr_has_service_name(self):
        assert repr(self.service_model) == 'ServiceModel(endpoint-prefix)'

    def test_shape_for_error_code(self):
        self.model['shapes'].update(self.error_shapes)
        self.service_model = model.ServiceModel(self.model)
        shape = self.service_model.shape_for_error_code('ExceptionOne')
        assert shape.name == 'ExceptionOne'
        shape = self.service_model.shape_for_error_code('FooCode')
        assert shape.name == 'ExceptionTwo'

    def test_error_shapes(self):
        self.model['shapes'].update(self.error_shapes)
        self.service_model = model.ServiceModel(self.model)
        error_shapes = self.service_model.error_shapes
        error_shape_names = [shape.name for shape in error_shapes]
        assert len(error_shape_names) == 2
        assert 'ExceptionOne' in error_shape_names
        assert 'ExceptionTwo' in error_shape_names


class TestOperationModelFromService(unittest.TestCase):
    def setUp(self):
        self.model = {
            'metadata': {'protocol': 'query', 'endpointPrefix': 'foo'},
            'documentation': '',
            'operations': {
                'OperationName': {
                    'http': {
                        'method': 'POST',
                        'requestUri': '/',
                    },
                    'name': 'OperationName',
                    'input': {
                        'shape': 'OperationNameRequest'
                    },
                    'output': {
                        'shape': 'OperationNameResponse',
                    },
                    'errors': [{'shape': 'NoSuchResourceException'}],
                    'documentation': 'Docs for OperationName',
                    'authtype': 'v4'
                },
                'OperationTwo': {
                    'http': {
                        'method': 'POST',
                        'requestUri': '/',
                    },
                    'name': 'OperationTwo',
                    'input': {
                        'shape': 'OperationNameRequest'
                    },
                    'output': {
                        'shape': 'OperationNameResponse',
                    },
                    'errors': [{'shape': 'NoSuchResourceException'}],
                    'documentation': 'Docs for OperationTwo',
                }
            },
            'shapes': {
                'OperationNameRequest': {
                    'type': 'structure',
                    'members': {
                        'Arg1': {'shape': 'stringType'},
                        'Arg2': {'shape': 'stringType'},
                    }
                },
                'OperationNameResponse': {
                    'type': 'structure',
                    'members': {
                        'String': {
                            'shape': 'stringType',
                        }
                    }
                },
                'NoSuchResourceException': {
                    'type': 'structure',
                    'members': {}
                },
                'stringType': {
                    'type': 'string',
                }
            }
        }
        self.service_model = model.ServiceModel(self.model)

    def test_wire_name_always_matches_model(self):
        service_model = model.ServiceModel(self.model)
        operation = model.OperationModel(
            self.model['operations']['OperationName'], service_model, 'Foo')
        assert operation.name == 'Foo'
        assert operation.wire_name == 'OperationName'

    def test_operation_name_in_repr(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        self.assertIn('OperationName', repr(operation))

    def test_name_and_wire_name_defaults_to_same_value(self):
        service_model = model.ServiceModel(self.model)
        operation = model.OperationModel(
            self.model['operations']['OperationName'], service_model)
        assert operation.name == 'OperationName'
        assert operation.wire_name == 'OperationName'

    def test_name_from_service(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert operation.name == 'OperationName'

    def test_name_from_service_model_when_differs_from_name(self):
        self.model['operations']['Foo'] = \
            self.model['operations']['OperationName']
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('Foo')
        assert operation.name == 'Foo'

    def test_operation_input_model(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert operation.name == 'OperationName'
        # Operations should also have a reference to the top level metadata.
        assert operation.metadata['protocol'] == 'query'
        assert operation.http['method'] == 'POST'
        assert operation.http['requestUri'] == '/'
        shape = operation.input_shape
        assert shape.name == 'OperationNameRequest'
        assert list(sorted(shape.members)) == ['Arg1', 'Arg2']

    def test_has_documentation_property(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert operation.documentation == 'Docs for OperationName'

    def test_service_model_available_from_operation_model(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        # This is an identity comparison because we don't implement
        # __eq__, so we may need to change this in the future.
        assert operation.service_model == service_model

    def test_operation_output_model(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        output = operation.output_shape
        assert list(output.members) == ['String']
        assert not operation.has_streaming_output

    def test_operation_shape_not_required(self):
        # It's ok if there's no output shape. We'll just get a return value of
        # None.
        del self.model['operations']['OperationName']['output']
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        output_shape = operation.output_shape
        assert output_shape is None

    def test_error_shapes(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        # OperationName only has a NoSuchResourceException
        assert len(operation.error_shapes) == 1
        assert operation.error_shapes[0].name == 'NoSuchResourceException'

    def test_has_auth_type(self):
        operation = self.service_model.operation_model('OperationName')
        assert operation.auth_type == 'v4'

    def test_auth_type_not_set(self):
        operation = self.service_model.operation_model('OperationTwo')
        assert operation.auth_type is None

    def test_deprecated_present(self):
        self.model['operations']['OperationName']['deprecated'] = True
        service_model = model.ServiceModel(self.model)
        operation_name = service_model.operation_model('OperationName')
        assert operation_name.deprecated

    def test_deprecated_present_false(self):
        self.model['operations']['OperationName']['deprecated'] = False
        service_model = model.ServiceModel(self.model)
        operation_name = service_model.operation_model('OperationName')
        assert not operation_name.deprecated

    def test_deprecated_absent(self):
        service_model = model.ServiceModel(self.model)
        operation_two = service_model.operation_model('OperationTwo')
        assert not operation_two.deprecated

    def test_endpoint_operation_present(self):
        self.model['operations']['OperationName']['endpointoperation'] = True
        service_model = model.ServiceModel(self.model)
        operation_name = service_model.operation_model('OperationName')
        assert operation_name.is_endpoint_discovery_operation

    def test_endpoint_operation_present_false(self):
        self.model['operations']['OperationName']['endpointoperation'] = False
        service_model = model.ServiceModel(self.model)
        operation_name = service_model.operation_model('OperationName')
        assert not operation_name.is_endpoint_discovery_operation

    def test_endpoint_operation_absent(self):
        operation_two = self.service_model.operation_model('OperationName')
        assert not operation_two.is_endpoint_discovery_operation

    def test_endpoint_discovery_required(self):
        operation = self.model['operations']['OperationName']
        operation['endpointdiscovery'] = {'required': True}
        service_model = model.ServiceModel(self.model)
        assert service_model.endpoint_discovery_required

    def test_endpoint_discovery_required_false(self):
        self.model['operations']['OperationName']['endpointdiscovery'] = {}
        service_model = model.ServiceModel(self.model)
        assert not service_model.endpoint_discovery_required

    def test_endpoint_discovery_required_no_value(self):
        operation = self.model['operations']['OperationName']
        assert operation.get('endpointdiscovery') is None
        service_model = model.ServiceModel(self.model)
        assert not service_model.endpoint_discovery_required

    def test_endpoint_discovery_present(self):
        operation = self.model['operations']['OperationName']
        operation['endpointdiscovery'] = {'required': True}
        service_model = model.ServiceModel(self.model)
        operation_name = service_model.operation_model('OperationName')
        assert operation_name.endpoint_discovery.get('required')

    def test_endpoint_discovery_absent(self):
        operation_name = self.service_model.operation_model('OperationName')
        assert operation_name.endpoint_discovery is None


class TestOperationModelEventStreamTypes(unittest.TestCase):
    def setUp(self):
        super(TestOperationModelEventStreamTypes, self).setUp()
        self.model = {
            'metadata': {'protocol': 'rest-xml', 'endpointPrefix': 'foo'},
            'documentation': '',
            'operations': {
                'OperationName': {
                    'http': {
                        'method': 'POST',
                        'requestUri': '/',
                    },
                    'name': 'OperationName',
                    'input': {'shape': 'OperationRequest'},
                    'output': {'shape': 'OperationResponse'},
                }
            },
            'shapes': {
                'NormalStructure': {
                    'type': 'structure',
                    'members': {
                        'Input': {'shape': 'StringType'}
                    }
                },
                'OperationRequest': {
                    'type': 'structure',
                    'members': {
                        'String': {'shape': 'StringType'},
                        "Body": {'shape': 'EventStreamStructure'}
                    },
                    'payload': 'Body'
                },
                'OperationResponse': {
                    'type': 'structure',
                    'members': {
                        'String': {'shape': 'StringType'},
                        "Body": {'shape': 'EventStreamStructure'}
                    },
                    'payload': 'Body'
                },
                'StringType': {'type': 'string'},
                'BlobType': {'type': 'blob'},
                'EventStreamStructure': {
                    'eventstream': True,
                    'type': 'structure',
                    'members': {
                        'EventA': {'shape': 'EventAStructure'},
                        'EventB': {'shape': 'EventBStructure'}
                    }
                },
                'EventAStructure': {
                    'event': True,
                    'type': 'structure',
                    'members': {
                        'Payload': {
                            'shape': 'BlobType',
                            'eventpayload': True
                        },
                        'Header': {
                            'shape': 'StringType',
                            'eventheader': True
                        }
                    }
                },
                'EventBStructure': {
                    'event': True,
                    'type': 'structure',
                    'members': {
                        'Records': {'shape': 'StringType'}
                    }
                }
            }
        }

    def update_operation(self, **kwargs):
        operation = self.model['operations']['OperationName']
        operation.update(kwargs)

    def test_event_stream_input_for_operation(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert operation.has_event_stream_input
        event_stream_input = operation.get_event_stream_input()
        assert event_stream_input.name == 'EventStreamStructure'

    def test_no_event_stream_input_for_operation(self):
        self.update_operation(input={'shape': 'NormalStructure'})
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert not operation.has_event_stream_input
        assert operation.get_event_stream_input() is None

    def test_event_stream_output_for_operation(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert operation.has_event_stream_output
        output = operation.get_event_stream_output()
        assert output.name == 'EventStreamStructure'

    def test_no_event_stream_output_for_operation(self):
        self.update_operation(output={'shape': 'NormalStructure'})
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert not operation.has_event_stream_output
        assert operation.get_event_stream_output() is None

    def test_no_output_shape(self):
        self.update_operation(output=None)
        del self.model['operations']['OperationName']['output']
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert not operation.has_event_stream_output
        assert operation.get_event_stream_output() is None


class TestOperationModelStreamingTypes(unittest.TestCase):
    def setUp(self):
        super(TestOperationModelStreamingTypes, self).setUp()
        self.model = {
            'metadata': {'protocol': 'query', 'endpointPrefix': 'foo'},
            'documentation': '',
            'operations': {
                'OperationName': {
                    'name': 'OperationName',
                    'input': {
                        'shape': 'OperationRequest',
                    },
                    'output': {
                        'shape': 'OperationResponse',
                    },
                }
            },
            'shapes': {
                'OperationRequest': {
                    'type': 'structure',
                    'members': {
                        'String': {
                            'shape': 'stringType',
                        },
                        "Body": {
                            'shape': 'blobType',
                        }
                    },
                    'payload': 'Body'
                },
                'OperationResponse': {
                    'type': 'structure',
                    'members': {
                        'String': {
                            'shape': 'stringType',
                        },
                        "Body": {
                            'shape': 'blobType',
                        }
                    },
                    'payload': 'Body'
                },
                'stringType': {
                    'type': 'string',
                },
                'blobType': {
                    'type': 'blob'
                }
            }
        }

    def remove_payload(self, type):
        self.model['shapes']['Operation' + type].pop('payload')

    def test_streaming_input_for_operation(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert operation.has_streaming_input
        assert operation.get_streaming_input().name == 'blobType'

    def test_not_streaming_input_for_operation(self):
        self.remove_payload('Request')
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert not operation.has_streaming_input
        assert operation.get_streaming_input() is None

    def test_streaming_output_for_operation(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert operation.has_streaming_output
        assert operation.get_streaming_output().name == 'blobType'

    def test_not_streaming_output_for_operation(self):
        self.remove_payload('Response')
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        assert not operation.has_streaming_output
        assert operation.get_streaming_output() is None


class TestDeepMerge(unittest.TestCase):
    def setUp(self):
        self.shapes = {
            'SetQueueAttributes': {
                'type': 'structure',
                'members': {
                    'MapExample': {'shape': 'StrToStrMap',
                                   'locationName': 'Attribute'},
                }
            },
            'SetQueueAttributes2': {
                'type': 'structure',
                'members': {
                    'MapExample': {'shape': 'StrToStrMap',
                                   'locationName': 'Attribute2'},
                }
            },
            'StrToStrMap': {
                'type': 'map',
                'key': {'shape': 'StringType', 'locationName': 'Name'},
                'value': {'shape': 'StringType', 'locationName': 'Value'},
                'flattened': True,
                'name': 'NotAttribute',
            },
            'StringType': {'type': 'string'}
        }
        self.shape_resolver = model.ShapeResolver(self.shapes)

    def test_deep_merge(self):
        shape = self.shape_resolver.get_shape_by_name('SetQueueAttributes')
        map_merged = shape.members['MapExample']
        # map_merged has a serialization as a member trait as well as
        # in the StrToStrMap.
        # The member trait should have precedence.
        assert map_merged.serialization == {
                         # member beats the definition.
                         'name': 'Attribute',
                          # From the definition.
                          'flattened': True,}
        # Ensure we don't merge/mutate the original dicts.
        assert map_merged.key.serialization['name'] == 'Name'
        assert map_merged.value.serialization['name'] == 'Value'
        assert map_merged.key.serialization['name'] == 'Name'

    def test_merges_copy_dict(self):
        shape = self.shape_resolver.get_shape_by_name('SetQueueAttributes')
        map_merged = shape.members['MapExample']
        assert map_merged.serialization.get('name') == 'Attribute'

        shape2 = self.shape_resolver.get_shape_by_name('SetQueueAttributes2')
        map_merged2 = shape2.members['MapExample']
        assert map_merged2.serialization.get('name') == 'Attribute2'


class TestShapeResolver(unittest.TestCase):
    def test_get_shape_by_name(self):
        shape_map = {
            'Foo': {
                'type': 'structure',
                'members': {
                    'Bar': {'shape': 'StringType'},
                    'Baz': {'shape': 'StringType'},
                }
            },
            "StringType": {
                "type": "string"
            }
        }
        resolver = model.ShapeResolver(shape_map)
        shape = resolver.get_shape_by_name('Foo')
        assert shape.name == 'Foo'
        assert shape.type_name == 'structure'

    def test_resolve_shape_reference(self):
        shape_map = {
            'Foo': {
                'type': 'structure',
                'members': {
                    'Bar': {'shape': 'StringType'},
                    'Baz': {'shape': 'StringType'},
                }
            },
            "StringType": {
                "type": "string"
            }
        }
        resolver = model.ShapeResolver(shape_map)
        shape = resolver.resolve_shape_ref({'shape': 'StringType'})
        assert shape.name == 'StringType'
        assert shape.type_name == 'string'

    def test_resolve_shape_references_with_member_traits(self):
        shape_map = {
            'Foo': {
                'type': 'structure',
                'members': {
                    'Bar': {'shape': 'StringType'},
                    'Baz': {'shape': 'StringType', 'locationName': 'other'},
                }
            },
            "StringType": {
                "type": "string"
            }
        }
        resolver = model.ShapeResolver(shape_map)
        shape = resolver.resolve_shape_ref({'shape': 'StringType',
                                            'locationName': 'other'})
        assert shape.serialization['name'] == 'other'
        assert shape.name == 'StringType'

    def test_serialization_cache(self):
        shape_map = {
            'Foo': {
                'type': 'structure',
                'members': {
                    'Baz': {'shape': 'StringType', 'locationName': 'other'},
                }
            },
            "StringType": {
                "type": "string"
            }
        }
        resolver = model.ShapeResolver(shape_map)
        shape = resolver.resolve_shape_ref({'shape': 'StringType',
                                            'locationName': 'other'})
        assert shape.serialization['name'] == 'other'
        # serialization is computed on demand, and a cache is kept.
        # This is just verifying that trying to access serialization again
        # gives the same result.  We don't actually care that it's cached,
        # we just care that the cache doesn't mess with correctness.
        assert shape.serialization['name'] == 'other'

    def test_shape_overrides(self):
        shape_map = {
            "StringType": {
                "type": "string",
                "documentation": "Original documentation"
            }
        }
        resolver = model.ShapeResolver(shape_map)
        shape = resolver.get_shape_by_name('StringType')
        assert shape.documentation == 'Original documentation'

        shape = resolver.resolve_shape_ref({'shape': 'StringType',
                                            'documentation': 'override'})
        assert shape.documentation == 'override'

    def test_shape_type_structure(self):
        shapes = {
            'ChangePasswordRequest': {
                'type': 'structure',
                'members': {
                    'OldPassword': {'shape': 'passwordType'},
                    'NewPassword': {'shape': 'passwordType'},
                }
            },
            'passwordType': {
                "type":"string",
            }
        }
        resolver = model.ShapeResolver(shapes)
        shape = resolver.get_shape_by_name('ChangePasswordRequest')
        assert shape.type_name == 'structure'
        assert shape.name == 'ChangePasswordRequest'
        assert list(sorted(shape.members)) == ['NewPassword', 'OldPassword']
        assert shape.members['OldPassword'].name == 'passwordType'
        assert shape.members['OldPassword'].type_name == 'string'
        assert shape.error_code is None

    def test_exception_error_code(self):
        shapes = {
            'FooException': {
                'exception': True,
                'type': 'structure',
                'members': {}
            }
        }
        # Test without explicit error code
        resolver = model.ShapeResolver(shapes)
        shape = resolver.get_shape_by_name('FooException')
        assert shape.metadata['exception']
        assert shape.error_code == 'FooException'
        # Test with explicit error code
        shapes['FooException']['error'] = {'code': 'ExceptionCode'}
        resolver = model.ShapeResolver(shapes)
        shape = resolver.get_shape_by_name('FooException')
        assert shape.metadata['exception']
        assert shape.error_code == 'ExceptionCode'

    def test_shape_metadata(self):
        shapes = {
            'ChangePasswordRequest': {
                'type': 'structure',
                'required': ['OldPassword', 'NewPassword'],
                'members': {
                    'OldPassword': {'shape': 'passwordType'},
                    'NewPassword': {'shape': 'passwordType'},
                }
            },
            'passwordType': {
                "type":"string",
                "min":1,
                "max":128,
                "sensitive":True
            }
        }
        resolver = model.ShapeResolver(shapes)
        shape = resolver.get_shape_by_name('ChangePasswordRequest')
        assert shape.metadata['required'] == ['OldPassword', 'NewPassword']
        member = shape.members['OldPassword']
        assert member.metadata['min'] == 1
        assert member.metadata['max'] == 128
        assert member.metadata['sensitive']

    def test_error_shape_metadata(self):
        shapes = {
            'ResourceNotFoundException': {
                'type': 'structure',
                'members': {
                    'message': {
                        'shape': 'ErrorMessage',
                    }
                },
                'exception': True,
                'retryable': {'throttling': True}
            }
        }
        resolver = model.ShapeResolver(shapes)
        shape = resolver.get_shape_by_name('ResourceNotFoundException')
        assert shape.metadata == {
            'exception': True, 'retryable': {'throttling': True}}

    def test_shape_list(self):
        shapes = {
            'mfaDeviceListType': {
                "type":"list",
                "member": {"shape": "MFADevice"},
            },
            'MFADevice': {
                'type': 'structure',
                'members': {
                    'UserName': {'shape': 'userNameType'}
                }
            },
            'userNameType': {
                'type': 'string'
            }
        }
        resolver = model.ShapeResolver(shapes)
        shape = resolver.get_shape_by_name('mfaDeviceListType')
        assert shape.member.type_name == 'structure'
        assert shape.member.name == 'MFADevice'
        assert list(shape.member.members) == ['UserName']

    def test_shape_does_not_exist(self):
        resolver = model.ShapeResolver({})
        with pytest.raises(model.NoShapeFoundError):
            resolver.get_shape_by_name('NoExistShape')

    def test_missing_type_key(self):
        shapes = {
            'UnknownType': {
                'NotTheTypeKey': 'someUnknownType'
            }
        }
        resolver = model.ShapeResolver(shapes)
        with pytest.raises(model.InvalidShapeError):
            resolver.get_shape_by_name('UnknownType')

    def test_bad_shape_ref(self):
        # This is an example of a denormalized model,
        # which should raise an exception.
        shapes = {
            'Struct': {
                'type': 'structure',
                'members': {
                    'A': {'type': 'string'},
                    'B': {'type': 'string'},
                }
            }
        }
        resolver = model.ShapeResolver(shapes)
        with pytest.raises(model.InvalidShapeReferenceError):
            struct = resolver.get_shape_by_name('Struct')
            # Resolving the members will fail because
            # the 'A' and 'B' members are not shape refs.
            struct.members

    def test_shape_name_in_repr(self):
        shapes = {
            'StringType': {
                'type': 'string',
            }
        }
        resolver = model.ShapeResolver(shapes)
        assert 'StringType' in repr(resolver.get_shape_by_name('StringType'))


class TestBuilders(unittest.TestCase):

    def test_structure_shape_builder_with_scalar_types(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {'type': 'string'},
            'B': {'type': 'integer'},
        }).build_model()
        assert isinstance(shape, model.StructureShape)
        assert sorted(list(shape.members)) == ['A', 'B']
        assert shape.members['A'].type_name == 'string'
        assert shape.members['B'].type_name == 'integer'

    def test_structure_shape_with_structure_type(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'structure',
                'members': {
                    'A-1': {'type': 'string'},
                }
            },
        }).build_model()
        assert isinstance(shape, model.StructureShape)
        assert list(shape.members) == ['A']
        assert shape.members['A'].type_name == 'structure'
        assert list(shape.members['A'].members) == ['A-1']

    def test_structure_shape_with_list(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'list',
                'member': {
                    'type': 'string'
                }
            },
        }).build_model()
        assert isinstance(shape.members['A'], model.ListShape)
        assert shape.members['A'].member.type_name == 'string'

    def test_structure_shape_with_map_type(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'map',
                'key': {'type': 'string'},
                'value': {'type': 'string'},
            }
        }).build_model()
        assert isinstance(shape.members['A'], model.MapShape)
        map_shape = shape.members['A']
        assert map_shape.key.type_name == 'string'
        assert map_shape.value.type_name == 'string'

    def test_nested_structure(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'structure',
                'members': {
                    'B': {
                        'type': 'structure',
                        'members': {
                            'C': {
                                'type': 'string',
                            }
                        }
                    }
                }
            }
        }).build_model()
        assert shape.members['A'].members['B'].members['C'].type_name == 'string'

    def test_enum_values_on_string_used(self):
        b = model.DenormalizedStructureBuilder()
        enum_values = ['foo', 'bar', 'baz']
        shape = b.with_members({
            'A': {
                'type': 'string',
                'enum': enum_values,
            },
        }).build_model()
        assert isinstance(shape, model.StructureShape)
        string_shape = shape.members['A']
        assert isinstance(string_shape, model.StringShape)
        assert string_shape.metadata['enum'] == enum_values
        assert string_shape.enum == enum_values

    def test_documentation_on_shape_used(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'string',
                'documentation': 'MyDocs',
            },
        }).build_model()
        assert shape.members['A'].documentation == 'MyDocs'

    def test_min_max_used_in_metadata(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'string',
                'documentation': 'MyDocs',
                'min': 2,
                'max': 3,
            },
        }).build_model()
        metadata = shape.members['A'].metadata
        assert metadata.get('min') == 2
        assert metadata.get('max') == 3

    def test_use_shape_name_when_provided(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'string',
                'shape_name': 'MyStringShape',
            },
        }).build_model()
        assert shape.members['A'].name == 'MyStringShape'

    def test_unknown_shape_type(self):
        b = model.DenormalizedStructureBuilder()
        with pytest.raises(model.InvalidShapeError):
            b.with_members({
                'A': {
                    'type': 'brand-new-shape-type',
                },
            }).build_model()

    def test_ordered_shape_builder(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members(OrderedDict(
            [
                ('A', {
                    'type': 'string'
                }),
                ('B', {
                    'type': 'structure',
                    'members': OrderedDict(
                        [
                            ('C', {
                                'type': 'string'
                            }),
                            ('D', {
                                'type': 'string'
                            })
                        ]
                    )
                })
            ]
        )).build_model()

        # Members should be in order
        assert list(shape.members.keys()) == ['A', 'B']

        # Nested structure members should *also* stay ordered
        assert list(shape.members['B'].members.keys()) == ['C', 'D']


if __name__ == '__main__':
    unittest.main()
