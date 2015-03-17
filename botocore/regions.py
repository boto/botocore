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
"""Implements endpoint heuristics.

This module implements the endpoint heuristics used by the AWS SDKs.
In a nutshell, you give it some input data (a service name, a
region name, and a scheme) and it gives you a complete url.

"""
from botocore.exceptions import UnknownEndpointError
from botocore.exceptions import NoRegionError


class EndpointResolver(object):
    _CONSTRAINT_FUNCS = {
        'startsWith': lambda x, y: str(x).startswith(y),
        'notStartsWith': lambda x, y: not str(x).startswith(y),
        'equals': lambda x, y: x == y,
        'notEquals': lambda x, y: x != y,
        'oneOf': lambda x, y: x in y
    }
    DEFAULT_SCHEME = 'https'

    def __init__(self, rules):
        self._rules = rules

    def get_rules_for_service(self, service_name):
        """Return the rules for a given service.

        Note that the list returned is a reference to the actual list of
        rules used for the service.  This list can be mutated to insert your
        own heuristic rules.  You can also use a service name of ``_default``
        to get the list of default rules that are applied if no service
        name matches.

        """
        return self._rules.get(service_name)

    def construct_endpoint(self, service_name, region_name, **kwargs):
        # We take **kwargs so that custom rules can be added that have
        # additional constraint keys that we don't know about.
        # We also need to fold the names used in the spec into **kwargs
        # so we can format the URI later.
        kwargs['service'] = service_name
        kwargs['region'] = region_name
        if 'scheme' not in kwargs:
            kwargs['scheme'] = self.DEFAULT_SCHEME
        service_rules = self._rules.get(service_name, [])
        endpoint = self._match_rules(service_rules, region_name, **kwargs)
        if endpoint is None:
            # If we didn't find any in the service section, try again
            # with the default section.
            endpoint = self._match_rules(self._rules.get('_default', []),
                                         region_name, **kwargs)

        if endpoint is None:
            if region_name is None:
                # Raise a more specific error message that will give
                # better guidance to the user what needs to happen.
                raise NoRegionError()
            else:
                raise UnknownEndpointError(service_name=service_name,
                                           region_name=region_name)
        return endpoint

    def _match_rules(self, service_rules, region_name, **kwargs):
        for rule in service_rules:
            if self._matches_rule(rule, region_name, **kwargs):
                return {'uri': rule['uri'].format(**kwargs),
                        'properties': rule.get('properties', {})}
        # If we can't find any rules, then try again with the _default
        # section.

    def _matches_rule(self, rule, region_name, **kwargs):
        for constraint in rule.get('constraints', []):
            if not self._matches_constraint(constraint, **kwargs):
                return False
        return True

    def _matches_constraint(self, constraint, **kwargs):
        # Each constraint consists of an attribute in the first index (e.g.,
        # "scheme", "region", "service"), an assertion in the second index
        # (e.g., "startsWith", "equals", "oneOf"), and a value in the third
        # index (e.g., "us-east-1").
        x, func, y = (kwargs[constraint[0]],
                      self._CONSTRAINT_FUNCS[constraint[1]],
                      constraint[2])
        return func(x, y)
