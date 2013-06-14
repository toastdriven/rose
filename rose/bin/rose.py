import sys
from rose.runner import RoseRunner


if __name__ == '__main__':
    runner = RoseRunner()
    retval = runner.run()
    sys.exit(retval)
