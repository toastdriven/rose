from __future__ import unicode_literals
import glob
import os
import re

from rose.base import BaseCommand


class BumpVersion(BaseCommand):
    def help(self, *args, **kwargs):
        return '\n'.join([
            "Usage: rose bump <major>.<minor>.<patch>[-prerelease]",
            "",
            "Increments the version in the `setup.py`, the Sphinx `conf.py` & package itself.",
            "It will skip any of those files if they can not be found."
        ])

    def read_lines(self, path):
        if not os.path.exists(path):
            return []

        with open(path, 'r') as raw_file:
            return raw_file.readlines()

    def write_lines(self, path, lines):
        with open(path, 'w') as raw_file:
            for line in lines:
                raw_file.write(line)

    def substitute_setup(self, lines, version_tuple):
        full_version = self.rose.build_full_version(version_tuple)

        for offset, line in enumerate(lines[:]):
            if 'version' in line:
                lines[offset] = re.sub(r'(version\s*?=\s*?).*?,', r"\1'%s'," % full_version, line)

        return lines

    def substitute_sphinx(self, lines, version_tuple):
        short_version = self.rose.build_short_version(version_tuple)
        full_version = self.rose.build_full_version(version_tuple)

        for offset, line in enumerate(lines[:]):
            if line.startswith('version'):
                lines[offset] = "version = '%s'\n" % short_version

            if line.startswith('release'):
                lines[offset] = "release = '%s'\n" % full_version

        return lines

    def substitute_code(self, lines, version_tuple):
        for offset, line in enumerate(lines[:]):
            if line.startswith('__version__'):
                lines[offset] = '__version__ = %s\n' % (version_tuple,)

        return lines

    def replace_version_setup(self, version_tuple):
        setup_path = os.path.join(self.rose.base_dir, 'setup.py')
        lines = self.read_lines(setup_path)

        if not lines:
            self.out("Couldn't find a 'setup.py' at the expected location.")
            return False

        lines = self.substitute_setup(lines, version_tuple)
        self.write_lines(setup_path, lines)
        return True

    def replace_version_sphinx(self, version_tuple):
        sphinx_path = self.rose.get_config('sphinx_path')
        conf_path = os.path.join(self.rose.base_dir, sphinx_path)
        lines = self.read_lines(conf_path)

        if not lines:
            self.out("Couldn't find a Sphinx config at the expected '%s' path." % conf_path)
            return False

        lines = self.substitute_sphinx(lines, version_tuple)
        self.write_lines(conf_path, lines)
        return True

    def replace_version_code(self, version_tuple):
        mod_path = self.rose.get_config('module_path')
        code_files = glob.glob(os.path.join(self.rose.base_dir, mod_path))

        for code_path in code_files:
            lines = self.read_lines(code_path)
            lines = self.substitute_code(lines, version_tuple)
            self.write_lines(code_path, lines)

        return True

    def run(self, *args, **kwargs):
        raw_version = args[0]
        version_tuple = self.rose.parse_version(raw_version)

        self.replace_version_setup(version_tuple)
        self.replace_version_sphinx(version_tuple)
        self.replace_version_code(version_tuple)
        self.exit_code = 0


command_class = BumpVersion