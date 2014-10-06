"""Abstractions to interact with service models."""
from botocore.utils import CachedProperty
from botocore.compat import OrderedDict


NOT_SET = object()


class NoShapeFoundError(Exception):
     pass


class InvalidShapeError(Exception):
    pass


class OperationNotFoundError(Exception):
    pass


class InvalidShapeReferenceError(Exception):
    pass


class Shape(object):
    """Object representing a shape from the service model."""
    # To simplify serialization logic, all shape params that are
    # related to serialization are moved from the top level hash into
    # a 'serialization' hash.  This list below contains the names of all
    # the attributes that should be moved.
    SERIALIZED_ATTRS = ['locationName', 'queryName', 'flattened', 'location',
                        'payload', 'streaming', 'timestampFormat',
                        'xmlNamespace', 'resultWrapper', 'xmlAttribute']
    METADATA_ATTRS = ['required', 'min', 'max', 'sensitive', 'enum']
    MAP_TYPE = OrderedDict

    def __init__(self, shape_name, shape_model, shape_resolver=None):
        self.name = shape_name
        self.type_name = shape_model['type']
        self.documentation = shape_model.get('documentation', '')
        self._shape_model = shape_model
        if shape_resolver is None:
            # If a shape_resolver is not provided, we create an object
            # that will throw errors if you attempt to resolve
            # a shape.  This is actually ok for scalar shapes
            # because they don't need to resolve shapes and shouldn't
            # be required to provide an object they won't use.
            shape_resolver = UnresolvableShapeMap()
        self._shape_resolver = shape_resolver
        self._cache = {}

    @CachedProperty
    def serialization(self):
        model = self._shape_model
        serialization = {}
        for attr in self.SERIALIZED_ATTRS:
            if attr in self._shape_model:
                serialization[attr] = model[attr]
        # For consistency, locationName is renamed to just 'name'.
        if 'locationName' in serialization:
            serialization['name'] = serialization.pop('locationName')
        return serialization

    @CachedProperty
    def metadata(self):
        model = self._shape_model
        metadata = {}
        for attr in self.METADATA_ATTRS:
            if attr in self._shape_model:
                metadata[attr] = model[attr]
        return metadata

    @CachedProperty
    def required_members(self):
        return self.metadata.get('required', [])

    def _resolve_shape_ref(self, shape_ref):
        return self._shape_resolver.resolve_shape_ref(shape_ref)

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__,
                             self.name)


class StructureShape(Shape):
    @CachedProperty
    def members(self):
        members = self._shape_model['members']
        # The members dict looks like:
        #    'members': {
        #        'MemberName': {'shape': 'shapeName'},
        #        'MemberName2': {'shape': 'shapeName'},
        #    }
        # We return a dict of member name to Shape object.
        shape_members = self.MAP_TYPE()
        for name, shape_ref in members.items():
            shape_members[name] = self._resolve_shape_ref(shape_ref)
        return shape_members


class ListShape(Shape):
    @CachedProperty
    def member(self):
        return self._resolve_shape_ref(self._shape_model['member'])


class MapShape(Shape):
    @CachedProperty
    def key(self):
        return self._resolve_shape_ref(self._shape_model['key'])

    @CachedProperty
    def value(self):
        return self._resolve_shape_ref(self._shape_model['value'])


class ServiceModel(object):
    """

    :ivar service_description: The parsed service description dictionary.

    """
    # Any type not in this mapping will default to the Shape class.
    SHAPE_CLASSES = {
        'structure': StructureShape,
        'list': ListShape,
        'map': MapShape,
    }
    def __init__(self, service_description):
        self._service_description = service_description
        # We want clients to be able to access metadata directly.
        self.metadata = service_description.get('metadata', {})
        self._shape_resolver = ShapeResolver(
            service_description.get('shapes', {}))
        self._signature_version = NOT_SET

    def shape_for(self, shape_name, member_traits=None):
        return self._shape_resolver.get_shape_by_name(
            shape_name, member_traits)

    def resolve_shape_ref(self, shape_ref):
        return self._shape_resolver.resolve_shape_ref(shape_ref)

    def operation_model(self, operation_name):
        try:
            model = self._service_description['operations'][operation_name]
        except KeyError:
            raise OperationNotFoundError(operation_name)
        return OperationModel(model, self)

    @CachedProperty
    def operation_names(self):
        return list(self._service_description['operations'])

    @CachedProperty
    def endpoint_prefix(self):
        return self.metadata['endpointPrefix']

    @CachedProperty
    def signing_name(self):
        """The name to use when computing signatures.

        If the model does not define a signing name, this
        value will be the endpoint prefix defined in the model.
        """
        signing_name = self.metadata.get('signingName')
        if signing_name is None:
            signing_name = self.endpoint_prefix
        return signing_name

    @CachedProperty
    def api_version(self):
        return self.metadata['apiVersion']

    @CachedProperty
    def protocol(self):
        return self.metadata['protocol']

    # Signature version is one of the rare properties
    # than can be modified so a CachedProperty is not used here.

    @property
    def signature_version(self):
        if self._signature_version is NOT_SET:
            signature_version = self.metadata.get('signatureVersion')
            self._signature_version = signature_version
        return self._signature_version

    @signature_version.setter
    def signature_version(self, value):
        self._signature_version = value


class OperationModel(object):
    def __init__(self, operation_model, service_model):
        self._operation_model = operation_model
        self._service_model = service_model
        # Clients can access '.name' to get the operation name
        # and '.metadata' to get the top level metdata of the service.
        self.name = operation_model.get('name')
        self.metadata = service_model.metadata
        self.http = operation_model.get('http', {})

    @CachedProperty
    def input_shape(self):
        if 'input' not in self._operation_model:
            # Some operations do not accept any input and do not define an
            # input shape.
            return None
        return self._service_model.resolve_shape_ref(
            self._operation_model['input'])

    @CachedProperty
    def output_shape(self):
        if 'output' not in self._operation_model:
            # Some operations do not define an output shape,
            # in which case we return None to indicate the
            # operation has no expected output.
            return None
        return self._service_model.resolve_shape_ref(
            self._operation_model['output'])

    @CachedProperty
    def has_streaming_output(self):
        output_shape = self.output_shape
        if output_shape is None:
            return False
        payload = output_shape.serialization.get('payload')
        if payload is not None:
            payload_shape = output_shape.members[payload]
            if payload_shape.type_name == 'blob':
                return True
        return False


class ShapeResolver(object):
    """Resolves shape references."""

    # Any type not in this mapping will default to the Shape class.
    SHAPE_CLASSES = {
        'structure': StructureShape,
        'list': ListShape,
        'map': MapShape,
    }

    def __init__(self, shape_map):
        self._shape_map = shape_map
        self._shape_cache = {}

    def get_shape_by_name(self, shape_name, member_traits=None):
        try:
            shape_model = self._shape_map[shape_name]
        except KeyError:
            raise NoShapeFoundError(shape_name)
        try:
            shape_cls = self.SHAPE_CLASSES.get(shape_model['type'], Shape)
        except KeyError:
            raise InvalidShapeError("Shape is missing required key 'type': %s"
                                    % shape_model)
        if member_traits:
            shape_model = shape_model.copy()
            shape_model.update(member_traits)
        return shape_cls(shape_name, shape_model, self)

    def resolve_shape_ref(self, shape_ref):
        # A shape_ref is a dict that has a 'shape' key that
        # refers to a shape name as well as any additional
        # member traits that are then merged over the shape
        # definition.  For example:
        # {"shape": "StringType", "locationName": "Foobar"}
        if len(shape_ref) == 1 and 'shape' in shape_ref:
            # It's just a shape ref with no member traits, we can avoid
            # a .copy().  This is the common case so it's specifically
            # called out here.
            return self.get_shape_by_name(shape_ref['shape'])
        else:
            member_traits = shape_ref.copy()
            try:
                shape_name = member_traits.pop('shape')
            except KeyError:
                raise InvalidShapeReferenceError(
                    "Invalid model, missing shape reference: %s" % shape_ref)
            return self.get_shape_by_name(shape_name, member_traits)


class UnresolvableShapeMap(object):
    """A ShapeResolver that will throw ValueErrors when shapes are resolved.
    """
    def get_shape_by_name(self, shape_name, member_traits=None):
        raise ValueError("Attempted to lookup shape '%s', but no shape "
                         "map was provided.")

    def resolve_shape_ref(self, shape_ref):
        raise ValueError("Attempted to resolve shape '%s', but no shape "
                         "map was provided.")
