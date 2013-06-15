import os
import shutil
import unittest

from rose.base import Rose


class BaseRoseTestCase(unittest.TestCase):
    def setUp(self):
        super(BaseRoseTestCase, self).setUp()
        self.base = os.path.join('/tmp', 'rose_tests')
        self.data = os.path.join(self.base, 'data')
        self.config = os.path.join(self.base, 'config')

        # Nuke in-case the old dirs are still there.
        shutil.rmtree(self.base, ignore_errors=True)
        shutil.rmtree(self.config, ignore_errors=True)
        os.makedirs(self.base)
        os.makedirs(self.config)

        # Stash/set ``os.environ['HOME']`` to simulate loading from the home
        # directory.
        self.old_home = os.environ.get('HOME', '')
        os.environ['HOME'] = self.config

    def tearDown(self):
        # Restore.
        os.environ['HOME'] = self.old_home
        shutil.rmtree(self.base, ignore_errors=True)
        super(BaseRoseTestCase, self).tearDown()

    def create_rose(self):
        return Rose(base_dir=self.data)
