"""
rose
====

"A version by any other name would be just as sweet."

An end-user tool for creating & releasing Python packages.
"""
from __future__ import print_function
import json
import os
import re
import sys

from rose.exceptions import VersionError


__author__ = 'Daniel Lindsley'
__license__ = 'New BSD'
__version__ = (2, 0, 0)



class Rose(object):
    def __init__(self, base_dir=None):
        self._base_dir = base_dir
        self.config = {
            'search_for': [
                '^__version__ = ',
                'version\s?=\s?',
            ],
        }
        self._config_loaded = False

    def get_config(self, key):
        if not self._config_loaded:
            self.setup()

        return self.config.get(key)

    def set_config(self, key, value):
        if not self._config_loaded:
            self.setup()

        self.config[key] = value
        return value

    @property
    def base_dir(self):
        if self._base_dir is None:
            self._base_dir = os.getcwdu()

        return self._base_dir

    def setup(self):
        home_path = os.environ.get('HOME')

        if home_path:
            home_config = os.path.join(home_path, '.rose')
            self.config.update(self.load_config_file(home_config, create=True))

        per_project_config = os.path.join(self.base_dir, '.rose')
        self.config.update(self.load_config_file(per_project_config))
        self._config_loaded = True

    def load_config_file(self, path, create=False):
        if not os.path.exists(path):
            if not create:
                return {}

            return self.save_config_file(path)

        with open(path, 'r') as config_file:
            return json.load(config_file)

    def save_config_file(self, path):
        with open(path, 'w') as config_file:
            json.dump(self.config, config_file, indent=4)

        return self.config

    def parse_version(self, version_string):
        version_bits = version_string.split('-')

        if len(version_bits) > 2:
            raise VersionError("Versions must be in '<major>.<minor>.<patch>[-<release>]' format. Saw: %s" % version_bits)

        major_minor_patch = version_bits.pop(0).split('.')

        if len(major_minor_patch) != 3:
            raise VersionError("Versions must be in '<major>.<minor>.<patch>[-<release>]' format. Saw: %s" % major_minor_patch)

        major_minor_patch = [int(bit) for bit in major_minor_patch]

        if version_bits:
            major_minor_patch.append(version_bits[0])

        return tuple(major_minor_patch)

    def build_short_version(self, version_tuple):
        return '.'.join([str(bit) for bit in version_tuple[:3]])

    def build_full_version(self, version_tuple):
        version = self.build_short_version(version_tuple)

        if len(version_tuple) > 3:
            version = '-'.join([version] + [str(bit) for bit in version_tuple[3:]])

        return version


class BaseCommand(object):
    STDOUT = 1
    STDERR = 2

    def __init__(self, rose):
        self.rose = rose
        self.output = []
        self.exit_code = 0

    def run(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the 'run' method.")

    def out(self, msg):
        self.output.append((
            BaseCommand.STDOUT,
            msg
        ))

    def err(self, msg):
        self.output.append((
            BaseCommand.STDERR,
            msg
        ))

    def has_output(self):
        return len(self.output) > 0

    def send_output(self):
        for out_type, msg in self.output:
            if out_type == BaseCommand.STDOUT:
                print(msg)
            elif out_type == BaseCommand.STDERR:
                sys.stderr.write(msg + '\n')

        self.output = []
