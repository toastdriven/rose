from __future__ import unicode_literals
from rose.base import BaseCommand


class Help(BaseCommand):
    def run(self, *args, **kwargs):
        self.err("Usage: rose <command_name> [args] [flags]")
        self.exit_code = 1


command_class = Help
