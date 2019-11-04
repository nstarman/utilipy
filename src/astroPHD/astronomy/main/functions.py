#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : functions
# AUTHOR  : Nathaniel Starkman
# PROJECT : astronat
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
r"""Astronomy functions.

TODO incorporate astropy cosmology

"""

__author__ = "Nathaniel Starkman"

##############################################################################
# IMPORTS

# General
from functools import wraps
import numpy as np

# Custom Imports
from ... import units as u


##############################################################################
# Angular Distance

@u.quantity_io()
def angular_distance(lon1: u.deg, lat1: u.deg, lon2: u.deg, lat2: u.deg):
    r"""Angular distance on-sky.

    for longitude (ra) \alpha and latitude (dec) \delta
    .. math::
        \cos{\theta} = \left[\sin(\delta_1)\sin(\delta_2) +
                             \cos(\delta_1)\cos(\delta_2)\cos(\alpha_1-\alpha_2)
                       \right]

    Parameters
    ----------
    lon1 : scalar or array
        the longitude of the 1st point
        if array, lat1, lon2, lat2 must be same-size arrays, or scalars
    lat1 : scalar or array
        the latitude of the 1st point
        if array, lon1, lon2, lat2 must be same-size arrays, or scalars
    lon2 : scalar or array
        the longitude of the 2nd point
        if array, lon1, lat1, lat2 must be same-size arrays, or scalars
    lat2 : scalar or array
        the latitude of the 2nd point
        if array, lon1, lat1, lon2 must be same-size arrays, or scalars

    Returns
    -------
    res : scalar or array
        the angular distance on-sky
        same shape as largest of lon1, lat1, lon2, lat2

    Info
    ----
    for reference:
        ICRS: lon=ra, lat=dec

    """
    latcomp = np.sin(lat1) * np.sin(lat2)  # latitude component
    loncomp = np.cos(lat1) * np.cos(lat2) * np.cos(lon1 - lon2)  # longitude component

    res = np.arccos(latcomp + loncomp)

    return res
# /def


##############################################################################
# Distance Modulus

@u.quantity_io(m=u.mag, d_L='distance')
def apparent_to_absolute_magnitude(m: u.mag, d_L: u.pc, **kw) -> u.mag:
    """
    calculate the absolute magnitude
    M = m - 5 log10(d) + 5

    Parameters
    ----------
    m: array_like
        apparent magnitude
    d_L: array_like
        luminosity distance to object in pc

    Returns
    -------
    M: ndarray
        absolute magnitudes
    """

    M = m - 5.0 * np.log10(d_L) + 5.0

    return M
# /def


@u.quantity_io(M=u.mag, d_L='distance')
def absolute_to_apparent_magnitude(M: u.mag, d_L: u.pc, **kw) -> u.mag:
    """
    calculate the apparent magnitude
    m = M + 5 log10(d) - 5

    Parameters
    ----------
    M: array_like
        absolute magnitude
    d_L: array_like
        luminosity distance to object in pc

    Returns
    -------
    m: ndarray
        apparent magnitudes
    """

    m = M + 5.0 * np.log10(d_L) - 5.0

    return m
# /def


##############################################################################
# Distance Modulus

@u.quantity_io(d='length', A=u.mag,
               annot2dfu=True, default_units={'A': u.mag})
def distanceModulus_magnitude(d: u.pc, A=0 * u.mag, obs=True, **kw) -> u.mag:
    r"""Distance Modulus
    equation:  DM = 5 log10(d / 10) + A

    mtrue - M = 5 log10(d / 10)
    if there is line-of-sight extinction
    mobs = mtrue + A
    | mobs - M = 5 log10(d / 10) + A
    | true - M = 5 log10(d / 10) - A

    Arguments
    ---------
    d: scalar, array, Quantity
        distance
        no units => parsecs
    A: scalar, array, Quantity (in mag)
        extinction in magnitudes
    obs: bool (default True)
        whether to return (mobs - M) or (mtrue - M)
        defualt: (mobs - M)
        **don't change unless specifically required

    Returns
    -------
    DM: scalar, array
        default units: u.mag
    """

    if not obs:
        A *= -1

    return (5 * u.mag) * (np.log10(d.to_value(u.pc)) - 1) + A
# /def


# --------------------------------------------------------------------------

@u.quantity_io(DM=u.mag, annot2dfu=True)
def distanceModulus_distance(DM: u.mag, **kw) -> u.pc:
    r"""Distance Modulus
    equation:  DM = 5 log10(d / 10) -> d = 10^{\frac{DM}{5}+1}

    Arguments
    ---------
    DM: scalar, array
        in magnitudes
        if Quantity, pass as distance.to_value('mag')

    Returns
    -------
    distance: scalar, array
        in parsecs
        no units attached
    """

    return np.power(10., np.divide(DM, 5. * u.mag) + 1) * u.pc
# /def


# --------------------------------------------------------------------------

# TODO annot2dfu = T/F?
@u.quantity_io(arg=('length', u.mag), A=u.mag,
               annot2dfu=True, default_units={'A': u.mag})
def distanceModulus(arg, A=0 * u.mag, obs=True, **kw):
    r"""Distance Modulus
    equation:  DM = 5 log10(d / 10) + A

    mtrue - M = 5 log10(d / 10)
    if there is line-of-sight extinction
    mobs = mtrue + A
    | mobs - M = 5 log10(d / 10) + A
    | true - M = 5 log10(d / 10) - A

    Arguments
    ---------
    d: scalar, array, Quantity
        no units => parsecs
    A: scalar, array, Quantity (in mag)
        extinction in magnitudes
    obs: bool (default True)
        whether to return (mobs - M) or (mtrue - M)
        defualt: (mobs - M)
        **don't change unless specifically required

    Returns
    -------
    DM: scalar, array
        default units: u.mag
    """

    if u.get_physical_type(arg) == 'length':
        if not obs:
            A *= -1

        return (5 * u.mag) * (np.log10(arg.to_value(u.pc)) - 1) + A
        # return distanceModulus_magnitude(arg, A=A, obs=obs,
        #                                  _skip_decorator=True)

    else:
        return np.power(10., np.divide(arg, 5. * u.mag) + 1) * u.pc
        # return distanceModulus_distance(arg, _skip_decorator=True)
# /def


##############################################################################
# Parallax

@u.quantity_io(d='length')
def parallax_angle(d: u.pc, **kw) -> u.deg:
    r"""compute parallax angle
    """
    return np.arctan(1 * u.AU / d)
# /def

# --------------------------------------------------------------------------


@u.quantity_io(p='angle')
def parallax_distance(p: u.deg, **kw) -> u.pc:
    r"""compyte parallax distance
    """
    return 1 * u.AU / np.tan(p)
# /def

# --------------------------------------------------------------------------


@u.quantity_io(arg=('angle', 'length'))
def parallax(arg, **kw):
    if u.get_physical_type(arg) == 'angle':
        return parallax_distance(arg)
    elif u.get_physical_type(arg) == 'length':
        return parallax_angle(arg)
    else:
        raise TypeError(f"{arg} must have units of distance or angle")
# /def


##############################################################################
# Angular Separation

@u.quantity_io(doff='length', dto='length')
def max_angular_separation(doff, dto, **kw) -> u.deg:
    """
    doff: distance
        distance offset from coordinate
    dto: distance
        distance to original coordinate

    the maximum angular separation comes from moving
    at right angle from current position

    Returns
    -------
    angle: deg
        angular separation
    """
    return np.fabs(np.arctan(np.divide(doff, dto))) * u.rad
# /def


##############################################################################
# Docs
