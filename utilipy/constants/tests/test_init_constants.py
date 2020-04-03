# -*- coding: utf-8 -*-
# see LICENSE.rst

# ----------------------------------------------------------------------------
#
# TITLE   : test constants data
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""tests.

Routine Listings
----------------

"""

__author__ = "Nathaniel Starkman"

# __all__ = [
#     ""
# ]


##############################################################################
# IMPORTS

# GENERAL

import os


# PROJECT-SPECIFIC

from ... import constants  # TODO relative import


##############################################################################
# TESTS
##############################################################################


def test_top_level_imports():
    """Test Top-Level Imports."""
    # First test they exist
    subpkg: str
    for subpkg in constants.__all_top_imports__:
        assert hasattr(constants, subpkg)

    # Next test that top-levels are all the possible top-levels
    drct: str = os.path.split(constants.__file__)[0]  # directory
    donottest = ("__pycache__", "data", "tests")  # stuff not to test

    for file in os.listdir(drct):  # iterate through directory
        # test?
        if os.path.isdir(drct + "/" + file) and file not in donottest:
            assert file in constants.__all_top_imports__
        else:  # nope, chuck testa.
            pass

    return


# /def


# --------------------------------------------------------------------------


def test_specific_imports():
    """Test specific imports."""
    # imports same as __init__
    from utilipy.constants.values import ConstantsValues, values
    from utilipy.constants._frozen import FrozenConstants, frozen

    # test equality
    assert constants.ConstantsValues is ConstantsValues
    assert constants.default_values is values
    assert constants.FrozenConstants is FrozenConstants
    assert constants.frozen is frozen

    return


# /def


# --------------------------------------------------------------------------


##############################################################################
# END
