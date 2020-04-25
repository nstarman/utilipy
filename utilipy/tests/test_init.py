# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE  : test initialization
#
# ----------------------------------------------------------------------------

"""Tests for __init__.py."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

import os


# PROJECT-SPECIFIC

from .. import (
    __all_top_imports__ as all_top_imports,
    __file__ as _file,
    __dict__ as D,
)


##############################################################################
# PARAMETERS


##############################################################################
# TEST FUNCTIONS
##############################################################################


def test_top_level_imports():
    """Test Top-Level Imports."""
    # First test they exist
    subpkg: str
    for subpkg in all_top_imports:
        assert subpkg in D

    # Next test that top-levels are all the possible top-levels
    drct: str = os.path.split(_file)[0]  # directory
    donottest = ("tests", "__pycache__")  # stuff not to test

    for file in os.listdir(drct):  # iterate through directory
        # test?
        if os.path.isdir(drct + "/" + file) and file not in donottest:
            assert file in all_top_imports
        else:  # nope, chuck testa.
            pass

    return


# /def


# --------------------------------------------------------------------------


def test_specific_imports():
    """Test specific imports."""
    # imports same as __init__
    import utilipy

    from utilipy.utils.logging import LogFile
    from utilipy.utils.collections import ObjDict
    from utilipy.utils.functools import wraps

    # test equality
    assert utilipy.LogFile is LogFile
    assert utilipy.ObjDict is ObjDict
    assert utilipy.wraps is wraps

    return


# /def


##############################################################################
# END
