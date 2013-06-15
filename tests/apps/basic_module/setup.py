#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(
    name='basic',
    version='0.9.1-beta',
    description='A test package.',
    author='John Doe',
    author_email='john@example.com',
    py_modules=['basic']
)
