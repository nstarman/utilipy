# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.math.core`."""


__all__ = [
    "test_quadrature",
    "test_as_quantity",
    "test_qsquare",
    "test_qnorm",
    "test_qarange",
]


##############################################################################
# IMPORTS

# BUILT-IN

import warnings


# THIRD PARTY

import astropy.units as u
import numpy as np
import pytest


# PROJECT-SPECIFIC

from .. import core


##############################################################################
# PARAMETERS

_NP_V = [
    int(v) for i, v in enumerate(np.__version__.split(".")) if i < 3
]
if (_NP_V[0] <= 1) and (_NP_V[1] <= 16):  # v1.16
    warnings.warn(
        (
            "Need to set the environment variable "
            "NUMPY_EXPERIMENTAL_ARRAY_FUNCTION=1"
        )
    )


##############################################################################
# CODE
##############################################################################


@pytest.mark.skip(reason="TODO")
def test_quadrature():
    """Test :class:`~utilipy.math.core.quadrature`."""
    # ------------------
    # No input

    with pytest.raises(ValueError):
        core.quadrature()

    # ------------------
    # 1 argument

    assert core.quadrature(2.0) == 2.0
    assert core.quadrature(-2.0) == 2.0

    # axis argument can matter
    assert core.quadrature(-2.0, axis=1) == 2.0

    with pytest.raises(np.AxisError):
        core.quadrature(2, axis=2)

    # ------------------
    # many scalar arguments

    assert core.quadrature(3.0, 4.0) == 5.0
    assert core.quadrature(-3, 4.0) == 5.0

    # axis argument can matter
    assert core.quadrature(3.0, 4.0, axis=-1) == 5.0

    with pytest.raises(np.AxisError):
        core.quadrature(3.0, 4.0, axis=2)

    # ------------------
    # 1 vector argument

    x = [3.0, 12.0]

    # not expanded
    actual = core.quadrature(x)
    expected = 12.36931687685298
    assert np.testing.assert_equal(actual, expected)

    # same as expanded
    actual = core.quadrature(*x)
    assert np.testing.assert_equal(actual, expected)

    # axis argument can matter
    actual = core.quadrature(x, axis=-1)
    np.testing.assert_equal(actual, expected)

    with pytest.raises(np.AxisError):
        core.quadrature(x, axis=2)

    # ------------------
    # many vector arguments

    x = [3.0, 12.0]
    y = [4.0, 5.0]

    actual = core.quadrature(x, y)
    expected = np.array([5.0, 13.0])
    assert np.testing.assert_equal(actual, expected)

    # axis argument matters
    actual = core.quadrature(x, y, axis=-1)
    expected = np.array([12.36931688, 6.40312424])
    assert np.testing.assert_almost_equal(actual, expected)

    with pytest.raises(np.AxisError):
        core.quadrature(x, y, axis=2)

    pass


# /def


# -------------------------------------------------------------------


def test_as_quantity():
    """Test :func:`~utilipy.math.core.as_quantity`."""
    # ------------------
    # Quantities Unchanged

    # single number
    x = 1 * u.m
    y = core.as_quantity(x)
    assert y == x

    # array
    x = [1, 2] * u.m
    y = core.as_quantity(x)
    assert all(y == x)

    # ------------------
    # Change Copies

    # array
    x = [1, 2, 3] * u.m
    y = core.as_quantity(x)
    assert all(y == x)

    # changed
    x[0] = 0 * u.m
    assert all(y == x)

    # ------------------
    # Recast arrays

    # array
    x = [1 * u.m, 2 * u.m, 3 * u.m]
    y = core.as_quantity(x)
    assert all(y == [1, 2, 3] * u.m)

    # array, with conversion
    x = [1 * u.m, 200 * u.cm, 3 * u.m]
    y = core.as_quantity(x)
    assert all(y == [1, 2, 3] * u.m)

    # ------------------
    # Failure Tests

    with pytest.raises(NotImplementedError):
        core.as_quantity("arg")


# /def


# -------------------------------------------------------------------


def test_qsquare():
    """Test :func:`~utilipy.math.core.qsquare`.

    Most tests are covered by `test_as_quantity`
    and numpy's internal testing for :func:`~numpy.square`

    """
    x = 2 * u.m
    y = core.qsquare(x)
    assert y == x ** 2


# /def


# -------------------------------------------------------------------


@pytest.mark.skip(
    (_NP_V[0] <= 1) & (_NP_V[1] <= 16), reason="Numpy version <= 1.16"
)
def test_qnorm():
    """Test :func:`~utilipy.math.core.qnorm`.

    Most tests are covered by `test_as_quantity`
    and numpy's internal testing for :func:`~numpy.linalg.norm`

    """
    # norm a scalar
    x = -2 * u.m
    y = core.qnorm(x)
    assert y == -x

    # norm an array
    x = [3, 4] * u.m
    y = core.qnorm(x)
    assert y == 5 * u.m


# /def


# -------------------------------------------------------------------


def test_qarange():
    """Test :func:`~utilipy.math.core.qarange`.

    Most tests are covered by `test_as_quantity`
    and numpy's internal testing for :func:`~numpy.arange`

    """
    # basic test
    start = 1 * u.m
    stop = 10 * u.m
    step = 1 * u.m

    expected = np.arange(1, 10, 1) * u.m
    assert all(core.qarange(start, stop, step) == expected)

    # change unit
    expected = np.arange(1, 10, 1) * 100 * u.cm
    assert all(core.qarange(start, stop, step, unit=u.cm) == expected)

    # change step
    step = 1 * u.cm
    expected = np.arange(100, 1000, 1) * u.cm
    assert all(core.qarange(start, stop, step) == expected)

    # raise error
    with pytest.raises(AttributeError):
        core.qarange(start, stop, 1)


# /def


##############################################################################
# END
