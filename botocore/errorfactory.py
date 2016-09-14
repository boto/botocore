from botocore.utils import CachedProperty
from botocore.exceptions import ClientError


class ServiceErrorFactory:
    def __init__(self, service_model):
        self._service_model = service_model

    @CachedProperty
    def _error_shapes(self):
        shapes = {}
        for op_name in self._service_model.operation_names:
            op_model = self._service_model.operation_model(op_name)
            for shape in op_model.error_shapes:
                shapes[shape.name] = shape
        return shapes

    def __getattr__(self, attr):
        if attr in self._error_shapes:
            setattr(self, attr, type(attr, (ClientError, ), {}))
            return getattr(self, attr)
        raise AttributeError(attr)

    def __dir__(self):
        return list(self._error_shapes)
