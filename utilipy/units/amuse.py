# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : composite units
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Astropy units, extended for AMUSE compatibility.

These units are also available in the :mod:`~utilipy.units` namespace.

Not all AMUSE units are compatible with Astropy since some unit names are
already present in Astropy. These units are:

- ms (meters per second), which in Astropy means milliseconds
- myr (million years), which in Astropy means milliyear

This module prioritizes Astropy compatibility, so uses the Astropy versions.
For full AMUSE definitions in astropy units, the
:mod:`~utilipy.units.full_amuse` should be used.

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# THIRD-PARTY

import numpy as np

from astropy.units.core import def_unit
from astropy import constants, units
from astropy.units.utils import generate_unit_summary as _generate_unit_summary


##############################################################################
# PARAMETERS

_ns = globals()


##############################################################################
# AMUSE Units

#####################################################################
# SI

_to_add = [
    "m",
    "kg",
    "s",
    "A",
    "K",
    "mol",
    "cd",  # included by astropy automatically
]

for _u in _to_add:
    _ns[_u] = getattr(units, _u)


def_unit(
    ["kelvin"],
    represents=units.K,
    doc="Kelvin, AMUSE compatibility",
    format={"latex": r"K", "latex_inline": r"K"},
    namespace=_ns,
)


#####################################################################
# Derived SI

_to_add = [
    "Hz",
    "MHz",  # included by astropy automatically
    "rad",
    "sr",
    "N",
    "Pa",
    "J",
    "W",
    "F",
    "C",
    "V",
    "T",
    "tesla",  # included by astropy automatically
    "ohm",
    "S",
    "Wb",
    "weber",  # included by astropy automatically
]

for _u in _to_add:
    _ns[_u] = getattr(units, _u)


#####################################################################
# Units

###########################################################
# misc every day

_to_add = [
    "minute",
    "hour",
    "day",
    "yr",  # included by astropy automatically
    # "ms",  # can't be included. see :mod:`~utilipy.units.full_amuse`
]

for _u in _to_add:
    _ns[_u] = getattr(units, _u)


def_unit(
    ["julianyr"],
    represents=365.25 * units.day,
    doc="julian year, AMUSE compatibility",
    format={"latex": r"365.25{\cdot}d", "latex_inline": r"365.25{\cdot}d"},
    namespace=_ns,
)

def_unit(
    ["kms"],
    represents=units.km / units.s,
    doc="kilometer per seconds, AMUSE compatibility",
    format={"latex": r"\frac{km}{s}", "latex_inline": r"km\,s^{-1}"},
    namespace=_ns,
)


###########################################################
# units based on measured quantities

_to_add = [
    "eV",
    "Ry",
    "MeV",
    "GeV",  # included by astropy automatically
]

for _u in _to_add:
    _ns[_u] = getattr(units, _u)


def_unit(
    ["e"],
    represents=constants.e,
    doc="electron charge, AMUSE compatibility",
    format={"latex": r"|\rm{e}^{-1}|", "latex_inline": r"|\rm{e}^{-1}|"},
    namespace=_ns,
)

def_unit(
    ["E_h", "Hartree_energy"],
    represents=2 * units.Ry,
    doc="Hartree energy, AMUSE compatibility",
    format={"latex": r"2\rm{Ryd}", "latex_inline": r"2\rm{Ryd}"},
    namespace=_ns,
)

def_unit(
    ["amu"],
    represents=units.u,
    doc="atomic mass unit, AMUSE compatibility",
    format={"latex": r"\rm{amu}", "latex_inline": r"\rm{amu}"},
    namespace=_ns,
)


###########################################################
# astronomical units

_to_add = [
    "AU",
    "au",  # included by astropy automatically
    "angstrom",  # included by astropy automatically
    "kpc",
    "Mpc",
    "Gpc",
    "lightyear",
    "parsec",  # included by astropy automatically
    "kyr",  # included by astropy automatically
    # "myr",  # can't be included. see :mod:`~utilipy.units.full_amuse`
    "Myr",  # included by astropy automatically
    "Gyr",  # included by astropy automatically
    "pc",  # included by astropy automatically
]

for _u in _to_add:
    _ns[_u] = getattr(units, _u)


def_unit(
    ["AUd"],
    represents=149597870691.0 * units.m / units.day,
    doc="AU per day, AMUSE compatibility",
    format={"latex": r"\rm{AUd}", "latex_inline": r"\rm{AUd}"},
    namespace=_ns,
)

def_unit(
    ["ly"],
    represents=units.lyr,
    doc="light year, AMUSE compatibility",
    format={"latex": r"\rm{lyr}", "latex_inline": r"\rm{lyr}"},
    namespace=_ns,
)

def_unit(
    ["gyr"],
    represents=units.Gyr,
    doc="billion years, AMUSE compatibility.",
    format={"latex": r"Myr", "latex_inline": r"Myr"},
    namespace=_ns,
)

def_unit(
    ["LSun"],
    represents=units.solLum,
    doc="solar luminosity, AMUSE compatibility",
    format={"latex": r"\rm{L}_{\odot}", "latex_inline": r"\rm{L}_{\odot}"},
    namespace=_ns,
)

def_unit(
    ["MSun"],
    represents=units.M_sun,
    doc="solar mass, AMUSE compatibility",
    format={"latex": r"\rm{M}_{\odot}", "latex_inline": r"\rm{M}_{\odot}"},
    namespace=_ns,
)

def_unit(
    ["MJupiter"],
    represents=units.M_jup,
    doc="Jupiter mass, AMUSE compatibility",
    format={"latex": r"\rm{M}_{\rm{J}}", "latex_inline": r"\rm{M}_{\rm{J}}"},
    namespace=_ns,
)

def_unit(
    ["MEarth"],
    represents=units.M_earth,
    doc="Jupiter mass, AMUSE compatibility",
    format={"latex": r"\rm{M}_{\oplus}", "latex_inline": r"\rm{M}_{\oplus}"},
    namespace=_ns,
)

def_unit(
    ["RSun"],
    represents=units.R_sun,
    doc="solar radius, AMUSE compatibility",
    format={"latex": r"\rm{R}_{\odot}", "latex_inline": r"\rm{R}_{\odot}"},
    namespace=_ns,
)

def_unit(
    ["RJupiter"],
    represents=units.R_jup,
    doc="Jupiter radius, AMUSE compatibility",
    format={"latex": r"\rm{R}_{\rm{J}}", "latex_inline": r"\rm{R}_{\rm{J}}"},
    namespace=_ns,
)

def_unit(
    ["REarth"],
    represents=units.R_earth,
    doc="Jupiter radius, AMUSE compatibility",
    format={"latex": r"\rm{R}_{\oplus}", "latex_inline": r"\rm{R}_{\oplus}"},
    namespace=_ns,
)


###########################################################
# cgs units

_to_add = [
    "g",
    "cm",
    "erg",
    "barye",  # included by astropy automatically
]

for _u in _to_add:
    _ns[_u] = getattr(units, _u)


###########################################################
# miscellaneous

_to_add = [
    "percent",  # included by astropy automatically
]

for _u in _to_add:
    _ns[_u] = getattr(units, _u)


def_unit(
    ["metallicity"],
    namespace=_ns,
    prefixes=True,
    doc="metallicity: base unit of metallicity in AMUSE",
)

def_unit(
    ["string"],
    namespace=_ns,
    prefixes=True,
    doc="string: base string unit in AMUSE",
)

def_unit(
    ["stellar_type"],
    namespace=_ns,
    prefixes=True,
    doc="stellar_type: base stellar type unit in AMUSE",
)

# stellar_type = core.enumeration_unit(
#     'stellar_type',
#     'stellar_type',
#     None,
#     [
#         "deeply or fully convective low mass MS star",
#         "Main Sequence star",
#         "Hertzsprung Gap",
#         "First Giant Branch",
#         "Core Helium Burning",
#         "First Asymptotic Giant Branch",
#         "Second Asymptotic Giant Branch",
#         "Main Sequence Naked Helium star",
#         "Hertzsprung Gap Naked Helium star",
#         "Giant Branch Naked Helium star",
#         "Helium White Dwarf",
#         "Carbon/Oxygen White Dwarf",
#         "Oxygen/Neon White Dwarf",
#         "Neutron Star",
#         "Black Hole",
#         "Massless Supernova",
#         "Unknown stellar type",
#         "Pre-main-sequence Star"
#     ]
# )

# special unit for keys of particles
def_unit(
    ["object_key"],
    namespace=_ns,
    prefixes=True,
    doc="object_key: base particle key unit in AMUSE",
)


###########################################################
# angles

_to_add = [  # included by astropy automatically
    "rad",
    "deg",
    "arcmin",
    "arcsec",
]

for _u in _to_add:
    _ns[_u] = getattr(units, _u)


def_unit(
    ["pi"],
    represents=np.pi * units.rad,
    doc="pi radians, AMUSE compatibility",
    format={"latex": r"\pi\rm{rad}", "latex_inline": r"\pi\rm{rad}"},
    namespace=_ns,
)

def_unit(
    ["rev"],
    represents=(2 * np.pi) * units.rad,
    doc="revolutions, AMUSE compatibility",
    format={"latex": r"\rm{rev}", "latex_inline": r"\rm{rev}"},
    namespace=_ns,
)


##############################################################################
# CLEANUP

del def_unit
del units


##############################################################################
# DOCSTRING

# This generates a docstring for this module that describes all of the
# standard units defined here.
if __doc__ is not None:
    __doc__ += "\n" + _generate_unit_summary(globals())


##############################################################################
# END
