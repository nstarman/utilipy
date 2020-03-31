# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : data_util decorators
#
# ----------------------------------------------------------------------------

"""Test data_util decorators."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

import numpy as np


# PROJECT-SPECIFIC

from ..decorators import idxDecorator


##############################################################################
# PARAMETERS

x = np.arange(2)
y = np.arange(2) + 2

z = np.c_[x, y].T


##############################################################################
# TESTS
##############################################################################

##########################################################################
# idxDecorator


def test_idxDecorator_standard():
    """Test standard use of idxDecorator."""
    # defining function
    @idxDecorator
    def func1(x):
        return x < 1

    # /def

    # calling normally
    assert all(func1(x) == np.array([True, False]))

    # using added kwarg
    assert all(func1(x, as_ind=True) == np.array([0]))

    return


# /def


# ------------------------------------------------------------------------


def test_idxDecorator_defaults():
    """Test setting default in idxDecorator."""
    # defining function
    @idxDecorator(as_ind=True)
    def func2(x):
        return x < 1

    # /def

    # calling normally, defaulted to index
    assert all(func2(x) == np.array([0]))

    # using added kwarg
    assert all(func2(x, as_ind=False) == np.array([True, False]))

    return


# /def


# ------------------------------------------------------------------------


def test_idxDecorator_new_decorator():
    """Test making new decorator."""
    # making new decorator with different value
    trueidxdec = idxDecorator(as_ind=True)

    # defining function
    @trueidxdec
    def func3(x):
        return x < 1

    # /def

    # calling normally, defaulted to index
    assert func3(x) == np.array([0])

    # using added kwarg
    assert all(func3(x, as_ind=False) == np.array([True, False]))

    return


# /def


# ------------------------------------------------------------------------


def test_idxDecorator_existing_function():
    """Test wrapping existing function with idxDecorator."""
    # defining function
    def func(x):
        return x < 1

    # /def

    # wrapping existing function
    newfunc = idxDecorator(func, as_ind=True)

    # calling normally, defaulted to index
    assert newfunc(x) == np.array([0])

    # using added kwarg
    assert all(newfunc(x, as_ind=False) == np.array([True, False]))

    return


# /def

# ------------------------------------------------------------------------


##############################################################################
# END
