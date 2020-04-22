# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : composite units
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Composite Astropy units."""

__author__ = "Nathaniel Starkman"


# __all__ = []


##############################################################################
# IMPORTS

# THIRD-PARTY

# from astropy.units import *

from astropy.units.core import def_unit
from astropy import units
from astropy.units.utils import generate_unit_summary as _generate_unit_summary


# PROJECT-SPECIFIC

from .amuse import *


##############################################################################
# PARAMETERS

_ns = globals()


##############################################################################
# AMUSE Units
# override from .amuse

# del ms, myr

def_unit(
    ["ms"],
    represents=units.m / units.s,
    doc="meter per seconds, AMUSE compatibility. Overrides millisecond.",
    format={"latex": r"\frac{m}{s}", "latex_inline": r"m\,s^{-1}"},
    namespace=_ns,
)


def_unit(
    ["myr"],
    represents=units.Myr,
    doc="million years, AMUSE compatibility. Overrides milliyear.",
    format={"latex": r"Myr", "latex_inline": r"Myr"},
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
