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

# THIRD PARTY
import numpy as np
import pytest

# PROJECT-SPECIFIC
from utilipy.data_utils.select import _inRange, ioRange, outRange

from utilipy.data_utils.select import inRange  # ellipse,; circle,


##############################################################################
# PARAMETERS

x = np.arange(2)  # [0, 1]
y = np.arange(2) + 10  # [10, 11]

z = np.c_[x, y].T  # [[0,  1], [10, 11]]
zT = z.T  # [[0,  10], [1, 11]]


##############################################################################
# _inRange


def test__inRange_1D_default():
    """Test _inRange."""
    # standard  (lbi=True, ubi=False)
    assert all(_inRange(x, rng=[0, 1]) == np.array([True, False]))


# /def


@pytest.mark.parametrize(
    "flags, expected",
    [
        ((False, False), np.array([False, False])),
        ((False, True), np.array([False, True])),
        ((True, False), np.array([True, False])),
        ((True, True), np.array([True, True])),
    ],
    ids=["non-inclusive", "ubi", "lbi", "inclusive"],
)
def test__inRange_1D_options(flags, expected):
    """Test _inRange, 1D, flag options."""
    assert all(_inRange(x, rng=[0, 1], lbi=flags[0], ubi=flags[1]) == expected)


# /def


def test__inRange():
    """Test _inRange."""

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


def test_ioRange_raises():
    """Test ioRange for expected failures."""
    with pytest.raises(ValueError):
        ioRange(incl=None, excl=None)


# /def


@pytest.mark.parametrize(
    "rng, expected",
    [
        (([0, 1], [11, 12]), np.array([True, False])),
        (([0, 1], [10, 11]), np.array([False, False])),
        (([1, 2], [11, 12]), np.array([False, False])),
    ],
    ids=["in & out", "both in", "both out"],
)
def test_ioRange_single_1D_argument(rng, expected):
    """Test ioRange for a single, 1D argument."""
    assert all(ioRange(incl=x, excl=y, rng=rng) == expected)


# /def


##############################################################################
# Ellipse


##############################################################################
# Circle


##############################################################################
# END
