#!/usr/bin/env
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
from nose.tools import assert_true

from botocore import errorfactory
from botocore.exceptions import ClientError

def test_errorfactory():
    assert_true(isinstance(errorfactory.__all__, list))
    assert_true(isinstance(errorfactory.__file__, str))
    assert_true(isinstance(errorfactory.__name__, str))
    assert_true(issubclass(errorfactory.Foo, ClientError))
