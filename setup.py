# -*- coding: utf-8 -*-

"""astroPHD setup.py.

#############################################################################

setup method referenced from
referenced from https://github.com/pytorch/vision/blob/master/setup.py

"""

#############################################################################
# IMPORTS

import os
import io
import re
from setuptools import setup, find_packages
from pkg_resources import get_distribution, DistributionNotFound


#############################################################################
# FUNCTIONS

def read(*names, **kwargs):
    """read."""
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()
# /def


def get_dist(pkgname):
    """Get distribution."""
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None
# /def


def find_version(*file_paths):
    """Find version."""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")
# /def


#############################################################################
# RUNNING

README = open('README.md').read()

VERSION = find_version(os.path.join('src/astroPHD/', '__init__.py'))

requirements = [
    'numpy>=1.7',
    'scipy',
    'matplotlib',
    'astropy',
    'wrapt',
    'tqdm',  # or extras?
]

classifiers = [
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]

setup(
    name='astroPHD',
    version=VERSION,
    author='Nathaniel Starkman',
    author_email='n.starkman@mail.utoronto.ca',
    url='https://github.com/nstarman/astroPHD.git',
    description='Useful python and astrophysics-concomitant tools',
    long_description=README,
    long_description_content_type="text/markdown",
    license='New BSD',

    # Package info
    package_dir={'': 'src'},
    packages=find_packages(exclude=('tests', 'scratch')),

    zip_safe=True,
    install_requires=requirements,
    extras_require={
        "fitting": ['scipy', 'lmfit'],
        "amuse": ['amuse-framework', 'amuse-bhtree', 'amuse-seba']
    },
)

#############################################################################
# END
