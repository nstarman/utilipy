# -*- coding: utf-8 -*-

"""Test extended Astropy units.

Assuming that the base Astropy units are well tested,
only need to test the ones added by ``_added_units.py``

"""


__all__ = [
    "test_unit_equivalency",
]


##############################################################################
# IMPORTS

# THIRD PARTY

import pytest

import astropy.units as units


# PROJECT-SPECIFIC

from .. import composite as cu


##############################################################################
# CODE
##############################################################################


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (cu.m_s, units.m / units.s),
        (cu.mps, units.m / units.s),
        (cu.km_s, units.km / units.s),
        (cu.kmps, units.km / units.s),
        (cu.km_sMpc, units.km / units.s / units.Mpc),
        (cu.kmpspMpc, units.km / units.s / units.Mpc),
        (cu.hubble, units.km / units.s / units.Mpc),
        (cu.Hubble, units.km / units.s / units.Mpc),
        (cu.km_skpc, units.km / units.s / units.kpc),
        (cu.kmpspkpc, units.km / units.s / units.kpc),
        (cu.mas_yr, units.mas / units.yr),
        (cu.maspyr, units.mas / units.yr),
    ],
)
def test_unit_equivalency(test_input, expected):
    """Test Astropy-AMUSE unit equivalencies.

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
