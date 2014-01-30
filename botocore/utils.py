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


def normalize_url_path(path):
    if not path:
        return '/'
    return remove_dot_segments(path)


def remove_dot_segments(url):
    # RFC 2986, section 5.2.4 "Remove Dot Segments"
    output = []
    while url:
        if url.startswith('../'):
            url = url[3:]
        elif url.startswith('./'):
            url = url[2:]
        elif url.startswith('/./'):
            url = '/' + url[3:]
        elif url.startswith('/../'):
            url = '/' + url[4:]
            if output:
                output.pop()
        elif url.startswith('/..'):
            url = '/' + url[3:]
            if output:
                output.pop()
        elif url.startswith('/.'):
            url = '/' + url[2:]
        elif url == '.' or url == '..':
            url = ''
        elif url.startswith('//'):
            # As far as I can tell, this is not in the RFC,
            # but AWS auth services require consecutive
            # slashes are removed.
            url = url[1:]
        else:
            if url[0] == '/':
                next_slash = url.find('/', 1)
            else:
                next_slash = url.find('/', 0)
            if next_slash == -1:
                output.append(url)
                url = ''
            else:
                output.append(url[:next_slash])
                url = url[next_slash:]
    return ''.join(output)
