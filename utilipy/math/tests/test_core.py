# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.math.core`."""


__all__ = [
    "test_quadrature_no_input",
    "test_quadrature_single_argument",
    "test_quadrature_multi_scalar_argument",
    "test_quadrature_single_vector_argument",
    "test_quadrature_multi_vector_argument",
    "test_as_quantity_unchanged",
    "test_as_quantity_modifications",
    "test_as_quantity_recast",
    "test_as_quantity_exceptions",
    "test_qsquare",
    "test_qnorm",
    "test_qarange",
]


##############################################################################
# IMPORTS

# BUILT-IN
import os

# THIRD PARTY
import astropy.units as u
import numpy as np
import pytest

# PROJECT-SPECIFIC
from utilipy.math import core

##############################################################################
# PARAMETERS

_NP_V = [int(v) for i, v in enumerate(np.__version__.split(".")) if i < 3]


##############################################################################
# CODE
##############################################################################

# -------------------------------------------------------------------
# Quadrature


def test_quadrature_no_input():
    """Test :class:`~utilipy.math.core.quadrature` no input Exception."""
    with pytest.raises(ValueError):
        core.quadrature()  # No input


# /def


def test_quadrature_single_argument():
    """Test :class:`~utilipy.math.core.quadrature` single input."""
    assert core.quadrature(2.0) == 2.0
    assert core.quadrature(-2.0) == 2.0

    # axis argument can matter
    with pytest.raises(np.AxisError):
        assert core.quadrature(-2.0, axis=1) == 2.0

    with pytest.raises(np.AxisError):
        core.quadrature(2, axis=2)


# /def


def test_quadrature_multi_scalar_argument():
    """Test :class:`~utilipy.math.core.quadrature` multi-scalar inputs."""
    assert core.quadrature(3.0, 4.0) == 5.0
    assert core.quadrature(-3, 4.0) == 5.0

    # axis argument can matter
    assert core.quadrature(3.0, 4.0, axis=-1) == 5.0

    with pytest.raises(np.AxisError):
        core.quadrature(3.0, 4.0, axis=2)


# /def


def test_quadrature_single_vector_argument():
    """Test :class:`~utilipy.math.core.quadrature` single vector inputs."""
    x = [3.0, 12.0]

    # not expanded
    actual = core.quadrature(x)
    expected = 12.36931687685298
    np.testing.assert_almost_equal(actual, expected, decimal=7)

    # same as expanded
    actual = core.quadrature(*x)
    np.testing.assert_equal(actual, expected)

    # axis argument can matter
    actual = core.quadrature(x, axis=-1)
    np.testing.assert_equal(actual, expected)

    with pytest.raises(np.AxisError):
        core.quadrature(x, axis=2)


# /def


def test_quadrature_multi_vector_argument():
    """Test :class:`~utilipy.math.core.quadrature` multi-vector argument."""
    x = [3.0, 12.0]
    y = [4.0, 5.0]

    actual = core.quadrature(x, y)
    expected = np.array([5.0, 13.0])
    np.testing.assert_equal(actual, expected)

    # axis argument matters
    actual = core.quadrature(x, y, axis=-1)
    expected = np.array([12.36931688, 6.40312424])
    np.testing.assert_almost_equal(actual, expected)

    with pytest.raises(np.AxisError):
        core.quadrature(x, y, axis=2)


# /def


# -------------------------------------------------------------------
# As_quantity


def test_as_quantity_unchanged():
    """Test :func:`~utilipy.math.core.as_quantity` pass-through."""
    # single number
    x = 1 * u.m
    y = core.as_quantity(x)
    assert y == x

    # array
    x = [1, 2] * u.m
    y = core.as_quantity(x)
    assert all(y == x)


# /def


def test_as_quantity_modifications():
    """Test :func:`~utilipy.math.core.as_quantity` in-place modification."""
    # array
    x = [1, 2, 3] * u.m
    y = core.as_quantity(x)
    assert all(y == x)

    # changed
    x[0] = 0 * u.m
    assert all(y == x)


# /def


def test_as_quantity_recast():
    """Test :func:`~utilipy.math.core.as_quantity` array recasting."""
    # array
    x = [1 * u.m, 2 * u.m, 3 * u.m]
    y = core.as_quantity(x)
    assert all(y == [1, 2, 3] * u.m)

    # array, with conversion
    x = [1 * u.m, 200 * u.cm, 3 * u.m]
    y = core.as_quantity(x)
    assert all(y == [1, 2, 3] * u.m)


# /def


def test_as_quantity_exceptions():
    """Test :func:`~utilipy.math.core.as_quantity` expected Exceptions."""
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


def test_qnorm():
    """Test :func:`~utilipy.math.core.qnorm`.

    Most tests are covered by `test_as_quantity`
    and numpy's internal testing for :func:`~numpy.linalg.norm`

    """
    # Have to split into pre and post numpy 1.16
    # https://docs.astropy.org/en/lts/whatsnew/4.0.html
    if (
        (os.environ.get("NUMPY_EXPERIMENTAL_ARRAY_FUNCTION", 0) == 0)
        & (_NP_V[0] <= 1)
        & (_NP_V[1] <= 16)
    ):
        # norm a scalar
        x = -2 * u.m
        y = core.qnorm(x)
        assert y == 2.0

        # norm an array
        x = [3, 4] * u.m
        y = core.qnorm(x)
        assert y == 5.0

    else:

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
