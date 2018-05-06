# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import string

import jmespath
from jmespath.exceptions import JMESPathError

import botocore.session


KNOWN_PAGE_KEYS = set(
    ['input_token', 'py_input_token', 'output_token', 'result_key',
     'limit_key', 'more_results', 'non_aggregate_keys'])
MEMBER_NAME_CHARS = set(string.ascii_letters + string.digits)


def test_lint_pagination_configs():
    session = botocore.session.get_session()
    loader = session.get_component('data_loader')
    services = loader.list_available_services('paginators-1')
    for service_name in services:
        service_model = session.get_service_model(service_name)
        page_config = loader.load_service_model(service_name,
                                                'paginators-1',
                                                service_model.api_version)
        for op_name, single_config in page_config['pagination'].items():
            yield (
                _lint_single_paginator,
                op_name,
                single_config,
                service_model
            )


def _lint_single_paginator(operation_name, page_config,
                           service_model):
    _validate_known_pagination_keys(page_config)
    _valiate_result_key_exists(page_config)
    _validate_referenced_operation_exists(operation_name, service_model)
    _validate_operation_has_output(operation_name, service_model)
    _validate_input_keys_match(operation_name, page_config, service_model)
    _validate_output_keys_match(operation_name, page_config, service_model)


def _validate_known_pagination_keys(page_config):
    for key in page_config:
        if key not in KNOWN_PAGE_KEYS:
            raise AssertionError("Unknown key '%s' in pagination config: %s"
                                 % (key, page_config))


def _valiate_result_key_exists(page_config):
    if 'result_key' not in page_config:
        raise AssertionError("Required key 'result_key' is missing "
                             "from pagination config: %s" % page_config)


def _validate_referenced_operation_exists(operation_name, service_model):
    if operation_name not in service_model.operation_names:
        raise AssertionError("Pagination config refers to operation that "
                             "does not exist: %s" % operation_name)


def _validate_operation_has_output(operation_name, service_model):
    op_model = service_model.operation_model(operation_name)
    output = op_model.output_shape
    if output is None or not output.members:
        raise AssertionError("Pagination config refers to operation "
                             "that does not have any output: %s"
                             % operation_name)


def _validate_input_keys_match(operation_name, page_config, service_model):
    input_tokens = page_config['input_token']
    if not isinstance(input_tokens, list):
        input_tokens = [input_tokens]
    valid_input_names = service_model.operation_model(
        operation_name).input_shape.members
    for token in input_tokens:
        if token not in valid_input_names:
            raise AssertionError("input_token '%s' refers to a non existent "
                                 "input member for operation: %s"
                                 % (token, operation_name))
    if 'limit_key' in page_config:
        limit_key = page_config['limit_key']
        if limit_key not in valid_input_names:
            raise AssertionError("limit_key '%s' refers to a non existent "
                                 "input member for operation: %s"
                                 % (limit_key, operation_name))


def _validate_output_keys_match(operation_name, page_config, service_model):
    # NOTE: The original version of this function from translate.py had logic
    # to ensure that the entire set of output_members was accounted for in the
    # union of 'result_key', 'output_token', 'more_results', and
    # 'non_aggregate_keys'.
    # There's enough state drift (especially with non_aggregate_keys) that
    # this is no longer a realistic thing to check.  Someone would have to
    # backport the missing keys to all the paginators.
    output_shape = service_model.operation_model(operation_name).output_shape
    output_members = output_shape.members
    for key_name, output_key in _get_all_page_output_keys(page_config):
        if _looks_like_jmespath(output_key):
            _validate_jmespath_compiles(output_key)
        else:
            if output_key not in output_members:
                raise AssertionError("Pagination key '%s' refers to an output "
                                     "member that does not exist: %s" % (
                                         key_name, output_key))


def _looks_like_jmespath(expression):
    if all(ch in MEMBER_NAME_CHARS for ch in expression):
        return False
    return True


def _validate_jmespath_compiles(expression):
    try:
        jmespath.compile(expression)
    except JMESPathError as e:
        raise AssertionError("Invalid JMESPath expression used "
                             "in pagination config: %s\nerror: %s"
                             % (expression, e))


def _get_all_page_output_keys(page_config):
    for key in _get_list_value(page_config, 'result_key'):
        yield 'result_key', key
    for key in _get_list_value(page_config, 'output_token'):
        yield 'output_token', key
    if 'more_results' in page_config:
        yield 'more_results', page_config['more_results']
    for key in page_config.get('non_aggregate_keys', []):
        yield 'non_aggregate_keys', key


def _get_list_value(page_config, key):
    # Some pagination config values can be a scalar value or a list of scalars.
    # This function will always return a list of scalar values, converting as
    # necessary.
    value = page_config[key]
    if not isinstance(value, list):
        value = [value]
    return value
