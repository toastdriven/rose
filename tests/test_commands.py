# -*- coding: utf-8 -*-
"""
TODO
----

* Eventually, actual unit tests per-command would be nice. For now, we'll
  do integration tests.

"""
import os
import shutil

import mock
from shell import Shell

from rose.base import Rose
from rose.commands.release import ReleasePackage
from rose.commands.tag import TagVersion

from .utils import BaseRoseTestCase


class FakeShell(Shell):
    def __init__(self, *args, **kwargs):
        super(FakeShell, self).__init__(*args, **kwargs)
        self.cmds = []

    def run(self, cmd):
        self.cmds.append(cmd)
        self.code = 0
        return self


class BaseRoseCommandsTestCase(BaseRoseTestCase):
    # TODO:
    # * Initialize with git
    # * Mock.patch shell to *NOT* run the command
    def setUp(self):
        super(BaseRoseCommandsTestCase, self).setUp()
        self.apps_path = os.path.join(os.path.dirname(__file__), 'apps')
        self.orig_basic_module = os.path.join(self.apps_path, 'basic_module')

        self.temp_apps = os.path.join(self.base, 'apps')
        self.basic_module = os.path.join(self.temp_apps, 'basic_module')
        os.makedirs(self.temp_apps)
        shutil.copytree(self.orig_basic_module, self.basic_module)

    def tearDown(self):
        shutil.rmtree(self.temp_apps)
        super(BaseRoseCommandsTestCase, self).tearDown()

    # Override this to pick up the correct ``base_dir``.
    def create_rose(self):
        return Rose(base_dir=self.basic_module)


class RoseIntegrationTestCase(BaseRoseCommandsTestCase):
    def test_bump(self):
        runner = self.create_runner()
        cmd = runner.run(['bump', '1.0.1-final'])
        self.assertEqual(cmd.exit_code, 0)

        raw_setup = open(os.path.join(self.basic_module, 'setup.py'), 'r').read()
        self.assertTrue("version='1.0.1-final'" in raw_setup)
        raw_conf = open(os.path.join(self.basic_module, 'docs', 'conf.py'), 'r').read()
        self.assertTrue("version = '1.0.1'" in raw_conf)
        self.assertTrue("release = '1.0.1-final'" in raw_conf)
        raw_code = open(os.path.join(self.basic_module, 'basic', '__init__.py'), 'r').read()
        self.assertTrue("__version__ = (1, 0, 1, 'final')" in raw_code)

    def test_tag_git(self):
        tag = TagVersion(rose=self.create_rose())
        faked = FakeShell()

        with mock.patch.object(tag, 'shell', faked) as fake_tag:
            tag.run('v1.0.1')

        self.assertEqual(faked.cmds, ['git tag v1.0.1'])

    def test_tag_git_flow(self):
        tag = TagVersion(rose=self.create_rose())
        faked = FakeShell()

        with mock.patch.object(tag, 'shell', faked) as fake_tag:
            tag.run('v1.0.1', t='git-flow')

        self.assertEqual(faked.cmds, [
            'git checkout -b release-v1.0.1',
            'git co master',
            'git merge release-v1.0.1',
            'git co develop',
            'git merge master',
        ])

    def test_release(self):
        release = ReleasePackage(rose=self.create_rose())
        faked = FakeShell()

        with mock.patch.object(release, 'shell', faked) as fake_tag:
            release.run()

        self.assertEqual(faked.cmds, [
            'python setup.py sdist',
            'python setup.py sdist upload',
        ])

    def test_setup(self):
        runner = self.create_runner()
        pass


# class BumpVersionTestCase(BaseRoseCommandsTestCase):
#     pass
#
#
# class TagTestCase(BaseRoseCommandsTestCase):
#     pass
#
#
# class CreateSetupTestCase(BaseRoseCommandsTestCase):
#     pass
#
#
# class ReleaseTestCase(BaseRoseCommandsTestCase):
#     pass
