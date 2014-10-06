from tests import unittest

from nose.tools import assert_raises

from botocore import model


def test_missing_model_attribute_raises_exception():
    service_model = model.ServiceModel({'metadata': {}})

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
            raise AssertionError("Expected UndefinedModelAttributeError to "
                                 "be raised, but no exception was raised.")

    for name in ['endpoint_prefix', 'signing_name', 'api_version', 'protocol']:
        yield _test_attribute_raise_exception, name


class TestServiceModel(unittest.TestCase):

    def setUp(self):
        self.model = {
            'metadata': {'protocol': 'query'},
            'documentation': '',
            'operations': {},
            'shapes': {}
        }
        self.service_model = model.ServiceModel(self.model)

    def test_metadata_available(self):
        # You should be able to access the metadata in a service description
        # through the service model object.
        self.assertEqual(self.service_model.metadata.get('protocol'), 'query')

    def test_operation_does_not_exist(self):
        with self.assertRaises(model.OperationNotFoundError):
            self.service_model.operation_model('NoExistOperation')


class TestOperationModelFromService(unittest.TestCase):
    def setUp(self):
        self.model = {
            'metadata': {'protocol': 'query'},
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

    def test_operation_input_model(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        self.assertEqual(operation.name, 'OperationName')
        # Operations should also have a reference to the top level metadata.
        self.assertEqual(operation.metadata['protocol'], 'query')
        self.assertEqual(operation.http['method'], 'POST')
        self.assertEqual(operation.http['requestUri'], '/')
        shape = operation.input_shape
        self.assertEqual(shape.name, 'OperationNameRequest')
        self.assertEqual(list(sorted(shape.members)), ['Arg1', 'Arg2'])

    def test_operation_output_model(self):
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        output = operation.output_shape
        self.assertEqual(list(output.members), ['String'])
        self.assertFalse(operation.has_streaming_output)

    def test_operation_shape_not_required(self):
        # It's ok if there's no output shape. We'll just get a return value of
        # None.
        del self.model['operations']['OperationName']['output']
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        output_shape = operation.output_shape
        self.assertIsNone(output_shape)

    def test_streaming_output_for_operation(self):
        self.model = {
            'metadata': {'protocol': 'query'},
            'documentation': '',
            'operations': {
                'OperationName': {
                    'name': 'OperationName',
                    'output': {
                        'shape': 'OperationNameResponse',
                    },
                }
            },
            'shapes': {
                'OperationNameResponse': {
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
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        self.assertTrue(operation.has_streaming_output)

    def test_payload_thats_not_streaming(self):
        self.model = {
            'metadata': {'protocol': 'query'},
            'operations': {
                'OperationName': {
                    'name': 'OperationName',
                    'output': {
                        'shape': 'OperationNameResponse',
                    },
                }
            },
            'shapes': {
                'OperationNameResponse': {
                    'type': 'structure',
                    'members': {
                        'String': {
                            'shape': 'stringType',
                        },
                    },
                    'payload': 'String'
                },
                'stringType': {
                    'type': 'string',
                },
            }
        }
        service_model = model.ServiceModel(self.model)
        operation = service_model.operation_model('OperationName')
        self.assertFalse(operation.has_streaming_output)


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
        self.assertEqual(map_merged.serialization,
                          # member beats the definition.
                         {'name': 'Attribute',
                          # From the definition.
                          'flattened': True,})
        # Ensure we don't merge/mutate the original dicts.
        self.assertEqual(map_merged.key.serialization['name'], 'Name')
        self.assertEqual(map_merged.value.serialization['name'], 'Value')
        self.assertEqual(map_merged.key.serialization['name'], 'Name')

    def test_merges_copy_dict(self):
        shape = self.shape_resolver.get_shape_by_name('SetQueueAttributes')
        map_merged = shape.members['MapExample']
        self.assertEqual(map_merged.serialization.get('name'), 'Attribute')

        shape2 = self.shape_resolver.get_shape_by_name('SetQueueAttributes2')
        map_merged2 = shape2.members['MapExample']
        self.assertEqual(map_merged2.serialization.get('name'), 'Attribute2')


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
        self.assertEqual(shape.name, 'Foo')
        self.assertEqual(shape.type_name, 'structure')

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
        self.assertEqual(shape.name, 'StringType')
        self.assertEqual(shape.type_name, 'string')

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
        self.assertEqual(shape.serialization['name'], 'other')
        self.assertEqual(shape.name, 'StringType')

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
        self.assertEqual(shape.serialization['name'], 'other')
        # serialization is computed on demand, and a cache is kept.
        # This is just verifying that trying to access serialization again
        # gives the same result.  We don't actually care that it's cached,
        # we just care that the cache doesn't mess with correctness.
        self.assertEqual(shape.serialization['name'], 'other')

    def test_shape_overrides(self):
        shape_map = {
            "StringType": {
                "type": "string",
                "documentation": "Original documentation"
            }
        }
        resolver = model.ShapeResolver(shape_map)
        shape = resolver.get_shape_by_name('StringType')
        self.assertEqual(shape.documentation, 'Original documentation')

        shape = resolver.resolve_shape_ref({'shape': 'StringType',
                                            'documentation': 'override'})
        self.assertEqual(shape.documentation, 'override')

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
        self.assertEqual(shape.type_name, 'structure')
        self.assertEqual(shape.name, 'ChangePasswordRequest')
        self.assertEqual(list(sorted(shape.members)),
                         ['NewPassword', 'OldPassword'])
        self.assertEqual(shape.members['OldPassword'].name, 'passwordType')
        self.assertEqual(shape.members['OldPassword'].type_name, 'string')

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
        self.assertEqual(shape.metadata['required'],
                         ['OldPassword', 'NewPassword'])
        member = shape.members['OldPassword']
        self.assertEqual(member.metadata['min'], 1)
        self.assertEqual(member.metadata['max'], 128)
        self.assertEqual(member.metadata['sensitive'], True)

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
        self.assertEqual(shape.member.type_name, 'structure')
        self.assertEqual(shape.member.name, 'MFADevice')
        self.assertEqual(list(shape.member.members), ['UserName'])

    def test_shape_does_not_exist(self):
        resolver = model.ShapeResolver({})
        with self.assertRaises(model.NoShapeFoundError):
            resolver.get_shape_by_name('NoExistShape')

    def test_missing_type_key(self):
        shapes = {
            'UnknownType': {
                'NotTheTypeKey': 'someUnknownType'
            }
        }
        resolver = model.ShapeResolver(shapes)
        with self.assertRaises(model.InvalidShapeError):
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
        with self.assertRaises(model.InvalidShapeReferenceError):
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
        self.assertIn('StringType',
                      repr(resolver.get_shape_by_name('StringType')))


class TestBuilders(unittest.TestCase):

    def test_structure_shape_builder_with_scalar_types(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {'type': 'string'},
            'B': {'type': 'integer'},
        }).build_model()
        self.assertIsInstance(shape, model.StructureShape)
        self.assertEqual(sorted(list(shape.members)), ['A', 'B'])
        self.assertEqual(shape.members['A'].type_name, 'string')
        self.assertEqual(shape.members['B'].type_name, 'integer')

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
        self.assertIsInstance(shape, model.StructureShape)
        self.assertEqual(list(shape.members), ['A'])
        self.assertEqual(shape.members['A'].type_name, 'structure')
        self.assertEqual(list(shape.members['A'].members), ['A-1'])

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
        self.assertIsInstance(shape.members['A'], model.ListShape)
        self.assertEqual(shape.members['A'].member.type_name, 'string')

    def test_structure_shape_with_map_type(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'map',
                'key': {'type': 'string'},
                'value': {'type': 'string'},
            }
        }).build_model()
        self.assertIsInstance(shape.members['A'], model.MapShape)
        map_shape = shape.members['A']
        self.assertEqual(map_shape.key.type_name, 'string')
        self.assertEqual(map_shape.value.type_name, 'string')

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
        self.assertEqual(
            shape.members['A'].members['B'].members['C'].type_name, 'string')

    def test_enum_values_on_scalar_used(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'string',
                'enum': ['foo', 'bar', 'baz'],
            },
        }).build_model()
        self.assertIsInstance(shape, model.StructureShape)
        self.assertEqual(shape.members['A'].metadata['enum'],
                         ['foo', 'bar', 'baz'])

    def test_documentation_on_shape_used(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'string',
                'documentation': 'MyDocs',
            },
        }).build_model()
        self.assertEqual(shape.members['A'].documentation,
                         'MyDocs')

    def test_use_shape_name_when_provided(self):
        b = model.DenormalizedStructureBuilder()
        shape = b.with_members({
            'A': {
                'type': 'string',
                'shape_name': 'MyStringShape',
            },
        }).build_model()
        self.assertEqual(shape.members['A'].name, 'MyStringShape')

    def test_unknown_shape_type(self):
        b = model.DenormalizedStructureBuilder()
        with self.assertRaises(model.InvalidShapeError):
            b.with_members({
                'A': {
                    'type': 'brand-new-shape-type',
                },
            }).build_model()


if __name__ == '__main__':
    unittest.main()
