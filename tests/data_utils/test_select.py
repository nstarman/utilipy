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

def test_inRange_single_1D_argument():

    rng = [0, 1]

    # standard  (lbi=True, ubi=False)
    assert all(inRange(x, rng=rng) == np.array([True, False]))

    # going through options
    assert all(inRange(x, rng=rng, lbi=False, ubi=False) == np.array([False, False]))
    assert all(inRange(x, rng=rng, lbi=False, ubi=True ) == np.array([False, True ]))
    assert all(inRange(x, rng=rng, lbi=True,  ubi=False) == np.array([True , False]))
    assert all(inRange(x, rng=rng, lbi=True,  ubi=True ) == np.array([True , True ]))

    return
# /def


def test_inRange_many_1D_argmuents():

    rng = [[0, 1], [10, 11]]

    # standard  (lbi=True, ubi=False)
    assert (inRange(x, y, rng=rng) == np.array([True, False])).all()

    # going through options
    assert (inRange(x, y, rng=rng, lbi=False, ubi=False) == np.array([False, False])).all()
    assert (inRange(x, y, rng=rng, lbi=False, ubi=True) == np.array([False, True])).all()
    assert (inRange(x, y, rng=rng, lbi=True, ubi=False) == np.array([True, False])).all()
    assert (inRange(x, y, rng=rng, lbi=True, ubi=True) == np.array([True, True])).all()

    return
# /def


def test_inRange_single_ND_argument():

    rng = [[0, 1], [10, 11]]

    # standard  (lbi=True, ubi=False)
    assert (inRange(z, rng=rng) == np.array([[True, False], [True, False]])).all()

    # going through options
    assert (inRange(z, rng=rng, lbi=False, ubi=False) == np.array([[False, False], [False, False]])).all()
    assert (inRange(z, rng=rng, lbi=False, ubi=True ) == np.array([[False, True ], [False, True ]])).all()
    assert (inRange(z, rng=rng, lbi=True,  ubi=False) == np.array([[True,  False], [True,  False]])).all()
    assert (inRange(z, rng=rng, lbi=True,  ubi=True ) == np.array([[True,  True],  [True,  True ]])).all()

    return
# /def


def test_inRange_many_ND_arguments():

    # ---------------------------------
    # Mutliple ND Arguments
    # TODO

    return
# /def


def test_inRange_mixing_1D_and_ND_arguments():

    # ---------------------------------
    # Mixing ND and 1D Arguments
    # TODO

    return
# /def


##############################################################################
### outRange


def test_outRange_single_1D_argument():
    # TODO
    return
# /def


def test_outRange_many_1D_argmuents():
    # TODO
    return
# /def


def test_outRange_single_ND_argument():
    # TODO
    return
# /def


def test_outRange_many_ND_arguments():
    # TODO
    return
# /def


def test_outRange_mixing_1D_and_ND_arguments():
    # TODO
    return
# /def


##############################################################################
### ioRange


##############################################################################
### Ellipse


##############################################################################
### Circle


##############################################################################
### END
