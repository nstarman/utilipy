#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_select
#
# ----------------------------------------------------------------------------


"""Test functions for data_utils/select."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General
import numpy as np

# Project-Specific
from utilipy.data_utils.select import (
    _inRange,
    inRange,
    outRange,
    ioRange,
    # ellipse,
    # circle,
)


##############################################################################
# PARAMETERS

x = np.arange(2)  # [0, 1]
y = np.arange(2) + 10  # [10, 11]

z = np.c_[x, y].T  # [[0,  1], [10, 11]]
zT = z.T  # [[0,  10], [1, 11]]


##############################################################################
# _inRange


def test__inRange():
    """Test _inRange."""
    # ---------------------------------
    # 1-Dimensional

    # set range
    rng = [0, 1]

    # standard  (lbi=True, ubi=False)
    assert all(_inRange(x, rng) == np.array([True, False]))

    # going through options
    assert all(
        _inRange(x, rng, lbi=False, ubi=False) == np.array([False, False])
    )
    assert all(
        _inRange(x, rng, lbi=False, ubi=True) == np.array([False, True])
    )
    assert all(
        _inRange(x, rng, lbi=True, ubi=False) == np.array([True, False])
    )
    assert all(_inRange(x, rng, lbi=True, ubi=True) == np.array([True, True]))

    # ---------------------------------
    # N-Dimensional

    rng = [[0, 1], [10, 11]]

    # standard  (lbi=True, ubi=False)
    assert (_inRange(z, rng) == np.array([[True, False], [True, False]])).all()

    # going through options
    assert (
        _inRange(z, rng, lbi=False, ubi=False)
        == np.array([[False, False], [False, False]])
    ).all()
    assert (
        _inRange(z, rng, lbi=False, ubi=True)
        == np.array([[False, True], [False, True]])
    ).all()
    assert (
        _inRange(z, rng, lbi=True, ubi=False)
        == np.array([[True, False], [True, False]])
    ).all()
    assert (
        _inRange(z, rng, lbi=True, ubi=True)
        == np.array([[True, True], [True, True]])
    ).all()

    return


# /def


##############################################################################
# inRange


def test_inRange_single_1D_argument():
    """Test inRange for a single, 1D argument."""
    # set range
    rng = [0, 1]

    # standard  (lbi=True, ubi=False)
    assert all(inRange(x, rng=rng) == np.array([True, False]))

    # going through options
    assert all(
        inRange(x, rng=rng, lbi=False, ubi=False) == np.array([False, False])
    )
    assert all(
        inRange(x, rng=rng, lbi=False, ubi=True) == np.array([False, True])
    )
    assert all(
        inRange(x, rng=rng, lbi=True, ubi=False) == np.array([True, False])
    )
    assert all(
        inRange(x, rng=rng, lbi=True, ubi=True) == np.array([True, True])
    )

    return


# /def


def test_inRange_many_1D_argmuents():
    """Test inRange for many 1D arguments."""
    # ---------------------------------
    # range agreement
    # set range
    rng = [[0, 1], [10, 11]]

    # standard  (lbi=True, ubi=False)
    assert (inRange(x, y, rng=rng) == np.array([True, False])).all()

    # going through options
    assert (
        inRange(x, y, rng=rng, lbi=False, ubi=False)
        == np.array([False, False])
    ).all()
    assert (
        inRange(x, y, rng=rng, lbi=False, ubi=True) == np.array([False, True])
    ).all()
    assert (
        inRange(x, y, rng=rng, lbi=True, ubi=False) == np.array([True, False])
    ).all()
    assert (
        inRange(x, y, rng=rng, lbi=True, ubi=True) == np.array([True, True])
    ).all()

    # ---------------------------------
    # different ranges, the second never matters

    rng = [[0, 1], [9, 12]]

    # standard  (lbi=True, ubi=False)
    assert (inRange(x, y, rng=rng) == np.array([True, False])).all()

    # going through options
    assert (
        inRange(x, y, rng=rng, lbi=False, ubi=False)
        == np.array([False, False])
    ).all()
    assert (
        inRange(x, y, rng=rng, lbi=False, ubi=True) == np.array([False, True])
    ).all()
    assert (
        inRange(x, y, rng=rng, lbi=True, ubi=False) == np.array([True, False])
    ).all()
    assert (
        inRange(x, y, rng=rng, lbi=True, ubi=True) == np.array([True, True])
    ).all()

    return


# /def


def test_inRange_single_ND_argument():
    """Test inRange for a single N-D argument."""
    # ---------------------------------
    # range agreement

    rng = [[0, 1], [10, 11]]

    # standard  (lbi=True, ubi=False)
    assert (
        inRange(z, rng=rng) == np.array([[True, False], [True, False]])
    ).all()

    # going through options
    assert (
        inRange(z, rng=rng, lbi=False, ubi=False)
        == np.array([[False, False], [False, False]])
    ).all()
    assert (
        inRange(z, rng=rng, lbi=False, ubi=True)
        == np.array([[False, True], [False, True]])
    ).all()
    assert (
        inRange(z, rng=rng, lbi=True, ubi=False)
        == np.array([[True, False], [True, False]])
    ).all()
    assert (
        inRange(z, rng=rng, lbi=True, ubi=True)
        == np.array([[True, True], [True, True]])
    ).all()

    # ---------------------------------
    # different ranges

    rng = [[0, 1], [9, 12]]

    # standard  (lbi=True, ubi=False)
    assert (
        inRange(z, rng=rng) == np.array([[True, False], [True, True]])
    ).all()

    # going through options
    assert (
        inRange(z, rng=rng, lbi=False, ubi=False)
        == np.array([[False, False], [True, True]])
    ).all()
    assert (
        inRange(z, rng=rng, lbi=False, ubi=True)
        == np.array([[False, True], [True, True]])
    ).all()
    assert (
        inRange(z, rng=rng, lbi=True, ubi=False)
        == np.array([[True, False], [True, True]])
    ).all()
    assert (
        inRange(z, rng=rng, lbi=True, ubi=True)
        == np.array([[True, True], [True, True]])
    ).all()

    return


# /def


def test_inRange_many_ND_arguments():
    """Test inRange for many N-D arguments."""
    # ---------------------------------
    # range agreement

    rng = ([[0, 1], [10, 11]], [[0, 10], [1, 11]])  # for z  # for zT

    # standard  (lbi=True, ubi=False)
    assert (
        inRange(z, zT, rng=rng) == np.array([[True, False], [True, False]])
    ).all()

    # going through options
    assert (
        inRange(z, zT, rng=rng, lbi=False, ubi=False)
        == np.array([[False, False], [False, False]])
    ).all()
    assert (
        inRange(z, zT, rng=rng, lbi=False, ubi=True)
        == np.array([[False, True], [False, True]])
    ).all()
    assert (
        inRange(z, zT, rng=rng, lbi=True, ubi=False)
        == np.array([[True, False], [True, False]])
    ).all()
    assert (
        inRange(z, zT, rng=rng, lbi=True, ubi=True)
        == np.array([[True, True], [True, True]])
    ).all()

    # ---------------------------------
    # different ranges, z rng does not matter

    rng = ([[-1, 2], [9, 12]], [[0, 10], [1, 11]])  # for z  # for zT

    # standard  (lbi=True, ubi=False)
    assert (
        inRange(z, zT, rng=rng) == np.array([[True, False], [True, False]])
    ).all()

    # going through options
    assert (
        inRange(z, zT, rng=rng, lbi=False, ubi=False)
        == np.array([[False, False], [False, False]])
    ).all()
    assert (
        inRange(z, zT, rng=rng, lbi=False, ubi=True)
        == np.array([[False, True], [False, True]])
    ).all()
    assert (
        inRange(z, zT, rng=rng, lbi=True, ubi=False)
        == np.array([[True, False], [True, False]])
    ).all()
    assert (
        inRange(z, zT, rng=rng, lbi=True, ubi=True)
        == np.array([[True, True], [True, True]])
    ).all()

    # ---------------------------------
    # different ranges, zT rng does not matter

    rng = ([[0, 1], [10, 11]], [[-1, 11], [0, 12]])  # for z  # for zT

    # standard  (lbi=True, ubi=False)
    assert (
        inRange(z, zT, rng=rng) == np.array([[True, False], [True, False]])
    ).all()

    # going through options
    assert (
        inRange(z, zT, rng=rng, lbi=False, ubi=False)
        == np.array([[False, False], [False, False]])
    ).all()
    assert (
        inRange(z, zT, rng=rng, lbi=False, ubi=True)
        == np.array([[False, True], [False, True]])
    ).all()
    assert (
        inRange(z, zT, rng=rng, lbi=True, ubi=False)
        == np.array([[True, False], [True, False]])
    ).all()
    assert (
        inRange(z, zT, rng=rng, lbi=True, ubi=True)
        == np.array([[True, True], [True, True]])
    ).all()

    return


# /def


def test_inRange_mixing_1D_and_ND_arguments():
    """Test inRange for a mix of 1D and N-D arguments.

    only mixed by breaking the ND arguments into a series of 1D arrays

    """
    # ---------------------------------
    # range agreement

    rng = (
        [0, 1],  # for x
        *[[0, 1], [10, 11]],  # for z
        [10, 11],  # for y
        *[[0, 10], [1, 11]],  # for zT
    )

    # standard  (lbi=True, ubi=False)
    assert (
        inRange(x, *z, y, *zT, rng=rng)
        == np.array([[True, False], [True, False]])
    ).all()

    # going through options
    assert (
        inRange(x, *z, y, *zT, rng=rng, lbi=False, ubi=False)
        == np.array([[False, False], [False, False]])
    ).all()
    assert (
        inRange(x, *z, y, *zT, rng=rng, lbi=False, ubi=True)
        == np.array([[False, True], [False, True]])
    ).all()
    assert (
        inRange(x, *z, y, *zT, rng=rng, lbi=True, ubi=False)
        == np.array([[True, False], [True, False]])
    ).all()
    assert (
        inRange(x, *z, y, *zT, rng=rng, lbi=True, ubi=True)
        == np.array([[True, True], [True, True]])
    ).all()

    return


# /def


##############################################################################
# outRange


def test_outRange_single_1D_argument():
    """Test outRange for a single, 1D argument."""
    # set range
    rng = [0, 1]

    # standard  (lbi=True, ubi=False)
    assert all(outRange(x, rng=rng) == ~np.array([True, False]))

    # going through options
    assert all(
        outRange(x, rng=rng, lbi=False, ubi=False) == ~np.array([False, False])
    )
    assert all(
        outRange(x, rng=rng, lbi=False, ubi=True) == ~np.array([False, True])
    )
    assert all(
        outRange(x, rng=rng, lbi=True, ubi=False) == ~np.array([True, False])
    )
    assert all(
        outRange(x, rng=rng, lbi=True, ubi=True) == ~np.array([True, True])
    )

    return


# /def


def test_outRange_many_1D_argmuents():
    """Test outRange for many 1D arguments."""
    # ---------------------------------
    # range agreement
    # set range
    rng = [[0, 1], [10, 11]]

    # standard  (lbi=True, ubi=False)
    assert (outRange(x, y, rng=rng) == ~np.array([True, False])).all()

    # going through options
    assert (
        outRange(x, y, rng=rng, lbi=False, ubi=False)
        == ~np.array([False, False])
    ).all()
    assert (
        outRange(x, y, rng=rng, lbi=False, ubi=True)
        == ~np.array([False, True])
    ).all()
    assert (
        outRange(x, y, rng=rng, lbi=True, ubi=False)
        == ~np.array([True, False])
    ).all()
    assert (
        outRange(x, y, rng=rng, lbi=True, ubi=True) == ~np.array([True, True])
    ).all()

    # ---------------------------------
    # different ranges, the second never matters

    rng = [[0, 1], [9, 12]]

    # standard  (lbi=True, ubi=False)
    assert (outRange(x, y, rng=rng) == ~np.array([True, False])).all()

    # going through options
    assert (
        outRange(x, y, rng=rng, lbi=False, ubi=False)
        == ~np.array([False, False])
    ).all()
    assert (
        outRange(x, y, rng=rng, lbi=False, ubi=True)
        == ~np.array([False, True])
    ).all()
    assert (
        outRange(x, y, rng=rng, lbi=True, ubi=False)
        == ~np.array([True, False])
    ).all()
    assert (
        outRange(x, y, rng=rng, lbi=True, ubi=True) == ~np.array([True, True])
    ).all()

    return


# /def


def test_outRange_single_ND_argument():
    """Test outRange for a single N-D argument."""
    # ---------------------------------
    # range agreement

    rng = [[0, 1], [10, 11]]

    # standard  (lbi=True, ubi=False)
    assert (
        outRange(z, rng=rng) == ~np.array([[True, False], [True, False]])
    ).all()

    # going through options
    assert (
        outRange(z, rng=rng, lbi=False, ubi=False)
        == ~np.array([[False, False], [False, False]])
    ).all()
    assert (
        outRange(z, rng=rng, lbi=False, ubi=True)
        == ~np.array([[False, True], [False, True]])
    ).all()
    assert (
        outRange(z, rng=rng, lbi=True, ubi=False)
        == ~np.array([[True, False], [True, False]])
    ).all()
    assert (
        outRange(z, rng=rng, lbi=True, ubi=True)
        == ~np.array([[True, True], [True, True]])
    ).all()

    # ---------------------------------
    # different ranges

    rng = [[0, 1], [9, 12]]

    # standard  (lbi=True, ubi=False)
    assert (
        outRange(z, rng=rng) == ~np.array([[True, False], [True, True]])
    ).all()

    # going through options
    assert (
        outRange(z, rng=rng, lbi=False, ubi=False)
        == ~np.array([[False, False], [True, True]])
    ).all()
    assert (
        outRange(z, rng=rng, lbi=False, ubi=True)
        == ~np.array([[False, True], [True, True]])
    ).all()
    assert (
        outRange(z, rng=rng, lbi=True, ubi=False)
        == ~np.array([[True, False], [True, True]])
    ).all()
    assert (
        outRange(z, rng=rng, lbi=True, ubi=True)
        == ~np.array([[True, True], [True, True]])
    ).all()

    return


# /def


def test_outRange_many_ND_arguments():
    """Test outRange for many N-D arguments."""
    # ---------------------------------
    # range agreement

    rng = ([[0, 1], [10, 11]], [[0, 10], [1, 11]])  # for z  # for zT

    # standard  (lbi=True, ubi=False)
    assert (
        outRange(z, zT, rng=rng) == ~np.array([[True, False], [True, False]])
    ).all()

    # going through options
    assert (
        outRange(z, zT, rng=rng, lbi=False, ubi=False)
        == ~np.array([[False, False], [False, False]])
    ).all()
    assert (
        outRange(z, zT, rng=rng, lbi=False, ubi=True)
        == ~np.array([[False, True], [False, True]])
    ).all()
    assert (
        outRange(z, zT, rng=rng, lbi=True, ubi=False)
        == ~np.array([[True, False], [True, False]])
    ).all()
    assert (
        outRange(z, zT, rng=rng, lbi=True, ubi=True)
        == ~np.array([[True, True], [True, True]])
    ).all()

    # ---------------------------------
    # different ranges, z rng does not matter

    rng = ([[-1, 2], [9, 12]], [[0, 10], [1, 11]])  # for z  # for zT

    # standard  (lbi=True, ubi=False)
    assert (
        outRange(z, zT, rng=rng) == ~np.array([[True, False], [True, False]])
    ).all()

    # going through options
    assert (
        outRange(z, zT, rng=rng, lbi=False, ubi=False)
        == ~np.array([[False, False], [False, False]])
    ).all()
    assert (
        outRange(z, zT, rng=rng, lbi=False, ubi=True)
        == ~np.array([[False, True], [False, True]])
    ).all()
    assert (
        outRange(z, zT, rng=rng, lbi=True, ubi=False)
        == ~np.array([[True, False], [True, False]])
    ).all()
    assert (
        outRange(z, zT, rng=rng, lbi=True, ubi=True)
        == ~np.array([[True, True], [True, True]])
    ).all()

    # ---------------------------------
    # different ranges, zT rng does not matter

    rng = ([[0, 1], [10, 11]], [[-1, 11], [0, 12]])  # for z  # for zT

    # standard  (lbi=True, ubi=False)
    assert (
        outRange(z, zT, rng=rng) == ~np.array([[True, False], [True, False]])
    ).all()

    # going through options
    assert (
        outRange(z, zT, rng=rng, lbi=False, ubi=False)
        == ~np.array([[False, False], [False, False]])
    ).all()
    assert (
        outRange(z, zT, rng=rng, lbi=False, ubi=True)
        == ~np.array([[False, True], [False, True]])
    ).all()
    assert (
        outRange(z, zT, rng=rng, lbi=True, ubi=False)
        == ~np.array([[True, False], [True, False]])
    ).all()
    assert (
        outRange(z, zT, rng=rng, lbi=True, ubi=True)
        == ~np.array([[True, True], [True, True]])
    ).all()

    return


# /def


def test_outRange_mixing_1D_and_ND_arguments():
    """Test outRange for a mix of 1D and N-D arguments.

    only mixed by breaking the ND arguments into a series of 1D arrays

    """
    # ---------------------------------
    # range agreement

    rng = (
        [0, 1],  # for x
        *[[0, 1], [10, 11]],  # for z
        [10, 11],  # for y
        *[[0, 10], [1, 11]],  # for zT
    )

    # standard  (lbi=True, ubi=False)
    assert (
        outRange(x, *z, y, *zT, rng=rng)
        == ~np.array([[True, False], [True, False]])
    ).all()

    # going through options
    assert (
        outRange(x, *z, y, *zT, rng=rng, lbi=False, ubi=False)
        == ~np.array([[False, False], [False, False]])
    ).all()
    assert (
        outRange(x, *z, y, *zT, rng=rng, lbi=False, ubi=True)
        == ~np.array([[False, True], [False, True]])
    ).all()
    assert (
        outRange(x, *z, y, *zT, rng=rng, lbi=True, ubi=False)
        == ~np.array([[True, False], [True, False]])
    ).all()
    assert (
        outRange(x, *z, y, *zT, rng=rng, lbi=True, ubi=True)
        == ~np.array([[True, True], [True, True]])
    ).all()

    return


# /def


##############################################################################
# ioRange


def test_ioRange_single_1D_argument():
    """Test outRange for a single, 1D argument."""
    # ---------------------------------
    # in & out

    rng = ([0, 1], [11, 12])

    # standard  (lbi=True, ubi=False)
    assert all(ioRange(incl=x, excl=y, rng=rng) == np.array([True, False]))

    # going through options
    # NO OPTIONS

    # ---------------------------------
    # both in

    rng = ([0, 1], [10, 11])

    # standard  (lbi=True, ubi=False)
    assert all(ioRange(incl=(x, y), rng=rng) == np.array([True, False]))

    # going through options
    # NO OPTIONS

    # ---------------------------------
    # both out

    rng = ([1, 2], [11, 12])

    # standard  (lbi=True, ubi=False)
    assert all(ioRange(excl=(x, y), rng=rng) == np.array([True, False]))

    # going through options
    # NO OPTIONS

    return


# /def


##############################################################################
# Ellipse


##############################################################################
# Circle


##############################################################################
# END
