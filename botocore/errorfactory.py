import sys


class ClientErrorFactory:
    cache = {}
    _file = __file__

    def __getattr__(self, attr):
        if attr == '__all__':
            return list(self.cache)
        if attr == '__file__':
            return self._file
        if attr == '__path__' or attr == '__loader__':
            return None
        if attr not in self.cache:
            from botocore.exceptions import ClientError
            self.cache[attr] = type(attr, (ClientError, ), {})
        return self.cache[attr]

sys.modules[__name__] = ClientErrorFactory()
