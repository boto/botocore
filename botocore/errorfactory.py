import threading

from botocore.utils import CachedProperty
from botocore.exceptions import ClientError


class ServiceErrorFactory(object):
    ClientError = ClientError

    def __init__(self, service_model):
        self._service_model = service_model
        self._lock = threading.Lock()

    @CachedProperty
    def _error_shapes(self):
        shapes = {}
        for op_name in self._service_model.operation_names:
            op_model = self._service_model.operation_model(op_name)
            for shape in op_model.error_shapes:
                shapes[shape.name] = shape
        return shapes

    @CachedProperty
    def _error_shapes_by_code(self):
        shapes = {}
        for shape in self._error_shapes.values():
            if shape._shape_model.get("error", {}).get("code"):
                shapes[shape._shape_model["error"]["code"]] = shape
        return shapes

    def _from_code(self, code):
        if code in self._error_shapes_by_code:
            return getattr(self, self._error_shapes_by_code[code].name)
        else:
            return getattr(self, code, ClientError)

    def __getattr__(self, attr):
        if attr.startswith("_"):
            raise AttributeError(attr)
        if attr not in self._error_shapes:
            raise AttributeError(attr)
        with self._lock:
            if attr not in self.__dict__:
                setattr(self, attr, type(attr, (ClientError, ), {}))
        return getattr(self, attr)

    def __dir__(self):
        return list(str(shape) for shape in self._error_shapes)
