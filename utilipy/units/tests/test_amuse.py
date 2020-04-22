# -*- coding: utf-8 -*-

"""Test extended Astropy units.

Assuming that the base Astropy units are well tested,
only need to test the ones added by ``_added_units.py``

"""


__all__ = [
    "test_unit_equivalency",
    "test_added_units",
]


##############################################################################
# IMPORTS

# THIRD PARTY

import pytest

import numpy as np

import astropy.units as units
import astropy.constants as constants


# PROJECT-SPECIFIC

from .. import amuse as amu


##############################################################################
# CODE
##############################################################################


@pytest.mark.parametrize(
    "test_input,expected",
    [
        # SI
        (amu.m, units.m),
        (amu.kg, units.kg),
        (amu.s, units.s),
        (amu.A, units.A),
        (amu.K, units.K),
        (amu.mol, units.mol),
        (amu.cd, units.cd),
        (amu.kelvin, units.K),
        # Derived SI
        (amu.Hz, units.Hz),
        (amu.MHz, units.MHz),
        (amu.rad, units.rad),
        (amu.sr, units.sr),
        (amu.N, units.N),
        (amu.Pa, units.Pa),
        (amu.J, units.J),
        (amu.W, units.W),
        (amu.F, units.F),
        (amu.C, units.C),
        (amu.V, units.V),
        (amu.T, units.T),
        (amu.tesla, units.tesla),
        (amu.ohm, units.ohm),
        (amu.S, units.S),
        (amu.Wb, units.Wb),
        (amu.weber, units.weber),
        # misc every day
        (amu.minute, units.minute),
        (amu.hour, units.hour),
        (amu.day, units.day),
        (amu.yr, units.yr),
        # (amu.ms, units.ms),  # can't be included.
        (amu.julianyr, 365.25 * units.day),
        (amu.kms, units.km / units.s),
        # units based on measured quantities
        (amu.eV, units.eV),
        (amu.Ry, units.Ry),
        (amu.MeV, units.MeV),
        (amu.GeV, units.GeV),
        (amu.e, constants.e),
        (amu.E_h, 2 * units.Ry),
        (amu.Hartree_energy, 2 * units.Ry),
        (amu.amu, units.u),
        # astronomical units
        (amu.AU, units.AU),
        (amu.au, units.au),
        (amu.angstrom, units.angstrom),
        (amu.kpc, units.kpc),
        (amu.Mpc, units.Mpc),
        (amu.Gpc, units.Gpc),
        (amu.lightyear, units.lightyear),
        (amu.parsec, units.parsec),
        (amu.kyr, units.kyr),
        # (amu.myr, units.myr),  # can't be included.
        (amu.Myr, units.Myr),
        (amu.Gyr, units.Gyr),
        (amu.pc, units.pc),
        (amu.AUd, 149597870691.0 * units.m / units.day),
        (amu.ly, units.lyr),
        (amu.gyr, units.Gyr),
        (amu.LSun, units.solLum),
        (amu.MSun, units.M_sun),
        (amu.MJupiter, units.M_jup),
        (amu.MEarth, units.M_earth),
        (amu.RSun, units.R_sun),
        (amu.RJupiter, units.R_jup),
        (amu.REarth, units.R_earth),
        # cgs units
        (amu.g, units.g),
        (amu.cm, units.cm),
        (amu.erg, units.erg),
        (amu.barye, units.barye),
        (amu.percent, units.percent),
        # angles
        (amu.rad, units.rad),
        (amu.deg, units.deg),
        (amu.arcmin, units.arcmin),
        (amu.arcsec, units.arcsec),
        (amu.pi, np.pi * units.rad),
        (amu.rev, (2 * np.pi) * units.rad),
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


@pytest.mark.parametrize(
    "test_input", ["metallicity", "string", "stellar_type", "object_key"],
)
def test_added_units(test_input):
    """Test completely new units added for AMUSE compatibility.

    Parameters
    ----------
    test_input : `~astropy.units.Unit`
        the added unit, to be tested that it does NOT exist in base astropy.

    Raises
    ------
    Exception
        if `test_input` is in base astropy

    """
    with pytest.raises(AssertionError):
        assert hasattr(units, test_input)

    return


# /def


##############################################################################
# END
