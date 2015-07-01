# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

from tests import unittest
from botocore.translate import ModelFiles, translate, merge_dicts, \
                               resembles_jmespath_exp


SERVICES = {
  "service_full_name": "AWS Security Token Service",
  "service_abbreviation": "AWS STS",
  "type": "query",
  "signature_version": "v4",
  "result_wrapped": True,
  "global_endpoint": "sts.amazonaws.com",
  "api_version": "2011-06-15",
  "endpoint_prefix": "sts",
  "xmlnamespace": "https://sts.amazonaws.com/doc/2011-06-15/",
  "documentation": "docs",
  "operations": {
    "AssumeRole": {
      "name": "AssumeRole",
      "input": {
        "shape_name": "AssumeRoleRequest",
        "type": "structure",
        "members": {
          "RoleArn": {
            "shape_name": "arnType",
            "type": "string",
            "min_length": 20,
            "max_length": 2048,
            "documentation": "docs",
            "required": True
          },
          "RoleSessionName": {
            "shape_name": "userNameType",
            "type": "string",
            "min_length": 2,
            "max_length": 32,
            "pattern": "[\\w+=,.@-]*",
            "documentation": "docs",
            "required": True
          },
          "Policy": {
            "shape_name": "sessionPolicyDocumentType",
            "type": "string",
            "pattern": "[\\u0009\\u000A\\u000D\\u0020-\\u00FF]+",
            "min_length": 1,
            "max_length": 2048,
            "documentation": "docs"
          },
          "DurationSeconds": {
            "shape_name": "roleDurationSecondsType",
            "type": "integer",
            "min_length": 900,
            "max_length": 3600,
            "documentation": "docs"
          },
          "ExternalId": {
            "shape_name": "externalIdType",
            "type": "string",
            "min_length": 2,
            "max_length": 96,
            "pattern": "[\\w+=,.@:-]*",
            "documentation": "docs"
          },
          # Not in the actual description, but this is to test pagination.
          "NextToken": {
              "shape_name": "String",
              "type": "string",
              "documentation": None
          },
          "TokenToken": {
              "shape_name": "String",
              "type": "string",
              "documentation": None,
              "xmlname": "tokenToken"
          },
          "MaxResults": {
              "shape_name": "Integer",
              "type": "int",
              "documentation": None,
              "xmlname": "maxResults"
          }
        },
        "documentation": "docs"
      },
      "output": {
        "shape_name": "AssumeRoleResponse",
        "type": "structure",
        "members": {
          "Credentials": {
            "shape_name": "Credentials",
            "type": "structure",
            "members": {
              "AccessKeyId": {
                "shape_name": "accessKeyIdType",
                "type": "string",
                "min_length": 16,
                "max_length": 32,
                "pattern": "[\\w]*",
                "documentation": "docs",
                "required": True
              },
              "SecretAccessKey": {
                "shape_name": "accessKeySecretType",
                "type": "string",
                "documentation": "docs",
                "required": True
              },
              "SessionToken": {
                "shape_name": "tokenType",
                "type": "string",
                "documentation": "docs",
                "required": True
              },
              "Expiration": {
                "shape_name": "dateType",
                "type": "timestamp",
                "documentation": "docs",
                "required": True
              }
            },
            "documentation": "docs"
          },
          "AssumedRoleUser": {
            "shape_name": "AssumedRoleUser",
            "type": "structure",
            "members": {
              "AssumedRoleId": {
                "shape_name": "assumedRoleIdType",
                "type": "string",
                "min_length": 2,
                "max_length": 96,
                "pattern": "[\\w+=,.@:-]*",
                "documentation": "docs",
                "required": True
              },
              "Arn": {
                "shape_name": "arnType",
                "type": "string",
                "min_length": 20,
                "max_length": 2048,
                "documentation": "docs",
                "required": True
              }
            },
            "documentation": "docs"
          },
          "PackedPolicySize": {
            "shape_name": "nonNegativeIntegerType",
            "type": "integer",
            "min_length": 0,
            "documentation": "docs"
          },
          "NextToken": {
              "shape_name": "String",
              "type": "string",
              "documentation": None,
              "xmlname": "nextToken"
          },
        },
        "documentation": "docs"
      },
      "errors": [
        {
          "shape_name": "MalformedPolicyDocumentException",
          "type": "structure",
          "members": {
            "message": {
              "shape_name": "malformedPolicyDocumentMessage",
              "type": "string",
              "documentation": "docs"
            }
          },
          "documentation": "docs"
        },
        {
          "shape_name": "PackedPolicyTooLargeException",
          "type": "structure",
          "members": {
            "message": {
              "shape_name": "packedPolicyTooLargeMessage",
              "type": "string",
              "documentation": "docs"
            }
          },
          "documentation": "docs"
        }
      ],
      "documentation": "docs"
    },
    "RealOperation2013_02_04": {
      "name": "RealOperation2013_02_04",
      "input": {},
      "output": {
        "shape_name": "RealOperation2013_02_04Response",
        "type": "structure",
        "members": {
          "Result": {
            "shape_name": "Result",
            "type": "string",
            "documentation": ""
          }
        }
      },
      "errors": [],
      "documentation": "docs"
    },
    "NoOutputOperation": {
      "name": "NoOutputOperation",
      "input": {},
      "output": {},
      "errors": [],
      "documentation": "docs"
    },
    "DeprecatedOperation": {
      "input": {
        "shape_name": "DeprecatedOperationRequest",
        "type": "structure",
        "members": {
          "FooBar": {
            "shape_name": "foobarType",
            "type": "string",
            "documentation": "blah blah <![CDATA[\n\nfoobar ]]>blah blah",
          },
          "FieBaz": {
            "shape_name": "fiebazType",
            "type": "string",
            "documentation": "Don't use this, it's deprecated"
          }
        }
      },
      "documentation": "This is my <![CDATA[none of \nthis stuff should be here]]> stuff"
    },
    "DeprecatedOperation2": {
      "input": {
        "shape_name": "DeprecatedOperation2Request",
        "type": "structure",
        "members": {
          "FooBar": {
            "shape_name": "foobarType",
            "type": "string",
            "documentation": "blah blah blah blah",
          },
          "FieBaz": {
            "shape_name": "fiebazType",
            "type": "string",
            "documentation": ""
          }
        }
      },
      "documentation": "This operation has been deprecated."
    },
    "RenameOperation": {
      "input": {
        "shape_name": "RenameOperation",
        "type": "structure",
        "members": {
          "RenameMe": {
            "shape_name": "RenameMe",
            "type": "string",
            "documentation": "blah blah blah blah",
          },
          "FieBaz": {
            "shape_name": "fiebazType",
            "type": "string",
            "documentation": ""
          }
        }
      },
      "documentation": "This operation has been deprecated."
    },
    "EchoedOutputParams": {
      "name": "EchoedOutputParams",
      "input": {
        "shape_name": "EchoedOutputParams",
        "type": "structure",
        "members": {
          "Marker": {
            "shape_name": "String",
            "type": "string",
            "documentation": "blah blah blah blah",
          },
        }
      },
      "documentation": "",
      "output": {
        "shape_name": "EchoedOutputParamsResponse",
        "type": "structure",
        "members": {
          "Marker": {
            "shape_name": "String",
            "type": "string",
            "documentation": "",
          },
          "NextMarker": {
            "shape_name": "String",
            "type": "string",
            "documentation": "",
          },
          "ResultKey": {
            "shape_name": "String",
            "type": "string",
            "documentation": "",
          },
        }
      },
    }
  }
}


class TestTranslateExtensions(unittest.TestCase):
    def setUp(self):
        self.model = ModelFiles(SERVICES, {}, {}, {})

    def test_can_add_extras_top_level_keys(self):
        # A use case here would be adding the iterator/waiter configs.
        new_keys = {'extra': {'paginators': 'paginator_config'}}
        self.model.enhancements = new_keys
        new_model = translate(self.model)
        # There should be a new top level key 'iterators' that was merged in.
        self.assertEqual(new_model['paginators'], 'paginator_config')
        self.assertIn('operations', new_model)

    def test_can_add_fields_to_operation(self):
        # A use case would be to add checksum info for a param.

        # We could go for a more streamlined syntax, but this way, it's
        # clear how this maps onto the existing json model.
        new_keys = {
            'operations': {
                'AssumeRole': {
                    'input': {
                        'checksum': 'md5',
                    }
                },
            }
        }
        self.model.enhancements = new_keys
        new_model = translate(self.model)
        self.assertEqual(
            new_model['operations']['AssumeRole']['input']['checksum'],
            'md5')

    def test_can_add_fields_to_op_params(self):
        # A use case would be if we want to annotate that a
        # string type might also come from a file (keypairs, s3 uploads, etc).
        new_keys = {
            'operations': {
                'AssumeRole': {
                    'input': {
                        'members': {
                            'Policy': {
                                'alsofrom': 'filename',
                            },
                        }
                    }
                },
            }
        }
        self.model.enhancements = new_keys
        new_model = translate(self.model)
        self.assertEqual(
            new_model['operations']['AssumeRole']['input']['members']\
                    ['Policy']['alsofrom'],
            'filename')
        self.assertEqual(
            new_model['operations']['AssumeRole']['input']['members']\
                    ['Policy']['type'],
            'string')
        self.assertEqual(
            new_model['operations']['AssumeRole']['input']['members']\
                    ['RoleArn']['shape_name'],
            'arnType')


class TestTranslateModel(unittest.TestCase):
    def setUp(self):
        self.model = ModelFiles(SERVICES, {}, {}, {})

    def test_operations_is_a_dict_not_list(self):
        # In order to make overriding easier, we want the list of
        # operations to be a dict, not a list.  The way we don't have
        # to search through the list to find the operation we want to
        # change.  It also makes it easier to annontate operations.
        new_model = translate(self.model)
        self.assertIn('AssumeRole', new_model['operations'])

    def test_iterators_are_merged_into_operations(self):
        # This may or may not pan out, but if a pagination config is
        # specified, that info is merged into the specific operations.
        extra = {
            'pagination': {
                'AssumeRole': {
                    'input_token': 'NextToken',
                    'output_token': 'NextToken',
                    'limit_key': 'MaxResults',
                    'result_key': 'Credentials',
                    'non_aggregate_keys': ['PackedPolicySize',
                                           'AssumedRoleUser'],
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        op = new_model['operations']['AssumeRole']
        self.assertDictEqual(
            op['pagination'], {
                'input_token': 'NextToken',
                'py_input_token': 'next_token',
                'output_token': 'NextToken',
                'limit_key': 'MaxResults',
                'result_key': 'Credentials',
                'non_aggregate_keys': ['PackedPolicySize',
                                        'AssumedRoleUser'],
            })

    def test_py_input_name_is_not_added_if_it_exists(self):
        # This may or may not pan out, but if a pagination config is
        # specified, that info is merged into the specific operations.
        extra = {
            'pagination': {
                'AssumeRole': {
                    'input_token': 'NextToken',
                    'output_token': 'NextToken',
                    'py_input_token': 'other_value',
                    'limit_key': 'MaxResults',
                    'result_key': 'Credentials',
                    'non_aggregate_keys': ['PackedPolicySize',
                                           'AssumedRoleUser'],
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        op = new_model['operations']['AssumeRole']
        # Note how 'py_input_token' is left untouched.  This allows us
        # to override this naming if we need to.
        self.assertDictEqual(
            op['pagination'], {
                'input_token': 'NextToken',
                'py_input_token': 'other_value',
                'output_token': 'NextToken',
                'limit_key': 'MaxResults',
                'result_key': 'Credentials',
                    'non_aggregate_keys': ['PackedPolicySize',
                                           'AssumedRoleUser'],
            })

    def test_paginators_are_validated(self):
        # Can't create a paginator config that refers to a non existent
        # operation.
        extra = {
            'pagination': {
                'UnknownOperation': {
                    'input_token': 'NextToken',
                    'output_token': 'NextToken',
                    'max_results': 'MaxResults',
                }
            }
        }
        self.model.enhancements = extra
        with self.assertRaises(ValueError):
            new_model = translate(self.model)

    def test_paginators_are_placed_into_top_level_key(self):
        extra = {
            'pagination': {
                'AssumeRole': {
                    'input_token': 'NextToken',
                    'output_token': 'NextToken',
                    'result_key': 'Credentials',
                    'non_aggregate_keys': ['PackedPolicySize',
                                           'AssumedRoleUser'],
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        self.assertEqual(new_model['pagination'], extra['pagination'])

    def test_extra_key(self):
        # Anything in "extra" is merged as a top level key.
        extra = {
            "extra": {
                "signature_version": "v2",
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        self.assertEqual(new_model['signature_version'], 'v2')
        self.assertEqual(new_model['documentation'], 'docs')

    def test_paginator_with_multiple_input_outputs(self):
        extra = {
            'pagination': {
                'AssumeRole': {
                    'input_token': ['NextToken', 'TokenToken'],
                    'output_token': ['NextToken'],
                    'result_key': 'Credentials',
                    'non_aggregate_keys': ['PackedPolicySize',
                                           'AssumedRoleUser'],
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        op = new_model['operations']['AssumeRole']
        self.assertDictEqual(
            op['pagination'], {
                'input_token': ['NextToken', 'TokenToken'],
                'py_input_token': ['next_token', 'token_token'],
                'output_token': ['NextToken'],
                'result_key': 'Credentials',
                'non_aggregate_keys': ['PackedPolicySize',
                                        'AssumedRoleUser'],
            })

    def test_result_key_validation(self):
        # result_key must exist.
        extra = {
            'pagination': {
                'AssumeRole': {
                    'input_token': ['Token', 'TokenToken'],
                    'output_token': ['NextToken']
                }
            }
        }
        self.model.enhancements = extra
        with self.assertRaises(ValueError):
            translate(self.model)

    def test_result_key_exists_in_output(self):
        extra = {
            'pagination': {
                'AssumeRole': {
                    'input_token': ['Token', 'TokenToken'],
                    'output_token': ['NextToken', 'NextTokenToken'],
                    'result_key': 'DoesNotExist',
                }
            }
        }
        self.model.enhancements = extra
        with self.assertRaises(ValueError):
            translate(self.model)

    def test_result_key_can_be_a_list(self):
        extra = {
            'pagination': {
                'AssumeRole': {
                    'input_token': ['NextToken'],
                    'output_token': ['NextToken'],
                    'result_key': ['Credentials', 'AssumedRoleUser'],
                    'non_aggregate_keys': ['PackedPolicySize'],
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        self.assertEqual(new_model['pagination'], extra['pagination'])

    def test_expected_schema_exists(self):
        # In this case, the key 'output_tokens' is suppose to be 'output_token'
        # so we should get an error when this happens.
        extra = {
            'pagination': {
                'AssumeRole': {
                    'input_token': ['Token', 'TokenToken'],
                    'output_tokens': ['NextToken', 'NextTokenToken'],
                    'result_key': ['Credentials', 'AssumedRoleUser'],
                }
            }
        }
        self.model.enhancements = extra
        with self.assertRaises(ValueError):
            translate(self.model)

    def test_input_tokens_exist_in_model(self):
        extra = {
            'pagination': {
                'AssumeRole': {
                    # In this case, "DoesNotExist" token is not in the input
                    # model, so we get an exception complaining about this.
                    'input_token': ['NextToken', 'DoesNotExist'],
                    'output_token': ['NextToken', 'NextTokenToken'],
                    'result_key': ['Credentials', 'AssumedRoleUser'],
                }
            }
        }
        self.model.enhancements = extra
        with self.assertRaises(ValueError):
            translate(self.model)

    def test_validate_limit_key_is_in_input(self):
        extra = {
            'pagination': {
                'AssumeRole': {
                    'input_token': 'NextToken',
                    'output_token': ['NextToken', 'NextTokenToken'],
                    'result_key': ['Credentials', 'AssumedRoleUser'],
                    # In this case, "DoesNotExist" token is not in the input
                    # model, so we get an exception complaining about this.
                    'limit_key': 'DoesNotExist',
                }
            }
        }
        self.model.enhancements = extra
        with self.assertRaises(ValueError):
            translate(self.model)

    def test_cant_add_pagination_to_nonexistent_operation(self):
        extra = {
            'pagination': {
                'ThisOperationDoesNotExist': {
                    'input_token': 'NextToken',
                    'output_token': ['NextToken', 'NextTokenToken'],
                    'result_key': ['Credentials', 'AssumedRoleUser'],
                    'limit_key': 'Foo',
                }
            }
        }
        self.model.enhancements = extra
        with self.assertRaisesRegexp(
                ValueError, "Trying to add pagination config for non "
                            "existent operation: ThisOperationDoesNotExist"):
            translate(self.model)

    def test_skip_jmespath_validation(self):
        # This would fail previously.
        extra = {
            'pagination': {
                'AssumeRole': {
                    'input_token': ['NextToken'],
                    'output_token': ['NextToken'],
                    'result_key': 'Credentials.AssumedRoleUser',
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        self.assertEqual(new_model['pagination'], extra['pagination'])

    def test_result_key_validation_with_no_output(self):
        extra = {
            'pagination': {
                # RealOperation does not have any output members so
                # we should get an error message telling us this.
                'NoOutputOperation': {
                    'input_token': 'NextToken',
                    'output_token': ['NextToken', 'NextTokenToken'],
                    'result_key': ['Credentials', 'AssumedRoleUser'],
                    'limit_key': 'Foo',
                }
            }
        }
        self.model.enhancements = extra
        with self.assertRaisesRegexp(
                ValueError, "Trying to add pagination config for an "
                            "operation with no output members: "
                            "NoOutputOperation"):
            translate(self.model)

    def test_echoed_input_params_ignored(self):
        extra = {
            'pagination': {
                'EchoedOutputParams': {
                    'input_token': ['Marker'],
                    'output_token': ['NextMarker'],
                    'result_key': 'ResultKey',
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        self.assertEqual(new_model['pagination'], extra['pagination'])


class TestBuildRetryConfig(unittest.TestCase):
    def setUp(self):
        self.retry = {
            "definitions": {
                "def_name": {
                    "from": {"definition": "file"}
                }
            },
            "retry": {
                "__default__": {
                    "max_attempts": 5,
                    "delay": "global_delay",
                    "policies": {
                        "global_one": "global",
                        "override_me": "global",
                    }
                },
                "sts": {
                    "__default__": {
                        "delay": "service_specific_delay",
                        "policies": {
                            "service_one": "service",
                            "override_me": "service",
                        }
                    },
                    "AssumeRole": {
                        "policies": {
                            "name": "policy",
                            "other": {"$ref": "def_name"}
                        }
                    }
                }
            }
        }

    def test_inject_retry_config(self):
        model = ModelFiles(SERVICES, self.retry, {})
        new_model = translate(model)
        self.assertIn('retry', new_model)
        retry = new_model['retry']
        self.assertIn('__default__', retry)
        self.assertEqual(
            retry['__default__'], {
                "max_attempts": 5,
                "delay": "service_specific_delay",
                "policies": {
                    "global_one": "global",
                    "override_me": "service",
                    "service_one": "service",
                }
            }
        )
        # Policies should be merged.
        operation_config = retry['AssumeRole']
        self.assertEqual(operation_config['policies']['name'], 'policy')

    def test_resolve_reference(self):
        model = ModelFiles(SERVICES, self.retry, {})
        new_model = translate(model)
        operation_config = new_model['retry']['AssumeRole']
        # And we should resolve references.
        self.assertEqual(operation_config['policies']['other'],
                         {"from": {"definition": "file"}})


class TestReplacePartOfOperation(unittest.TestCase):
    def test_replace_operation_key_name(self):
        enhancements = {
            'transformations': {
                'operation-name': {'remove': r'\d{4}_\d{2}_\d{2}'}
            }
        }
        model = ModelFiles(SERVICES, retry={},
                           enhancements=enhancements)
        new_model = translate(model)
        # But the key into the operation dict is stripped of the
        # matched regex.
        self.assertEqual(list(sorted(new_model['operations'].keys())),
                         ['AssumeRole', 'DeprecatedOperation',
                          'DeprecatedOperation2', 'EchoedOutputParams',
                          'NoOutputOperation','RealOperation',
                          'RenameOperation'])
        # But the name key attribute is left unchanged.
        self.assertEqual(new_model['operations']['RealOperation']['name'],
                         'RealOperation2013_02_04')

    def test_merging_occurs_after_transformation(self):
        enhancements = {
            'transformations': {
                'operation-name': {'remove': r'\d{4}_\d{2}_\d{2}'}
            },
            'operations': {
                'RealOperation': {
                    'input': {
                        'checksum': 'md5',
                    }
                },
            }
        }
        model = ModelFiles(SERVICES, retry={}, enhancements=enhancements)
        model.enhancements = enhancements
        new_model = translate(model)
        self.assertIn('RealOperation', new_model['operations'])
        self.assertEqual(
            new_model['operations']['RealOperation']['input']['checksum'],
            'md5')


class TestRemovalOfDeprecatedParams(unittest.TestCase):

    def test_remove_deprecated_params(self):
        enhancements = {
            'transformations': {
                'remove-deprecated-params': {'deprecated_keyword': 'deprecated'}
                }
            }
        model = ModelFiles(SERVICES, retry={}, enhancements=enhancements)
        new_model = translate(model)
        operation = new_model['operations']['DeprecatedOperation']
        # The deprecated param should be gone, the other should remain
        self.assertIn('FooBar', operation['input']['members'])
        self.assertNotIn('FieBaz', operation['input']['members'])

class TestRemovalOfDeprecatedOps(unittest.TestCase):

    def test_remove_deprecated_ops(self):
        enhancements = {
            'transformations': {
                'remove-deprecated-operations':
                    {'deprecated_keyword': 'deprecated'}
                }
            }
        model = ModelFiles(SERVICES, retry={}, enhancements=enhancements)
        new_model = translate(model)
        # The deprecated operation should be gone
        self.assertNotIn('DeprecatedOperation2', new_model['operations'])


class TestFilteringOfDocumentation(unittest.TestCase):

    def test_remove_deprecated_params(self):
        enhancements = {
            "transformations": {
                "filter-documentation": {
                    "filter": {
                        "regex": "<!\\[CDATA\\[.*\\]\\]>",
                        "replacement": ""
                        }
                    }
                }
            }
        model = ModelFiles(SERVICES, retry={}, enhancements=enhancements)
        new_model = translate(model)
        operation = new_model['operations']['DeprecatedOperation']
        # The deprecated param should be gone, the other should remain
        self.assertEqual(operation['documentation'], 'This is my  stuff')
        param = operation['input']['members']['FooBar']
        self.assertEqual(param['documentation'], 'blah blah blah blah')


class TestRenameParams(unittest.TestCase):
    def test_rename_param(self):
        enhancements = {
            'transformations': {
                'renames': {
                    'RenameOperation.input.members.RenameMe': 'BeenRenamed',
                }
            }
        }
        model = ModelFiles(SERVICES, retry={}, enhancements=enhancements)
        new_model = translate(model)
        arguments = new_model['operations']['RenameOperation']['input']['members']
        self.assertNotIn('RenameMe', arguments)
        self.assertIn('BeenRenamed', arguments)


class TestWaiterDenormalization(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.model = ModelFiles(SERVICES, {}, {})

    def test_waiter_default_resolved(self):
        extra = {
            'waiters': {
                '__default__': {
                    'interval': 20,
                    'operation': 'AssumeRole',
                    'max_attempts': 25,
                    'acceptor_type': 'output',
                    'acceptor_path': 'path',
                    'acceptor_value': 'value',
                },
                # Note that this config doesn't make any actual sense,
                # this is just testing we denormalize fields properly.
                'RoleExists': {
                    'operation': 'AssumeRole',
                    'ignore_errors': ['Error1'],
                    'success_type': 'output',
                    'success_path': 'Table.TableStatus',
                    'success_value': ['ACTIVE'],
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        denormalized = {
            'RoleExists': {
                'interval': 20,
                'max_attempts': 25,
                'operation': 'AssumeRole',
                'ignore_errors': ['Error1'],
                'success': {
                    'type': 'output',
                    'path': 'Table.TableStatus',
                    'value': ['ACTIVE'],
                },
                'failure': {
                    'type': 'output',
                    'path': 'path',
                    'value': ['value'],
                }
            }
        }
        self.assertEqual(new_model['waiters'], denormalized)

    def test_default_and_extends(self):
        extra = {
            'waiters': {
                '__default__': {
                    'interval': 20,
                    'max_attempts': 25,
                },
                '__RoleResource': {
                    'operation': 'AssumeRole',
                    'max_attempts': 50,
                },
                'RoleExists': {
                    'extends': '__RoleResource',
                    'ignore_errors': ['Error1'],
                    'success_type': 'output',
                    'success_path': 'Table.TableStatus',
                    'success_value': 'ACTIVE',
                    'failure_type': 'output',
                    'failure_path': 'Table.TableStatus',
                    'failure_value': 'ACTIVE',
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        denormalized = {
            'RoleExists': {
                # From __default__
                'interval': 20,
                # Overriden from __RoleResource
                'max_attempts': 50,
                # Defined in __RoleResource
                'operation': 'AssumeRole',
                # Defined in RoleExists
                'ignore_errors': ['Error1'],
                'success': {
                    'type': 'output',
                    'path': 'Table.TableStatus',
                    'value': ['ACTIVE'],
                },
                'failure': {
                    'type': 'output',
                    'path': 'Table.TableStatus',
                    'value': ['ACTIVE'],
                }
            }
        }
        self.assertEqual(new_model['waiters'], denormalized)

    def test_acceptor_path_resolution(self):
        extra = {
            'waiters': {
                'RoleExists': {
                    'operation': 'AssumeRole',
                    'acceptor_type': 'output',
                    'acceptor_path': 'acceptor_path',
                    'success_value': 'success_value',
                    'failure_value': 'failure_value',
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        denormalized = {
            'RoleExists': {
                'operation': 'AssumeRole',
                # We should only have success/failure values,
                # no acceptor types, those are all resolved.
                'success': {
                    # From acceptor_type.
                    'type': 'output',
                    # From acceptor_path.
                    'path': 'acceptor_path',
                    # From success_value.
                    'value': ['success_value'],
                },
                'failure': {
                    # From acceptor_type.
                    'type': 'output',
                    # From acceptor_path.
                    'path': 'acceptor_path',
                    # From failure_value.
                    'value': ['failure_value'],
                }
            }
        }
        self.assertEqual(new_model['waiters'], denormalized)

    def test_only_acceptors_provided(self):
        extra = {
            'waiters': {
                'RoleExists': {
                    'operation': 'AssumeRole',
                    'acceptor_type': 'output',
                    'acceptor_path': 'acceptor_path',
                    'acceptor_value': 'acceptor_value',
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        denormalized = {
            'RoleExists': {
                'operation': 'AssumeRole',
                'success': {
                    'type': 'output',
                    'path': 'acceptor_path',
                    'value': ['acceptor_value'],
                },
                'failure': {
                    'type': 'output',
                    'path': 'acceptor_path',
                    'value': ['acceptor_value'],
                }
            }
        }
        self.assertEqual(new_model['waiters'], denormalized)

    def test_validate_valid_operation(self):
        extra = {
            'waiters': {
                '__default__': {
                    'interval': 20,
                    'max_attempts': 25,
                },
                '__RoleResource': {
                    'operation': 'THISOPERATIONDOESNOTEXIST',
                    'max_attempts': 50,
                },
                'RoleExists': {
                    'extends': '__RoleResource',
                    'ignore_errors': ['Error1'],
                    'success_type': 'output',
                    'success_path': 'Table.TableStatus',
                    'success_value': 'ACTIVE',
                    'failure_type': 'output',
                    'failure_path': 'Table.TableStatus',
                    'failure_value': 'ACTIVE',
                }
            }
        }
        self.model.enhancements = extra
        with self.assertRaises(ValueError):
            new_model = translate(self.model)

    def test_only_success_defined(self):
        extra = {
            'waiters': {
                '__default__': {
                    "interval": 15,
                    "max_attempts": 40,
                    "acceptor_type": "output"
                },
                'AssumeRole': {
                    "operation": "AssumeRole",
                    "success_path": "Snapshots[].State",
                    "success_value": "completed"
                }
            }
        }
        self.model.enhancements = extra
        new_model = translate(self.model)
        denormalized = {
            'AssumeRole': {
                'interval': 15,
                'max_attempts': 40,
                'operation': 'AssumeRole',
                'success': {
                    'type': 'output',
                    'path': 'Snapshots[].State',
                    'value': ['completed'],
                },
                # This is technically "incorrect", in the sense that this is
                # not a valid waiter config, but the waiter module has tests
                # to verify that it handles this "incorrect" case.
                'failure': {
                    'type': 'output',
                }
            }
        }
        self.assertEqual(new_model['waiters'], denormalized)


class TestResemblesJMESPath(unittest.TestCase):
    maxDiff = None

    def test_is_jmespath(self):
      self.assertTrue(resembles_jmespath_exp('Something.Else'))
      self.assertTrue(resembles_jmespath_exp('Something[1]'))

    def test_is_not_jmespath(self):
      self.assertFalse(resembles_jmespath_exp('Something'))


if __name__ == '__main__':
    unittest.main()
