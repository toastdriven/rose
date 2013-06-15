# -*- coding: utf-8 -*-
import json
import os
from rose.base import Rose
from rose.exceptions import VersionError

from .utils import BaseRoseTestCase


class RoseTestCase(BaseRoseTestCase):
    def test_parse_version_fails(self):
        rose = self.create_rose()
        self.assertRaises(VersionError, rose.parse_version, '0')
        self.assertRaises(VersionError, rose.parse_version, '0.1')
        self.assertRaises(ValueError, rose.parse_version, 'a.b.c')
        self.assertRaises(VersionError, rose.parse_version, '0.9.3-beta-gamma')

    def test_parse_version(self):
        rose = self.create_rose()
        self.assertEqual(rose.parse_version('1.0.0'), (1, 0, 0))
        self.assertEqual(rose.parse_version('1.0.0-beta'), (1, 0, 0, 'beta'))
        self.assertEqual(rose.parse_version('0.9.13-alpha/security'), (0, 9, 13, 'alpha/security'))

    def test_build_short_version(self):
        rose = self.create_rose()
        self.assertEqual(rose.build_short_version((1,)), '1')
        self.assertEqual(rose.build_short_version((1, 0)), '1.0')
        self.assertEqual(rose.build_short_version((1, 0, 2)), '1.0.2')
        self.assertEqual(rose.build_short_version((2, 3, 4, 'beta')), '2.3.4')
        self.assertEqual(rose.build_short_version((2, 3, 4, 'rc', 2)), '2.3.4')

    def test_build_full_version(self):
        rose = self.create_rose()
        self.assertEqual(rose.build_full_version((1,)), '1')
        self.assertEqual(rose.build_full_version((1, 0)), '1.0')
        self.assertEqual(rose.build_full_version((1, 0, 2)), '1.0.2')
        self.assertEqual(rose.build_full_version((2, 3, 4, 'beta')), '2.3.4-beta')
        self.assertEqual(rose.build_full_version((2, 3, 4, 'rc', 2)), '2.3.4-rc-2')

    def test_auto_initialization(self):
        # The only thing to test is that the base dir gets set automatically.
        rose = Rose()
        self.assertTrue(len(rose.base_dir) > 0)
        self.assertNotEqual(rose.base_dir, self.data)

    def test_manual_initialization(self):
        rose = self.create_rose()
        self.assertEqual(rose.base_dir, self.data)

    def test_get_set_config(self):
        rose = self.create_rose()
        self.assertTrue('search_for' in rose.config)
        self.assertEqual(rose.get_config('search_for'), [
            '^__version__ = ',
            'version\\s?=\\s?',
        ])
        self.assertEqual(rose.get_config('does_not_exist'), None)

        rose.set_config('does_not_exist', 'does now')
        self.assertEqual(rose.get_config('does_not_exist'), 'does now')

    def test_save_config_file(self):
        config_path = os.path.join(self.config, '.rose')
        rose = self.create_rose()
        rose.set_config('want_a_pony', True)

        rose.save_config_file(config_path)
        self.assertTrue(os.path.exists(config_path))

        with open(config_path, 'r') as config:
            data = json.load(config)

        self.assertTrue('want_a_pony' in data)

    def test_load_config_file(self):
        config_path = os.path.join(self.config, '.rose')

        with open(config_path, 'w') as config:
            json.dump({
                'test_config': 'whee!',
            }, config)

        rose = self.create_rose()
        self.assertTrue('test_config' in rose.load_config_file(config_path))
