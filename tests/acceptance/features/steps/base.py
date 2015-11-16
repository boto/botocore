import json

from botocore import xform_name
from botocore.exceptions import ClientError

import jmespath
from behave import when, then
from nose.tools import assert_equal
from nose.tools import assert_is_instance


def _params_from_table(table):
    # Unfortunately the way we're using table is not quite how
    # behave expects tables to be used:
    # They expect:
    #
    #     | name      | department  |
    #     | Barry     | Beer Cans   |
    #     | Pudey     | Silly Walks |
    #     | Two-Lumps | Silly Walks |
    #
    # Where the first row are headings that indicate the
    # key name you can use to retrieve row values,
    # e.g row['name'] -> Barry.
    #
    #
    # We just use:
    #      | LaunchConfigurationName | hello, world |
    #      | ImageId                 | ami-12345678 |
    #      | InstanceType            | m1.small     |
    #
    # So we have to grab the headings before iterating over
    # the table rows.
    params = {table.headings[0]: table.headings[1]}
    for row in table:
        params[row[0]] = row[1]
    return params


@when(u'I call the "{}" API')
def api_call_no_args(context, operation):
    context.response = getattr(context.client, xform_name(operation))()


@when(u'I call the "{}" API with')
def api_call_with_args(context, operation):
    params = _params_from_table(context.table)
    context.response = getattr(context.client, xform_name(operation))(**params)


@when(u'I call the "{}" API with JSON')
def api_call_with_json(context, operation):
    params = json.loads(context.text)
    context.response = getattr(context.client, xform_name(operation))(**params)


@when(u'I attempt to call the "{}" API with')
def api_call_with_error(context, operation):
    params = _params_from_table(context.table)
    try:
        getattr(context.client, xform_name(operation))(**params)
    except ClientError as e:
        context.error_response = e


@when(u'I attempt to call the "{}" API with JSON')
def api_call_with_json_and_error(context, operation):
    params = json.loads(context.text)
    try:
        getattr(context.client, xform_name(operation))(**params)
    except ClientError as e:
        context.error_response = e


@then(u'I expect the response error code to be "{}"')
def then_expected_error(context, code):
    assert_equal(context.error_response.response['Error']['Code'], code)


@then(u'the value at "{}" should be a list')
def then_expected_type_is_list(context, expression):
    response = context.response
    result = jmespath.search(expression, response)
    assert_is_instance(result, list)


@then(u'the response should contain a "{}"')
def then_should_contain_key(context, key):
    if key not in context.response:
        raise AssertionError("Expected %s in response: %s"
                             % (key, context.response))


@then(u'the error message should contain')
def then_ignore_me(context, msg):
    # TODO: These steps will be removed.
    pass


@then(u'I expect the response error message to include')
def step_impl(context):
    # TODO: These steps will be removed.
    pass
