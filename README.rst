====
rose
====

"""A version by any other name would be just as sweet."""

A small library for keeping your version up-to-date easily & everywhere.

The pain of having to update your ``setup.py``, your Sphinx ``conf.py``, your
``__init__.py`` & everything else on every release of your Python package sucks.
Make your life easier (& very semver_!)

.. _semver: http://semver.org/

By putting your version number in a top-level VERSION file & using this library,
you can cut duplication & tedious manual work **without** having to lean on
crazy import hacks.

Inspired by crazy discussion with George Hickman (ghickman) at PyCon 2013.


Requirements
============

* Python 2.5+


Usage
=====

To start, first install ``rose`` (see below). Then, push your version
number into it's own file (typically called ``VERSION``)::

    $ echo '1.0.0-beta' > VERSION

Update your ``setup.py`` to look like::

    # ...

    import rose

    setup(
        name='your_package_name_here',
        # UPDATE THIS LINE!
        version=rose.load_version('VERSION'),
        # The usual follows...

Then update your ``__init__.py``::

    # Whatever is there, then...

    import os
    import rose

    # If you don't care about being cross-platform, you can just pass a simple
    # path instead.
    VERSION_FILE = os.path.join(os.path.dirname('VERSION'))
    __version__ = rose.build_version('your_package_name_here', rose.load_version(VERSION_FILE))

And if you're documenting with Sphinx, you can update your ``conf.py`` with::

    # ADD THIS!
    import rose
    RELEASE_VERSION = rose.load_version('../VERSION')
    SHORT_VERSION = RELEASE_VERSION.split('-')[0]

    # The version info for the project you're documenting, acts as replacement for
    # |version| and |release|, also used in various other places throughout the
    # built documents.
    #
    # The short X.Y version.
    version = SHORT_VERSION
    # The full version, including alpha/beta/rc tags.
    release = RELEASE_VERSION


Installation
============

Using ``pip``, simply run::

    pip install rose


License
=======

New BSD
