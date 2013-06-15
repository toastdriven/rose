"""
This is an example module.
"""

__author__ = 'John Doe'
__version__ = (0, 9, 1, 'beta')


def something_else(*args):
    # Shouldn't get modified.
    version = 1.2
    # This logic doesn't matter.
    return '\n'.join(['hello', 'world'])
