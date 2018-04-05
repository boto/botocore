# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from jsonschema import Draft4Validator

import botocore.session
from botocore import xform_name


SERVICE_SCHEMA = {
    "type": "object",
    "properties": {
        "shapes": {
            "type": "object",
            "patternProperties": {
                ".+": {
                    "type": "object",
                    "properties": {
                        "members": {
                            "type": "object",
                            "patternProperties": {
                                ".+": {
                                    "type": "object",
                                    "properties": {
                                        "cliArgumentName": {"type": "string"},
                                    }
                                }
                            }
                        }
                    }
                },
            },
        }
    },
}


def test_lint_cliargmentname_configs():
    session = botocore.session.get_session()
    validator = Draft4Validator(SERVICE_SCHEMA)
    for service_name in session.get_available_services():
        client = session.create_client(service_name, 'us-east-1')
        service_model = client.meta.service_model
        loader = session.get_component('data_loader')
        service_model = loader.load_service_model(service_name, 'service-2')
        yield _validate_schema, validator, service_model
        renames = {}
        for shape_name, shape in service_model.get("shapes", {}).items():
            yield _lint_rename_collisions, shape.get("members", {})
            for member_name, member_shape in shape.get("members", {}).items():
                if "cliArgumentName" in member_shape:
                    yield _lint_single_member, member_name, member_shape
                    renames.setdefault(member_name, []).append(
                        member_shape["cliArgumentName"]
                    )
        yield _lint_consistent_renames, renames


def _lint_rename_collisions(members):
    arguments = [
        shape.get("cliArgumentName", xform_name(name))
        for name, shape in members.items()
    ]
    if len(set(arguments)) != len(arguments):
        raise AssertionError(
            "The cliArgumentName collides with an existing member name.")


def _lint_single_member(member_name, member_shape):
    original_cli_name = xform_name(member_name)
    assert original_cli_name in member_shape["cliArgumentName"]


def _validate_schema(validator, waiter_json):
    errors = list(e.message for e in validator.iter_errors(waiter_json))
    if errors:
        raise AssertionError('\n'.join(errors))


def _lint_consistent_renames(renames):
    for member, clinames in renames.items():
        if len(set(clinames)) > 1:
            raise AssertionError(
                "Inconsistent names for the same member across shapes"
            )
