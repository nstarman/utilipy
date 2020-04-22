# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Test `utilipy.units.core`
# PROJECT : `utilipy`
#
# ----------------------------------------------------------------------------

"""Test `utilipy.units.core`."""

__author__ = "Nathaniel Starkman"


__all__ = ["test_quantity_return_"]


##############################################################################
# IMPORTS

# GENERAL

import astropy.units as u


# PROJECT-SPECIFIC

from ..core import quantity_return_


##############################################################################
# CODE
##############################################################################


def test_quantity_return_():
    """Test Quantity Return Function."""
    # ------------------------------------------
    # Basic Test

    def function_no_change(x):
        """Function with No Changes."""
        return quantity_return_(x)

    # /def

    assert function_no_change(1 * u.km) == 1 * u.km
    assert function_no_change(1) == 1

    # ------------------------------------------
    # Convert Unit

    def function_convert_unit(x):
        """Function Converting Output Units."""
        return quantity_return_(x, unit=u.km)

    # /def

    assert function_convert_unit(1000 * u.m) == 1 * u.km
    assert function_convert_unit(1000 * u.m).value == 1
    assert function_convert_unit(1) == 1

    # ------------------------------------------
    # To Value

    def function_to_value(x):
        """Function Returning Value."""
        return quantity_return_(x, to_value=True)

    # /def

    assert function_to_value(1000 * u.m) == 1000
    assert function_to_value(1) == 1

    # ------------------------------------------
    # Equivalencies

    def function_equivalencies(x):
        """Function Returning Units Using Equivalencies."""
        return quantity_return_(x, unit=u.parsec, equivalencies=u.parallax())

    # /def

    assert function_equivalencies(1 * u.arcsec) == 1 * u.parsec
    assert function_equivalencies(1) == 1

    # ------------------------------------------
    # Decompose

    def function_decompose(x):
        """Function Returning Units, Decomposed."""
        return quantity_return_(x, decompose=True)

    # /def

    assert function_decompose(1 * u.km) == 1000 * u.m
    assert function_decompose(1) == 1

    # ------------------------------------------
    # Full Function Input

    def function_full(
        x, unit=None, to_value=False, equivalencies=[], decompose=False
    ):
        return quantity_return_(
            x,
            unit=unit,
            to_value=to_value,
            equivalencies=equivalencies,
            decompose=decompose,
        )

    # /def

    assert function_full(1) == 1
    assert function_full(1 * u.km) == 1 * u.km
    # unit
    assert function_full(1 * u.km, unit=u.m) == 1000 * u.m
    # to_value
    assert function_full(1 * u.km, to_value=True) == 1
    # equivalencies
    assert (
        function_full(1 * u.arcsec, unit=u.parsec, equivalencies=u.parallax())
        == 1 * u.parsec
    )
    # decompose
    assert function_full(1 * u.km, decompose=True) == 1000 * u.m
    assert function_full(1 * u.km, decompose=[u.mm]) == 1e6 * u.mm

    # combined calls
    assert function_full(1 * u.km, unit=u.m, to_value=True) == 1000

    return


# /def


# ------------------------------------------------------------------------


##############################################################################
# END
