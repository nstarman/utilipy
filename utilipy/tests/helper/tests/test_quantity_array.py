# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.tests.quantity_array.quantity_array`."""

__all__ = [
    "Test_eltwise_quantity_isclose",
    "Test_eltwise_quantity_allclose",
    "Test_eltwise_assert_quantity_isclose",
    "Test_eltwise_assert_quantity_allclose",
]


##############################################################################
# IMPORTS

# THIRD PARTY
import astropy.units as u
import numpy as np
import pytest

# PROJECT-SPECIFIC
from utilipy.tests.helper import quantity_array  # BaseClassDependentTests,

##############################################################################
# CODE
##############################################################################


class Test_eltwise_quantity_isclose:
    """Test :func:`~utilipy.tests.helper.eltwise_quantity_isclose`."""

    @property
    def func(self):
        """Tested function."""
        return quantity_array.eltwise_quantity_isclose

    @pytest.mark.parametrize(
        "a,b,rtol,atol,expected", [(1, 1 + 1e-16, 1e-15, None, True)]
    )
    def test_nounit(self, a, b, rtol, atol, expected):
        """Test when don't pass units."""
        assert self.func(a, b, rtol=rtol, atol=atol) == expected

    # /def

    @pytest.mark.parametrize(
        "a,b,rtol,atol,expected", [(1 * u.m, 1 * u.s, 1e-15, None, True)]
    )
    def test_wrongunit(self, a, b, rtol, atol, expected):
        """Test when pass wrong units."""
        with pytest.raises(u.UnitsError):
            assert self.func(a, b, rtol, atol)

    # /def

    @pytest.mark.parametrize(
        "a,b,rtol,atol,expected",
        [
            (1 * u.m, 1 * u.m, 1e-15, None, True),
            (0 * u.m, 0 * u.m, 1e-15, None, True),  # basic
            (1e-17 * u.m, 0 * u.m, 0, 1e-15 * u.m, True),  # close to 0
            (0 * u.m, 1e-17 * u.m, 0, 1e-15 * u.m, True),  # close to 0
            (0 * u.m, 1 * u.m, 1e-15, None, False),  # fails
            (0 * u.m, 1 * u.m, 2, None, True),  # adjust rtol to make work
        ],
    )
    def test_scalar(self, a, b, rtol, atol, expected):
        """Test when arguments are scalars.

        .. todo::

            Add hypothesis tests

        """
        assert self.func(a, b, rtol=rtol, atol=atol) == expected

    # /def

    @pytest.mark.parametrize(
        "a,b,rtol,atol,expected",
        [
            ([0, 0] * u.m, [0, 1] * u.m, 1e-15, None, [True, False]),  # basic
            ([1e-17, 0] * u.m, [0, 0] * u.m, 0, 1e-15 * u.m, [True, True]),
            ([1, 0] * u.m, [0, 1e-17] * u.m, 0, 1e-15 * u.m, [False, True]),
            ([0, 1] * u.m, [1, 1] * u.m, 1e-15, None, [False, True]),  # fails
            ([0, 1] * u.m, [1, 2] * u.m, 2, None, [True, True]),
            (  # units IN the list
                [0 * u.m, 1 * u.s],
                [0 * u.m, 1 * u.s],
                1e-15,
                None,
                [True, True],
            ),
            (
                [0 * u.m, 1 * u.s],
                [0 * u.m, 2 * u.s],
                1e-15,
                None,
                [True, False],
            ),
        ],
    )
    def test_vector(self, a, b, rtol, atol, expected):
        """Tests when arguments are vectors.

        To address [#148]

        .. todo::

            Add hypothesis tests

        """
        assert np.all(self.func(a, b, rtol=rtol, atol=atol) == expected)

    # /def


# /class

# -------------------------------------------------------------------


class Test_eltwise_quantity_allclose(Test_eltwise_quantity_isclose):
    """Test :func:`~utilipy.tests.helper.eltwise_quantity_allclose`."""

    @property
    def func(self):
        """Tested function."""
        return quantity_array.eltwise_quantity_allclose

    @pytest.mark.parametrize(
        "a,b,rtol,atol,expected",
        [
            ([0, 0] * u.m, [0, 0] * u.m, 1e-15, None, True),  # basic
            ([1e-17, 0] * u.m, [0, 0] * u.m, 0, 1e-15 * u.m, True),
            ([0, 0] * u.m, [1e-17, 0] * u.m, 0, 1e-15 * u.m, True),
            ([0, 1] * u.m, [1, 1] * u.m, 1e-15, None, False),  # fails
            ([0, 1] * u.m, [1, 2] * u.m, 2, None, True),
            # units IN the list
            ([0 * u.m, 1 * u.s], [0 * u.m, 1 * u.s], 1e-15, None, True),
        ],
    )
    def test_vector(self, a, b, rtol, atol, expected):
        """Tests when arguments are vectors.

        Unit tests IN the list are from [#148].

        .. todo::

            Add hypothesis tests

        """
        assert self.func(a, b, rtol=rtol, atol=atol) == expected

    # /def

    @pytest.mark.parametrize(
        "a,b,rtol,atol",
        [
            # units mismatch
            ([0 * u.m, 1 * u.s], [0 * u.m, 2 * u.m], 1e-15, None),
        ],
    )
    def test_vector_fails(self, a, b, rtol, atol):
        """Tests when arguments are vectors.

        Unit tests IN the list are from [#148].

        .. todo::

            Add hypothesis tests

        """
        with pytest.raises(u.UnitsError):
            self.func(a, b, rtol=rtol, atol=atol)

    # /def


# /class


# -------------------------------------------------------------------


class Test_eltwise_assert_quantity_isclose:
    """Test `~utilipy.tests.helper.eltwise_assert_quantity_isclose`.

    test no-units, wrong units, and scalar inputs.

    """

    @property
    def func(self):
        """Tested function."""
        return quantity_array.eltwise_assert_quantity_isclose

    @pytest.mark.parametrize(
        "a,b,rtol,atol",
        [
            (1, 1 + 1e-16, 1e-15, None),
        ],
    )
    def test_nounit(self, a, b, rtol, atol):
        """Test when don't pass units."""
        self.func(a, b, rtol=rtol, atol=atol)

    # /def

    @pytest.mark.parametrize(
        "a,b,rtol,atol",
        [(1 * u.m, 1 * u.s, 1e-15, None)],
    )
    def test_wrongunit(self, a, b, rtol, atol):
        """Test when pass wrong units."""
        with pytest.raises(u.UnitsError):
            self.func(a, b, rtol, atol)

    # /def

    @pytest.mark.parametrize(
        "a,b,rtol,atol",
        [
            (1 * u.m, 1 * u.m, 1e-15, None),
            (0 * u.m, 0 * u.m, 1e-15, None),  # basic
            (1e-17 * u.m, 0 * u.m, 0, 1e-15 * u.m),  # close to 0
            (0 * u.m, 1e-17 * u.m, 0, 1e-15 * u.m),  # close to 0
            (0 * u.m, 1 * u.m, 2, None),  # adjust rtol to make work
        ],
    )
    def test_scalar(self, a, b, rtol, atol):
        """Test when arguments are scalars.

        .. todo::

            Add hypothesis tests

        """
        self.func(a, b, rtol=rtol, atol=atol)

    # /def

    @pytest.mark.parametrize(
        "a,b,rtol,atol",
        [
            (0 * u.m, 1 * u.m, 1e-15, None),
        ],  # fails
    )
    def test_scalar_fails(self, a, b, rtol, atol):
        """Test when arguments are scalars.

        .. todo::

            Add hypothesis tests

        """
        with pytest.raises(AssertionError):
            self.func(a, b, rtol=rtol, atol=atol)

    # /def

    @pytest.mark.parametrize(
        "a,b,rtol,atol",
        [
            ([0, 0] * u.m, [0, 0] * u.m, 1e-15, None),
            ([1e-17, 0] * u.m, [0, 0] * u.m, 0, 1e-15 * u.m),
            ([0, 0] * u.m, [1e-17, 0] * u.m, 0, 1e-15 * u.m),
            ([0, 1] * u.m, [1, 2] * u.m, 2, None),
        ],
    )
    def test_vector(self, a, b, rtol, atol):
        """Tests when arguments are vectors.

        To address [#148]

        .. todo::

            Add hypothesis tests

        """
        self.func(a, b, rtol=rtol, atol=atol)

    # /def

    @pytest.mark.parametrize(
        "a,b,rtol,atol",
        [([0, 1] * u.m, [1, 1] * u.m, 1e-15, None)],
    )
    def test_vector_fails(self, a, b, rtol, atol):
        """Tests when arguments are vectors.

        .. todo::

            Add hypothesis tests

        """
        with pytest.raises(AssertionError):
            self.func(a, b, rtol=rtol, atol=atol)

    # /def


# /class


# -------------------------------------------------------------------


class Test_eltwise_assert_quantity_allclose(
    Test_eltwise_assert_quantity_isclose
):
    """Test `~utilipy.tests.helper.eltwise_assert_quantity_isclose`.

    Based on the Test_eltwise_assert_quantity_isclose tests.

    """

    @property
    def func(self):
        """Tested function."""
        return quantity_array.eltwise_assert_quantity_allclose

    @pytest.mark.parametrize(
        "a,b,rtol,atol",
        [
            ([0, 0] * u.m, [0, 0] * u.m, 1e-15, None),
            ([1e-17, 0] * u.m, [0, 0] * u.m, 0, 1e-15 * u.m),
            ([0, 0] * u.m, [1e-17, 0] * u.m, 0, 1e-15 * u.m),
            ([0, 1] * u.m, [1, 2] * u.m, 2, None),
            # units IN the list
            ([0 * u.m, 1 * u.s], [0 * u.m, 1 * u.s], 1e-15, None),
        ],
    )
    def test_vector(self, a, b, rtol, atol):
        """Tests when arguments are vectors.

        Unit tests IN the list are from [#148].

        .. todo::

            Add hypothesis tests

        """
        self.func(a, b, rtol=rtol, atol=atol)

    # /def

    @pytest.mark.parametrize(
        "a,b,rtol,atol",
        [
            ([0, 1] * u.m, [1, 1] * u.m, 1e-15, None),
            # units IN the list
            ([0 * u.m, 1 * u.s], [0 * u.m, 2 * u.m], 1e-15, None),
        ],
    )
    def test_vector_fails(self, a, b, rtol, atol):
        """Tests when arguments are vectors.

        Unit tests IN the list are from [#148].

        .. todo::

            Add hypothesis tests

        """
        # Raises AssertionError or UnitsError
        with pytest.raises((AssertionError, u.UnitsError)):
            self.func(a, b, rtol=rtol, atol=atol)

    # /def


# /class

# -------------------------------------------------------------------


##############################################################################
# END
