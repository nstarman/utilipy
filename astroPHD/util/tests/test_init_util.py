# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE  : test util/__init__
#
# ----------------------------------------------------------------------------

"""tests for util/__init__.py."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

import os


# PROJECT-SPECIFIC

from ... import util


##############################################################################
# TESTS
##############################################################################


def test_top_level_imports():
    """Test Top-Level Imports."""
    # First test they exist
    subpkg: str
    for subpkg in util.__all_top_imports__:
        assert hasattr(util, subpkg)

    # Next test that top-levels are all the possible top-levels
    drct: str = os.path.split(util.__file__)[0]  # directory
    donottest = ("tests", "__pycache__")  # stuff not to test

    for file in os.listdir(drct):  # iterate through directory
        # test?
        if os.path.isdir(drct + "/" + file) and file not in donottest:
            assert file in util.__all_top_imports__
        else:  # nope, chuck testa.
            pass

    return


# /def


# --------------------------------------------------------------------------


def test_specific_imports():
    """Test specific imports."""
    # imports same as __init__
    from astroPHD.util.logging import LogPrint, LogFile
    from astroPHD.util.collections import ObjDict
    from astroPHD.util import functools, pickle

    # test equality
    assert util.LogPrint is LogPrint
    assert util.LogFile is LogFile
    assert util.ObjDict is ObjDict
    assert util.functools is functools
    assert util.pickle is pickle

    return


# /def


##############################################################################
# END
