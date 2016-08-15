import sys
import botocore.exceptions


class ClientErrorFactory:
    ClientError = botocore.exceptions.ClientError
    __file__ = __file__
    __name__ = __name__
    __path__ = None
    __loader__ = None
    __all__ = [botocore.exceptions.ClientError]

    def __getattr__(self, attr):
        setattr(self, attr, type(attr, (self.ClientError, ), {}))
        return getattr(self, attr)

sys.modules[__name__] = ClientErrorFactory()
