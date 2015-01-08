import glob
import os

from botocore import BOTOCORE_ROOT
from botocore.compat import json
from botocore.compat import OrderedDict
from botocore.exceptions import ApiVersionNotFoundError
from botocore.exceptions import DataNotFoundError


def cachable(func):
    """
    A convenient decorator for getting the data (either from the cache or
    populating the cache).

    For use on instances (not plain functions) that have a ``self._cache``
    instance variable.

    Usage::

        class Loader(object):
            @cachable
            def load_service_model(self, service):
                data = self.load_file(self, 'aws/{0}'.format(service))
                return data

    """
    def _wrapper(self, orig_key, **kwargs):
        key = orig_key

        # Make the full key, including all kwargs.
        # Sort them to prevent hash randomization from creating accidental
        # cache misses.
        for name in sorted(kwargs.keys()):
            key += '/{0}/{1}'.format(
                name,
                kwargs[name]
            )

        if key in self._cache:
            return self._cache[key]

        data = func(self, orig_key, **kwargs)
        self._cache[key] = data
        return data

    return _wrapper


class JSONFileLoader(object):
    """
    Handles actually loading the files themselves.

    Split off as a seperate class to allow for swapping with more complex
    implementations.
    """
    def load_file(self, file_path):
        """
        Loads a regular data file (format-specific to subclass).

        This load is done uncached, so that you can always get the latest data
        as needed.

        Usage::

            >>> loader = JSONFileLoader()
            >>> loader.load_file('/path/to/some/thing.json')
            {
                # ...JSON data...
            }

        """
        try:
            with open(file_path) as fp:
                return json.load(fp, object_pairs_hook=OrderedDict)
        except ValueError:
            # For backward-compatibility with the previous implementation,
            # if the JSON is bad, we'll raise a ``DataNotFoundError`` exception
            # instead of letting it propagate.
            raise DataNotFoundError(data_path=file_path)


class Loader(object):
    """
    Intelligently loads the data botocore needs.

    Handles listing the available services, loading service data & loading
    arbitrary data.

    Default implementation uses JSON files (the ``JSONFileLoader``) & a plain
    cache (``Cache``).
    """
    file_loader_class = JSONFileLoader
    extension = '.json'
    service_extension = 'normal.json'

    def __init__(self, data_path='', file_loader_class=None, extension=None,
                 cache=None):
        """
        Sets up the Loader.

        Requires a ``data_path`` argument, which should be a unix-style PATH
        variable (multiple file paths, colon-delimited).

        Optionally accepts a ``file_loader_class`` parameter, which should be a
        class to use for loading files. Default is ``JSONFileLoader``.

        Optionally accepts an ``extension`` parameter, which should be a
        string of the file extension to use. Default is ``.json``.

        Optionally accepts a ``cache`` parameter, which should be a
        an instance with the same interface as the ``Cache`` class.
        Default is ``None`` (creates its own ``Cache()`` instance).
        """
        super(Loader, self).__init__()
        self._data_path = data_path
        self._cache = {}

        if file_loader_class is not None:
            self.file_loader_class = file_loader_class

        if extension is not None:
            self.extension = extension

        if cache is not None:
            self._cache = cache

        self.file_loader = self.file_loader_class()

    @property
    def data_path(self):
        return self._data_path

    @data_path.setter
    def data_path(self, value):
        self._data_path = value

    def get_search_paths(self):
        """
        Return the all the paths that data could be found on when searching for
        files.

        Usage::

            # Default:
            >>> loader = Loader('/path/to/botocore/data')
            >>> loader.get_search_paths()
            [
                '/path/to/botocore/data',
            ]

            # User-added paths
            >>> loader = Loader('~/.botocore/my_overrides:/path/to/botocore/data')
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
        search_path = self.data_path

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

    @cachable
    def load_data(self, data_path):
        """
        Either loads a regular data file (format-specific to subclass) or
        returns previously loaded data from the cache.

        Returns a dictionary of data from the file.

        Usage::

            >>> loader = Loader('/path/to/botocore/data')
            >>> loader.load_data('aws/ec2/2013-02-01')
            {
                # ...EC2 service data...
            }
            >>> loader.load_data('_endpoints')
            {
                # ...Endpoint data...
            }

        """
        # Here, we'll cache it.
        return self._load_data(data_path)

    def _load_data(self, data_path):
        # This is the uncached version for use with ``load_service_model``.
        # We go in-order, returning the first matching path we find
        # based on the search paths.
        for possible_path in self.get_search_paths():
            full_path = os.path.join(
                possible_path,
                data_path + self.extension
            )

            try:
                return self.file_loader.load_file(full_path)
            except IOError:
                continue

        # We didn't find anything that matched on any path.
        raise DataNotFoundError(data_path=data_path)

    @cachable
    def load_service_model(self, data_path, api_version=None):
        """
        Loads a given service's model data.

        Requires a ``data_path`` parameter, which should be a string. This
        indicates the desired path to load, seperated by slashes. It should
        **NOT** include absolute path information nor file extensions. (i.e.
        ``aws/ec2``, not ``/botocore/data/aws/ec2/2010-01-01.json``)

        Optionally accepts an ``api_version`` parameter, which should be a
        string of the desired API version. This is used when you want to pin to
        a given API version rather than picking up the latest version.
        An example looks like ``2013-08-27``. Default is ``None``, which means
        pick the latest.

        Returns a dictionary of service model data.

        Usage::

            >>> loader = Loader('/path/to/botocore/data')
            >>> loader.load_service_model('aws/ec2')
            {
                # The latest EC2 service data...
                'api_version': '2013-08-27',
                # ...many more keys & values...
            }
            >>> loader.load_service_model('aws/ec2', api_version='2013-02-01')
            {
                # The EC2 service data for version 2013-02-01...
                'api_version': '2013-02-01',
                # ...many more keys & values...
            }

        """
        actual_data_path = self.determine_latest(
            data_path,
            api_version=api_version
        )

        # Use the private method, so that we don't double-cache.
        return self._load_data(actual_data_path)

    @cachable
    def list_available_services(self, data_path):
        """
        Loads all the service options available.

        Requires a ``data_path`` parameter, which should be a string. This
        indicates the desired path to load, seperated by slashes if needed.

        Returns a list of service names.

        Usage::

            >>> loader = Loader('/path/to/botocore/data')
            >>> loader.list_available_services('aws')
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

        return sorted(options)

    def determine_latest(self, data_path, api_version=None):
        """
        For given desired data_path, searches all possible locations for the
        version of the data file that best matches.

        This is used primarily for the service models themselves, which
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
        ``ApiVersionNotFoundError`` exception will be thrown.

        Usage::

            >>> loader = Loader('~/.botocore/my_overrides:/path/to/botocore/data')

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
            ApiVersionNotFoundError: Unable to load data aws/rds for: 2010-05-16

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
            glob_exp = os.path.join(path, '*' + self.service_extension)
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
            raise ApiVersionNotFoundError(
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
                # ``opt`` will be something like "2014-01-01.normal" so we need
                # to strip off the ".normal" part.
                if opt.split('.')[0] == api_version:
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
            raise ApiVersionNotFoundError(
                data_path=data_path,
                api_version=api_version
            )

        # We've got the best match. Make a real path out of it & return that
        # for use elsewhere.
        return os.path.join(data_path, best_match)
