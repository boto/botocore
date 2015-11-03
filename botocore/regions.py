# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Resolves regions and endpoints.

This module implements endpoint resolution, including resolving endpoints for a
given service and region and resolving the available endpoints for a service
in a specific AWS partition.
"""
import logging
import re

from botocore.exceptions import NoRegionError

LOG = logging.getLogger(__name__)
DEFAULT_URI_TEMPLATE = '{service}.{region}.{dnsSuffix}'


def create_resolver_from_files(data_loader, partitions):
    """Creates an endpoint resolver from a list of partitions

    The first partition in the list will be eagerly loaded, and the remaining
    partitions will be lazily loaded. The returned resolver will also account
    for S3 specific customizations.
    """
    if not partitions:
        raise ValueError('Must provide one or more partition files')
    eager_loaded_data = data_loader.load_partition_data(partitions[0])
    resolvers = [PartitionEndpointResolver(eager_loaded_data)]
    for name in partitions[1:]:
        resolvers.append(LazyPartitionEndpointResolver(data_loader, name))
    return S3CompatResolver(EndpointResolverChain(resolvers))


class BaseEndpointResolver(object):
    """Resolves regions and endpoints. Must be subclassed."""
    def construct_endpoint(self, service_name, region_name):
        """Resolves an endpoint for a service and region combination.

        :type service_name: string
        :param service_name: Name of the service to resolve an endpoint for
            (e.g., s3)

        :type region_name: string
        :param region_name: Region/endpoint name to resolve (e.g., us-east-1)

        :rtype: dict
        :return: Returns a dict containing the following keys:
            - partition: (string, required) Resolved partition name
            - endpointName: (string, required) Resolved endpoint name
            - hostname: (string, required) Hostname to use for this endpoint
            - sslCommonName: (string) sslCommonName to use for this endpoint.
            - credentialScope: (dict) Signature version 4 credential scope
              - region: (string) region name override when signing.
              - service: (string) service name override when signing.
            - signatureVersions: (list<string>) A list of possible signature
              versions, including s3, v4, v2, and s3v4
            - protocols: (list<string>) A list of supported protocols
              (e.g., http, https)
            - ...: Other keys may be included as well based on the metadata
        """
        raise NotImplementedError

    def list_endpoint_names(self, service_name, partition_name='aws',
                            allow_non_regional=False):
        """Lists the endpoint names of a particular partition.

        :type service_name: string
        :param service_name: Name of a service to list endpoint for (e.g., s3)

        :type partition_name: string
        :param partition_name: Name of the partition to limit endpoints to.
            (e.g., aws for the public AWS endpoints, aws-cn for AWS China
            endpoints, aws-us-gov for AWS GovCloud (US) Endpoints, etc.

        :type allow_non_regional: bool
        :param allow_non_regional: Set to True to include endpoints that are
             not regional endpoints (e.g., s3-external-1,
             fips-us-gov-west-1, etc).
        :return: Returns an iterable of endpoint names (e.g., us-east-1).
        """
        raise NotImplementedError


class S3CompatResolver(BaseEndpointResolver):
    """Adds S3 specific customizations to an endpoint resolver.

    This resolver proxies to another resolver and sets a default region
    of us-east-1 for "s3".
    """
    def __init__(self, endpoint_resolver):
        self._proxy = endpoint_resolver

    def list_endpoint_names(self, service_name, partition_name='aws',
                            allow_non_regional=False):
        return self._proxy.list_endpoint_names(
            service_name, partition_name, allow_non_regional)

    def construct_endpoint(self, service_name, region_name):
        # Use us-east-1 as the default region for S3.
        if service_name == 's3' and region_name is None:
            region_name = 'us-east-1'
        return self._proxy.construct_endpoint(service_name, region_name)


class EndpointResolverChain(BaseEndpointResolver):
    """Resolves endpoints using a chain of endpoint resolvers"""
    def __init__(self, endpoint_resolvers):
        self.endpoint_resolvers = endpoint_resolvers

    def list_endpoint_names(self, service_name, partition_name='aws',
                            allow_non_regional=False):
        for resolver in self.endpoint_resolvers:
            endpoints = resolver.list_endpoint_names(
                service_name, partition_name, allow_non_regional)
            if endpoints:
                return endpoints
        return []

    def construct_endpoint(self, service_name, region_name):
        for resolver in self.endpoint_resolvers:
            endpoint = resolver.construct_endpoint(service_name, region_name)
            if endpoint:
                return endpoint
        return None


class LazyPartitionEndpointResolver(object):
    """Lazily instantiates and proxies calls to a PartitionEndpointResolver"""
    def __init__(self, data_loader, partition_name):
        self.partition_name = partition_name
        self._data_loader = data_loader
        self._proxy = None

    def _load(self):
        if not self._proxy:
            LOG.debug('Lazy loading partition file: %s', self.partition_name)
            data = self._data_loader.load_partition_data(self.partition_name)
            self._proxy = PartitionEndpointResolver(data)
        return self._proxy

    def list_endpoint_names(self, service_name, partition_name='aws',
                            allow_non_regional=False):
        return self._load().list_endpoint_names(
            service_name, partition_name, allow_non_regional)

    def construct_endpoint(self, service_name, region_name):
        return self._load().construct_endpoint(service_name, region_name)


class PartitionEndpointResolver(BaseEndpointResolver):
    """Resolves endpoints based on partition endpoint metadata"""
    def __init__(self, partition_data):
        """
        :param partition_data: A dict of partition data.
        """
        self._default_service_data = {'endpoints': {}}
        required = ['partition', 'regions', 'services', 'dnsSuffix']
        for key in required:
            if key not in partition_data:
                raise ValueError('Missing %s in partition data' % key)
        self._partition = partition_data
        self._regexp = None

    def list_endpoint_names(self, service_name, partition_name='aws',
                            allow_non_regional=False):
        result = []
        if self._partition['partition'] == partition_name:
            services = self._partition['services']
            if service_name in services:
                for endpoint_name in services[service_name]['endpoints']:
                    if allow_non_regional \
                            or endpoint_name in self._partition['regions']:
                        result.append(endpoint_name)
        return result

    def construct_endpoint(self, service_name, region_name):
        if region_name is None:
            raise NoRegionError()
        # Get the service from the partition, or an empty template.
        service_data = self._partition['services'].get(
            service_name, self._default_service_data)
        # Attempt to resolve the exact region for this partition.
        if region_name in service_data['endpoints']:
            return self._resolve(service_name, service_data, region_name)
        # Check to see if the endpoint provided is valid for the partition.
        if self._region_match(region_name):
            # Use the partition endpoint if set and not regionalized.
            partition_endpoint = service_data.get('partitionEndpoint')
            is_regionalized = service_data.get('isRegionalized', True)
            if partition_endpoint and not is_regionalized:
                LOG.debug('Using partition endpoint for %s, %s: %s',
                          service_name, region_name, partition_endpoint)
                return self._resolve(
                    service_name, service_data, partition_endpoint)
            LOG.debug('Creating a regex based endpoint for %s, %s',
                      service_name, region_name)
            return self._resolve(service_name, service_data, region_name)

    def _region_match(self, region_name):
        if region_name in self._partition['regions']:
            return True
        if not self._regexp and self._partition.get('regionRegex'):
            self._regexp = re.compile(self._partition['regionRegex'])
        return self._regexp and self._regexp.match(region_name)

    def _resolve(self, service_name, service_data, endpoint_name):
        result = service_data['endpoints'].get(endpoint_name, {})
        result['partition'] = self._partition['partition']
        result['endpointName'] = endpoint_name
        # Merge in the service defaults then the partition defaults.
        self._merge_keys(service_data.get('defaults', {}), result)
        self._merge_keys(self._partition.get('defaults', {}), result)
        hostname = result.get('hostname', DEFAULT_URI_TEMPLATE)
        result['hostname'] = self._expand_template(
            result['hostname'], service_name, endpoint_name)
        if 'sslCommonName' in result:
            result['sslCommonName'] = self._expand_template(
                result['sslCommonName'], service_name, endpoint_name)
        return result

    def _merge_keys(self, from_data, result):
        for key in from_data:
            if key not in result:
                result[key] = from_data[key]

    def _expand_template(self, template, service_name, endpoint_name):
        return template.format(
            service=service_name, region=endpoint_name,
            dnsSuffix=self._partition['dnsSuffix'])
