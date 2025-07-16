# Copyright 2025 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import os
from unittest import mock

from botocore.context import (
    ClientContext,
    get_context,
    start_as_current_context,
)
from botocore.plugin import get_botocore_plugins


def test_get_botocore_plugins_env():
    with start_as_current_context(ClientContext()):
        ctx = get_context()
        ctx.plugins = None  # Explicitly unset to test env fallback
        with mock.patch.dict(
            os.environ, {'BOTOCORE_EXPERIMENTAL__PLUGINS': 'a=b'}
        ):
            assert get_botocore_plugins() == 'a=b'
        assert get_botocore_plugins() is None


def test_get_botocore_plugins_ctx_takes_precedence():
    with (
        start_as_current_context(ClientContext()),
        mock.patch.dict(
            os.environ, {'BOTOCORE_EXPERIMENTAL__PLUGINS': 'DISABLED'}
        ),
    ):
        ctx = get_context()
        ctx.plugins = "a=b"
        assert get_botocore_plugins() == 'a=b'
