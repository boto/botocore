# Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

# NOTE: All classes and functions in this module are considered private and not
# subject to backwards compatibility guarantees. Please do not use them directly.


# NOTE: To view the raw JSON that the objects in this module represent, please
# go to any `endpoint-rule-set.json` file in /botocore/data/<service>/<api version>/
# or you can look at the test files in /tests/unit/data/endpoints/valid-rules/


import logging
import re
from enum import Enum
from functools import lru_cache
from string import Formatter
from typing import NamedTuple

from botocore import xform_name
from botocore.compat import quote, urlparse
from botocore.exceptions import EndpointResolutionError
from botocore.utils import (
    ArnParser,
    InvalidArnException,
    is_valid_ipv4_endpoint_url,
    is_valid_ipv6_endpoint_url,
    normalize_url_path,
    percent_encode,
)

logger = logging.getLogger(__name__)

TEMPLATE_STRING_RE = re.compile(r"\{[a-zA-Z#]+\}")
GET_ATTR_RE = re.compile(r"(\w+)\[(\d+)\]")
VALID_HOST_LABEL_RE = re.compile(
    r"^(?!-)[a-zA-Z\d-]{1,63}(?<!-)$",
)
CACHE_SIZE = 100
ARN_PARSER = ArnParser()
STRING_FORMATTER = Formatter()


class RuleSetStandardLibary:
    """A set of functions supported in rule sets and helpers."""

    def __init__(self, partitions_data):
        self.partitions_data = partitions_data

    def _is_func(self, argument):
        """Determine if an object is a function object.

        :type argument: Any
        :rtype: bool
        """
        return isinstance(argument, dict) and "fn" in argument

    def _is_ref(self, argument):
        """Determine if an object is a reference object.

        :type argument: Any
        :rtype: bool
        """
        return isinstance(argument, dict) and "ref" in argument

    def _is_template(self, argument):
        """Determine if an object contains a template string.

        :type argument: Any
        :rtpe: bool
        """
        return (
            isinstance(argument, str)
            and TEMPLATE_STRING_RE.search(argument) is not None
        )

    def _resolve_template_string(self, value, scope_vars):
        """Resolve and inject values into a template string.

        :type value: str
        :type scope_vars: dict
        :rtype: str
        """
        result = ""
        for literal, reference, _, _ in STRING_FORMATTER.parse(value):
            if reference is not None:
                template_value = scope_vars
                template_params = reference.split("#")
                for param in template_params:
                    template_value = template_value[param]
                result += f"{literal}{template_value}"
            else:
                result += literal
        return result

    def _resolve_value(self, value, scope_vars):
        """Return evaluated value based on type.

        :type value: Any
        :type scope_vars: dict
        :rtype: Any
        """
        if self._is_func(value):
            return self._call_function(value, scope_vars)
        elif self._is_ref(value):
            return scope_vars.get(value["ref"])
        elif self._is_template(value):
            return self._resolve_template_string(value, scope_vars)

        return value

    def _convert_func_name(self, value):
        """Normalize function names.

        :type value: str
        :rtype: str
        """
        change_case = f"_{xform_name(value)}"
        return change_case.replace(".", "_")

    def _call_function(self, func_signature, scope_vars):
        """Call the function with the resolved arguments and assign to `scope_vars`
        when applicable.

        :type func_signature: dict
        :type scope_vars: dict
        :rtype: Any
        """
        func_args = [
            self._resolve_value(arg, scope_vars)
            for arg in func_signature["argv"]
        ]
        func_name = self._convert_func_name(func_signature["fn"])
        func = getattr(self, func_name)
        result = func(*func_args)
        if "assign" in func_signature:
            assign = func_signature["assign"]
            if assign in scope_vars:
                raise EndpointResolutionError(
                    msg=f"Assignment {assign} already exists in "
                    "scoped variables and cannot be overwritten"
                )
            scope_vars[assign] = result
        return result

    def _is_set(self, value):
        """Evaluates whether a value (such as an endpoint parameter) is set
        (aka not None).

        :type value: Any
        :rytpe: bool
        """
        return value is not None

    def _get_attr(self, value, path):
        """Find an attribute within a value given a path string. The path can contain
        the name of the attribute and an index in brackets. A period separating attribute
        names indicates the one to the right is nested. The index will always occur at
        the end of the path.

        :type value: dict or list
        :type path: str
        :rtype: Any
        """
        for part in path.split("."):
            match = GET_ATTR_RE.search(part)
            if match is not None:
                name, index = match.groups()
                index = int(index)
                value = value.get(name)
                if value is None or index >= len(value):
                    return None
                return value[index]
            else:
                value = value[part]
        return value

    def _format_partition_output(self, partition):
        output = partition["outputs"]
        output["name"] = partition["id"]
        return output

    def _is_partition_match(self, region, partition):
        return (
            region in partition["regions"]
            or re.match(partition["regionRegex"], region) is not None
        )

    def _aws_partition(self, value):
        """Match a region string to an AWS partition.

        :type value: str
        :rtype: dict
        """
        if value is None:
            return None

        partitions = self.partitions_data['partitions']
        for partition in partitions:
            if self._is_partition_match(value, partition):
                return self._format_partition_output(partition)

        # return the default partition if no matches were found
        aws_partition = partitions[0]
        return self._format_partition_output(aws_partition)

    def _aws_parse_arn(self, value):
        """Parse and validate string for ARN components.

        :type value: str
        :rtype: dict
        """
        if value is None or not value.startswith("arn:"):
            return None

        try:
            arn_dict = ARN_PARSER.parse_arn(value)
        except InvalidArnException:
            return None

        # these three components are the only ones that cannot be empty
        if not all(
            (arn_dict["partition"], arn_dict["service"], arn_dict["resource"])
        ):
            return None

        arn_dict["accountId"] = arn_dict.pop("account")

        resource = arn_dict.pop("resource")
        delimiter = ":" if ":" in resource else "/"
        arn_dict["resourceId"] = resource.split(delimiter)

        return arn_dict

    def _is_valid_host_label(self, value, allow_subdomains):
        """Evaluates whether one or more string values are valid host labels per
        RFC 1123. If allow_subdomains is True, split on `.` and recurse with
        it set to False.

        :type value: str
        :type allow_subdomains: bool
        :rtype: bool
        """
        if value is None or allow_subdomains is False and value.count(".") > 0:
            return False

        if allow_subdomains is True:
            return all(
                self._is_valid_host_label(label, False)
                for label in value.split(".")
            )

        return VALID_HOST_LABEL_RE.match(value) is not None

    def _string_equals(self, value1, value2):
        """Evaluates two string values for equality and returns a boolean indicating
        if they match or not.

        :type value1: str
        :type value2: str
        :rtype: bool
        """
        if not all(isinstance(val, str) for val in (value1, value2)):
            raise EndpointResolutionError(
                msg=(
                    f"Both values must be strings.\n"
                    f"value1: {value1}\n"
                    f"value2: {value2}"
                )
            )
        return value1 == value2

    def _uri_encode(self, value):
        """Perform percent-encoding on an input string.

        :type value: str
        :rytpe: str
        """
        if value is None:
            return None

        return percent_encode(value)

    def _parse_url(self, value):
        """Parse a URL string into components.

        :type value: str
        :rtype: dict
        """
        if value is None:
            return None

        url_components = urlparse(value)
        # urlparse will silently include a port in the authority (netloc) even if
        # the value is not a base-10 integer.
        try:
            url_components.port
        except ValueError:
            return None

        scheme = url_components.scheme
        query = url_components.query
        # URLs with queries are not supported
        if scheme not in ["https", "http"] or len(query) > 0:
            return None

        path = url_components.path
        normalized_path = quote(normalize_url_path(path))
        if not normalized_path.endswith("/"):
            normalized_path = f"{normalized_path}/"

        return {
            "scheme": scheme,
            "authority": url_components.netloc,
            "path": path,
            "normalizedPath": normalized_path,
            "isIp": is_valid_ipv4_endpoint_url(value)
            or is_valid_ipv6_endpoint_url(value),
        }

    def _boolean_equals(self, value1, value2):
        """Evaluates two boolean values for equality.

        :type value1: bool
        :type value2: bool
        :rtype: bool
        """
        if not all(isinstance(val, bool) for val in (value1, value2)):
            raise EndpointResolutionError(
                msg=(
                    f"Both arguments must be booleans.\n"
                    f"value1: {value1}\n"
                    f"value2: {value2}"
                )
            )
        return value1 is value2

    def _is_ascii(self, string):
        """Evaluates if a string only contains ASCII characters.

        :type string: str
        :rtype: bool
        """
        try:
            string.encode("ascii")
            return True
        except UnicodeEncodeError:
            return False

    def _substring(self, string_input, start, stop, reverse):
        """Computes a substring given the start index and end index. If `reverse` is
        True, slice the string from the end instead.

        :type string_input: str
        :type start: int
        :type end: int
        :type reverse: bool
        :rtype: str
        """
        if not isinstance(string_input, str):
            raise EndpointResolutionError(
                msg=(
                    f"Input must be a string.\n"
                    f"string_input: {string_input}"
                )
            )
        if (
            start >= stop
            or len(string_input) < stop
            or not self._is_ascii(string_input)
        ):
            return None

        if reverse is True:
            r_start = len(string_input) - stop
            r_stop = len(string_input) - start
            return string_input[r_start:r_stop]

        return string_input[start:stop]

    def _not(self, value):
        """A function implementation of the logical operator `not`.

        :type value: Any
        :rtype: bool
        """
        return not value


class BaseRule:
    """A rule within a rule set. All rules contain a conditions property,
    which can be empty, and documentation about the rule.
    """

    def __init__(self, conditions, documentation=None):
        self.conditions = conditions
        self.documentation = documentation

    def evaluate(self, scope_vars, standard_library):
        raise NotImplementedError()

    def evaluate_conditions(self, scope_vars, standard_library):
        """Determine if all conditions in a rule are met.

        :type scope_vars: dict
        :type standard_library: RuleSetStandardLibrary
        :rtype: bool
        """
        for func_signature in self.conditions:
            result = standard_library._call_function(
                func_signature, scope_vars
            )
            if result is False or result is None:
                return False
        return True


class RuleSetEndpoint(NamedTuple):
    """A fully resolved endpoint object returned by a rule."""

    url: str
    properties: dict
    headers: dict


class EndpointRule(BaseRule):
    def __init__(self, endpoint, **kwargs):
        super().__init__(**kwargs)
        self.endpoint = endpoint

    def evaluate(self, scope_vars, standard_library):
        """If an endpoint rule's conditions are met, return the fully resolved
        endpoint object.

        :type scope_vars: dict
        :rtype: RuleSetEndpoint
        """
        if self.evaluate_conditions(scope_vars, standard_library) is True:
            url = standard_library._resolve_value(
                self.endpoint["url"], scope_vars
            )
            properties = self.resolve_properties(
                self.endpoint.get("properties", {}),
                scope_vars,
                standard_library,
            )
            headers = self.resolve_headers(scope_vars, standard_library)
            return RuleSetEndpoint(
                url=url, properties=properties, headers=headers
            )

        return None

    def resolve_properties(self, properties, scope_vars, standard_library):
        """Recurse through an endpoint's `properties` attribute, resolving template
        strings when found. Return the fully resolved attribute.

        :type properties: dict/list/str
        :type scope_vars: dict
        :type standard_library: RuleSetStandardLibrary
        :rtype: dict
        """
        if isinstance(properties, list):
            return [
                self.resolve_properties(prop, scope_vars, standard_library)
                for prop in properties
            ]
        elif isinstance(properties, dict):
            return {
                key: self.resolve_properties(
                    value, scope_vars, standard_library
                )
                for key, value in properties.items()
            }
        elif standard_library._is_template(properties):
            return standard_library._resolve_template_string(
                properties, scope_vars
            )
        return properties

    def resolve_headers(self, scope_vars, standard_library):
        """Iterate through an endpoint's headers attribute resolving values along
        the way. Return the fully resolved attribute.

        :type scope_vars: dict
        :type standard_library: RuleSetStandardLibrary
        :rtype: dict
        """
        resolved_headers = {}
        headers = self.endpoint.get("headers", {})

        for header, values in headers.items():
            resolved_headers[header] = [
                standard_library._resolve_value(item, scope_vars)
                for item in values
            ]
        return resolved_headers


class ErrorRule(BaseRule):
    def __init__(self, error, **kwargs):
        super().__init__(**kwargs)
        self.error = error

    def evaluate(self, scope_vars, standard_library):
        """If an error rule's conditions are met, raise the fully resolved error rule

        :type scope_vars: dict
        :type standard_library: RuleSetStandardLibrary
        :rtype: EndpointResolutionError
        """
        if self.evaluate_conditions(scope_vars, standard_library) is True:
            error = standard_library._resolve_value(self.error, scope_vars)
            raise EndpointResolutionError(msg=error)
        return None


class TreeRule(BaseRule):
    """A tree rule is non-terminal meaning it will never be returned to a provider.
    Additionally this means it has no attributes that need to be resolved.
    """

    def __init__(self, rules, **kwargs):
        super().__init__(**kwargs)
        self.rules = [RuleCreator.create(**rule) for rule in rules]

    def evaluate(self, scope_vars, standard_library):
        """If a tree rule's conditions evaluate successfully, iterate over its
        subordinate rules and return a result if there is one. If any of the
        subsequent rules are trees, the function will recurse until it reaches
        an error or an endpoint rule.

        :type scope_vars: dict
        :type standard_library: RuleSetStandardLibrary
        :rtype: RuleSetEndpoint/EndpointResolutionError
        """
        if self.evaluate_conditions(scope_vars, standard_library) is True:
            for rule in self.rules:
                # newly set parameters via "assign" cannot be shared between
                # adjacent rules
                rule_result = rule.evaluate(
                    scope_vars.copy(), standard_library
                )
                if rule_result:
                    return rule_result
        return None


class RuleCreator:

    endpoint = EndpointRule
    error = ErrorRule
    tree = TreeRule

    @classmethod
    def create(cls, **kwargs):
        """Create a class instance from rule metadata.

        :rtype: TreeRule/EndpointRule/ErrorRule
        """
        rule_type = kwargs.pop("type")
        try:
            rule_class = getattr(cls, rule_type)
        except AttributeError:
            raise EndpointResolutionError(
                msg=f"Unknown rule type: {rule_type}. A rule must "
                "be of type tree, endpoint or error."
            )
        else:
            return rule_class(**kwargs)


class ParameterDefinition:
    """The spec of an individual parameter defined in a rule set object."""

    def __init__(
        self,
        name,
        parameter_type,
        documentation=None,
        builtIn=None,
        default=None,
        required=None,
        deprecated=None,
    ):
        self.name = name
        try:
            self.parameter_type = getattr(
                self.ParameterType, parameter_type.lower()
            ).value
        except AttributeError:
            raise EndpointResolutionError(
                msg=f"Unknown parameter type: {parameter_type}. "
                "A parameter must be of type string or boolean"
            )
        self.documentation = documentation
        self.built_in = builtIn
        self.default = default
        self.required = required
        self.deprecated = deprecated

    class ParameterType(Enum):
        """An enum that translates a parameter definition's `type` attribute to
        its corresponding python native type.
        """

        string = str
        boolean = bool

    def validate_input(self, input_param):
        """Validate that an input parameter matches the type provided in its spec.

        :type input_param: Any
        :raises: EndpointParametersError
        """

        if not isinstance(input_param, self.parameter_type):
            raise EndpointResolutionError(
                msg=f"Input parameter {self.name} is the wrong "
                f"type. Must be {self.parameter_type}"
            )
        if self.deprecated is not None:
            depr_string = f"{self.name} has been deprecated."
            msg = self.deprecated["message"]
            if msg:
                depr_string += f"\n{msg}"
            since = self.deprecated.get("since")
            if since:
                depr_string += f"\nDeprecated since {since}."
            logger.info(depr_string)
        return None


class RuleSet:
    """An entire rule set object. Every rule set contains a version, parameters
    (specification of parameters not values) and rules. Additionally, it is provided
    with input parameters from a client to validate against its defined parameter
    traits and an instance of an endpoint provider.
    """

    def __init__(
        self, version, parameters, rules, partitions, documentation=None
    ):
        self.version = version
        self.parameters = {
            name: ParameterDefinition(
                name,
                spec["type"],
                spec.get("documentation"),
                spec.get("builtIn"),
                spec.get("default"),
                spec.get("required"),
                spec.get("deprecated"),
            )
            for name, spec in parameters.items()
        }
        self.rules = [RuleCreator.create(**rule) for rule in rules]
        self.standard_library = RuleSetStandardLibary(partitions)
        self.documentation = documentation

    def validate_input_parameters(self, input_parameters):
        """Validate each input parameter against its spec. If not provided, add
        the default value to the `input_parameters` dictionary.

        :type input_parameters: dict
        """
        for param_name, param_spec in self.parameters.items():
            input_param = input_parameters.get(param_name)
            if input_param is None and param_spec.default is not None:
                input_parameters[param_name] = param_spec.default
            elif input_param is not None:
                param_spec.validate_input(input_param)
        return None

    def evaluate(self, input_parameters):
        """Evaluate the rule set against the input parameters. Return the first rule
        the parameters match against.

        :type input_parameters: dict
        """
        self.validate_input_parameters(input_parameters)
        for rule in self.rules:
            # newly set parameters via "assign" cannot be shared between
            # adjacent rules
            evaluation = rule.evaluate(
                input_parameters.copy(), self.standard_library
            )
            if evaluation is not None:
                return evaluation
        return None


class EndpointProvider:
    """Provides a resolved endpoint for a set of input parameters after evaluating
    them against a service rule set.
    """

    def __init__(self, ruleset_data, partition_data):
        self.ruleset = RuleSet(**ruleset_data, partitions=partition_data)

    @lru_cache(maxsize=CACHE_SIZE)
    def resolve_endpoint(self, **input_parameters):
        """Match input parameters to a rule.

        :type input_parameters: dict
        :rtype: RuleSetEndpoint
        """
        params_for_error = input_parameters.copy()
        endpoint = self.ruleset.evaluate(input_parameters)
        if endpoint is None:
            param_string = "\n".join(
                [f"{key}: {value}" for key, value in params_for_error.items()]
            )
            raise EndpointResolutionError(
                msg=f"No endpoint found for parameters:\n{param_string}"
            )
        return endpoint
