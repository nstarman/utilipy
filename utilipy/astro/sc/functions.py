#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : functions
# PROJECT : astronat
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Astronomy functions.

TODO
----
incorporate astropy cosmology

"""

__author__ = "Nathaniel Starkman"

##############################################################################
# IMPORTS

# General
import numpy as np

# Custom Imports
from ...units import (
    quantity_io,
    get_physical_type,
    rad as RAD,
    deg as DEG,
    pc as PC,
    mag as MAG,
    AU,
    m as METER,
)


###############################################################################
# Distance Modulus


@quantity_io(m=MAG)
def apparent_to_absolute_magnitude(sc, m: MAG, **kw) -> MAG:
    """Calculate absolute magnitude.

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
    M: array_like
        absolute magnitudes

    """
    M = m - 5.0 * np.log10(sc.spherical.distance) + 5.0
    return M


# /def


@quantity_io(M=MAG)
def absolute_to_apparent_magnitude(sc, M: MAG, **kw) -> MAG:
    """Calculate apparent magnitude.

        m = M + 5 log10(d) - 5

    Parameters
    ----------
    M: array_like
        absolute magnitude
    sc: SkyCoord
        gets sc.spherical.distance
        .. warning:: check if skycoord frame centered on Earth

    Returns
    -------
    m: ndarray
        apparent magnitudes

    """
    m = M + 5.0 * np.log10(sc.spherical.distance) - 5.0
    return m


# /def


@quantity_io()
def distanceModulus_magnitude(sc, **kw) -> MAG:
    """Distance modulus from distance in Skycoord.

        DM = 5 log10(d / 10) + A

    the Skycoord already has the distance
    equivalent to `sc.spherical.distance.distmod`

    Parameters
    ----------
    sc: SkyCoord
        .. warning:: check if Skycoord frame centered on Earth

    Returns
    -------
    DM: scalar, array
        default units: MAG

    """
    return sc.spherical.distance.distmod


# /def


@quantity_io()
def distanceModulus_distance(sc, **kw) -> PC:
    """Distance from distance modulus in Skycoord.

        DM = 5 log10(d / 10) + A

    the Skycoord already has the distance,
    equivalent to `sc.spherical.distance`

    Parameters
    ----------
    sc: SkyCoord
        .. warning:: check if Skycoord frame centered on Earth

    Returns
    -------
    DM: scalar, array
        default units u.mag

    """
    return sc.spherical.distance


# /def


@quantity_io()
def distanceModulus(sc, d2dm=True, **kw):
    """Distance Modulus.

        DM = 5 log10(d / 10) + A

    Parameters
    ----------
    sc: SkyCoord

    d2dm: bool
        if true: distance -> DM
           else: DM -> distance

    Returns
    -------
    DM or distance: scalar, array

    TODO
    ----
    A, obs

    """
    if d2dm:
        distanceModulus_magnitude(sc)
    else:
        distanceModulus_distance(sc)


# /def


###############################################################################
# Parallax


@quantity_io()
def parallax_angle(sc, **kw) -> DEG:
    """Compute parallax angle from skycoord.

    Parameters
    ----------
    sc: SkyCoord
        ** warning: check if skycoord frame centered on Earth

    Returns
    -------
    p: deg
        parallax angle

    """
    return np.arctan(1 * AU / sc.spherical.distance)


# /def


@quantity_io()
def parallax_distance(sc, **kw) -> PC:
    """Compute distance from parallax angle.

    Parameters
    ----------
    sc: SkyCoord
        .. warning:: check if skycoord frame centered on Earth

    """
    return np.arctan(1 * AU / sc.spherical.distance)
    # return 1 * AU / np.tan(p)


# /def


def parallax(sc, d2p=True, **kw):
    """Parallax.

    Parameters
    ----------
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


@quantity_io()
def max_angular_separation(sc, doff: METER, **kw):
    """Maximum angular separation.

    doff: distance
        distance offset from coordinate
    dto: distance
        distance to original coordinate

    the maximum angular separation comes from movint at right angle from current position

    TODO
    ----
    support zero point
    """

    return np.fabs(np.arctan(np.divide(doff, sc.spherical.distance)))


# /def
