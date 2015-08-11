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
import re

class SharedExampleBuilder(object):
    def __init__(self, params, operation_name, comments, is_input=True):
        self._params = params
        self._operation_name = operation_name
        self._comments = comments
        self._is_input = is_input

    def example_code(self, prefix=''):
        if self._is_input:
            return prefix + self._visit(self._params, '', [], is_param=True)
        else:
            return self._visit(self._params, '', [], is_param=False)

    def _visit(self, value, indent, path, is_param=False):
        if is_param:
            return self._visit_param(value, indent, path)
        if isinstance(value, dict):
            return self._visit_struct(value, indent, path)
        elif isinstance(value, list):
            return self._visit_list(value, indent, path)
        elif isinstance(value, basestring):
            return "'%s'" % value
        else:
            return value

    def _visit_param(self, value, indent, path):
        lines = ['(']
        for key, val in value.items():
            path.append('.%s' % key)
            comment = self._apply_comment(path)
            shape_val = self._visit(val, '    ' + indent, path)
            lines.append("%s    %s=%s, %s" %
                (indent, key, shape_val, comment))
            path.pop()
        lines.append('%s)' % indent)
        return '\n'.join(lines)


    def _visit_struct(self, value, indent, path):
        lines = ['{']
        for key, val in value.items():
            path.append('.%s' % key)
            comment = self._apply_comment(path)
            shape_val = self._visit(val, '    ' + indent, path)
            lines.append("%s    '%s': %s, %s" %
                (indent, key, shape_val, comment))
            path.pop()
        lines.append('%s}' % indent)
        return '\n'.join(lines)

    def _visit_list(self, value, indent, path):
        lines = ['[']
        for ind, val in enumerate(value):
            path.append('[%s]' % ind)
            comment = self._apply_comment(path)
            shape_val = self._visit(val, '    ' + indent, path)
            lines.append('%s    %s, %s' %
                (indent, shape_val, comment))
            path.pop()
        lines.append('%s]' % indent)
        return '\n'.join(lines)

    def _apply_comment(self, path):
        key = re.sub('^\.', '', ''.join(path))
        if self._comments and key in self._comments:
            return '# ' + self._comments[key]
        else:
            return ''
