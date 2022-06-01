# Copyright (c) 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import contextlib
import copy
import os
import pathlib
import zipfile

from botocore.exceptions import DataNotFoundError, UnknownServiceError
from botocore.loaders import (
    ExtrasProcessor,
    JSONFileLoader,
    Loader,
    SearchPathList,
    create_loader,
)
from tests import BaseEnvVar, mock


class TestJSONFileLoader(BaseEnvVar):
    def setUp(self):
        super().setUp()
        self.data_path = pathlib.Path(__file__).parent.joinpath('data')
        self.zip_data_path = zipfile.Path(
            self.data_path.joinpath('Archive.zip')
        )
        self.file_loader = JSONFileLoader()
        self.valid_file_path = self.data_path.joinpath('foo')
        self.zip_valid_file_path = self.zip_data_path.joinpath('foo')
        self.compressed_file_path = self.data_path.joinpath('compressed')
        self.zip_compressed_file_path = self.zip_data_path.joinpath(
            'compressed'
        )

    def test_load_file(self):
        data = self.file_loader.load_file(self.valid_file_path)
        self.assertEqual(len(data), 3)
        self.assertTrue('test_key_1' in data)

        zip_data = self.file_loader.load_file(self.zip_valid_file_path)
        self.assertEqual(len(zip_data), 3)
        self.assertTrue('test_key_1' in zip_data)

        self.assertEqual(data, zip_data)

    def test_load_compressed_file(self):
        data = self.file_loader.load_file(self.compressed_file_path)
        self.assertEqual(len(data), 3)
        self.assertTrue('test_key_1' in data)

        zip_data = self.file_loader.load_file(self.zip_compressed_file_path)
        self.assertEqual(len(zip_data), 3)
        self.assertTrue('test_key_1' in data)

        self.assertEqual(data, zip_data)

    def test_load_compressed_file_exists_check(self):
        self.assertTrue(self.file_loader.exists(self.compressed_file_path))
        self.assertTrue(self.file_loader.exists(self.zip_compressed_file_path))

    def test_load_json_file_does_not_exist_returns_none(self):
        # None is used to indicate that the loader could not find a
        # file to load.
        self.assertIsNone(
            self.file_loader.load_file(pathlib.Path('fooasdfasdfasdf'))
        )
        # can't instantiate a zipfile.Path object if the path doesn't exist
        self.assertIsNone(
            self.file_loader.load_file(
                self.zip_data_path.joinpath('fooasdfasdfasdf')
            )
        )

    def test_file_exists_check(self):
        self.assertTrue(self.file_loader.exists(self.valid_file_path))
        self.assertTrue(self.file_loader.exists(self.zip_valid_file_path))

    def test_file_does_not_exist_returns_false(self):
        self.assertFalse(
            self.file_loader.exists(
                self.data_path.joinpath('does', 'not', 'exist')
            )
        )
        self.assertFalse(
            self.file_loader.exists(
                self.zip_data_path.joinpath('does', 'not', 'exist')
            )
        )

    def test_file_with_non_ascii(self):
        try:
            filename = self.data_path.joinpath('non_ascii')
            self.assertTrue(self.file_loader.load_file(filename) is not None)
        except UnicodeDecodeError:
            self.fail('Fail to handle data file with non-ascii characters')

        try:
            filename = self.zip_data_path.joinpath('non_ascii')
            self.assertTrue(self.file_loader.load_file(filename) is not None)
        except UnicodeDecodeError:
            self.fail('Fail to handle data file with non-ascii characters')


class TestLoader(BaseEnvVar):
    def test_default_search_paths(self):
        loader = Loader()
        self.assertEqual(len(loader.search_paths), 2)
        # We should also have ~/.aws/models added to
        # the search path.  To deal with cross platform
        # issues we'll just check for a path that ends
        # with .aws/models.
        home_dir_path = os.path.join('.aws', 'models')
        self.assertTrue(
            any(str(p).endswith(home_dir_path) for p in loader.search_paths)
        )
        self.assertIsInstance(loader.search_paths, SearchPathList)

    def test_can_add_to_search_path(self):
        loader = Loader()
        loader.search_paths.append('mypath')
        self.assertIn(pathlib.Path('mypath'), loader.search_paths)
        self.assertIsInstance(loader.search_paths, SearchPathList)

    def test_can_initialize_with_search_paths(self):
        loader = Loader(extra_search_paths=['foo', 'bar'])
        # Note that the extra search paths are before
        # the customer/builtin data paths.

        self.assertIsInstance(loader.search_paths, SearchPathList)
        self.assertEqual(
            loader.search_paths,
            [
                pathlib.Path('foo'),
                pathlib.Path('bar'),
                loader.CUSTOMER_DATA_PATH,
                loader.BUILTIN_DATA_PATH,
            ],
        )

    def test_cant_add_wrong_type_to_search_path(self):

        bad_types = (
            None,
            [1],
            1,
            1.5,
            {'bad': 'type'},
            b'bad_type',
            False,
            {'bad_type'},
        )
        for _type in bad_types:
            with self.assertRaises(TypeError):
                Loader(extra_search_paths=[_type])

            loader = Loader()
            with self.assertRaises(TypeError):
                loader.search_paths.append(_type)

    # The file loader isn't consulted unless the current
    # search path exists, so we're patching isdir to always
    # say that a directory exists.
    @mock.patch('pathlib.Path.is_dir', mock.Mock(return_value=True))
    def test_load_data_uses_loader(self):
        search_paths = ['foo', 'bar', 'baz']

        class FakeLoader:
            def load_file(self, name):
                expected_ending = os.path.join('bar', 'baz')
                if str(name).endswith(expected_ending):
                    return ['loaded data']

        loader = Loader(
            extra_search_paths=search_paths, file_loader=FakeLoader()
        )
        loaded = loader.load_data('baz')
        self.assertEqual(loaded, ['loaded data'])

    def test_data_not_found_raises_exception(self):
        class FakeLoader:
            def load_file(self, name):
                # Returning None indicates that the
                # loader couldn't find anything.
                return None

        loader = Loader(file_loader=FakeLoader())
        with self.assertRaises(DataNotFoundError):
            loader.load_data('baz')

    @mock.patch('pathlib.Path.is_dir', mock.Mock(return_value=True))
    def test_error_raised_if_service_does_not_exist(self):
        loader = Loader(
            extra_search_paths=[], include_default_search_paths=False
        )
        with self.assertRaises(DataNotFoundError):
            loader.determine_latest_version('unknownservice', 'service-2')

    @mock.patch('pathlib.Path.is_dir', mock.Mock(return_value=True))
    def test_load_service_model(self):
        class FakeLoader:
            def load_file(self, name):
                return ['loaded data']

        loader = Loader(
            extra_search_paths=['foo'],
            file_loader=FakeLoader(),
            include_default_search_paths=False,
            include_default_extras=False,
        )
        loader.determine_latest_version = mock.Mock(return_value='2015-03-01')
        loader.list_available_services = mock.Mock(return_value=['baz'])
        loaded = loader.load_service_model('baz', type_name='service-2')
        self.assertEqual(loaded, ['loaded data'])

    @mock.patch('pathlib.Path.is_dir', mock.Mock(return_value=True))
    def test_load_service_model_enforces_case(self):
        class FakeLoader:
            def load_file(self, name):
                return ['loaded data']

        loader = Loader(
            extra_search_paths=['foo'],
            file_loader=FakeLoader(),
            include_default_search_paths=False,
        )
        loader.determine_latest_version = mock.Mock(return_value='2015-03-01')
        loader.list_available_services = mock.Mock(return_value=['baz'])

        # Should have a) the unknown service name and b) list of valid
        # service names.
        with self.assertRaisesRegex(
            UnknownServiceError, 'Unknown service.*BAZ.*baz'
        ):
            loader.load_service_model('BAZ', type_name='service-2')

    def test_load_service_model_uses_provided_type_name(self):
        loader = Loader(
            extra_search_paths=['foo'],
            file_loader=mock.Mock(),
            include_default_search_paths=False,
        )
        loader.list_available_services = mock.Mock(return_value=['baz'])

        # Should have a) the unknown service name and b) list of valid
        # service names.
        provided_type_name = 'not-service-2'
        with self.assertRaisesRegex(
            UnknownServiceError, 'Unknown service.*BAZ.*baz'
        ):
            loader.load_service_model('BAZ', type_name=provided_type_name)

        loader.list_available_services.assert_called_with(provided_type_name)

    def test_create_loader_parses_data_path(self):
        search_path = os.pathsep.join(['foo', 'bar', 'baz'])
        loader = create_loader(search_path)
        self.assertIn(pathlib.Path('foo'), loader.search_paths)
        self.assertIn(pathlib.Path('bar'), loader.search_paths)
        self.assertIn(pathlib.Path('baz'), loader.search_paths)

    def test_zip_path_created(self):
        search_path = os.path.join(
            os.path.dirname(__file__), 'data', 'Archive.zip', 'foo'
        )
        loader = create_loader(search_path)
        self.assertIn(
            search_path + os.sep, [str(path) for path in loader.search_paths]
        )
        zip_path = zipfile.Path(os.path.dirname(search_path)).joinpath('foo')
        # two identical zipfile.Path objects do not 'equal' each other
        self.assertIn(
            str(zip_path), (str(path) for path in loader.search_paths)
        )
        # sanity check that one of the paths is a zipfile.Path
        # since it can't be checked directly
        self.assertTrue(
            any(isinstance(path, zipfile.Path) for path in loader.search_paths)
        )

    def test_zipped_load_data(self):
        path = os.path.join(os.path.dirname(__file__), 'data', 'Archive.zip')
        loader = Loader(
            extra_search_paths=[path], include_default_search_paths=False
        )
        data = loader.load_data('foo')
        self.assertEqual(len(data), 3)
        self.assertTrue('test_key_1' in data)

    def test_zipped_data_not_found_raises_exception(self):
        path = os.path.join(os.path.dirname(__file__), 'data', 'Archive.zip')
        loader = Loader(
            extra_search_paths=[path], include_default_search_paths=False
        )
        with self.assertRaises(DataNotFoundError):
            loader.load_data('cheese')

    def test_zipped_model_not_found_raises_exception(self):
        path = os.path.join(os.path.dirname(__file__), 'data', 'Archive.zip')
        loader = Loader(
            extra_search_paths=[path], include_default_search_paths=False
        )
        with self.assertRaises(DataNotFoundError):
            loader.load_service_model('bestServiceEver', 'service-2')

    def test_load_zipped_service_model(self):
        path = os.path.join(
            os.path.dirname(__file__), 'data', 'Archive.zip', 'foo'
        )
        loader = Loader(
            extra_search_paths=[path], include_default_search_paths=False
        )
        model = loader.load_service_model('myCoolService', 'service-2')
        self.assertIn("foo", model)

    def test_zipped_list_available_services(self):
        path = os.path.join(
            os.path.dirname(__file__), 'data', 'Archive.zip', 'foo'
        )
        loader = Loader(
            extra_search_paths=[path], include_default_search_paths=False
        )
        available_services = loader.list_available_services('service-2')
        self.assertEqual(
            available_services, ['dynamodb', 'ec2', 'myCoolService']
        )

    def test_zipped_list_api_versions(self):
        path = os.path.join(
            os.path.dirname(__file__), 'data', 'Archive.zip', 'foo'
        )
        loader = Loader(
            extra_search_paths=[path], include_default_search_paths=False
        )
        api_versions = loader.list_api_versions('ec2', 'service-2')
        self.assertEqual(api_versions, ['2010-01-01', '2014-10-01'])


class TestMergeExtras(BaseEnvVar):
    def setUp(self):
        super().setUp()
        self.file_loader = mock.Mock()
        self.data_loader = Loader(
            extra_search_paths=['datapath'],
            file_loader=self.file_loader,
            include_default_search_paths=False,
        )
        self.data_loader.determine_latest_version = mock.Mock(
            return_value='2015-03-01'
        )
        self.data_loader.list_available_services = mock.Mock(
            return_value=['myservice']
        )

        isdir_mock = mock.Mock(return_value=True)
        self.isdir_patch = mock.patch('pathlib.Path.is_dir', isdir_mock)
        self.isdir_patch.start()

    def tearDown(self):
        super().tearDown()
        self.isdir_patch.stop()

    def test_merge_extras(self):
        service_data = {'foo': 'service', 'bar': 'service'}
        sdk_extras = {'merge': {'foo': 'sdk'}}
        self.file_loader.load_file.side_effect = [service_data, sdk_extras]

        loaded = self.data_loader.load_service_model('myservice', 'service-2')
        expected = {'foo': 'sdk', 'bar': 'service'}
        self.assertEqual(loaded, expected)

        call_args = self.file_loader.load_file.call_args_list
        call_args = [c[0][0] for c in call_args]
        base_path = pathlib.Path('datapath', 'myservice', '2015-03-01')
        expected_call_args = [
            base_path.joinpath('service-2'),
            base_path.joinpath('service-2.sdk-extras'),
        ]
        self.assertEqual(call_args, expected_call_args)

    def test_extras_not_found(self):
        service_data = {'foo': 'service', 'bar': 'service'}
        service_data_copy = copy.copy(service_data)
        self.file_loader.load_file.side_effect = [service_data, None]

        loaded = self.data_loader.load_service_model('myservice', 'service-2')
        self.assertEqual(loaded, service_data_copy)

    def test_no_merge_in_extras(self):
        service_data = {'foo': 'service', 'bar': 'service'}
        service_data_copy = copy.copy(service_data)
        self.file_loader.load_file.side_effect = [service_data, {}]

        loaded = self.data_loader.load_service_model('myservice', 'service-2')
        self.assertEqual(loaded, service_data_copy)

    def test_include_default_extras(self):
        self.data_loader = Loader(
            extra_search_paths=['datapath'],
            file_loader=self.file_loader,
            include_default_search_paths=False,
            include_default_extras=False,
        )
        self.data_loader.determine_latest_version = mock.Mock(
            return_value='2015-03-01'
        )
        self.data_loader.list_available_services = mock.Mock(
            return_value=['myservice']
        )

        service_data = {'foo': 'service', 'bar': 'service'}
        service_data_copy = copy.copy(service_data)
        sdk_extras = {'merge': {'foo': 'sdk'}}
        self.file_loader.load_file.side_effect = [service_data, sdk_extras]

        loaded = self.data_loader.load_service_model('myservice', 'service-2')
        self.assertEqual(loaded, service_data_copy)

    def test_append_extra_type(self):
        service_data = {'foo': 'service', 'bar': 'service'}
        sdk_extras = {'merge': {'foo': 'sdk'}}
        cli_extras = {'merge': {'cli': True}}
        self.file_loader.load_file.side_effect = [
            service_data,
            sdk_extras,
            cli_extras,
        ]

        self.data_loader.extras_types.append('cli')

        loaded = self.data_loader.load_service_model('myservice', 'service-2')
        expected = {'foo': 'sdk', 'bar': 'service', 'cli': True}
        self.assertEqual(loaded, expected)

        call_args = self.file_loader.load_file.call_args_list
        call_args = [c[0][0] for c in call_args]
        base_path = pathlib.Path('datapath', 'myservice', '2015-03-01')
        expected_call_args = [
            base_path.joinpath('service-2'),
            base_path.joinpath('service-2.sdk-extras'),
            base_path.joinpath('service-2.cli-extras'),
        ]
        self.assertEqual(call_args, expected_call_args)

    def test_sdk_empty_extras_skipped(self):
        service_data = {'foo': 'service', 'bar': 'service'}
        cli_extras = {'merge': {'foo': 'cli'}}
        self.file_loader.load_file.side_effect = [
            service_data,
            None,
            cli_extras,
        ]

        self.data_loader.extras_types.append('cli')
        loaded = self.data_loader.load_service_model('myservice', 'service-2')
        expected = {'foo': 'cli', 'bar': 'service'}
        self.assertEqual(loaded, expected)


class TestExtrasProcessor(BaseEnvVar):
    def setUp(self):
        super().setUp()
        self.processor = ExtrasProcessor()
        self.service_data = {
            'shapes': {
                'StringShape': {'type': 'string'},
            }
        }
        self.service_data_copy = copy.deepcopy(self.service_data)

    def test_process_empty_list(self):
        self.processor.process(self.service_data, [])
        self.assertEqual(self.service_data, self.service_data_copy)

    def test_process_empty_extras(self):
        self.processor.process(self.service_data, [{}])
        self.assertEqual(self.service_data, self.service_data_copy)

    def test_process_merge_key(self):
        extras = {'merge': {'shapes': {'BooleanShape': {'type': 'boolean'}}}}
        self.processor.process(self.service_data, [extras])
        self.assertNotEqual(self.service_data, self.service_data_copy)

        boolean_shape = self.service_data['shapes'].get('BooleanShape')
        self.assertEqual(boolean_shape, {'type': 'boolean'})

    def test_process_in_order(self):
        extras = [
            {'merge': {'shapes': {'BooleanShape': {'type': 'boolean'}}}},
            {'merge': {'shapes': {'BooleanShape': {'type': 'string'}}}},
        ]
        self.processor.process(self.service_data, extras)
        self.assertNotEqual(self.service_data, self.service_data_copy)

        boolean_shape = self.service_data['shapes'].get('BooleanShape')
        self.assertEqual(boolean_shape, {'type': 'string'})


class TestLoadersWithDirectorySearching(BaseEnvVar):
    def setUp(self):
        super().setUp()
        self.fake_directories = {}

    def tearDown(self):
        super().tearDown()

    @contextlib.contextmanager
    def loader_with_fake_dirs(self):
        _parent = os.path.dirname(__file__)
        search_paths = [
            os.path.join(_parent, 'data', 'foo'),
            os.path.join(_parent, 'data', 'bar'),
        ]
        loader = Loader(
            extra_search_paths=search_paths,
            include_default_search_paths=False,
        )
        yield loader

    def test_list_available_services(self):

        with self.loader_with_fake_dirs() as loader:
            self.assertEqual(
                loader.list_available_services(type_name='service-2'),
                ['dynamodb', 'ec2', 'myCoolService'],
            )
            self.assertEqual(
                loader.list_available_services(type_name='resource-1'), ['rds']
            )

    def test_determine_latest(self):

        with self.loader_with_fake_dirs() as loader:
            self.assertEqual(
                loader.determine_latest_version('ec2', 'service-2'),
                '2014-10-01',
            )
            self.assertEqual(
                loader.determine_latest_version('ec2', 'service-1'),
                '2015-03-01',
            )
