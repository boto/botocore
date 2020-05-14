import os
import sys
import tempfile
import shutil
import subprocess
import unittest


class ZipTest(unittest.TestCase):
    def _create_bdist_egg(self, tmp_dir):
        # Iterate to the root of the project
        project_root = os.path.abspath(__file__)
        for i in range(3):
            project_root = os.path.dirname(project_root)
        # Produce a bdist_egg via shell to minimize
        # runtime context pollution
        dist_dir = os.path.join(tmp_dir, 'dist')
        cmd = [
            sys.executable,
            'setup.py',
            'bdist_egg',
            '--dist-dir={}'.format(dist_dir),
            '--bdist-dir={}'.format(os.path.join(tmp_dir, 'bdist')),
        ]
        try:
            proc = subprocess.run(
                cmd,
                check=True,
                cwd=project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            self.fail(exc.stdout)
        pkg_filename = os.listdir(dist_dir)[0]
        return os.path.join(dist_dir, pkg_filename)

    def _create_venv(self, tmp_dir, extra_sys_path=None):
        import venv
        env_dir = os.path.join(tmp_dir, 'venv')
        venv.create(env_dir, system_site_packages=True)
        import jmespath
        import dateutil
        import six
        import urllib3
        mods = [jmespath, dateutil, six, urllib3]
        # Unfortunately venv.EnvBuilder doesn't expose
        # libpath, but this reproduces the behavior from cPython
        if sys.platform == 'win32':
            libpath = os.path.join(env_dir, 'Lib', 'site-packages')
        else:
            libpath = os.path.join(env_dir, 'lib',
                                   'python%d.%d' % sys.version_info[:2],
                                   'site-packages')
        # Symlink these dependencies into the new venv
        for mod in mods:
            link = mod.__spec__.origin
            if os.path.basename(link) == '__init__.py':
                link = os.path.dirname(link)
            os.symlink(
                link,
                os.path.join(libpath, os.path.basename(link)),
            )

        sys_paths = []
        if extra_sys_path is not None:
            sys_paths.append(extra_sys_path)

        sys_paths.append(libpath)

        # The environment implied by `python -S -I`
        # varies significantly so we need to ensure
        # that basic Python packages (like logging)
        # are guaranteed to be in the search path
        # including lib/pythonX.Y and lib/pythonXY.zip
        path_endings = [
            os.path.join('lib', 'python%d.%d' % sys.version_info[:2]),
            os.path.join('lib', 'python%d%d.zip' % sys.version_info[:2]),
        ]
        system_paths = []
        for path in sys.path:
            for path_ending in path_endings:
                if path.endswith(path_ending):
                    sys_paths.append(path)

        # Setup sys.path for the subprocess script.
        script = 'import sys;'
        for sys_path in sys_paths:
            script += 'sys.path.append("{sys_path}");'.format(sys_path=sys_path)
        return script, libpath

    def _run_isolated_python_subprocess_or_fail(self, script):
        cmd = [
            sys.executable,
            '-S',
            '-I',
            '-c',
            script
        ]
        try:
            proc = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            self.fail(exc.stdout)

    @unittest.skipIf(
        sys.version_info.major < 3 or sys.version_info.minor < 7,
        "importlib.resources available starting with Python 3.7")
    def test_loader_load_from_zip(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            egg_path = self._create_bdist_egg(tmp_dir)
            script, libpath = self._create_venv(tmp_dir, extra_sys_path=egg_path)
            script += 'import botocore.loaders;'
            script += 'botocore.loaders.Loader().load_data("endpoints");'
            self._run_isolated_python_subprocess_or_fail(script)

    @unittest.skipIf(
        sys.version_info.major < 3 or sys.version_info.minor < 5,
        "tempfile.TemporaryDirectory and subprocess calls require 3.5")
    def test_loader_load_from_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            egg_path = self._create_bdist_egg(tmp_dir)
            script, libpath = self._create_venv(tmp_dir)
            shutil.unpack_archive(egg_path, libpath, format='zip')
            script += 'import botocore.loaders;'
            script += 'botocore.loaders.Loader().load_data("endpoints");'
            self._run_isolated_python_subprocess_or_fail(script)

    @unittest.skipIf(
        sys.version_info.major < 3 or sys.version_info.minor < 7,
        "importlib.resources available starting with Python 3.7")
    def test_httpsession_cert_load_from_zip(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            egg_path = self._create_bdist_egg(tmp_dir)
            script, libpath = self._create_venv(tmp_dir, extra_sys_path=egg_path)
            script += 'import botocore.httpsession; import botocore.awsrequest;'
            script += 'req = botocore.awsrequest.AWSRequest(method="GET", url="https://www.amazon.com/");'
            script += 'session = botocore.httpsession.URLLib3Session(timeout=10);'
            script += 'session.send(req.prepare());'
            self._run_isolated_python_subprocess_or_fail(script)

    @unittest.skipIf(
        sys.version_info.major < 3 or sys.version_info.minor < 5,
        "tempfile.TemporaryDirectory and subprocess calls require 3.5")
    def test_httpsession_cert_load_from_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            egg_path = self._create_bdist_egg(tmp_dir)
            script, libpath = self._create_venv(tmp_dir)
            shutil.unpack_archive(egg_path, libpath, format='zip')
            script += 'import botocore.httpsession; import botocore.awsrequest;'
            script += 'req = botocore.awsrequest.AWSRequest(method="GET", url="https://www.amazon.com/");'
            script += 'session = botocore.httpsession.URLLib3Session(timeout=10);'
            script += 'session.send(req.prepare());'
            self._run_isolated_python_subprocess_or_fail(script)