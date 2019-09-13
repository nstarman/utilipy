#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : functions
# AUTHOR  : Nathaniel Starkman
# PROJECT : astronat
#
# ----------------------------------------------------------------------------
### Docstring and Metadata
r"""astronomy functions

TODO incorporate astropy cosmology
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### IMPORTS

## General
import numpy as np
from functools import wraps

## Custom Imports
from ..util.starkopy import units as u


###############################################################################
# Distance Modulus

@u.quantity_io(m=u.mag)
def apparent_to_absolute_magnitude(sc, m: u.mag, **kw) -> u.mag:
    """
    calculate the absolute magnitude
    M = m - 5 log10(d) + 5

    Parameters
    ----------
    sc: SkyCoord
        ** warning: check if skycoord frame centered on Earth
        gets sc.spherical.distance
    m: array_like
        apparent magnitude

    Returns
    -------
    M: ndarray
        absolute magnitudes
    """

    M = m - 5.0 * np.log10(sc.spherical.distance) + 5.0

    return M
# /def


@u.quantity_io(M=u.mag)
def absolute_to_apparent_magnitude(sc, M: u.mag, **kw) -> u.mag:
    """
    calculate the apparent magnitude
    m = M + 5 log10(d) - 5

    Parameters
    ----------
    M: array_like
        absolute magnitude
    sc: SkyCoord
        ** warning: check if skycoord frame centered on Earth
        gets sc.spherical.distance

    Returns
    -------
    m: ndarray
        apparent magnitudes
    """

    m = M + 5.0 * np.log10(sc.spherical.distance) - 5.0

    return m
# /def


@u.quantity_io()
def distanceModulus_magnitude(sc, **kw) -> u.mag:
    r"""distance modulus from distance in skycoord
    equation:  DM = 5 log10(d / 10) + A

    the skycoord already has the distance
    equivalent to
        sc.spherical.distance.distmod

    Arguments
    ---------
    sc: SkyCoord
        ** warning: check if skycoord frame centered on Earth

    Returns
    -------
    DM: scalar, array
        default units: u.mag

    # TODO
        A, obs
        skycoord frame. what if skycoord not centered at earth?
    """

    return sc.spherical.distance.distmod
# /def


@u.quantity_io()
def distanceModulus_distance(sc, **kw) -> u.pc:
    r"""distance from distance modulus in skycoord
    equation:  DM = 5 log10(d / 10) + A

    the skycoord already has the distance,
    equivalent to
        sc.spherical.distance

    Arguments
    ---------
    sc: SkyCoord
        ** warning: check if skycoord frame centered on Earth

    Returns
    -------
    DM: scalar, array
        default units: u.mag

    # TODO
        A, obs
        skycoord frame. what if skycoord not centered at earth?
    """

    return sc.spherical.distance
# /def


@u.quantity_io()
def distanceModulus(sc, d2dm=True, **kw):
    r"""Distance Modulus
    equation:  DM = 5 log10(d / 10) + A

    Arguments
    ---------
    sc: SkyCoord

    d2dm: bool
        if true: distance -> DM
           else: DM -> distance

    Returns
    -------
    DM or distance: scalar, array

    # TODO
        A, obs
    """
    if d2dm:
        distanceModulus_magnitude(sc)
    else:
        distanceModulus_distance(sc)
# /def


###############################################################################
# Parallax


@u.quantity_io()
def parallax_angle(sc, **kw) -> u.deg:
    r"""compute parallax angle from skycoord

    Arguments
    ---------
    sc: SkyCoord
        ** warning: check if skycoord frame centered on Earth

    Returns
    -------
    p: deg
        parallax angle
    """
    return np.arctan(1 * u.AU / sc.spherical.distance)
# /def


@u.quantity_io()
def parallax_distance(sc, **kw) -> u.pc:
    r"""compute distance from parallax angle

    Arguments
    ---------
    sc: SkyCoord
        ** warning: check if skycoord frame centered on Earth

    """
    return np.arctan(1 * u.AU / sc.spherical.distance)
    # return 1 * u.AU / np.tan(p)
# /def


def parallax(sc, d2p=True, **kw):
    r"""parallax

    Arguments
    ---------
    sc: SkyCoord
        ** warning: check if skycoord frame centered on Earth
    d2p: bool
        if true: arg = distance -> parallax_angle
           else: arg = parallax_angle -> distance

    Returns
    -------
    parallax_angle or distance: scalar, array
    """
    if d2p:
        return parallax_angle(sc)
    else:
        return parallax_distance(sc)
# /def


###############################################################################
# Angular Separation

@u.quantity_io()
def max_angular_separation(sc, doff: u.m, **kw):
    """
    doff: distance
        distance offset from coordinate
    dto: distance
        distance to original coordinate

    the maximum angular separation comes from movint at right angle from current position

    TODO support zero point
    """

    return np.fabs(np.arctan(np.divide(doff, sc.spherical.distance)))
# /def
