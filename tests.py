import unittest
from rose import build_version, load_version, VersionError


class VersionTestCase(unittest.TestCase):
    def test_build_version_fails(self):
        self.assertRaises(VersionError, build_version, 'rose', '0')
        self.assertRaises(VersionError, build_version, 'rose', '0.1')
        self.assertRaises(ValueError, build_version, 'rose', 'a.b.c')
        self.assertRaises(VersionError, build_version, 'rose', '0.9.3-beta-gamma')

    def test_build_version_success(self):
        self.assertEqual(build_version('rose', '1.0.0'), (1, 0, 0))
        self.assertEqual(build_version('rose', '1.0.0-beta'), (1, 0, 0, 'beta'))
        self.assertEqual(build_version('rose', '0.9.13-alpha/security'), (0, 9, 13, 'alpha/security'))

    def test_load_version(self):
        # Just make sure it's there.
        self.assertTrue(len(load_version('VERSION')))
