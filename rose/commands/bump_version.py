from __future__ import unicode_literals
from rose.base import BaseCommand


class BumpVersion(BaseCommand):
    def run(self, *args, **kwargs):
        pass


command_class = BumpVersion