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
from botocore.vendored.six import string_types


class SharedExampleBuilder(object):
    def __init__(self, params, operation_name, comments=None, is_input=True):
        self._params = params
        self._operation_name = operation_name
        self._comments = comments
        self._is_input = is_input

    def build_example_code(self, prefix=''):
        if self._is_input:
            return prefix + self._visit(self._params, '', [], is_param=True)
        else:
            return self._visit(self._params, '', [], is_param=False)

    def _visit(self, value, indent, path, is_param=False):
        if is_param:
            return self._visit_param(value, indent, path)
        if isinstance(value, dict):
            return self._visit_dict(value, indent, path)
        if isinstance(value, list):
            return self._visit_list(value, indent, path)
        if isinstance(value, string_types):
            return self._visit_str(value)

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

    def _visit_dict(self, value, indent, path):
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
        for index, val in enumerate(value):
            path.append('[%s]' % index)
            comment = self._apply_comment(path)
            shape_val = self._visit(val, '    ' + indent, path)
            lines.append('%s    %s, %s' %
                         (indent, shape_val, comment))
            path.pop()
        lines.append('%s]' % indent)
        return '\n'.join(lines)

    def _visit_str(self, value):
        return "'%s'" % value

    def _apply_comment(self, path):
        key = re.sub('^\.', '', ''.join(path))
        if self._comments and key in self._comments:
            return '# ' + self._comments[key]
        else:
            return ''


def document_shared_examples(section, operation_model, example_prefix,
                             shared_examples):
    """Documents the shared examples

    :param section: The section to write to.

    :param operation_model: The model of the operation.

    :param example_prefix: The prefix to use in the method example.

    :param shared_examples: The shared JSON examples from the model.
    """
    shared_example_section = section.add_new_section('shared-examples')
    shared_example_section.style.new_paragraph()
    shared_example_section.style.bold('Examples')
    for example in shared_examples:
        shared_example_section.style.new_paragraph()
        shared_example_section.write(example['description'])
        shared_example_section.style.new_line()
        comments = example['comments']
        request = SharedExampleBuilder(
            params=example['input'],
            operation_name=operation_model.name,
            comments=comments.get('input')).build_example_code(
            prefix=example_prefix).split('\n')
        shared_example_section.style.start_codeblock()
        shared_example_section.write(request.pop(0) + '\n')
        for line in request:
            shared_example_section.writeln(line)

        if 'output' in example:
            shared_example_section.style.new_line()
            shared_example_section.writeln('print(response)')
            shared_example_section.style.end_codeblock()
            shared_example_section.style.new_line()
            shared_example_section.write('Expected Output:')
            shared_example_section.style.new_line()
            response = SharedExampleBuilder(
                params=example['output'],
                operation_name=operation_model.name,
                comments=comments.get('output'),
                is_input=False).build_example_code().split('\n')
            response.insert(-1, "    'ResponseMetadata': {...}")
            shared_example_section.style.start_codeblock()
            shared_example_section.write(response.pop(0) + '\n')
            for line in response:
                shared_example_section.writeln(line)
            shared_example_section.style.end_codeblock()
        else:
            shared_example_section.style.end_codeblock()
