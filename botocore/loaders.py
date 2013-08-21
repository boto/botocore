import glob
import os

import botocore.base
from botocore.exceptions import DataNotFoundError


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
        """

        Possible data paths::

            # Loads all the files in ``data/aws/``
            'aws'
            # Loads ``data/cli.json``
            'cli'
            # Loads just the ``ServerError`` value out of
            # ``data/messages.json``
            'messages/ServerError'
            # Loads ``data/aws/_regions.json``
            'aws/_regions'
            # Loads the latest JSON from ``data/aws/ec2``, which is
            # ``data/aws/ec2/2013-02-01``
            'aws/ec2'
            # Loads the explicit JSON from ``data/aws/ec2/2013-02-01``
            'aws/ec2/2013-02-01'
            # Loads the ``operations/DescribeInstances/input/members`` value
            # out of the latest JSON from ``data/aws/ec2``
            'aws/ec2/operations/DescribeInstances/input/members'
            # Loads the ``operations/DescribeInstances/input/members`` value
            # out of the explicit JSON from ``data/aws/ec2/2013-02-01``
            'aws/ec2/2013-02-01/operations/DescribeInstances/input/members'

        By being explicit about paths::

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

    def get_data(self, data_path, api_version=None):
        """
        Retrieve the data associated with `data_path`.

        :type data_path: str
        :param data_path: The path to the data you wish to retrieve.

        :type api_version: str
        :param api_version: (Optional) The API version to use.
        """
        data_path = self.determine_latest(data_path, api_version=api_version)
        return botocore.base.get_data(self.session, data_path)
