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
from typing import Union, Dict

# PROJECT-SPECIFIC
import astroPHD  # TODO relative import


##############################################################################
# PARAMETERS


##############################################################################
# TEST FUNCTIONS
##############################################################################


def test_top_level_imports():
    """Test Top-Level Imports."""
    # First test they exist
    subpkg: str
    for subpkg in astroPHD.__all_top_imports__:
        assert hasattr(astroPHD, subpkg)

    # Next test that top-levels are all the possible top-levels
    drct: str = os.path.split(astroPHD.__file__)[0]  # directory
    donottest = ("tests", "__pycache__")  # stuff not to test

    for file in os.listdir(drct):  # iterate through directory
        # test?
        if os.path.isdir(drct + "/" + file) and file not in donottest:
            assert file in astroPHD.__all_top_imports__
        else:  # nope, chuck testa.
            pass

    return


# /def


# --------------------------------------------------------------------------


def test_specific_imports():
    """Test specific imports."""
    # imports same as __init__
    from astroPHD.utils.logging import LogFile
    from astroPHD.utils.collections import ObjDict
    from astroPHD.utils.functools import wraps

    # test equality
    assert astroPHD.LogFile is LogFile
    assert astroPHD.ObjDict is ObjDict
    assert astroPHD.wraps is wraps

    return


# /def


##############################################################################
# END
