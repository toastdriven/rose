# -*- coding: utf-8 -*-
from rose.commands import bump_version
from rose.exceptions import MissingCommandError, CommandNotFoundError

from .mock_commands import TestCommand
from .utils import BaseRoseTestCase


class RoseRunnerTestCase(BaseRoseTestCase):
    def test_runner_parse_args(self):
        runner = self.create_runner()
        self.assertRaises(MissingCommandError, runner.parse_args)
        self.assertEqual(runner.parse_args(cli_args=['hello']), ('hello', [], {}))
        self.assertEqual(runner.parse_args(cli_args=[
            'hello', 'world', '-t', '-n', 'whee', '--verbosity'
        ]), ('hello', ['world'], {'n': 'whee', 't': True, 'verbosity': True}))

    def test_runner_load_command(self):
        runner = self.create_runner()
        self.assertRaises(CommandNotFoundError, runner.load_command, 'not_there')
        self.assertEqual(runner.load_command('bump_version'), bump_version.command_class)

    def test_runner_run_command_help(self):
        runner = self.create_runner()
        help_cmd = runner.load_command('help')
        finished_cmd = runner.run_command(help_cmd)
        self.assertEqual(finished_cmd.exit_code, 1)
        self.assertEqual(finished_cmd.output, [
            (2, 'Usage: rose <command_name> [args] [flags]'),
        ])

    def test_runner_run_command_test(self):
        runner = self.create_runner()
        test_cmd = TestCommand
        finished_cmd = runner.run_command(test_cmd)
        self.assertEqual(finished_cmd.exit_code, 0)
        self.assertEqual(finished_cmd.output, [
            (1, 'Hello, '),
            (1, 'world!'),
            (2, 'Oops!'),
        ])
