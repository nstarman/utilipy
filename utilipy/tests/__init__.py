# -*- coding: utf-8 -*-
# see LICENSE.rst

"""Tests for :mod:`~utilipy`."""

__author__ = "Nathaniel"


__all__ = [
    # modules
    "test_init",
    "test_init_subpackages",
    # instance
    "test",
]


##############################################################################
# IMPORTS

# BUILT-IN
from pathlib import Path

# THIRD PARTY
from astropy.tests.runner import TestRunner

# PROJECT-SPECIFIC
from . import test_init, test_init_subpackages

##############################################################################
# TESTS
##############################################################################

test = TestRunner.make_test_runner_in(Path(__file__).parent.parent)

##############################################################################
# END
