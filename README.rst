====
rose
====

"""A version by any other name would be just as sweet."""

An end-user tool for creating & releasing Python packages.

semver_

.. _semver: http://semver.org/


Requirements
============

* Python 2.6+ or Python 3.3+


Usage
=====

Creating a new package (done within the code directory):

    rose create_package

Bumping the version in the package:

    rose bump_version 2.0.1

Releasing a new version (which bumps the version, tags a release & pushes a
source distribution to PyPI):

    rose release --scm=git 2.0.1


Future Additions
================

* git-flow support
* Fetch & show classifiers
* hg support?
* Check PyPI name availability?


Installation
============

Using ``pip``, simply run::

    pip install rose


License
=======

New BSD
