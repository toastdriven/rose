from __future__ import unicode_literals

from rose.base import BaseCommand


class ReleasePackage(BaseCommand):
    def help(self, *args, **kwargs):
        return '\n'.join([
            "Usage: rose release",
            "",
            "Pushes the release to PyPI.",
        ])

    def run(self, *args, **kwargs):
        sh = self.shell.run('python setup.py sdist')

        if not self.check_success(sh):
            return False

        sh = self.shell.run('python setup.py sdist upload')
        return self.check_success(sh)


command_class = ReleasePackage
