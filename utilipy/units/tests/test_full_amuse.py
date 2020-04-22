# -*- coding: utf-8 -*-

"""Test extended Astropy units.

Assuming that the base Astropy units are well tested,
only need to test the ones added by ``_added_units.py``

"""


__all__ = [
    "test_unit_overrides",
]


##############################################################################
# IMPORTS

# THIRD PARTY

import pytest

import astropy.units as units


# PROJECT-SPECIFIC

from .. import full_amuse as amu


##############################################################################
# CODE
##############################################################################


@pytest.mark.parametrize(
    "test_input,expected",
    [
        # SI
        (amu.ms, units.m / units.s),
        (amu.myr, units.Myr),
    ],
)
def test_unit_overrides(test_input, expected):
    """Test Astropy units overridden for AMUSE.

    Parameters
    ----------
    test_input : `~astropy.units.Unit`
        the added unit, to be tested against its value
    expected : `~astropy.units.Unit` or `~astropy.units.Quantity`
        the expected value of the unit

    Raises
    ------
    Exception
        if `test_input` != `expected`

    """
    assert test_input == expected

    return


# /def


# -------------------------------------------------------------------


##############################################################################
# END
