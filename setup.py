#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
"""
    astroPHD setup.py

#############################################################################

setup method referenced from
referenced from https://github.com/pytorch/vision/blob/master/setup.py

"""

#############################################################################
# Imports

import os
import io
import re
from setuptools import setup, find_packages
from pkg_resources import get_distribution, DistributionNotFound


#############################################################################
# Code

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


readme = open('README.md').read()

VERSION = find_version(os.path.join('astroPHD', '__init__.py'))

requirements = [
    'numpy>=1.7',
    'wrapt',
    'astropy'
]

classifiers = [
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]

setup(
    # Metadata
    name='astroPHD',
    version=VERSION,
    author='Nathaniel Starkman',
    author_email='n.starkman@mail.utoronto.ca',
    url='https://github.com/nstarman/astroPHD',
    description='assorted functions and packages',
    long_description=readme,
    license='New BSD',

    # Package info
    packages=find_packages(exclude=('tests',)),

    zip_safe=True,
    install_requires=requirements,
    extras_require={
        "scipy": ["scipy"],
        "lmfit": ['lmfit']
    },
)
