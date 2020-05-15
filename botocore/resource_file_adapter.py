"""
Provides an adapter layer that lets the user
arbitrarily operate against either files or
package resources (Python 3.7+) in a backwards
compatible manner.

This allows us to treat user-defined paths on
disk in a similar manner to files included in
the package that may be included in a binary
blob or zip file.

The functions are presented using names similar
to their more familiar os.* counterparts.

pkg://package_name/ is a "magic" reference that
refers to the root of this package, either on disk
for Python <3.7 or on disk or as a resource
for importlib.resources purposes.
"""
import os
import os.path

import botocore.compat

import importlib
try:
    import importlib.resources
except ImportError:
    importlib.resources = None


PACKAGE_SCHEME = 'pkg'


def _os_or_module_path_op(path_or_package, func):
    parsed = botocore.compat.urlparse(path_or_package)
    if parsed.scheme == PACKAGE_SCHEME:
        path_parts = split_path(parsed.path)
        # If importlib.resources isn't available, operate
        # relative to the root of the package name.
        lib = importlib.import_module(parsed.netloc)
        root = os.path.dirname(lib.__spec__.origin)
        path = os.path.join(root, *path_parts)
        return func(path)
    return func(path_or_package)


def split_path(path_or_package, parts=None):
    if parts is None:
        parts = []
    l, r = os.path.split(path_or_package)
    if r:
        parts.insert(0, r)
    if not l or l == '/':
        return parts
    return split_path(l, parts)


def read_text(path_or_package, encoding='utf-8'):
    parsed = botocore.compat.urlparse(path_or_package)
    if parsed.scheme == PACKAGE_SCHEME and importlib.resources is not None:
        path_parts = split_path(parsed.path)
        path_parts.insert(0, parsed.netloc)
        mod, resource = '.'.join(path_parts[:-1]), path_parts[-1]
        try:
            return importlib.resources.read_text(mod, resource, encoding=encoding)
        except ModuleNotFoundError:
            # TODO: Raise filenotfounderror
            return False
    with open(path_or_package, 'rb') as fp:
        payload = fp.read().decode(encoding)
        return payload


class PathAdapter(object):
    def isdir(self, path_or_package):
        """Return True if path_or_package is
        a directory or package."""
        parsed = botocore.compat.urlparse(path_or_package)
        if parsed.scheme == PACKAGE_SCHEME and importlib.resources is not None:
            path_parts = split_path(parsed.path)
            path_parts.insert(0, parsed.netloc)
            try:
                importlib.import_module('.'.join(path_parts))
                return True
            except ModuleNotFoundError:
                return False
        return _os_or_module_path_op(path_or_package, os.path.isdir)

    def isfile(self, path_or_package):
        """Return True if path_or_package is
        a file or resource."""
        parsed = botocore.compat.urlparse(path_or_package)
        if parsed.scheme == PACKAGE_SCHEME:
            if importlib.resources is not None:
                path_parts = split_path(parsed.path)
                path_parts.insert(0, parsed.netloc)
                mod, resource = '.'.join(path_parts[:-1]), path_parts[-1]
                try:
                    return importlib.resources.is_resource(mod, resource)
                except ModuleNotFoundError:
                    return False
        return _os_or_module_path_op(path_or_package, os.path.isfile)

    def exists(self, path_or_package):
        """Return True if path_or_package is
        a file, directory, resource or package."""
        return (
            self.isdir(path_or_package) or
            self.isfile(path_or_package) or
            os.path.exists(path_or_package)
        )

    def join(self, *paths_or_packages):
        """Emulates os.path.join behavior."""
        # TODO
        return os.path.join(*paths_or_packages)

    def expanduser(self, path):
        """Passthrough."""
        return os.path.expanduser(path)

    def expandvars(self, path):
        """Passthrough."""
        return os.path.expandvars(path)


# path_parts.insert(0, parsed.netloc)
# return importlib.resources.contents('.'.join(path_parts))
class OSAdapter(object):
    pathsep = os.pathsep

    def listdir(self, path_or_package):
        """Lists the contents of a directory
        or package."""
        parsed = botocore.compat.urlparse(path_or_package)
        if parsed.scheme == PACKAGE_SCHEME and importlib.resources is not None:
            path_parts = split_path(parsed.path)
            path_parts.insert(0, parsed.netloc)
            return importlib.resources.contents('.'.join(path_parts))
        return _os_or_module_path_op(path_or_package, os.listdir)

    def __init__(self):
        self.path = PathAdapter()


os_adapter = OSAdapter()