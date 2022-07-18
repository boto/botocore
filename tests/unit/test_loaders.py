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
import sys
import zipfile

import pytest

from botocore.exceptions import DataNotFoundError, UnknownServiceError
from botocore.loaders import (
    BotoZipPath,
    ExtrasProcessor,
    JSONFileLoader,
    Loader,
    create_loader,
)
from tests import BaseEnvVar, mock, requires_zip_support


class TestJSONFileLoader(BaseEnvVar):
    def setUp(self):
        super().setUp()
        self.data_path = pathlib.Path(__file__).parent.joinpath('data')
        self.file_loader = JSONFileLoader()
        self.valid_file_path = self.data_path.joinpath('foo')
        self.compressed_file_path = self.data_path.joinpath('compressed')
        self._set_zip_vars()

    @requires_zip_support()
    def _set_zip_vars(self):
        self.zip_data_path = BotoZipPath(
            self.data_path.joinpath('Archive.zip')
        )
        self.zip_valid_file_path = self.zip_data_path.joinpath('foo')
        self.zip_compressed_file_path = self.zip_data_path.joinpath(
            'compressed'
        )

    def test_load_file(self):
        data = self.file_loader.load_file(self.valid_file_path)
        self.assertEqual(len(data), 3)
        self.assertTrue('test_key_1' in data)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_load_zipped_file(self):

        zip_data = self.file_loader.load_file(self.zip_valid_file_path)
        self.assertEqual(len(zip_data), 3)
        self.assertTrue('test_key_1' in zip_data)

    def test_load_compressed_file(self):
        data = self.file_loader.load_file(self.compressed_file_path)
        self.assertEqual(len(data), 3)
        self.assertTrue('test_key_1' in data)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_load_zipped_compressed_file(self):
        zip_data = self.file_loader.load_file(self.zip_compressed_file_path)
        self.assertEqual(len(zip_data), 3)
        self.assertTrue('test_key_1' in zip_data)

    def test_load_compressed_file_exists_check(self):
        self.assertTrue(self.file_loader.exists(self.compressed_file_path))

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_load_zipped_compressed_file_exists_check(self):
        self.assertTrue(self.file_loader.exists(self.zip_compressed_file_path))

    def test_load_json_file_does_not_exist_returns_none(self):
        # None is used to indicate that the loader could not find a
        # file to load.
        self.assertIsNone(self.file_loader.load_file('fooasdfasdfasdf'))

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_load_zipped_json_file_does_not_exist_returns_none(self):
        # can't instantiate a BotoZipPath object if the path doesn't exist
        self.assertIsNone(
            self.file_loader.load_file(
                self.zip_data_path.joinpath('fooasdfasdfasdf')
            )
        )

    def test_file_exists_check(self):
        self.assertTrue(self.file_loader.exists(self.valid_file_path))

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_zipped_file_exists_check(self):
        self.assertTrue(self.file_loader.exists(self.zip_valid_file_path))

    def test_file_does_not_exist_returns_false(self):
        self.assertFalse(
            self.file_loader.exists(
                self.data_path.joinpath('does', 'not', 'exist')
            )
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_zipped_file_does_not_exist_returns_false(self):
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

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_zipped_file_with_non_ascii(self):
        try:
            filename = self.zip_data_path.joinpath('non_ascii')
            self.assertTrue(self.file_loader.load_file(filename) is not None)
        except UnicodeDecodeError:
            self.fail('Fail to handle data file with non-ascii characters')


@pytest.mark.parametrize(
    "bad_type",
    [None, [1], 1, 1.5, {'bad': 'type'}, b'bad_type', False, {'bad-type'}],
)
def test_cant_add_wrong_type_to_search_path(bad_type):

    with pytest.raises(TypeError):
        Loader(extra_search_paths=[bad_type])

    loader = Loader()
    with pytest.raises(TypeError):
        loader.search_paths.append(bad_type)


@pytest.mark.parametrize(
    "file_name,expected_unicode",
    [
        ("ar_SA", "\u0639\u0628\u062f \u0627\u0644\u0642\u0627\u062f\u0631"),
        ("az_AZ", "\u0130nqilab"),
        ("bg_BG", "\u041c\u0430\u0440\u0442\u0435\u043d"),
        ("bn_BD", "\u0906\u0936\u0932\u0924\u093e"),
        ("cs_CZ", "B\u0159etislav"),
        ("da_DK", "Asbj\u00f8rn"),
        ("de_CH", "K\u00e4ru"),
        ("de_DE", "Sch\u00e4fer"),
        ("el_GR", "\u039d\u03b5\u03ba\u03c4\u03b1\u03c1\u03af\u03b1"),
        ("es", "Mar\u00eda Luisa"),
        ("fa_IR", "\u0645\u062d\u0645\u062f \u0637\u0627\u0647\u0627"),
        ("fr_CA", "J\u00e9r\u00f4me"),
        ("he_IL", "\u05d9\u05e6\u05d7\u05e7"),
        ("hi_IN", "\u0938\u0941\u0932\u092d\u093e"),
        ("hr_HR", "Aljo\u0161a"),
        ("hu_HU", "\u00c1brah\u00e1m"),
        ("hy_AM", "\u054c\u0565\u0562\u0565\u056f\u0561"),
        ("ja_JP", "\u62d3\u771f"),
        ("ka_GE", "\u10d4\u10d5\u10d2\u10d4\u10dc\u10d8\u10d0"),
        ("ko_KR", "\ubcf4\ub78c"),
        ("ne_NP", "\u0927\u093f\u0930\u091c"),
        ("no_NO", "J\u00f8rgen"),
        ("or_IN", "\u0b36\u0b4d\u0b30\u0b40\u0b2e\u0b24\u0b40"),
        ("pt_PT", "\u00c2ngelo"),
        ("ru_RU", "\u041a\u043e\u043d\u0434\u0440\u0430\u0442\u0438\u0439"),
        ("sk_SK", "Tom\u00e1\u0161"),
        ("sl_SI", "Andra\u017e"),
        ("sv_SE", "\u00c5sa"),
        (
            "ta_IN",
            "\u0baa\u0bbe\u0b95\u0bcd\u0b95\u0bbf\u0baf\u0bb2\u0b95\u0bcd\u0bb7\u0bcd\u0bae\u0bbf",
        ),
        ("th_TH", "\u0e2a\u0e23\u0e32\u0e0d\u0e08\u0e34\u0e15\u0e15\u0e4c"),
        ("th", "\u0e44\u0e0a\u0e22\u0e20\u0e1e"),
        ("tr_TR", "\u00d6mar"),
        ("uk_UA", "\u041b\u0435\u043e\u043d\u0442\u0456\u0439"),
        ("vi_VN", "Tr\u00a3uc"),
        ("zh_CN", "\u5f3a"),
        ("zh_TW", "\u96c5\u60e0"),
    ],
)
def test_load_different_locales(file_name, expected_unicode):
    base_path = pathlib.Path(__file__).parent.joinpath('data', 'locales')
    file_loader = JSONFileLoader()
    data = file_loader.load_file(base_path.joinpath(file_name))
    encoded = data['name'].encode('utf-8')
    # it appears that pytest decodes unicode implicitly
    expected_encoded = expected_unicode.encode('utf-8')
    assert encoded == expected_encoded


class TestLoader(BaseEnvVar):
    def setUp(self):
        super().setUp()
        self.zip_path = os.path.join(
            os.path.dirname(__file__), 'data', 'Archive.zip'
        )
        self.zip_search_path = os.path.join(self.zip_path, 'foo')

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

    def test_can_add_to_search_path(self):
        loader = Loader()
        loader.search_paths.append('mypath')
        self.assertIn(pathlib.Path('mypath').resolve(), loader.search_paths)

    def test_can_initialize_with_search_paths(self):
        loader = Loader(extra_search_paths=['foo', 'bar'])
        # Note that the extra search paths are before
        # the customer/builtin data paths.

        self.assertEqual(
            loader.search_paths,
            [
                pathlib.Path('foo').resolve(),
                pathlib.Path('bar').resolve(),
                loader.CUSTOMER_DATA_PATH,
                loader.BUILTIN_DATA_PATH,
            ],
        )

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
        self.assertIn(pathlib.Path('foo').resolve(), loader.search_paths)
        self.assertIn(pathlib.Path('bar').resolve(), loader.search_paths)
        self.assertIn(pathlib.Path('baz').resolve(), loader.search_paths)

    @pytest.mark.skipif(
        sys.version_info >= (3, 9), reason="Python version >= 3.9"
    )
    def test_zips_not_suppored_python_lt_39(self):
        if not hasattr(zipfile, 'Path'):
            with self.assertRaises(RuntimeError):
                BotoZipPath(self.zip_path)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_zip_path_created(self):
        loader = create_loader(self.zip_search_path)
        zip_path = BotoZipPath(self.zip_path).joinpath('foo')
        # two identical BotoZipPath objects do not 'equal' each other
        matching_zips = [
            path for path in loader.search_paths if str(path) == str(zip_path)
        ]
        self.assertEqual(len(matching_zips), 1)
        self.assertIsInstance(matching_zips[0], BotoZipPath)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_zipped_load_data(self):
        loader = Loader(
            extra_search_paths=[self.zip_path],
            include_default_search_paths=False,
        )
        data = loader.load_data('foo')
        self.assertEqual(len(data), 3)
        self.assertTrue('test_key_1' in data)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_zipped_data_not_found_raises_exception(self):
        loader = Loader(
            extra_search_paths=[self.zip_path],
            include_default_search_paths=False,
        )
        with self.assertRaises(DataNotFoundError):
            loader.load_data('cheese')

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_zipped_model_not_found_raises_exception(self):
        loader = Loader(
            extra_search_paths=[self.zip_path],
            include_default_search_paths=False,
        )
        with self.assertRaises(DataNotFoundError):
            loader.load_service_model('bestServiceEver', 'service-2')

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_load_zipped_service_model(self):
        loader = Loader(
            extra_search_paths=[self.zip_search_path],
            include_default_search_paths=False,
        )
        model = loader.load_service_model('myCoolService', 'service-2')
        self.assertIn("foo", model)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_zipped_list_available_services(self):
        loader = Loader(
            extra_search_paths=[self.zip_search_path],
            include_default_search_paths=False,
        )
        available_services = loader.list_available_services('service-2')
        self.assertEqual(
            available_services, ['dynamodb', 'ec2', 'myCoolService']
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="Python version < 3.9"
    )
    def test_zipped_list_api_versions(self):
        loader = Loader(
            extra_search_paths=[self.zip_search_path],
            include_default_search_paths=False,
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
        base_path = pathlib.Path(
            'datapath', 'myservice', '2015-03-01'
        ).resolve()
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
        base_path = pathlib.Path(
            'datapath', 'myservice', '2015-03-01'
        ).resolve()
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
