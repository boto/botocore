# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
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

import sys
import xml.etree.cElementTree
import logging

from botocore import ScalarTypes
from botocore.hooks import first_non_none_response
from botocore.compat import json, set_socket_timeout, XMLParseError
from botocore.exceptions import IncompleteReadError


logger = logging.getLogger(__name__)


class Response(object):

    def __init__(self, session, operation):
        self.session = session
        self.operation = operation
        self.value = {}

    def parse(self, s, encoding):
        pass

    def get_value(self):
        value = ''
        if self.value:
            value = self.value
        return value

    def merge_header_values(self, headers):
        pass


class XmlResponse(Response):

    def __init__(self, session, operation):
        Response.__init__(self, session, operation)
        self.tree = None
        self.element_map = {}
        self.value = {}
        self._parent = None

    def clark_notation(self, tag):
        return '{%s}%s' % (self.operation.service.xmlnamespace, tag)

    def get_element_base_tag(self, elem):
        if '}' in elem.tag:
            elem_tag = elem.tag.split('}')[1]
        else:
            elem_tag = elem.tag
        return elem_tag

    def parse(self, s, encoding):
        if self.operation.output:
            self.build_element_map(self.operation.output, 'root')
        parser = xml.etree.cElementTree.XMLParser(
            target=xml.etree.cElementTree.TreeBuilder(),
            encoding=encoding)
        self.value = {}
        try:
            parser.feed(s)
        except XMLParseError as e:
            # Check the case where we have a single output member
            # that has a single element that's a payload.
            if self.operation.output and len(self.operation.output['members']) == 1:
                members = self.operation.output['members']
                member_name = list(members.keys())[0]
                if members[member_name].get('payload'):
                    # Then the final result is just a single key
                    # whose value is the response body.
                    self.value = {member_name: s, 'ResponseMetadata': {}}
                return
            else:
                raise
        else:
            self.tree = parser.close()
            self.start(self.tree)

    def get_response_metadata(self):
        rmd = {}
        self.value['ResponseMetadata'] = rmd
        rmd_elem = self.tree.find(self.clark_notation('ResponseMetadata'))
        if rmd_elem is not None:
            rmd_elem.tail = True
            request_id = rmd_elem.find(self.clark_notation('RequestId'))
        else:
            request_id = self.tree.find(self.clark_notation('requestId'))
            if request_id is None:
                request_id = self.tree.find(self.clark_notation('RequestId'))
            if request_id is None:
                request_id = self.tree.find('RequestID')
        if request_id is not None:
            request_id.tail = True
            rmd['RequestId'] = request_id.text.strip()

    def _get_error_data(self, error_elem):
        data = {}
        for elem in error_elem:
            elem.tail = True
            data[self.get_element_base_tag(elem)] = elem.text
        return data

    def get_response_errors(self):
        errors = None
        error_elems = self.tree.find('Errors')
        if error_elems is not None:
            error_elems.tail = True
            errors = [self._get_error_data(e) for e in error_elems]
        else:
            error_elems = self.tree.find(self.clark_notation('Error'))
            if error_elems is not None:
                error_elems.tail = True
                errors = [self._get_error_data(error_elems)]
            elif self.tree.tag == 'Error':
                errors = [self._get_error_data(self.tree)]
        if errors:
            self.value['Errors'] = errors

    def build_element_map(self, defn, keyname):
        xmlname = defn.get('xmlname', keyname)
        if not xmlname:
            xmlname = defn.get('shape_name')
        self.element_map[xmlname] = defn
        if defn['type'] == 'structure':
            for member_name in defn['members']:
                self.build_element_map(defn['members'][member_name],
                                       member_name)
        elif defn['type'] == 'list':
            self.build_element_map(defn['members'], None)
        elif defn['type'] == 'map':
            self.build_element_map(defn['keys'], 'key')
            self.build_element_map(defn['members'], 'value')

    def find(self, parent, tag):
        tag = tag.split(':')[-1]
        cn = self.clark_notation(tag)
        child = parent.find(cn)
        if child is None:
            child = parent.find('*/%s' % cn)
            if child is None \
                    and parent.tag == cn:
                child = parent
        return child

    def findall(self, parent, tag):
        cn = self.clark_notation(tag)
        children = parent.findall(cn)
        if not children:
            try:
                children = parent.findall('*/%s' % cn)
            except Exception:
                pass
        return children

    def parent_slow(self, elem, target):
        for child in elem:
            if child == target:
                self._parent = elem
                break
            self.parent_slow(child, target)

    def parent(self, elem):
        # We need the '..' operator in XPath but only that is only
        # available in Python versions >= 2.7
        if sys.version_info[0] == 2 and sys.version_info[1] == 6:
            self.parent_slow(self.tree, elem)
            parent = self._parent
            self._parent = None
        else:
            parent = self.tree.find('.//%s/..' % elem.tag)
        return parent

    def get_elem_text(self, elem):
        data = elem.text
        if data is not None:
            data = elem.text.strip()
        return data

    def _handle_string(self, elem, shape):
        data = self.get_elem_text(elem)
        if not data:
            children = list(elem)
            if len(children) == 1:
                data = self.get_elem_text(children[0])
        return data

    _handle_timestamp = _handle_string
    _handle_blob = _handle_string

    def _handle_integer(self, elem, shape):
        data = self.get_elem_text(elem)
        if data:
            data = int(data)
        return data

    _handle_long = _handle_integer

    def _handle_float(self, elem, shape):
        data = self.get_elem_text(elem)
        if data:
            data = float(data)
        return data

    _handle_double = _handle_float

    def _handle_boolean(self, elem, shape):
        return True if elem.text.lower() == 'true' else False

    def _handle_structure(self, elem, shape):
        new_data = {}
        xmlname = shape.get('xmlname')
        if xmlname:
            tagname = self.get_element_base_tag(elem)
            if xmlname != tagname:
                return new_data
        for member_name in shape['members']:
            member_shape = shape['members'][member_name]
            xmlname = member_shape.get('xmlname', member_name)
            child = self.find(elem, xmlname)
            if child is not None:
                new_data[member_name] = self.handle_elem(
                    member_name, child, member_shape)
        return new_data

    def _handle_list(self, elem, shape):
        xmlname = shape['members'].get('xmlname', 'member')
        children = self.findall(elem, xmlname)
        if not children and shape.get('flattened'):
            parent = self.parent(elem)
            if parent is not None:
                tagname = self.get_element_base_tag(elem)
                children = self.findall(parent, tagname)
        if not children:
            children = []
        return [self.handle_elem(None, child, shape['members'])
                for child in children]

    def _handle_map(self, elem, shape):
        data = {}
        # First collect all map entries
        xmlname = shape.get('xmlname', 'entry')
        keyshape = shape['keys']
        valueshape = shape['members']
        key_xmlname = keyshape.get('xmlname', 'key')
        value_xmlname = valueshape.get('xmlname', 'value')
        members = self.findall(elem, xmlname)
        if not members:
            parent = self.parent(elem)
            if parent is not None:
                members = self.findall(parent, xmlname)
        for member in members:
            key = self.find(member, key_xmlname)
            value = self.find(member, value_xmlname)
            cn = self.clark_notation(value_xmlname)
            value = member.find(cn)
            key_name = self.handle_elem(None, key, keyshape)
            data[key_name] = self.handle_elem(key_name, value, valueshape)
        return data

    def emit_event(self, tag, shape, value):
        if 'shape_name' in shape:
            event = self.session.create_event(
                'after-parsed', self.operation.service.endpoint_prefix,
                self.operation.name, shape['shape_name'], tag)
            rv = first_non_none_response(self.session.emit(event,
                                                           shape=shape,
                                                           value=value),
                                         None)
            if rv:
                value = rv
        return value

    def handle_elem(self, key, elem, shape):
        handler_name = '_handle_%s' % shape['type']
        elem.tail = True
        if hasattr(self, handler_name):
            value = getattr(self, handler_name)(elem, shape)
            value = self.emit_event(key, shape, value)
            return value
        else:
            logger.debug('Unhandled type: %s', shape['type'])

    def fake_shape(self, elem):
        shape = {}
        tags = set()
        nchildren = 0
        for child in elem:
            tags.add(child)
            nchildren += 1
        if nchildren == 0:
            shape['type'] = 'string'
        elif nchildren > 1 and len(tags) == 1:
            shape['type'] = 'list'
            shape['members'] = {'type': 'string'}
        else:
            shape['type'] = 'structure'
            shape['members'] = {}
            for tag in tags:
                base_tag = self.get_element_base_tag(tag)
                shape['members'][base_tag] = {'type': 'string'}
        return shape

    def start(self, elem):
        if self.operation.output:
            for member_name in self.operation.output['members']:
                member = self.operation.output['members'][member_name]
                xmlname = member.get('xmlname', member_name)
                child = self.find(elem, xmlname)
                if child is None and member['type'] not in ScalarTypes:
                    child = elem
                if child is not None:
                    self.value[member_name] = self.handle_elem(member_name,
                                                               child, member)
        self.get_response_metadata()
        self.get_response_errors()
        for child in self.tree:
            if child.tail is not True:
                child_tag = self.get_element_base_tag(child)
                if child_tag not in self.element_map:
                    if not child_tag.startswith(self.operation.name):
                        shape = self.fake_shape(child)
                        self.value[child_tag] = self.handle_elem(child_tag,
                                                                 child, shape)

    def merge_header_values(self, headers):
        if self.operation.output:
            for member_name in self.operation.output['members']:
                member = self.operation.output['members'][member_name]
                location = member.get('location')
                if location == 'header':
                    location_name = member.get('location_name')
                    if member['type'] == 'map':
                        self._merge_map_header_values(headers, location_name,
                                                      member_name, member)
                    elif location_name in headers:
                        self.value[member_name] = headers[location_name]

    def _merge_map_header_values(self, headers, location_name,
                                 member_name, member):
        final_map_value = {}
        for header_name in headers:
            if header_name.startswith(location_name):
                header_value = headers[header_name]
                actual_name = header_name[len(location_name):]
                final_map_value[actual_name] = header_value
        if final_map_value:
            self.value[member_name] = final_map_value


class JSONResponse(Response):

    def parse(self, s, encoding):
        try:
            decoded = s.decode(encoding)
            self.value = json.loads(decoded)
        except Exception as err:
            logger.debug('Error loading JSON response body, %r', err)

    def merge_header_values(self, headers):
        # Most JSON services return a __type in error response bodies.
        # Unfortunately, ElasticTranscoder does not.  It simply returns
        # a JSON body with a single key, "message".
        error = None
        if '__type' in self.value:
            error_type = self.value['__type']
            error = {'Type': error_type}
            del self.value['__type']
            for key in ['message', 'Message']:
                if key in self.value:
                    error['Message'] = self.value[key]
                    del self.value[key]
            code = self._parse_code_from_type(error_type)
            error['Code'] = code
        elif 'message' in self.value and len(self.value.keys()) == 1:
            error_type = 'Unspecified'
            if headers and 'x-amzn-errortype' in headers:
                # ElasticTranscoder suffixes errors with `:`, so we strip
                # them off when possible.
                error_type = headers.get('x-amzn-errortype').strip(':')
            error = {'Type': error_type, 'Code': error_type,
                     'Message': self.value['message']}
            del self.value['message']
        if error:
            self.value['Errors'] = [error]

    def _parse_code_from_type(self, error_type):
        return error_type.rsplit('#', 1)[-1]


class StreamingResponse(Response):

    def __init__(self, session, operation):
        Response.__init__(self, session, operation)
        self.value = {}

    def parse(self, headers, stream):
        for member_name in self.operation.output['members']:
            member_dict = self.operation.output['members'][member_name]
            if member_dict.get('location') == 'header':
                header_name = member_dict.get('location_name')
                if header_name and header_name in headers:
                    self.value[member_name] = headers[header_name]
            elif member_dict.get('type') == 'blob':
                if member_dict.get('payload'):
                    if member_dict.get('streaming'):
                        self.value[member_name] = stream


class StreamingBody(object):
    """Wrapper class for an http response body.

    This provides a few additional conveniences that do not exist
    in the urllib3 model:

        * Set the timeout on the socket (i.e read() timeouts)
        * Auto validation of content length, if the amount of bytes
          we read does not match the content length, an exception
          is raised.

    """
    def __init__(self, raw_stream, content_length):
        self._raw_stream = raw_stream
        self._content_length = content_length
        self._amount_read = 0

    def set_socket_timeout(self, timeout):
        """Set the timeout seconds on the socket."""
        # The problem we're trying to solve is to prevent .read() calls from
        # hanging.  This can happen in rare cases.  What we'd like to ideally
        # do is set a timeout on the .read() call so that callers can retry
        # the request.
        # Unfortunately, this isn't currently possible in requests.
        # See: https://github.com/kennethreitz/requests/issues/1803
        # So what we're going to do is reach into the guts of the stream and
        # grab the socket object, which we can set the timeout on.  We're
        # putting in a check here so in case this interface goes away, we'll
        # know.
        try:
            # To further complicate things, the way to grab the
            # underlying socket object from an HTTPResponse is different
            # in py2 and py3.  So this code has been pushed to botocore.compat.
            set_socket_timeout(self._raw_stream, timeout)
        except AttributeError:
            logger.error("Cannot access the socket object of "
                         "a streaming response.  It's possible "
                         "the interface has changed.", exc_info=True)
            raise

    def read(self, amt=None):
        chunk = self._raw_stream.read(amt)
        self._amount_read += len(chunk)
        if not chunk or amt is None:
            # If the server sends empty contents or
            # we ask to read all of the contents, then we know
            # we need to verify the content length.
            self._verify_content_length()
        return chunk

    def _verify_content_length(self):
        if self._content_length is not None and \
                self._amount_read != int(self._content_length):
            raise IncompleteReadError(
                actual_bytes=self._amount_read,
                expected_bytes=int(self._content_length))


def _validate_content_length(expected_content_length, body_length):
    # See: https://github.com/kennethreitz/requests/issues/1855
    # Basically, our http library doesn't do this for us, so we have
    # to do this ourself.
    if expected_content_length is not None:
        if int(expected_content_length) != body_length:
            raise IncompleteReadError(
                actual_bytes=body_length,
                expected_bytes=int(expected_content_length))


def get_response(session, operation, http_response):
    encoding = 'utf-8'
    if http_response.encoding:
        encoding = http_response.encoding
    content_type = http_response.headers.get('content-type')
    if content_type and ';' in content_type:
        content_type = content_type.split(';')[0]
        logger.debug('Content type from response: %s', content_type)
    if operation.is_streaming():
        logger.debug(
            "Response Headers:\n%s",
            '\n'.join("%s: %s" % (k, v) for k, v in http_response.headers.items()))
        streaming_response = StreamingResponse(session, operation)
        streaming_response.parse(
            http_response.headers,
            StreamingBody(http_response.raw,
                          http_response.headers.get('content-length')))
        if http_response.ok:
            return (http_response, streaming_response.get_value())
        else:
            xml_response = XmlResponse(session, operation)
            body = streaming_response.get_value()['Body'].read()
            # For streaming response, response body might be binary data,
            # so we log response body only when error happens.
            logger.debug("Response Body:\n%s", body)
            if body:
                try:
                    xml_response.parse(body, encoding)
                except xml.etree.cElementTree.ParseError as err:
                    raise xml.etree.cElementTree.ParseError(
                        "Error parsing XML response: %s\nXML received:\n%s" % (err, body))
            return (http_response, xml_response.get_value())
    body = http_response.content
    if not http_response.request.method == 'HEAD':
        _validate_content_length(
            http_response.headers.get('content-length'), len(body))
    logger.debug(
        "Response Headers:\n%s",
        '\n'.join("%s: %s" % (k, v) for k, v in http_response.headers.items()))
    logger.debug("Response Body:\n%s", body)
    if operation.service.type in ('json', 'rest-json'):
        json_response = JSONResponse(session, operation)
        if body:
            json_response.parse(body, encoding)
        json_response.merge_header_values(http_response.headers)
        return (http_response, json_response.get_value())
    # We are defaulting to an XML response handler because many query
    # services send XML error responses but do not include a Content-Type
    # header.
    xml_response = XmlResponse(session, operation)
    if body:
        xml_response.parse(body, encoding)
    xml_response.merge_header_values(http_response.headers)
    return (http_response, xml_response.get_value())
