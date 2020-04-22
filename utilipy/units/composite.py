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

from astropy.units.core import def_unit
from astropy import units
from astropy.units.utils import generate_unit_summary as _generate_unit_summary


##############################################################################
# PARAMETERS

_ns = globals()


##############################################################################
# New Units

def_unit(
    ["m_s", "mps"],
    represents=units.m / units.s,
    doc="meter per second composite unit",
    format={"latex": r"\frac{m}{s}", "latex_inline": r"m\,s^{-1}"},
    namespace=_ns,
)

def_unit(
    ["km_s", "kmps"],
    represents=units.km / units.s,
    doc="kilometer per second composite unit",
    format={"latex": r"\frac{km}{s}", "latex_inline": r"km\,s^{-1}"},
    namespace=_ns,
)

def_unit(
    ["km_sMpc", "kmpspMpc", "hubble", "Hubble"],
    represents=units.km / units.s / units.Mpc,
    doc="kilometer per second per Megaparsec composite unit",
    format={
        "latex": r"\frac{km}{s Mpc}",
        "latex_inline": r"km\,s^{-1}\,{Mpc}^{-1}",
    },
    namespace=_ns,
)

def_unit(
    ["km_skpc", "kmpspkpc"],
    represents=units.km / units.s / units.kpc,
    doc="kilometer per second per kiloparsec composite unit",
    format={
        "latex": r"\frac{km}{s kpc}",
        "latex_inline": r"km\,s^{-1}\,{kpc}^{-1}",
    },
    namespace=_ns,
)

def_unit(
    ["mas_yr", "maspyr"],
    represents=units.mas / units.yr,
    doc="milli-arcseconds / year composite unit",
    format={"latex": r"\frac{mas}{yr}", "latex_inline": r"mas\,yr^{-1}"},
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
