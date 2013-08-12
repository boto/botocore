import glob
import os

import botocore.base


class Loader(object):
    """
    A no-op base class, mostly to establish the protocol for loading
    the model data.
    """
    def __init__(self, session):
        self.session = session

    def get_data(self, data_path, api_version=None):
        raise NotImplementedError("Subclasses must implement 'get_data'.")


class JSONLoader(Loader):
    """
    Loads the JSON models from the filesystem.
    """
    def determine_latest(self, data_path, api_version=None):
        # If we know the API version, we can just create a concrete path.
        if api_version is not None:
            return os.path.join(data_path, api_version)

        # We don't have an api_version, so we'll need to find the latest
        # release.
        for path in botocore.base.get_search_paths(self.session):
            if os.path.isdir(path):
                glob_exp = os.path.join(path, "*.json")
                options = sorted(glob.glob(glob_exp), reverse=True)

                if len(options):
                    return options[0]

        # TODO: I'm not sure an exception is the right thing to raise here.
        #       Because it might be a deeper-lookup or maybe there just aren't
        #       any versions?
        raise DataNotFoundError(data_path=os.path.join(data_path, api_version))

    def get_data(self, data_path, api_version=None):
        """
        Retrieve the data associated with `data_path`.

        :type data_path: str
        :param data_path: The path to the data you wish to retrieve.

        :type api_version: str
        :param api_version: (Optional) The API version to use.
        """
        # FIXME: This sucks, because ``get_data`` is used for crazy arbitrary
        #        paths, which makes figuring out the path (& caching it)
        #        harder.
        data_path = self.determine_latest(data_path, api_version=api_version)
        return botocore.base.get_data(self, data_path)