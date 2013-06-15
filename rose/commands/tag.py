from __future__ import unicode_literals
from shell import Shell

from rose.base import BaseCommand
from rose.exceptions import ShowHelpError, FlagError


class TagVersion(BaseCommand):
    # TODO: Someday support:
    #     * hg
    #     * svn
    #     * Others?
    def __init__(self, *args, **kwargs):
        super(TagVersion, self).__init__(*args, **kwargs)
        self.shell = Shell()

    def help(self, *args, **kwargs):
        return '\n'.join([
            "Usage: rose tag <tag_name>",
            "",
            "Tags the version within your version control system.",
            "",
            "Flags:",
            "  -t, --type",
            "      Specifies the VCS (& type of tagging). Valid options are 'git' or 'git-flow'.",
        ])

    def mangle_to_snake_case(self, value):
        return value.replace('-', '_')

    def get_tag_name(self, *args):
        if len(args) != 1:
            raise ShowHelpError("No tag name provided!")

        return args[0]

    def get_tag_type(self, **kwargs):
        tag_type = 'git'

        if 't' in kwargs:
            tag_type = kwargs['t']

        if 'type' in kwargs:
            tag_type = kwargs['type']

        return tag_type

    def check_success(self, sh):
        if sh.code != 0:
            for error in sh.errors():
                self.err(error)

            self.exit_code = 1
            return False

        self.exit_code = 0
        return True

    def git(self, tag_name):
        sh = self.shell.run('git tag %s' % tag_name)
        return self.check_success(sh)

    def git_flow(self, tag_name):
        release_branch = 'release-%s' % tag_name
        commands = [
            'git checkout -b %s' % release_branch,
            'git co master',
            'git merge %s' % release_branch,
            'git co develop',
            'git merge master',
        ]

        for cmd in commands:
            sh = self.shell.run()

            if not self.check_success(sh):
                return False

        return True

    def run(self, *args, **kwargs):
        tag_name = self.get_tag_name(*args)
        tag_type = self.get_tag_type(**kwargs)
        tag_type = self.mangle_to_snake_case(tag_type)

        if not hasattr(self, tag_type):
            raise FlagError("Unknown tag type option '%s'." % tag_type)

        scm_method = getattr(self, tag_type)
        return scm_method(tag_name)


command_class = TagVersion