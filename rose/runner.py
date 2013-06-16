from __future__ import unicode_literals
import importlib

from rose.base import Rose, BaseCommand
from rose.exceptions import MissingCommandError, CommandNotFoundError


class RoseRunner(object):
    def __init__(self, rose=None):
        self.rose = rose

        if not self.rose:
            self.rose = Rose()

    def parse_args(self, cli_args=None):
        if cli_args is None:
            cli_args = []

        try:
            command_name = cli_args.pop(0)
        except IndexError:
            raise MissingCommandError("No command provided.")

        args = []
        kwargs = {}
        i = 0

        while i < len(cli_args):
            if not cli_args[i].startswith('-'):
                # Bare argument.
                args.append(cli_args[i])
            else:
                # Flag, which becomes a kwarg.
                key = cli_args[i].lstrip('-')

                try:
                    if not cli_args[i + 1].startswith('-'):
                        value = cli_args[i + 1]
                        i += 1
                    else:
                        value = True
                except IndexError:
                    value = True

                kwargs[key] = value

            i += 1

        return command_name, args, kwargs

    def load_command(self, command_name):
        # FIXME: Allow this to be extended via a config option.
        possible_paths = [
            # Fallback to the built-in ``rose`` commands.
            'rose.commands',
        ]

        for path in possible_paths:
            try:
                mod_path = '.'.join([path, command_name])
                mod = importlib.import_module(mod_path)

                if not hasattr(mod, 'command_class'):
                    raise CommandNotFoundError("Command '%s' module found, but it lacks a ``command_class``." % command_name)

                return mod.command_class
            except ImportError:
                continue

        raise CommandNotFoundError("Command '%s' can not be found." % command_name)

    def help(self, *args, **kwargs):
        help_command = BaseCommand(self.rose)
        help_command.exit_code = 1

        if not len(args):
            help_command.err("Usage: rose <command_name> [args] [flags]")
        else:
            help_command_name = args[0]
            command_class = self.load_command(help_command_name)
            help_command.err(command_class(self.rose).help())

            if kwargs.get('extra_message'):
                help_command.err('')
                help_command.err(kwargs['extra_message'])

        return help_command

    def run_command(self, command_class, *args, **kwargs):
        cmd = command_class(self.rose)
        cmd.run(*args, **kwargs)
        return cmd

    def run(self, cli_args):
        command_name, args, kwargs = self.parse_args(cli_args)

        if command_name == 'help':
            return self.help(*args, **kwargs)

        command_class = self.load_command(command_name)

        try:
            return self.run_command(command_class, *args, **kwargs)
        except ShowHelpError as err:
            kwargs['extra_message'] = "%s" % err
            return self.help(*args, **kwargs)

    def from_cli(self, cli_args):
        finished_cmd = self.run(cli_args)

        if finished_cmd.has_output():
            finished_cmd.send_output()

        return finished_cmd.exit_code
