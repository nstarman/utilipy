# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE  : test util/__init__
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""tests for util/__init__.py."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

# PROJECT-SPECIFIC
from astroPHD import util


##############################################################################
# Tests

def test_imported():
    """Test imports."""
    # imports same as __init__
    from astroPHD.util.logging import LogPrint, LogFile
    from astroPHD.util.collections import ObjDict
    from astroPHD.util import collections, functools, pickle

    # test equality
    assert util.LogPrint is LogPrint
    assert util.LogFile is LogFile
    assert util.ObjDict is ObjDict
    assert util.collections is collections
    assert util.functools is functools
    assert util.pickle is pickle

    return
# /def


# --------------------------------------------------------------------------


##############################################################################
# END
