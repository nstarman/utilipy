#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : fast functions
# AUTHOR  : Nathaniel Starkman
# PROJECT : astronat
#
# ----------------------------------------------------------------------------
### Docstring and Metadata
r"""fast astronomy functions
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### IMPORTS

import numpy as np


###############################################################################
### Parameters

_AU_to_pc = 0.000004848137
_pc_to_AU = 1 / _AU_to_pc

###############################################################################
# Distance Conversion

def AU_to_pc(AU):
    """convert AU to pc"""
    return AU * _AU_to_pc

def pc_from_AU(AU):
    """convert AU to pc"""
    return AU * _AU_to_pc

# -------------------------------------------------------------------------

def AU_from_pc(pc):
    """convert pc to AU"""
    return pc * _pc_to_AU

def pc_to_AU(pc):
    """convert pc to AU"""
    return pc * _pc_to_AU


###############################################################################
### Distance Modulus

def apparent_to_absolute_magnitude(m, d_L):
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


# -------------------------------------------------------------------------

def absolute_to_apparent_magnitude(M, d_L):
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

# -------------------------------------------------------------------------

def distanceModulus_magnitude(distance):
    r"""Distance Modulus
    equation:  DM = 5 log10(d / 10)

    Arguments
    ---------
    distance: scalar, array
        in parsecs
        if Quantity, pass as distance.to_value('pc')

    Returns
    -------
    DM: scalar, array
        in magnitudes
        no units attached
    """

    return 5 * (np.log10(distance) - 1)
# /def


# -------------------------------------------------------------------------

def distanceModulus_distance(DM):
    r"""Distance Modulus
    equation:  DM = 5 log10(d / 10)
    d = 10^{\frac{DM}{5}+1}

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

    return np.power(10., np.divide(DM, 5.) + 1)
# /def


# -------------------------------------------------------------------------

def distanceModulus(arg, d2dm=True):
    r"""Distance Modulus
    equation:  DM = 5 log10(d / 10)
    d = 10^{\frac{DM}{5}+1}

    not as fast as calling distanceModulus_magnitude(distance) directly

    Arguments
    ---------
    arg: scalar, array
        either: distance (d) in pc (.value)
            or  DM in magnitudes (.value)
        determined by *d2dm*
    d2dm: bool
        if true: arg = d -> DM
           else: arg = DM -> d

    Returns
    -------
    DM or d: scalar, array
        .value
    """
    if d2dm:
        return distanceModulus_magnitude(arg)
    else:
        return distanceModulus_distance(arg)
# /def


###############################################################################
# Parallax

def parallax_angle(d):
    r"""compute parallax angle

    Arguments
    ---------
    d: pc
        distance
        1 AU = 0.000004848137 pc

    Returns
    -------
    angle: deg
        atan(1 AU / d [pc]) * pi * deg / 180 rad

    """
    return np.arctan(_AU_to_pc / d) * np.pi / 180
# /def


# -------------------------------------------------------------------------

def parallax_distance(p):
    r"""compute parallax distance

    Arguments
    ---------
    p: radian
        parallax angle

    Returns
    -------
    d: AU
        distance
        1 AU / tan(p [radian])

    """
    return 1 / np.tan(p)
# /def


# -------------------------------------------------------------------------

def parallax(arg, d2p=True):
    r"""parallax

    not as fast as calling parallax_angle(distance) directly

    Arguments
    ---------
    arg: scalar, array
        either: distance (d) in pc (.value)
            or  parallax_angle (p) in radians (.value)
        determined by *d2p*
    d2p: bool
        if true: arg = d -> p
           else: arg = p -> d

    Returns
    -------
    p or d: scalar, array
        .value
    """
    if d2p:
        return parallax_angle(arg)
    else:
        return parallax_distance(arg)
# /def


###############################################################################
# Angular Separation

def max_angular_separation(doff, dto):
    """
    doff: distance
        distance offset from coordinate
    dto: distance
        distance to original coordinate

    Returns
    -------
    angle: rad
        angular separation
    """
    return np.fabs(np.arctan(np.divide(doff, dto)))
# /def


# -------------------------------------------------------------------------
