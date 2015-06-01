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
from botocore.docs.utils import traverse_and_document_shape
from botocore.docs.utils import py_default


class BaseExampleDocumenter(object):
    def document_example(self, section, shape, prefix=None, include=None,
                         exclude=None):
        """Generates an example based on a shape

        :param section: The section to write the documentation to.

        :param shape: The shape of the operation.

        :param prefix: Anything to be included before the example

        :type include: Dictionary where keys are parameter names and
            values are the shapes of the parameter names.
        :param include: The parameter shapes to include in the documentation.

        :type exclude: List of the names of the parameters to exclude.
        :param exclude: The names of the parameters to exclude from
            documentation.
        """
        history = []
        section.style.new_line()
        section.style.start_codeblock()
        if prefix is not None:
            section.write(prefix)
        traverse_and_document_shape(
            documenter=self, section=section, shape=shape, history=history,
            include=include, exclude=exclude)

    def document_recursive_shape(self, section, shape, **kwargs):
        section.write('{\'... recursive ...\'}')

    def document_shape_default(self, section, shape, history, include=None,
                               exclude=None, **kwargs):
        py_type = py_default(shape.type_name)
        section.write(py_type)

    def document_shape_type_string(self, section, shape, history,
                                   include=None, exclude=None, **kwargs):
        if 'enum' in shape.metadata:
            for i, enum in enumerate(shape.metadata['enum']):
                section.write('\'%s\'' % enum)
                if i < len(shape.metadata['enum']) - 1:
                    section.write('|')
        else:
            self.document_shape_default(section, shape, history)

    def document_shape_type_list(self, section, shape, history, include=None,
                                 exclude=None, **kwargs):
        self._start_nested_param(section, '[')
        param_shape = shape.member
        traverse_and_document_shape(
            documenter=self, section=section, shape=param_shape,
            history=history)
        section.write(',')
        self._end_nested_param(section, ']')

    def document_shape_type_structure(self, section, shape, history,
                                      include=None, exclude=None, **kwargs):
        self._start_nested_param(section, '{')

        input_members = self._add_members_to_shape(shape.members, include)

        for i, param in enumerate(input_members):
            if exclude and param in exclude:
                continue
            section.write('\'%s\': ' % param)
            param_shape = input_members[param]
            traverse_and_document_shape(
                documenter=self, section=section, shape=param_shape,
                history=history)
            if i < len(input_members) - 1:
                section.write(',')
                section.style.new_line()

        self._end_nested_param(section, '}')

    def document_shape_type_map(self, section, shape, history,
                                include=None, exclude=None, **kwargs):
        self._start_nested_param(section, '{')
        value_shape = shape.value
        section.write('\'string\': ')
        traverse_and_document_shape(
            documenter=self, section=section, shape=value_shape,
            history=history)
        self._end_nested_param(section, '}')

    def _add_members_to_shape(self, members, include):
        if include:
            members = members.copy()
            for param in include:
                members[param.name] = param
        return members

    def _start_nested_param(self, section, start=None):
        if start is not None:
            section.write(start)
        section.style.indent()
        section.style.indent()
        section.style.new_line()

    def _end_nested_param(self, section, end=None):
        section.style.dedent()
        section.style.dedent()
        section.style.new_line()
        if end is not None:
            section.write(end)


class ResponseExampleDocumenter(BaseExampleDocumenter):
    pass


class RequestExampleDocumenter(BaseExampleDocumenter):
    def document_shape_type_structure(self, section, shape, history,
                                      include=None, exclude=None, **kwargs):
        param_format = '\'%s\''
        operator = ': '
        start = '{'
        end = '}'

        if len(history) <= 1:
            operator = '='
            start = '('
            end = ')'
            param_format = '%s'

        self._start_nested_param(section, start)
        input_members = self._add_members_to_shape(shape.members, include)

        for i, param in enumerate(input_members):
            if exclude and param in exclude:
                continue
            section.write(param_format % param)
            section.write(operator)
            param_shape = input_members[param]
            traverse_and_document_shape(
                documenter=self, section=section, shape=param_shape,
                history=history)
            if i < len(input_members) - 1:
                section.write(',')
                section.style.new_line()
        self._end_nested_param(section, end)
