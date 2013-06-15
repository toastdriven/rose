from rose.base import BaseCommand


class TestCommand(BaseCommand):
    def run(self, *args, **kwargs):
        self.out('Hello, ')
        self.out('world!')
        self.err('Oops!')
        self.exit_code = 0
