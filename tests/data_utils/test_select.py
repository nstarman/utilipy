#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_select
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""test functions for data_utils/select
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
import numpy as np

## Project-Specific
from astroPHD.data_utils.select import (
    _inRange,
    inRange, outRange, ioRange,
    ellipse, circle
)


##############################################################################
### PARAMETERS

x = np.arange(2)
y = np.arange(2) + 10

z = np.c_[x, y].T  #  [[0, 1], [10, 11]]


##############################################################################
### _inRange

def test__inRange():

    # ---------------------------------
    # 1D

    rng = [0, 1]

    # standard  (lbi=True, ubi=False)
    assert all(_inRange(x, rng) == np.array([True, False]))

    # going through options
    assert all(_inRange(x, rng, lbi=False, ubi=False) == np.array([False, False]))
    assert all(_inRange(x, rng, lbi=False, ubi=True ) == np.array([False, True ]))
    assert all(_inRange(x, rng, lbi=True,  ubi=False) == np.array([True , False]))
    assert all(_inRange(x, rng, lbi=True,  ubi=True ) == np.array([True , True ]))

    # ---------------------------------
    # ND

    rng = [[0, 1], [10, 11]]

    # standard  (lbi=True, ubi=False)
    assert (_inRange(z, rng) == np.array([[True, False], [True, False]])).all()

    return
# /def


##############################################################################
### inRange

def test_inRange():

    # ---------------------------------
    # Basic

    rng = [0, 1]

    # standard  (lbi=True, ubi=False)
    assert all(inRange(x, rng=rng) == np.array([True, False]))

    # going through options
    assert all(inRange(x, rng=rng, lbi=False, ubi=False) == np.array([False, False]))
    assert all(inRange(x, rng=rng, lbi=False, ubi=True ) == np.array([False, True ]))
    assert all(inRange(x, rng=rng, lbi=True,  ubi=False) == np.array([True , False]))
    assert all(inRange(x, rng=rng, lbi=True,  ubi=True ) == np.array([True , True ]))

    # ---------------------------------
    # Many Arguments

    rng = [[0, 1], [10, 11]]

    # standard  (lbi=True, ubi=False)
    assert (inRange(x, y, rng=rng) == np.array([[True, False], [True, False]])).all()

    # going through options
    assert (inRange(x, y, rng=rng, lbi=False, ubi=False) ==
            np.array([[False, False], [False, False]])).all()
    assert (inRange(x, y, rng=rng, lbi=False, ubi=True) ==
            np.array([[False, True], [False, True]])).all()
    assert (inRange(x, y, rng=rng, lbi=True, ubi=False) ==
            np.array([[True, False], [True, False]])).all()
    assert (inRange(x, y, rng=rng, lbi=True, ubi=True) ==
            np.array([[True, True], [True, True]])).all()

    # ---------------------------------
    # MultiDim Argument

    rng = [[0, 1], [2, 3]]

    # standard  (lbi=True, ubi=False)
    # assert (inRange(z, rng=rng) == np.array([[True, False], [True, False]])).all()

    return
# /def

# --------------------------------------------------------------------------

##############################################################################
### END