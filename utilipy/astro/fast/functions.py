"""fast astro functions."""

__author__ = "Nathaniel Starkman"

##############################################################################
# IMPORTS

# GENERAL
from typing import Union, Sequence
import numpy as np

# PROJECT - SPECIFIC
from ...constants.values import AU_to_pc as _AU_to_pc, pc_to_AU as _pc_to_AU


###############################################################################
# Distance Conversion


def AU_to_pc(AU: Union[np.array, float]) -> Union[np.array, float]:
    """Convert AU to pc."""
    return AU * _AU_to_pc


# /def


def pc_from_AU(AU: Union[np.array, float]) -> Union[np.array, float]:
    """Convert AU to pc."""
    return AU * _AU_to_pc


# /def


# -------------------------------------------------------------------------


def AU_from_pc(pc: Union[np.array, float]) -> Union[np.array, float]:
    """Convert pc to AU."""
    return pc * _pc_to_AU


# /def


def pc_to_AU(pc: Union[np.array, float]) -> Union[np.array, float]:
    """Convert pc to AU."""
    return pc * _pc_to_AU


# /def


###############################################################################
# Distance Modulus


def apparent_to_absolute_magnitude(m: Sequence, d_L: Sequence) -> Sequence:
    """Calculate the absolute magnitude.

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


def absolute_to_apparent_magnitude(M: Sequence, d_L: Sequence) -> Sequence:
    """Calculate the apparent magnitude.

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


def distanceModulus_magnitude(distance: Sequence) -> Sequence:
    """Distance Modulus.

        DM = 5 log10(d / 10)

    Parameters
    ----------
    distance: array_like
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


def distanceModulus_distance(DM: Sequence) -> Sequence:
    r"""Distance Modulus.

    ..math:

        DM = 5 log10(d / 10)
        d = 10^{\frac{DM}{5}+1}

    Parameters
    ----------
    DM: array_like
        in magnitudes
        if Quantity, pass as distance.to_value('mag')

    Returns
    -------
    distance: scalar, array
        in parsecs
        no units attached

    """
    return np.power(10.0, np.divide(DM, 5.0) + 1)


# /def


# -------------------------------------------------------------------------


def distanceModulus(arg: Sequence, d2dm: bool = True) -> Sequence:
    r"""Distance Modulus.

    ..math::

        DM = 5 log10(d / 10) \\
        d = 10^{\frac{DM}{5}+1}

    not as fast as calling distanceModulus_magnitude(distance) directly

    Parameters
    ----------
    arg: array_like
        either distance (d) in pc (.value) or  DM in magnitudes (.value)
        determined by `d2dm`
    d2dm: bool
        if true arg = d -> D
        else arg = DM -> d

    Returns
    -------
    DM or d: scalar, array
        .value

    """
    if d2dm:
        return distanceModulus_magnitude(arg)
    return distanceModulus_distance(arg)


# /def


###############################################################################
# Parallax


def parallax_angle(d: Sequence) -> Sequence:
    r"""Compute parallax angle.

    Parameters
    ----------
    d: array_like
        distance in pc
        1 AU = 0.000004848137 pc

    Returns
    -------
    angle: deg
        atan(1 AU / d [pc]) * pi * deg / 180 rad

    """
    return np.arctan(_AU_to_pc / d) * np.pi / 180


# /def


# -------------------------------------------------------------------------


def parallax_distance(p: Sequence) -> Sequence:
    r"""Compute parallax distance.

    Parameters
    ----------
    p: array_like
        radian
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


def parallax(arg: Sequence, d2p: bool = True) -> Sequence:
    r"""Parallax.

    Not as fast as calling parallax_angle(distance) directly

    Parameters
    ----------
    arg: array_like
        either distance (d) in pc (.value)
        or  parallax_angle (p) in radians (.value)
        determined by `d2p`
    d2p: bool
        if true arg = d -> p
        else arg = p -> d

    Returns
    -------
    p or d: scalar, array
        .value

    """
    if d2p:
        return parallax_angle(arg)
    return parallax_distance(arg)


# /def


###############################################################################
# Angular Separation


def max_angular_separation(doff: Sequence, dto: Sequence) -> Sequence:
    """Maximum angular separation.

    doff: distance
        distance offset from coordinate
    dto: distance
        distance to original coordinate

    Returns
    -------
    angle: float
        in radians
        angular separation

    """
    return np.fabs(np.arctan(np.divide(doff, dto)))


# /def


###############################################################################
# END
