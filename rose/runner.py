import importlib
from rose.base import Rose
from rose.exceptions import MissingCommandError, CommandNotFoundError


class RoseRunner(object):
    def __init__(self):
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

        if command_name in ['-h', '--help', 'help']:
            return self.help()

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

    def run_command(self, command_class, *args, **kwargs):
        cmd = command_class(self.rose)
        cmd.run(*args, **kwargs)
        return cmd

    def run(self, cli_args):
        command_name, args, kwargs = self.parse_args(cli_args)
        command_class = self.load_command(command_name)
        finished_cmd = self.run_command(command_class, *args, **kwargs)

        if finished_cmd.has_output():
            finished_cmd.send_output()

        return finished_cmd.exit_code
