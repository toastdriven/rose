import json
import os
import shutil
import unittest
from rose.base import Rose, BaseCommand
from rose.commands import bump_version
from rose.exceptions import VersionError, MissingCommandError, CommandNotFoundError
from rose.runner import RoseRunner


class TestCommand(BaseCommand):
    def run(self, *args, **kwargs):
        self.out('Hello, ')
        self.out('world!')
        self.err('Oops!')
        self.exit_code = 0


class RoseTestCase(unittest.TestCase):
    def setUp(self):
        super(RoseTestCase, self).setUp()
        self.base = os.path.join('/tmp', 'rose_tests/data')
        self.config = os.path.join('/tmp', 'rose_tests/config')

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
        shutil.rmtree(os.path.join('/tmp', 'rose_tests'), ignore_errors=True)
        super(RoseTestCase, self).tearDown()

    def create_rose(self):
        return Rose(base_dir=self.base)

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
        self.assertNotEqual(rose.base_dir, self.base)

    def test_manual_initialization(self):
        rose = self.create_rose()
        self.assertEqual(rose.base_dir, self.base)

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

    def test_runner_parse_args(self):
        runner = RoseRunner()
        self.assertRaises(MissingCommandError, runner.parse_args)
        self.assertEqual(runner.parse_args(cli_args=['hello']), ('hello', [], {}))
        self.assertEqual(runner.parse_args(cli_args=[
            'hello', 'world', '-t', '-n', 'whee', '--verbosity'
        ]), ('hello', ['world'], {'n': 'whee', 't': True, 'verbosity': True}))

    def test_runner_load_command(self):
        runner = RoseRunner()
        self.assertRaises(CommandNotFoundError, runner.load_command, 'not_there')
        self.assertEqual(runner.load_command('bump_version'), bump_version.command_class)

    def test_runner_run_command_help(self):
        runner = RoseRunner()
        help_cmd = runner.load_command('help')
        finished_cmd = runner.run_command(help_cmd)
        self.assertEqual(finished_cmd.exit_code, 1)
        self.assertEqual(finished_cmd.output, [
            (2, 'Usage: rose <command_name> [args] [flags]'),
        ])

    def test_runner_run_command_test(self):
        runner = RoseRunner()
        test_cmd = TestCommand
        finished_cmd = runner.run_command(test_cmd)
        self.assertEqual(finished_cmd.exit_code, 0)
        self.assertEqual(finished_cmd.output, [
            (1, 'Hello, '),
            (1, 'world!'),
            (2, 'Oops!'),
        ])
