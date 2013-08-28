import glob
import os

from botocore import BOTOCORE_ROOT
from botocore.compat import json
from botocore.compat import OrderedDict
from botocore.exceptions import DataNotFoundError


class Loader(object):
    """
    A no-op base class, mostly to establish the protocol for loading
    the model data.
    """
    # TODO: Think about thread-safety here. Should this be a thread-local?
    _cache = {}

    def __init__(self, session):
        super(Loader, self).__init__()
        self.session = session

    def load_file(self, file_path):
        """
        Loads a regular data file (format-specific to subclass).

        This load is done uncached, so that you can always get the latest data
        as needed.

        .. warning::

            This method is not implemented here. Subclasses must override this
            method & provide a valid implementation.

        """
        raise NotImplementedError("Subclasses must implement 'load_file'.")

    def get_data(self, data_path):
        """
        Either loads a regular data file (format-specific to subclass) or
        returns previously loaded data from the cache.

        Returns a dictionary of data from the file.

        .. warning::

            This method is not implemented here. Subclasses must override this
            method & provide a valid implementation.

            They should also use the ``Loader.cachable`` decorator to cache the
            data.

        """
        raise NotImplementedError("Subclasses must implement 'get_data'.")

    def get_service_data(self, data_path, api_version=None):
        """
        Loads a given service's data.

        Requires a ``data_path`` parameter, which should be a string. This
        indicates the desired path to load, seperated by slashes. It should
        **NOT** include absolute path information nor file extensions. (i.e.
        ``aws/ec2``, not ``/botocore/data/aws/ec2/2010-01-01.json``)

        Optionally accepts an ``api_version`` parameter, which should be a
        string of the desired API version. This is used when you want to pin to
        a given API version rather than picking up the latest version.
        An example looks like ``2013-08-27``. Default is ``None``, which means
        pick the latest.

        .. note::

            Should use ``determine_latest`` to actually find the correct file
            path to load.

        Returns a dictionary of service data.

        .. warning::

            This method is not implemented here. Subclasses must override this
            method & provide a valid implementation.

            They should also use the ``Loader.cachable`` decorator to cache the
            data.

        """
        raise NotImplementedError(
            "Subclasses must implement 'get_service_data'."
        )

    def get_service_options(self, data_path):
        """
        Loads all the service options available.

        Requires a ``data_path`` parameter, which should be a string. This
        indicates the desired path to load, seperated by slashes if needed.

        .. warning::

            This method is not implemented here. Subclasses must override this
            method & provide a valid implementation.

            They should also use the ``Loader.cachable`` to cache the data.

        """
        raise NotImplementedError(
            "Subclasses must implement 'get_service_options'."
        )

    @classmethod
    def clear_cache(cls, key=None):
        """
        Clears either the entire cache or a given key from the cache.

        Called without parameters, it will clear out the entire cache.

        Optionally accepts ``key``, which should be a string. If provided, only
        the given key will be removed from the cache if found.
        Default is ``None``.
        """
        if key is None:
            cls._cache = {}
        else:
            try:
                del cls._cache[key]
            except KeyError:
                # It's not worth the error. We're just trying to make sure the
                # data isn't there, which it's not.
                pass

        return

    @staticmethod
    def cachable(func):
        """
        A convenient decorator for getting the data (either from the cache or
        populating the cache).

        Used primarily on the ``get_*`` methods. The ``load_file`` method should
        be left uncached, as a way to always get the freshest data.

        Usage::

            @Loader.cachable
            def get_service_data(self, service):
                data = self.load_file(self, 'aws/{0}'.format(service))
                return data

        """
        def _wrapper(self, key):
            cls = self.__class__

            if key in cls._cache:
                return cls._cache[key]

            data = func(key)
            cls._cache[key] = data
            return data


class JSONLoader(Loader):
    """
    A JSON-specific loader that uses the filesystem to load files.
    """
    def get_search_paths(self):
        """
        Return the all the paths that data could be found on when searching for
        files.

        Usage::

            # Default:
            >>> from botocore.session import Session
            >>> session = Session()
            >>> loader = JSONLoader(session)
            >>> loader.get_search_paths()
            [
                '/path/to/botocore/data',
            ]

            # User-added paths
            >>> session = Session(env_vars={
            ...     'data_path': '~/.botocore/my_overrides',
            ... })
            >>> loader = JSONLoader(session)
            >>> loader.get_search_paths()
            [
                '/home/somebody/.botocore/my_overrides',
                '/path/to/botocore/data',
            ]

        """
        paths = []

        # Now look for optional user-configured paths.
        # We keep the order in a familiar manner of traditional UNIX paths
        # (overrides first).
        search_path = session.get_variable('data_path')

        if search_path is not None:
            extra_paths = search_path.split(os.pathsep)

            for path in extra_paths:
                path = os.path.expandvars(path)
                path = os.path.expanduser(path)
                paths.append(path)

        # Automatically add ./botocore/data to the end of the
        # data search path.
        paths.append(os.path.join(BOTOCORE_ROOT, 'data'))
        return paths

    def load_file(self, file_path):
        """
        Loads a regular data file (format-specific to subclass).

        This load is done uncached, so that you can always get the latest data
        as needed.

        Usage::

            >>> from botocore.session import Session
            >>> session = Session()
            >>> loader = JSONLoader(session)
            >>> loader.load_file()
            {
                # ...JSON data...
            }

        """
        with open(file_path) as fp:
            return json.load(fp, object_pairs_hook=OrderedDict)

    @Loader.cachable
    def get_data(self, data_path):
        """
        Either loads a regular data file (format-specific to subclass) or
        returns previously loaded data from the cache.

        Returns a dictionary of data from the file.

        Usage::

            >>> from botocore.session import Session
            >>> session = Session()
            >>> loader = JSONLoader(session)
            >>> loader.get_data('aws/ec2/2013-02-01')
            {
                # ...EC2 service data...
            }
            >>> loader.get_data('_regions')
            {
                # ...Region data...
            }
        """
        data = {}
        data_found = False

        # We reverse the order, so that we attempt to load the data from
        # botocore itself first, then apply overrides.
        for possible_path in reversed(self.get_search_paths()):
            full_path = os.path.join(
                possible_path,
                data_path + '.json'
            )

            try:
                # Attempt loading it.
                found_data = self.load_file(full_path)
                data.update(found_data)
                data_found = True
            except IOError:
                # It wasn't there. Try the next path & hope for the best.
                continue

        if not data_found:
            raise DataNotFoundError(
                "No data could be found for path '{0}'.".format(data_path)
            )

        return data

    @Loader.cachable
    def get_service_data(self, data_path, api_version=None):
        """
        Loads a given service's data.

        Requires a ``data_path`` parameter, which should be a string. This
        indicates the desired path to load, seperated by slashes. It should
        **NOT** include absolute path information nor file extensions. (i.e.
        ``aws/ec2``, not ``/botocore/data/aws/ec2/2010-01-01.json``)

        Optionally accepts an ``api_version`` parameter, which should be a
        string of the desired API version. This is used when you want to pin to
        a given API version rather than picking up the latest version.
        An example looks like ``2013-08-27``. Default is ``None``, which means
        pick the latest.

        .. note::

            Should use ``determine_latest`` to actually find the correct file
            path to load.

        Returns a dictionary of service data.

        .. warning::

            This method is not implemented here. Subclasses must override this
            method & provide a valid implementation.

            They should also use the ``Loader.cachable`` decorator to cache the
            data.
        """
        raise NotImplementedError(
            "Subclasses must implement 'get_service_data'."
        )

    @Loader.cachable
    def get_service_options(self, data_path):
        """
        Loads all the service options available.

        Requires a ``data_path`` parameter, which should be a string. This
        indicates the desired path to load, seperated by slashes if needed.

        .. warning::

            This method is not implemented here. Subclasses must override this
            method & provide a valid implementation.

            They should also use the ``Loader.cachable`` to cache the data.
        """
        raise NotImplementedError(
            "Subclasses must implement 'get_service_options'."
        )

    def determine_latest(self, data_path, api_version=None):
        """
        For given desired data_path, searches all possible locations for the
        version of the data file that best matches.

        This is used for primarily for the service models themselves, which
        typically have an API version attached to them.

        Requires a ``data_path`` parameter, which should be a string. This
        indicates the desired path to load, seperated by slashes. It should
        **NOT** include absolute path information nor file extensions. (i.e.
        ``aws/ec2``, not ``/botocore/data/aws/ec2/2010-01-01.json``)

        Optionally accepts an ``api_version`` parameter, which should be a
        string of the desired API version. This is used when you want to pin to
        a given API version rather than picking up the latest version.
        An example looks like ``2013-08-27``. Default is ``None``, which means
        pick the latest.

        If the ``api_version`` desired can not be found, the loader will pick
        the next best match that is backward-compatible with the provided
        version. If a compatible version can not be found, an
        ``ApiVersionNotFound`` exception will be thrown.

            # Directory
            'aws'
            # Plain files
            'cli'
            'messages'
            'aws/_regions'
            # Directory, discovered version
            'aws/ec2'
            # Plain file
            'aws/ec2/2013-02-01'

        """
        # If we've got a version, toss it on the path & hope for the best.
        if api_version is not None:
            return os.path.join(data_path, api_version)

        # We don't have an api_version, so we'll need to find the latest
        # release.
        for base_path in botocore.base.get_search_path(self.session):
            path = os.path.join(base_path, data_path)

            if not os.path.exists(path):
                continue

            # If it's a directory, look inside for the right version.
            if not os.path.isdir(path):
                continue

            glob_exp = os.path.join(path, "*.json")
            # Reverse the list, so we can find the most recent
            # lexicographically.
            options = sorted(glob.glob(glob_exp), reverse=True)

            if not len(options):
                continue

            # Remove the extension.
            latest = os.path.splitext(options[0])[0]
            # Cut off the path.
            latest = latest.replace(base_path, '')

            # If the left-most character is a path separator,
            # remove that too.
            if latest[0] == os.path.sep:
                latest = latest[1:]

            # One last check. Ensure it looks roughly like a versioned file.
            # We need to do this in the case where someone is trying to
            # recursively load all files (like ``aws``).
            if not latest.count('-') == 2:
                continue

            return latest

        return data_path
