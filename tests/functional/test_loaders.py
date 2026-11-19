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
import json
import os
import shutil
import tempfile

from botocore import loaders
from botocore.exceptions import DataNotFoundError, UnknownServiceError
from tests import mock, temporary_file, unittest


class TestLoaderAllowsDataPathOverride(unittest.TestCase):
    def create_file(self, f, contents, name):
        f.write(contents)
        f.flush()
        dirname = os.path.dirname(os.path.abspath(f.name))
        override_name = os.path.join(dirname, name)
        shutil.copy(f.name, override_name)
        return override_name

    def test_can_override_session(self):
        with temporary_file('w') as f:
            # We're going to override _retry.json in
            # botocore/data by setting our own data directory.
            override_name = self.create_file(
                f, contents='{"foo": "bar"}', name='_retry.json'
            )
            new_data_path = os.path.dirname(override_name)
            loader = loaders.create_loader(search_path_string=new_data_path)

            new_content = loader.load_data('_retry')
            # This should contain the content we just created.
            self.assertEqual(new_content, {"foo": "bar"})


class TestLoadServiceModelDoesNotListServices(unittest.TestCase):
    def setUp(self):
        self.data_path = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.data_path)
        for service, api_version in [
            ('myservice', '2015-01-01'),
            ('myservice', '2016-01-01'),
            ('otherservice', '2015-01-01'),
        ]:
            api_dir = os.path.join(self.data_path, service, api_version)
            os.makedirs(api_dir)
            with open(os.path.join(api_dir, 'service-2.json'), 'w') as f:
                json.dump({'version': api_version}, f)
        self.loader = loaders.Loader(
            extra_search_paths=[self.data_path],
            include_default_search_paths=False,
        )

    def test_load_service_model_does_not_list_available_services(self):
        with mock.patch.object(
            self.loader,
            'list_available_services',
            wraps=self.loader.list_available_services,
        ) as list_services:
            latest = self.loader.load_service_model('myservice', 'service-2')
            explicit = self.loader.load_service_model(
                'myservice', 'service-2', api_version='2015-01-01'
            )
        self.assertEqual(latest, {'version': '2016-01-01'})
        self.assertEqual(explicit, {'version': '2015-01-01'})
        list_services.assert_not_called()

    def test_unknown_service_name_variants_are_rejected(self):
        for service_name in [
            'MYSERVICE',
            'myservice/',
            'myservice/2015-01-01',
            'otherservice/../myservice',
            os.path.join(self.data_path, 'myservice'),
            '.',
            '',
        ]:
            for api_version in [None, '2015-01-01']:
                with self.subTest(
                    service_name=service_name, api_version=api_version
                ):
                    with self.assertRaises(UnknownServiceError) as cm:
                        self.loader.load_service_model(
                            service_name, 'service-2', api_version
                        )
                    self.assertEqual(
                        cm.exception.kwargs['known_service_names'],
                        'myservice, otherservice',
                    )

    def test_unknown_type_name_raises_unknown_service_error(self):
        with self.assertRaises(UnknownServiceError) as cm:
            self.loader.load_service_model('myservice', 'waiters-2')
        self.assertEqual(cm.exception.kwargs['service_name'], 'myservice')
        self.assertEqual(cm.exception.kwargs['known_service_names'], '')

    def test_unavailable_api_version_raises_data_not_found_error(self):
        with self.assertRaises(DataNotFoundError) as cm:
            self.loader.load_service_model(
                'myservice', 'service-2', api_version='2099-01-01'
            )
        self.assertIs(type(cm.exception), DataNotFoundError)
        self.assertEqual(
            cm.exception.kwargs['data_path'],
            os.path.join('myservice', '2099-01-01', 'service-2'),
        )

    def test_unreadable_search_path_is_skipped(self):
        unreadable_path = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, unreadable_path)
        real_listdir = os.listdir

        def listdir(path):
            if path == unreadable_path:
                raise PermissionError(path)
            return real_listdir(path)

        loader = loaders.Loader(
            extra_search_paths=[unreadable_path, self.data_path],
            include_default_search_paths=False,
        )
        with mock.patch('os.listdir', side_effect=listdir):
            model = loader.load_service_model('myservice', 'service-2')
        self.assertEqual(model, {'version': '2016-01-01'})
