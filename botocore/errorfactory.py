import logging
import threading

from botocore.utils import CachedProperty
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class ServiceErrorFactory:
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

    def __getattr__(self, attr):
        if attr.startswith("_"):
            raise AttributeError(attr)
        if attr not in self._error_shapes:
            msg = 'Error "{0}" was not found in the service model'
            logger.warning(msg.format(attr))
        with self._lock:
            if attr not in self.__dict__:
                setattr(self, attr, type(attr, (ClientError, ), {}))
        return getattr(self, attr)

    def __dir__(self):
        return list(self._error_shapes)
