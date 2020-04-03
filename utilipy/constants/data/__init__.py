# -*- coding: utf-8 -*-
# see LICENSE.rst

# ----------------------------------------------------------------------------
#
# TITLE   : data
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Data Management.

Often data is packaged poorly and it can be difficult to understand how
the data should be read.
DON`T PANIC.
This module provides functions to read the contained data.

Routine Listings
----------------
read_constants
__all_constants__

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "read_constants",
    "__all_constants__",
]


###############################################################################
# IMPORTS


###############################################################################
# CODE
###############################################################################


def read_constants():
    """Read SI Constants."""

    data = {
        "G": {
            "name": "Gravitational constant",
            "value": 6.6743e-11,
            "uncertainty": 1.5e-15,
            "unit": "m3 / (kg s2)",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "N_A": {
            "name": "Avogadro's number",
            "value": 6.02214076e23,
            "uncertainty": 0.0,
            "unit": "1 / mol",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "R": {
            "name": "Gas constant",
            "value": 8.31446261815324,
            "uncertainty": 0.0,
            "unit": "J / (K mol)",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "Ryd": {
            "name": "Rydberg constant",
            "value": 10973731.56816,
            "uncertainty": 2.1e-05,
            "unit": "1 / m",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "a0": {
            "name": "Bohr radius",
            "value": 5.29177210903e-11,
            "uncertainty": 8e-21,
            "unit": "m",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "alpha": {
            "name": "Fine-structure constant",
            "value": 0.0072973525693,
            "uncertainty": 1.1e-12,
            "unit": "",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "atm": {
            "name": "Standard atmosphere",
            "value": 101325,
            "uncertainty": 0.0,
            "unit": "Pa",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "b_wien": {
            "name": "Wien wavelength displacement law constant",
            "value": 0.0028977719551851727,
            "uncertainty": 0.0,
            "unit": "K m",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "c": {
            "name": "Speed of light in vacuum",
            "value": 299792458.0,
            "uncertainty": 0.0,
            "unit": "m / s",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "e": {
            "name": "Electron charge",
            "value": 1.602176634e-19,
            "uncertainty": 0.0,
            "unit": "C",
            "source": "EMCODATA2018",
        },
        "eps0": {
            "name": "Vacuum electric permittivity",
            "value": 8.8541878128e-12,
            "uncertainty": 1.3e-21,
            "unit": "F / m",
            "reference": "CODATA 2018",
            "source": "EMCODATA2018",
        },
        "g0": {
            "name": "Standard acceleration of gravity",
            "value": 9.80665,
            "uncertainty": 0.0,
            "unit": "m / s2",
            "source": "CODATA2018",
        },
        "h": {
            "name": "Planck constant",
            "value": 6.62607015e-34,
            "uncertainty": 0.0,
            "unit": "J s",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "hbar": {
            "name": "Reduced Planck constant",
            "value": 1.0545718176461565e-34,
            "uncertainty": 0.0,
            "unit": "J s",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "k_B": {
            "name": "Boltzmann constant",
            "value": 1.380649e-23,
            "uncertainty": 0.0,
            "unit": "J / K",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "m_e": {
            "name": "Electron mass",
            "value": 9.1093837015e-31,
            "uncertainty": 2.8e-40,
            "unit": "kg",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "m_n": {
            "name": "Neutron mass",
            "value": 1.67492749804e-27,
            "uncertainty": 9.5e-37,
            "unit": "kg",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "m_p": {
            "name": "Proton mass",
            "value": 1.67262192369e-27,
            "uncertainty": 5.1e-37,
            "unit": "kg",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "mu0": {
            "name": "Vacuum magnetic permeability",
            "value": 1.25663706212e-06,
            "uncertainty": 1.9e-16,
            "unit": "N / A2",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "muB": {
            "name": "Bohr magneton",
            "value": 9.2740100783e-24,
            "uncertainty": 2.8e-33,
            "unit": "J / T",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "sigma_T": {
            "name": "Thomson scattering cross-section",
            "value": 6.6524587321e-29,
            "uncertainty": 6e-38,
            "unit": "m2",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "sigma_sb": {
            "name": "Stefan-Boltzmann constant",
            "value": 5.6703744191844314e-08,
            "uncertainty": 0.0,
            "unit": "W / (K4 m2)",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "u": {
            "name": "Atomic mass",
            "value": 1.6605390666e-27,
            "uncertainty": 5e-37,
            "unit": "kg",
            "reference": "CODATA 2018",
            "source": "CODATA2018",
        },
        "GM_earth": {
            "name": "Nominal Earth mass parameter",
            "value": 398600400000000.0,
            "uncertainty": 0.0,
            "unit": "m3 / s2",
            "source": "IAU2015",
        },
        "GM_jup": {
            "name": "Nominal Jupiter mass parameter",
            "value": 1.2668653e17,
            "uncertainty": 0.0,
            "unit": "m3 / s2",
            "source": "IAU2015",
        },
        "GM_sun": {
            "name": "Nominal solar mass parameter",
            "value": 1.3271244e20,
            "uncertainty": 0.0,
            "unit": "m3 / s2",
            "source": "IAU2015",
        },
        "L_bol0": {
            "name": "Luminosity for absolute bolometric magnitude 0",
            "value": 3.0128e28,
            "uncertainty": 0.0,
            "unit": "W",
            "source": "IAU2015",
        },
        "L_sun": {
            "name": "Nominal solar luminosity",
            "value": 3.828e26,
            "uncertainty": 0.0,
            "unit": "W",
            "reference": "IAU 2015 Resolution B 3",
            "source": "IAU2015",
        },
        "M_earth": {
            "name": "Earth mass",
            "value": 5.972167867791379e24,
            "uncertainty": 1.3422009501651213e20,
            "unit": "kg",
            "reference": "IAU 2015 Resolution B 3 + CODATA 2018",
            "source": "IAU2015",
        },
        "M_jup": {
            "name": "Jupiter mass",
            "value": 1.8981245973360505e27,
            "uncertainty": 4.26589589320839e22,
            "unit": "kg",
            "reference": "IAU 2015 Resolution B 3 + CODATA 2018",
            "source": "IAU2015",
        },
        "M_sun": {
            "name": "Solar mass",
            "value": 1.988409870698051e30,
            "uncertainty": 4.468805426856864e25,
            "unit": "kg",
            "reference": "IAU 2015 Resolution B 3 + CODATA 2018",
            "source": "IAU2015",
        },
        "R_earth": {
            "name": "Nominal Earth equatorial radius",
            "value": 6378100.0,
            "uncertainty": 0.0,
            "unit": "m",
            "reference": "IAU 2015 Resolution B 3",
            "source": "IAU2015",
        },
        "R_jup": {
            "name": "Nominal Jupiter equatorial radius",
            "value": 71492000.0,
            "uncertainty": 0.0,
            "unit": "m",
            "reference": "IAU 2015 Resolution B 3",
            "source": "IAU2015",
        },
        "R_sun": {
            "name": "Nominal solar radius",
            "value": 695700000.0,
            "uncertainty": 0.0,
            "unit": "m",
            "reference": "IAU 2015 Resolution B 3",
            "source": "IAU2015",
        },
        "au": {
            "name": "Astronomical Unit",
            "value": 149597870700.0,
            "uncertainty": 0.0,
            "unit": "m",
            "reference": "IAU 2012 Resolution B2",
            "source": "IAU2015",
        },
        "kpc": {
            "name": "Kiloparsec",
            "value": 3.0856775814671917e19,
            "uncertainty": 0.0,
            "unit": "m",
            "reference": "Derived from au",
            "source": "IAU2015",
        },
        "pc": {
            "name": "Parsec",
            "value": 3.0856775814671916e16,
            "uncertainty": 0.0,
            "unit": "m",
            "reference": "Derived from au",
            "source": "IAU2015",
        },
    }

    return data


# /def


# ------------------------------------------------------------------------


__all_constants__ = frozenset(read_constants().keys())


###############################################################################
# END
