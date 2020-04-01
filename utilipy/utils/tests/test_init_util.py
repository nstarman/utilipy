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

from ... import utils


##############################################################################
# TESTS
##############################################################################


def test_top_level_imports():
    """Test Top-Level Imports."""
    # First test they exist
    subpkg: str
    for subpkg in utils.__all_top_imports__:
        assert hasattr(utils, subpkg)

    # Next test that top-levels are all the possible top-levels
    drct: str = os.path.split(utils.__file__)[0]  # directory
    donottest = ("tests", "__pycache__")  # stuff not to test

    for file in os.listdir(drct):  # iterate through directory
        # test?
        if os.path.isdir(drct + "/" + file) and file not in donottest:
            assert file in utils.__all_top_imports__
        else:  # nope, chuck testa.
            pass

    return


# /def


# --------------------------------------------------------------------------


def test_specific_imports():
    """Test specific imports."""
    # imports same as __init__
    from utilipy.utils.logging import LogPrint, LogFile
    from utilipy.utils.collections import ObjDict
    from utilipy.utils import functools, pickle

    # test equality
    assert utils.LogPrint is LogPrint
    assert utils.LogFile is LogFile
    assert utils.ObjDict is ObjDict
    assert utils.functools is functools
    assert utils.pickle is pickle

    return


# /def


##############################################################################
# END
