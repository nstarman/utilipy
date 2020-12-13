# -*- coding: utf-8 -*-

"""Tests for utilipy initialization."""


##############################################################################
# IMPORTS

# BUILT-IN
import os

# THIRD PARTY
import pytest

# PROJECT-SPECIFIC
from utilipy import __all_top_imports__ as all_top_imports
from utilipy import __dict__ as D
from utilipy import __file__ as _file
from utilipy import imports, lookup, online_help, reload_config

##############################################################################
# TESTS
##############################################################################


def test_reload_config():
    """Test :func:`~utilipy.reload_config`."""
    # get initial value
    init_value = imports.conf.verbose_imports

    # set changed value and test
    imports.conf.verbose_imports = bool(~init_value)
    assert imports.conf.verbose_imports == bool(~init_value)

    # reload and test
    reload_config()
    assert imports.conf.verbose_imports == init_value


# /def


# --------------------------------------------------------------------------


@pytest.mark.remote_data
def test_online_help():  # TODO actual tests.
    """Test :fun:`~utilipy.online_help`."""
    # -----------
    # by object
    online_help(query=online_help)
    online_help(query=online_help, version="1.0")

    # -----------
    # by str
    online_help(query="online_help")
    online_help(query="online_help", version="1.0")

    # -----------
    # blank
    online_help(query=None)
    online_help(query=None, version="1.0")


# /def


# --------------------------------------------------------------------------


@pytest.mark.remote_data
def test_lookup():  # TODO actual tests.
    """Test :fun:`~utilipy.online_help`."""
    lookup(query="lookup", online=True)

    lookup(query="lookup", online=False)


# /def


# --------------------------------------------------------------------------


def test_top_level_imports():
    """Test Top-Level Imports."""
    # First test they exist
    subpkg: str
    for subpkg in all_top_imports:
        assert subpkg in D

    # Next test that top-levels are all the possible top-levels
    drct: str = os.path.split(_file)[0]  # directory
    donottest = ("tests", "__pycache__", "ipython")  # stuff not to test

    for file in os.listdir(drct):  # iterate through directory
        if os.path.isdir(drct + "/" + file) and file not in donottest:
            assert file in all_top_imports
        # else:  # nope, chuck testa.
        #     pass


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


# /def


##############################################################################
# END
