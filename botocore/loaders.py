import glob
import os

from botocore import BOTOCORE_ROOT
from botocore.compat import json
from botocore.compat import OrderedDict
from botocore.exceptions import ApiVersionNotFound
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
        def _wrapper(self, orig_key, **kwargs):
            cls = self.__class__
            key = orig_key

            # Make the full key, including all kwargs.
            # Sort them to prevent hash randomization from creating accidental
            # cache misses.
            for name in sorted(kwargs.keys()):
                key += '/{0}/{1}'.format(
                    name,
                    kwargs[name]
                )

            if key in cls._cache:
                return cls._cache[key]

            data = func(self, orig_key, **kwargs)
            cls._cache[key] = data
            return data

        return _wrapper


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
        search_path = self.session.get_variable('data_path')

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
        # Here, we'll cache it.
        return self._get_data(data_path)

    def _get_data(self, data_path):
        # This is the uncached version for use with ``get_service_data``.

        # Per the original behavior, this builds the data & updates/overrides
        # it as it goes.
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
            raise DataNotFoundError(data_path=data_path)

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

        Returns a dictionary of service data.

        Usage::

            >>> from botocore.session import Session
            >>> session = Session()
            >>> loader = JSONLoader(session)
            >>> loader.get_service_data('aws/ec2')
            {
                # ...The latest EC2 service data...
            }
            >>> loader.get_service_data('aws/ec2', api_version='2013-02-01')
            {
                # ...The EC2 service data for version 2013-02-01...
            }

        """
        actual_data_path = self.determine_latest(
            data_path,
            api_version=api_version
        )

        # Use the private method, so that we don't double-cache.
        return self._get_data(actual_data_path)

    @Loader.cachable
    def get_service_options(self, data_path):
        """
        Loads all the service options available.

        Requires a ``data_path`` parameter, which should be a string. This
        indicates the desired path to load, seperated by slashes if needed.

        Returns a list of service names.

        Usage::

            >>> from botocore.session import Session
            >>> session = Session()
            >>> loader = JSONLoader(session)
            >>> loader.get_service_options('aws')
            [
                'autoscaling',
                'cloudformation',
                # ...
            ]

        """
        options = []

        for possible_path in self.get_search_paths():
            option_glob = os.path.join(possible_path, data_path, '*')

            for possible_option in glob.glob(option_glob):
                if os.path.isdir(possible_option):
                    options.append(os.path.basename(possible_option))

        return options

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

        Usage::

            >>> from botocore.session import Session
            >>> session = Session()
            >>> loader = JSONLoader(session)

            # Just grabs the latest.
            >>> loader.determine_latest('aws/rds')
            'aws/rds/2013-05-15'

            # Grabs the matching version.
            >>> loader.determine_latest('aws/rds', api_version='2013-02-12')
            'aws/rds/2013-02-12'

            # Finds the best match.
            >>> loader.determine_latest('aws/rds', api_version='2013-01-31')
            'aws/rds/2013-01-10'

            # Couldn't find a match.
            >>> loader.determine_latest('aws/rds', api_version='2010-05-16')
            # Traceback, then...
            ApiVersionNotFound: Unable to load data aws/rds for: 2010-05-16

        """
        all_options = []
        best_match = None

        # Hunt down the options.
        for base_path in self.get_search_paths():
            path = os.path.join(base_path, data_path)

            # If it doesn't exist, skip it (might be in a later path).
            if not os.path.exists(path):
                continue

            # If it's not a directory, we're not going to find versions.
            # Carry on.
            if not os.path.isdir(path):
                continue

            # If it's a directory, look inside for the right version.
            glob_exp = os.path.join(path, "*.json")
            options = glob.glob(glob_exp)

            # No options == no dice. Move along.
            if not len(options):
                continue

            for raw_opt in options:
                # Rip off the extension.
                opt = os.path.splitext(raw_opt)[0]
                # Cut off the path.
                opt = opt.replace(path, '')

                # If the left-most character is a path separator,
                # remove that too.
                if opt[0] == os.path.sep:
                    opt = opt[1:]

                # One last check. Ensure it looks roughly like a versioned file.
                if not opt.count('-') == 2:
                    continue

                all_options.append(opt)

        if not len(all_options):
            # We don't have any matches. Error out.
            raise ApiVersionNotFound(
                data_path=data_path,
                api_version=api_version
            )

        # Reverse the list, so we can find the most correct/recent
        # lexicographically.
        all_options = sorted(all_options, reverse=True)

        if api_version is None:
            # We just care about the latest. Since they're in the proper order,
            # simply use the first one.
            best_match = all_options[0]
        else:
            # We need to look for an API version that either matches or is
            # the first to come before that (and hence, backward-compatible).
            for opt in all_options:
                if opt == api_version:
                    # Exact match. We win!
                    best_match = opt
                    break
                elif opt < api_version:
                    # Since it's in reverse sorted order & nothing previously
                    # matched, we know this is the closest API version that's
                    # backward-compatible.
                    best_match = opt
                    break

        if not best_match:
            # We didn't find anything. Error out.
            raise ApiVersionNotFound(
                data_path=data_path,
                api_version=api_version
            )

        # We've got the best match. Make a real path out of it & return that
        # for use elsewhere.
        return os.path.join(data_path, best_match)
