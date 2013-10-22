# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
import logging

from .endpoint import get_endpoint
from .operation import Operation
from .exceptions import ServiceNotInRegionError, NoRegionError


logger = logging.getLogger(__name__)


class Service(object):
    """
    A service, such as Elastic Compute Cloud (EC2).

    :ivar api_version: A string containing the API version this service
        is using.
    :ivar name: The full name of the service.
    :ivar service_name: The canonical name of the service.
    :ivar regions: A dict where each key is a region name and the
        optional value is an endpoint for that region.
    :ivar protocols: A list of protocols supported by the service.
    """

    def __init__(self, session, provider, service_name,
                 path='/', port=None):
        self.global_endpoint = None
        self.timestamp_format = 'iso8601'
        sdata = session.get_service_data(service_name)
        self.__dict__.update(sdata)
        self._operations_data = self.__dict__.pop('operations')
        self._operations = None
        self.session = session
        self.provider = provider
        self.path = path
        self.port = port
        self.cli_name = service_name
        if not hasattr(self, 'metadata'):
            # metadata is an option thing that comes from .extra.json
            # so if it's not there we just default to an empty dict.
            self.metadata = {}

    def _create_operation_objects(self):
        logger.debug("Creating operation objects for: %s", self)
        operations = []
        for operation_name in self._operations_data:
            data = self._operations_data[operation_name]
            data['name'] = operation_name
            op = Operation(self, data)
            operations.append(op)
        return operations

    def __repr__(self):
        return 'Service(%s)' % self.endpoint_prefix

    @property
    def operations(self):
        if self._operations is None:
            self._operations = self._create_operation_objects()
        return self._operations

    @property
    def region_names(self):
        return self.metadata.get('regions', {}).keys()

    def _build_endpoint_url(self, host, is_secure):
        if is_secure:
            scheme = 'https'
        else:
            scheme = 'http'
        if scheme not in self.metadata['protocols']:
            raise ValueError('Unsupported protocol: %s' % scheme)
        endpoint_url = '%s://%s%s' % (scheme, host, self.path)
        if self.port:
            endpoint_url += ':%d' % self.port
        return endpoint_url

    def get_endpoint(self, region_name=None, is_secure=True,
                     endpoint_url=None):
        """
        Return the Endpoint object for this service in a particular
        region.

        :type region_name: str
        :param region_name: The name of the region.

        :type is_secure: bool
        :param is_secure: True if you want the secure (HTTPS) endpoint.

        :type endpoint_url: str
        :param endpoint_url: You can explicitly override the default
            computed endpoint name with this parameter.  If this arg is
            provided then neither ``region_name`` nor ``is_secure``
            is used in building the final ``endpoint_url``.
            ``region_name`` can still be useful for services that require
            a region name independent of the endpoint_url (for example services
            that use Signature Version 4, which require a region name for
            use in the signature calculation).

        """
        if region_name is None:
            region_name = self.session.get_variable('region')
        if endpoint_url is not None:
            # Before getting into any of the region/endpoint
            # logic, if an endpoint_url is explicitly
            # provided, just use what's been explicitly passed in.
            return get_endpoint(self, region_name, endpoint_url)
        if region_name is None and not self.global_endpoint:
            # The only time it's ok to *not* provide a region is
            # if the service is a global_endpoint (e.g. IAM).
            envvar_name = self.session.env_vars['region'][1]
            raise NoRegionError(env_var=envvar_name)
        if region_name not in self.region_names:
            if self.global_endpoint:
                # If we haven't provided a region_name and this is a global
                # endpoint, we can just use the global_endpoint (which is a
                # string of the hostname of the global endpoint) to construct
                # the full endpoint_url.
                endpoint_url = self._build_endpoint_url(self.global_endpoint,
                                                        is_secure)
                region_name = 'us-east-1'
            else:
                # Otherwise we've specified a region name that is
                # not supported by the service so we raise
                # an exception.
                raise ServiceNotInRegionError(service_name=self.endpoint_prefix,
                                              region_name=region_name)
        # The 'regions' dict can call out the specific hostname
        # to use for a particular region.  If this is the case,
        # this will have precedence.
        # TODO: It looks like the region_name overrides shouldn't have the
        # protocol prefix.  Otherwise, it doesn't seem possible to override
        # the hostname for a region *and* support both http/https.  Should
        # be an easy change but it will be backwards incompatible to anyone
        # creating their own service descriptions with region overrides.
        endpoint_url = endpoint_url or self.metadata['regions'][region_name]
        if endpoint_url is None:
            # If the entry in the 'regions' dict is None,
            # then we fall back to the patter of
            # endpoint_prefix.region.amazonaws.com.
            host = '%s.%s.amazonaws.com' % (self.endpoint_prefix, region_name)
            endpoint_url = self._build_endpoint_url(host, is_secure)
        return get_endpoint(self, region_name, endpoint_url)

    def get_operation(self, operation_name):
        """
        Find an Operation object for a given operation_name.  The name
        provided can be the original camel case name, the Python name or
        the CLI name.

        :type operation_name: str
        :param operation_name: The name of the operation.
        """
        for operation in self.operations:
            op_names = (operation.name, operation.py_name, operation.cli_name)
            if operation_name in op_names:
                return operation
        return None


def get_service(session, service_name, provider):
    """
    Return a Service object for a given provider name and service name.

    :type service_name: str
    :param service_name: The name of the service.

    :type provider: Provider
    :param provider: The Provider object associated with the session.
    """
    logger.debug("Creating service object for: %s", service_name)
    return Service(session, provider, service_name)
