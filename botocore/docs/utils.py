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
import inspect
from collections import namedtuple


def py_type_name(type_name):
    """
    Get the Python type name for a given model type.

        >>> py_type_name('list')
        'list'
        >>> py_type_name('structure')
        'dict'

    :rtype: string
    """
    return {
        'blob': 'bytes',
        'character': 'string',
        'double': 'float',
        'long': 'integer',
        'map': 'dict',
        'structure': 'dict',
        'timestamp': 'datetime',
    }.get(type_name, type_name)


def py_default(type_name):
    """
    Get the Python default value for a given model type, useful
    for generated examples.

        >>> py_default('string')
        '\'string\''
        >>> py_default('list')
        '[...]'
        >>> py_default('unknown')
        '...'

    :rtype: string
    """
    return {
        'double': '123.0',
        'long': '123',
        'integer': '123',
        'string': "'string'",
        'blob': "b'bytes'",
        'boolean': 'True|False',
        'list': '[...]',
        'map': '{...}',
        'structure': '{...}',
        'timestamp': 'datetime(2015, 1, 1)',
    }.get(type_name, '...')


def get_official_service_name(service_model):
    """Generate the official name of an AWS Service

    :param service_model: The service model representing the service
    """
    official_name = service_model.metadata.get('serviceFullName')
    short_name = service_model.metadata.get('serviceAbbreviation', '')
    if short_name.startswith('Amazon'):
        short_name = short_name[7:]
    if short_name.startswith('AWS'):
        short_name = short_name[4:]
    if short_name and short_name.lower() not in official_name.lower():
        official_name += ' ({0})'.format(short_name)
    return official_name


def get_instance_methods(instance):
    """Retrieves an objects public methods and variables

    :param instance: The instance of the class to inspect
    :rtype: dict
    :returns: A dictionary that represents an instance's methods where
        the keys are the name of the methods and the
        values are the handler to the method.
    """
    instance_members = inspect.getmembers(instance)
    instance_methods = {}
    for name, member in instance_members:
        if not name.startswith('_'):
            if inspect.ismethod(member):
                instance_methods[name] = member
    return instance_methods


_DocumentedShape = namedtuple(
    'DocumentedShape', ['name', 'type_name', 'documentation', 'metadata'])


class DocumentedShape (_DocumentedShape):
    """Use this class to inject new shapes into a model for documentation"""
    def __new__(cls, name, type_name, documentation, metadata=None):
        if metadata is None:
            metadata = []
        return super(DocumentedShape, cls).__new__(
            cls, name, type_name, documentation, metadata)


class BaseMethodSignatureDocumentor(object):
    """Documents the method signature"""
    def document_signature(self, section, name, method_obj, include=None,
                           exclude=None):
        """Documents the signature of the method

        :param section: The section to write the documentation to.

        :param name: The name of the method

        :param method_obj: The object representing the method. For model
            driven methods it is an operation model. For custom
            methods it is the method handle.

        :type include: Dictionary where keys are parameter names and
            values are the shapes of the parameter names.
        :param include: The parameter shapes to include in the documentation.

        :type exclude: List of the names of the parameters to exclude.
        :param exclude: The names of the parameters to exclude from
            documentation.
        """
        self._document_signature(section, name, method_obj, include=include,
                                 exclude=exclude)


class ModelDrivenMethodSignatureDocumentor(BaseMethodSignatureDocumentor):
    """Documents a model method signature (i.e. has a JSON model)"""
    def _document_signature(self, section, name, method_obj, include=None,
                            exclude=None):
        params = {}
        required = []
        operation_model = method_obj
        if operation_model.input_shape:
            params = operation_model.input_shape.members
            required = operation_model.input_shape.required_members

        parameter_names = params.keys()

        if include is not None:
            for member in include:
                parameter_names.append(member.name)

        if exclude is not None:
            for member in exclude:
                if member in parameter_names:
                    parameter_names.remove(member)

        required_params = [k for k in parameter_names if k in required]
        optional_params = [k for k in parameter_names if k not in required]

        signature_params = ', '.join([
            ', '.join(['{0}=None'.format(k) for k in required_params]),
            ', '.join(['{0}=None'.format(k) for k in optional_params])
        ]).strip(', ')
        section.style.start_sphinx_py_method(name, signature_params)


class CustomMethodSignatureDocumentor(BaseMethodSignatureDocumentor):
    """Documents a custom method signature (i.e. not model driven)

    Note that currently the exclude and include parameters are ignored
    when documenting a custom method.
    """
    def _document_signature(self, section, name, method_obj, include=None,
                            exclude=None):
        args, varargs, keywords, defaults = inspect.getargspec(method_obj)
        args = args[1:]
        signature_params = inspect.formatargspec(
            args, varargs, keywords, defaults)
        signature_params = signature_params.lstrip('(')
        signature_params = signature_params.rstrip(')')
        section.style.start_sphinx_py_method(name, signature_params)


class BaseShapeDocumentor(object):
    """Generates documentation for a shape"""

    def _document_shape(self, section, shape, history, include=None,
                        exclude=None, **kwargs):
        param_type = shape.type_name
        if shape.name in history:
            # If the name of the shape is already in the history then
            # it is a recursive shape so quit recursing and document
            # the shape to indicate the shape is recursive.
            self._document_recursive_shape(section, shape, **kwargs)
        else:
            history.append(shape.name)
            getattr(self, '_document_shape_type_%s' % param_type,
                    self._document_shape_default)(
                        section, shape, history=history, include=include,
                        exclude=exclude, **kwargs)
            history.pop()

    def _document_recursive_shape(self, section, shape, **kwargs):
        pass

    def _document_shape_default(self, section, shape, history, include=None,
                                exclude=None, **kwargs):
        pass

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
        section.style.new_line()

    def _end_nested_param(self, section, end=None):
        section.style.dedent()
        section.style.new_line()
        if end is not None:
            section.write(end)


class BaseParamsDocumentor(BaseShapeDocumentor):
    def document_params(self, section, shape, include=None, exclude=None):
        """Fills out the documentation for a section given a model shape.

        :param section: The section to write the documentation to.

        :param shape: The shape of the operation.

        :type include: Dictionary where keys are parameter names and
            values are the shapes of the parameter names.
        :param include: The parameter shapes to include in the documentation.

        :type exclude: List of the names of the parameters to exclude.
        :param exclude: The names of the parameters to exclude from
            documentation.
        """
        history = []
        self._document_shape(section, shape, history, name=None,
                             include=include, exclude=exclude)

    def _document_recursive_shape(self, section, shape, **kwargs):
        self._add_member_documentation(section, shape, **kwargs)

    def _document_shape_default(self, section, shape, history, include=None,
                                exclude=None, **kwargs):
        self._add_member_documentation(section, shape, **kwargs)

    def _add_member_documentation(self, section, shape, **kwargs):
        pass

    def _document_shape_type_list(self, section, shape, history, include=None,
                                  exclude=None, **kwargs):
        self._add_member_documentation(section, shape, **kwargs)
        param_shape = shape.member
        self._start_nested_param(section)
        kwargs['name'] = None
        self._document_shape(section, param_shape, history, **kwargs)
        self._end_nested_param(section)

    def _document_shape_type_map(self, section, shape, history, include=None,
                                 exclude=None, **kwargs):
        self._add_member_documentation(section, shape, **kwargs)

        self._start_nested_param(section)
        self._add_member_documentation(section, shape.key)

        self._start_nested_param(section)
        kwargs['name'] = None
        self._document_shape(
            section, shape.value, history, **kwargs)
        self._end_nested_param(section)
        self._end_nested_param(section)

    def _document_shape_type_structure(self, section, shape, history,
                                       include=None, exclude=None, **kwargs):
        name = kwargs.get('name', None)
        members = self._add_members_to_shape(shape.members, include)
        self._add_member_documentation(section, shape, name=name)
        for param in members:
            if exclude and param in exclude:
                continue
            self._start_nested_param(section)
            param_shape = members[param]
            kwargs['name'] = param
            self._document_shape(section, param_shape, history, **kwargs)
            self._end_nested_param(section)


class ResponseParamsDocumentor(BaseParamsDocumentor):
    """Generates the description for the response parameters"""

    def _add_member_documentation(self, section, shape, **kwargs):
        name = kwargs.get('name', None)
        py_type = py_type_name(shape.type_name)
        section.write('- ')
        if name is not None:
            section.style.bold('%s ' % name)
        section.style.italics('(%s) -- ' % py_type)

        if shape.documentation:
            section.style.indent()
            section.include_doc_string(shape.documentation)
            section.style.dedent()
        section.style.new_paragraph()


class RequestParamsDocumentor(BaseParamsDocumentor):
    """Generates the description for the request parameters"""

    def _document_shape(self, section, shape, history, include=None,
                        exclude=None, **kwargs):
        name = kwargs.get('name', None)
        param_type = shape.type_name
        if shape.name in history:
            self._add_member_documentation(section, shape, name=name)
        else:
            history.append(shape.name)
            is_top_level_param = (len(history) == 2)
            is_required = kwargs.get('is_required', False)
            getattr(self, '_document_shape_type_%s' % param_type,
                    self._document_shape_default)(
                        section, shape, history=history, name=name,
                        is_top_level_param=is_top_level_param,
                        is_required=is_required, include=include,
                        exclude=exclude)
            history.pop()

    def _document_shape_type_structure(self, section, shape, history,
                                       include=None, exclude=None, **kwargs):
        if len(history) > 1:
            self._add_member_documentation(section, shape, **kwargs)
        members = self._add_members_to_shape(shape.members, include)
        for i, param in enumerate(members):
            if exclude and param in exclude:
                continue
            if len(history) > 1:
                section.style.indent()
            section.style.new_line()
            param_shape = members[param]
            is_required = param in shape.required_members
            self._document_shape(
                section, param_shape, history, name=param,
                is_required=is_required)
            if len(history) > 1:
                section.style.dedent()
            section.style.new_line()

    def _add_member_documentation(self, section, shape, name=None, **kwargs):
        is_top_level_param = kwargs.get('is_top_level_param', False)
        is_required = kwargs.get('is_required', False)

        py_type = py_type_name(shape.type_name)
        if is_top_level_param:
            section.write(':type %s: %s' % (name, py_type))
            section.style.new_line()
            section.write(':param %s: ' % name)

        else:
            section.write('- ')
            if name is not None:
                section.style.bold('%s ' % name)
            section.style.italics('(%s) -- ' % py_type)

        if is_required:
            section.style.indent()
            section.style.bold('[REQUIRED] ')
            section.style.dedent()
        if shape.documentation:
            section.style.indent()
            section.include_doc_string(shape.documentation)
            section.style.dedent()
        section.style.new_paragraph()


class BaseExampleDocumentor(BaseShapeDocumentor):
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
        self._document_shape(section, shape, history, include=include,
                             exclude=exclude)

    def _document_recursive_shape(self, section, shape, **kwargs):
        section.write('{\'... recursive ...\'}')

    def _document_shape_default(self, section, shape, history, include=None,
                                exclude=None):
        py_type = py_default(shape.type_name)
        section.write(py_type)

    def _document_shape_type_string(self, section, shape, history,
                                    include=None, exclude=None, **kwargs):
        if 'enum' in shape.metadata:
            for i, enum in enumerate(shape.metadata['enum']):
                section.write('\'%s\'' % enum)
                if i < len(shape.metadata['enum']) - 1:
                    section.write('|')
        else:
            self._document_shape_default(section, shape, history)

    def _document_shape_type_list(self, section, shape, history, include=None,
                                  exclude=None, **kwargs):
        self._start_nested_param(section, '[')
        param_shape = shape.member
        self._document_shape(section, param_shape, history)
        section.write(',')
        self._end_nested_param(section, ']')

    def _document_shape_type_structure(self, section, shape, history,
                                       include=None, exclude=None, **kwargs):
        self._start_nested_param(section, '{')

        input_members = self._add_members_to_shape(shape.members, include)

        for i, param in enumerate(input_members):
            if exclude and param in exclude:
                continue
            section.write('\'%s\': ' % param)
            param_shape = input_members[param]
            self._document_shape(section, param_shape, history)
            if i < len(input_members) - 1:
                section.write(',')
                section.style.new_line()

        self._end_nested_param(section, '}')

    def _document_shape_type_map(self, section, shape, history,
                                 include=None, exclude=None, **kwargs):
        self._start_nested_param(section, '{')
        value_shape = shape.value
        section.write('\'string\': ')
        self._document_shape(section, value_shape, history)
        self._end_nested_param(section, '}')

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


class ResponseExampleDocumentor(BaseExampleDocumentor):
    pass


class RequestExampleDocumentor(BaseExampleDocumentor):
    def _document_shape_type_structure(self, section, shape, history,
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
            self._document_shape(section, param_shape, history)
            if i < len(input_members) - 1:
                section.write(',')
                section.style.new_line()
        self._end_nested_param(section, end)


class ModelDrivenMethodDocumentor(object):
    def document_method(self, section, method_name, operation_model,
                        method_description=None, example_prefix=None,
                        include_input=None, include_output=None,
                        exclude_input=None, exclude_output=None,
                        document_output=True):
        """Documents an individual method

        :param section: The section to write to

        :param method_name: The name of the method

        :param operation_model: The model of the operation

        :param example_prefix: The prefix to use in the method example.

        :type include_input: Dictionary where keys are parameter names and
            values are the shapes of the parameter names.
        :param include_input: The parameter shapes to include in the
            input documentation.

        :type include_output: Dictionary where keys are parameter names and
            values are the shapes of the parameter names.
        :param include_input: The parameter shapes to include in the
            output documentation.

        :type exclude_input: List of the names of the parameters to exclude.
        :param exclude_input: The names of the parameters to exclude from
            input documentation.

        :type exclude_output: List of the names of the parameters to exclude.
        :param exclude_input: The names of the parameters to exclude from
            output documentation.

        :param document_output: A boolean flag to indicate whether to
            document the output.
        """
        # Add the signature.
        ModelDrivenMethodSignatureDocumentor().document_signature(
            section, method_name, operation_model, include=include_input,
            exclude=exclude_input)

        # Add the description for the method.
        method_intro_section = section.add_new_section('method-intro')
        method_intro_section.include_doc_string(method_description)

        # Add the example section.
        example_section = section.add_new_section('example')
        example_section.style.new_paragraph()
        example_section.style.bold('Example')
        if operation_model.input_shape:
            RequestExampleDocumentor().document_example(
                example_section, operation_model.input_shape,
                prefix=example_prefix, include=include_input,
                exclude=exclude_input)
        else:
            example_section.style.new_paragraph()
            example_section.style.start_codeblock()
            example_section.write(example_prefix + '()')

        # Add the request parameter documentation.
        request_params_section = section.add_new_section('request-params')
        if operation_model.input_shape:
            RequestParamsDocumentor().document_params(
                request_params_section, operation_model.input_shape,
                include=include_input, exclude=exclude_input)

        # Add the return value documentation
        return_section = section.add_new_section('return')
        return_section.style.new_line()
        if operation_model.output_shape is not None and document_output:
            return_section.write(':rtype: dict')
            return_section.style.new_line()
            return_section.write(':returns: ')
            return_section.style.indent()
            return_section.style.new_line()

            # Add an example return value
            return_example_section = return_section.add_new_section('example')
            return_example_section.style.new_line()
            return_example_section.style.bold('Response Example')
            return_example_section.style.new_paragraph()
            ResponseExampleDocumentor().document_example(
                return_example_section, operation_model.output_shape,
                include=include_output, exclude=exclude_output)
            return_example_section.style.new_paragraph()

            # Add a description for the return value
            return_description_section = return_section.add_new_section(
                'description')
            return_description_section.style.new_line()
            return_description_section.style.bold('Response Structure')
            return_description_section.style.new_paragraph()
            ResponseParamsDocumentor().document_params(
                return_description_section, operation_model.output_shape,
                include=include_output, exclude=exclude_output)
        else:
            return_section.write(':returns: None')
