# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : units
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Added units to Astropy units."""

__author__ = "Nathaniel Starkman"


__all__ = []


##############################################################################
# IMPORTS

import numpy as np
from astropy.units.core import def_unit
from astropy import units, constants
from astropy.units.utils import generate_unit_summary as _gen_summary


##############################################################################
# PARAMETERS

_us: dict = {}  # unit namespace. will be added to globals


##############################################################################
# New Units

def_unit(
    ["m_s", "mps"],
    represents=units.m / units.s,
    doc="meter per second composite unit",
    format={"latex": r"\frac{m}{s}", "latex_inline": r"m\,s^{-1}"},
    namespace=_us,
)

def_unit(
    ["km_s", "kmps"],
    represents=units.km / units.s,
    doc="kilometer per second composite unit",
    format={"latex": r"\frac{km}{s}", "latex_inline": r"km\,s^{-1}"},
    namespace=_us,
)

def_unit(
    ["km_sMpc", "kmpspMpc", "hubble", "Hubble"],
    represents=units.km / units.s / units.Mpc,
    doc="kilometer per second per Megaparsec composite unit",
    format={
        "latex": r"\frac{km}{s Mpc}",
        "latex_inline": r"km\,s^{-1}\,{Mpc}^{-1}",
    },
    namespace=_us,
)

def_unit(
    ["km_skpc", "kmpspkpc"],
    represents=units.km / units.s / units.kpc,
    doc="kilometer per second per kiloparsec composite unit",
    format={
        "latex": r"\frac{km}{s kpc}",
        "latex_inline": r"km\,s^{-1}\,{kpc}^{-1}",
    },
    namespace=_us,
)

def_unit(
    ["mas_yr", "maspyr"],
    represents=units.mas / units.yr,
    doc="milli-arcseconds / year composite unit",
    format={"latex": r"\frac{mas}{yr}", "latex_inline": r"mas\,yr^{-1}"},
    namespace=_us,
)


###########################################################################
# AMUSE compatibility

# base units, most already in astropy
# m = ('length', 'meter', 'm')
# kg = ('mass', 'kilogram', 'kg', system)
# s = ('time', 'second', 's', system)
# A = ('electric current', 'ampere', 'A', system)
# K = ('thermodynamic temperature', 'kelvin', 'K', system)
# mol = ('amount of substance', 'mole', 'mol', system)
# cd = ('luminous intensity', 'candela', 'cd', system)

def_unit(
    ["kelvin"],
    represents=units.K,
    doc="kelvin, AMUSE compatibility",
    format={"latex": r"K", "latex_inline": r"K"},
    namespace=_us,
)

# TODO SI prefixes
# deca, hecto, kilo, mega, giga, tera, peta, exa, zetta, yotta,
# deci, centi, milli, micro, nano, pico, femto, atto, zepto, yocto

# DERIVED SI, already in astropy
# Hz = named('hertz', 'Hz', 1/s)
# MHz = named('megahertz', 'MHz', 1e6*Hz)
# rad = named('radian','rad',m/m)
# sr = named('steradian','sr',m**2/m**2)
# N = named('newton', 'N', kg * m /s**2)
# Pa = named('pascal', 'Pa', N / (m ** 2))
# J = named('joule','J', kg * m **2  * s ** -2)
# W = named('watt', 'W', J / s)
# F = named('farad','F', s**4*A**2*m**(-2)*kg**(-1))
# C = named('coulomb','C', A*s)
# V = named('volt','V', J/C)
# T = named('tesla','T', kg/A/s/s)
# tesla = T
# ohm = named('ohm','ohm', V/A)
# S = named('siemens', 'S', A/V)
# Wb = named('weber','Wb', V*s)
# weber = Wb


# MISC EVERY DAY
# minute = named('minute', 'min', 60.0 * s)
# hour   = named('hour',   'hr',  60.0 * minute)
# day    = named('day',    'day', 24.0 * hour)
# yr     = named('year',   'yr',  365.242199 * day)
# julianyr = named('julian yr','julianyr',365.25* day)
# ms = named('meter per seconds', 'ms', m / s)
# kms = named('kilometer per seconds', 'kms', km / s)

def_unit(
    ["julianyr"],
    represents=365.25 * units.day,
    doc="julian year, AMUSE compatibility",
    format={"latex": r"365.25{\cdot}d", "latex_inline": r"365.25{\cdot}d"},
    namespace=_us,
)

# CANNOT DO ms B/C MEANS millisecond in astropy

def_unit(
    ["kms"],
    represents=units.km / units.s,
    doc="kilometer per second composite unit, AMUSE compatibility",
    format={"latex": r"\frac{km}{s}", "latex_inline": r"\rm{km}\,\rm{s}^{-1}"},
    namespace=_us,
)

# # units based on measured quantities
# e = named('electron charge', 'e', constants.elementary_charge.as_unit())
# eV=named('electron volt','eV', e*V)
# MeV=named('mega electron volt','MeV', 1e6*eV)
# GeV=named('giga electron volt','GeV', 1e9*eV)
# E_h = named('hartree energy', 'E_h', constants.Hartree_energy.as_unit())
# amu = named('atomic mass unit', 'amu', constants.u.as_unit())
# Ry = named(
#     "rydberg unit",
#     "Ry",
#     (constants.Rydberg_constant * constants.h * constants.c)
#     .as_quantity_in(eV)
#     .as_unit(),
# )

def_unit(
    ["e"],
    represents=constants.e,
    doc="electron charge, AMUSE compatibility",
    format={"latex": r"|\rm{e}^{-1}|", "latex_inline": r"|\rm{e}^{-1}|"},
    namespace=_us,
)
def_unit(
    ["E_h", "Hartree_energy"],
    represents=2 * units.Ry,
    doc="Hartree energy, AMUSE compatibility",
    format={"latex": r"2\rm{Ryd}", "latex_inline": r"2\rm{Ryd}"},
    namespace=_us,
)
def_unit(
    ["amu"],
    represents=units.u,
    doc="atomic mass unit, AMUSE compatibility",
    format={"latex": r"\rm{amu}", "latex_inline": r"\rm{amu}"},
    namespace=_us,
)

# # astronomical units
# angstrom = named('angstrom', 'angstrom', 1e-10*m)
# AU =  named('astronomical unit', 'AU', 149597870691.0  * m)
# au =  named('astronomical unit', 'au', 149597870691.0  * m)
# AUd = named('AU per day','AUd', 149597870691.0  * m / day)
# parsec=named('parsec','parsec', AU / numpy.tan(numpy.pi/(180*60*60)))
# kpc=named('kilo parsec','kpc',10**3 * parsec)
# Mpc=named('mega parsec','Mpc',10**6 * parsec)
# Gpc=named('giga parsec','Gpc',10**9 * parsec)
# lightyear = named('light year', 'ly', 9460730472580.8 * km)
# #lightyear = named('light year', 'ly', c*julianyr)
# LSun = named('solar luminosity', 'LSun', 3.839e26 * W)
# MSun = named('solar mass', 'MSun', 1.98892e30 * kg)
# MJupiter = named('jupiter mass', 'MJupiter', 1.8987e27 * kg)
# MEarth = named('earth mass', 'MEarth', 5.9722e24 * kg)
# RSun = named('solar radius', 'RSun', 6.955e8 * m)
# RJupiter = named('jupiter radius', 'RJupiter', 71492. * km)
# REarth = named('earth radius', 'REarth',  6371.0088 * km) # IUGG mean radius
# myr = named('million year', 'Myr', 1000000 * yr)
# Myr = myr
# gyr = named('giga (billion) year', 'Gyr', 1000000000 * yr)
# Gyr = gyr
# pc = parsec

def_unit(
    ["AUd"],
    represents=149597870691.0 * units.m / units.day,
    doc="AU per day, AMUSE compatibility",
    format={"latex": r"\rm{AUd}", "latex_inline": r"\rm{AUd}"},
    namespace=_us,
)

def_unit(
    ["ly"],
    represents=units.lyr,
    doc="light year, AMUSE compatibility",
    format={"latex": r"\rm{lyr}", "latex_inline": r"\rm{lyr}"},
    namespace=_us,
)

def_unit(
    ["LSun"],
    represents=units.solLum,
    doc="solar luminosity, AMUSE compatibility",
    format={"latex": r"\rm{L}_{\odot}", "latex_inline": r"\rm{L}_{\odot}"},
    namespace=_us,
)

def_unit(
    ["MSun"],
    represents=units.M_sun,
    doc="solar mass, AMUSE compatibility",
    format={"latex": r"\rm{M}_{\odot}", "latex_inline": r"\rm{M}_{\odot}"},
    namespace=_us,
)

def_unit(
    ["MJupiter"],
    represents=units.M_jup,
    doc="Jupiter mass, AMUSE compatibility",
    format={"latex": r"\rm{M}_{\rm{J}}", "latex_inline": r"\rm{M}_{\rm{J}}"},
    namespace=_us,
)

def_unit(
    ["MEarth"],
    represents=units.M_earth,
    doc="Jupiter mass, AMUSE compatibility",
    format={"latex": r"\rm{M}_{\oplus}", "latex_inline": r"\rm{M}_{\oplus}"},
    namespace=_us,
)

def_unit(
    ["RSun"],
    represents=units.R_sun,
    doc="solar radius, AMUSE compatibility",
    format={"latex": r"\rm{R}_{\odot}", "latex_inline": r"\rm{R}_{\odot}"},
    namespace=_us,
)

def_unit(
    ["RJupiter"],
    represents=units.R_jup,
    doc="Jupiter radius, AMUSE compatibility",
    format={"latex": r"\rm{R}_{\rm{J}}", "latex_inline": r"\rm{R}_{\rm{J}}"},
    namespace=_us,
)

def_unit(
    ["REarth"],
    represents=units.R_earth,
    doc="Jupiter radius, AMUSE compatibility",
    format={"latex": r"\rm{R}_{\oplus}", "latex_inline": r"\rm{R}_{\oplus}"},
    namespace=_us,
)

# CANNOT DO myr B/C MEANS milliyear in astropy

def_unit(
    ["gyr"],
    represents=units.Gyr,
    doc="giga year, AMUSE compatibility",
    format={"latex": r"\rm{Gyr}", "latex_inline": r"\rm{Gyr}"},
    namespace=_us,
)

# # cgs units
# g = named('gram','g', 1e-3 * kg)
# cm = named('centimeter','cm',0.01*m)
# erg = named('erg','erg', 1e-7 * J)
# barye = named('barye', 'Ba', 0.1*Pa)


# #angles
# #rad=named('radian','rad',m/m) (defined in derivedsi.py)
# pi=numpy.pi | rad
# rev=named('revolutions','rev',(2*numpy.pi) * rad)
# deg=named('degree','deg',(numpy.pi/180) *  rad)
# arcmin=named('arcminutes', 'arcmin', (1./60) * deg)
# arcsec=named('arcseconds', 'arcsec', (1./3600) * deg)

def_unit(
    ["pi"],
    represents=np.pi * units.rad,
    doc="pi radians, AMUSE compatibility",
    format={"latex": r"\pi\rm{rad}", "latex_inline": r"\pi\rm{rad}"},
    namespace=_us,
)


##############################################################################
# ADD ENABLED UNITS

for k in _us.keys():
    units.add_enabled_units([_us[k]])


_ns = globals()
_ns.update(_us)


##############################################################################
# CLEANUP

del np
del def_unit
del units
del constants


##############################################################################
# DOCSTRING

# This generates a docstring for this module that describes all of the
# standard units defined here.
if __doc__ is not None:
    __doc__ += _gen_summary(_ns)


##############################################################################
# END
