#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

import os

long_desc = ''

try:
    long_desc = os.path.join(os.path.dirname(__file__), 'README.rst').read()
except:
    # The description isn't worth a failed install...
    pass

setup(
    name='rose',
    # Ironically, I can't use rose here.
    version='1.0.0',
    description='A small library for keeping your version up-to-date easily & everywhere.',
    long_description=long_desc,
    author='Daniel Lindsley',
    author_email='daniel@toastdriven.com',
    url='http://github.com/toastdriven/rose',
    py_modules=['rose'],
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
