# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : functions
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Astronomy functions.

TODO incorporate astropy cosmology

"""

__author__ = "Nathaniel Starkman"

##############################################################################
# IMPORTS

# GENERAL
from typing import Any, Union
import numpy as np

# CUSTOM IMPORTS
from ...units import (
    quantity_io,
    get_physical_type,
    rad as RAD,
    deg as DEG,
    pc as PC,
    mag as MAG,
    AU,
)


##############################################################################
# Angular Distance


@quantity_io()
def angular_distance_on_sky(lon1: DEG, lat1: DEG, lon2: DEG, lat2: DEG) -> Any:
    r"""Angular distance on-sky.

    for longitude, \alpha, and latitude, \delta,

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

    Notes
    -----
    for reference:
    * ICRS: lon=ra, lat=dec

    """
    latcomp = np.sin(lat1) * np.sin(lat2)  # latitude component
    loncomp = (
        np.cos(lat1) * np.cos(lat2) * np.cos(lon1 - lon2)
    )  # longitude component

    res = np.arccos(latcomp + loncomp)

    return res


# /def


##############################################################################
# Distance Modulus


@quantity_io(m=MAG, d_L="distance")
def apparent_to_absolute_magnitude(m: MAG, d_L: PC, **kw) -> Any:
    """Convert apparent to absolute magnitude.

    calculate the absolute magnitude::

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


@quantity_io(M=MAG, d_L="distance")
def absolute_to_apparent_magnitude(M: MAG, d_L: PC, **kw) -> Any:
    """Convert absolute to apparent magnitude.

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


@quantity_io(
    d="length", A=MAG, assume_annotation_units=True, assumed_units={"A": MAG},
)
def distanceModulus_magnitude(d: PC, A=0 * MAG, obs=True, **kw) -> Any:
    r"""Distance Modulus distance to magnitude.

    .. math::

        DM = 5 log10(d / 10) + A

    Parameters
    ----------
    d: scalar, array, Quantity
        distance
        no units => parsecs
    A: array_like
        (default :math:`0 \rm{mag}`)
        extinction in magnitudes
    obs: bool
        (default True goes to :math:`mobs - M`)
        whether to return (:math:`mobs - M`) or (:math:`mtrue - M`)
        .. note:: don't change unless specifically required

    Returns
    -------
    DM: scalar, array
        default units: MAG

    Notes
    -----
    :math:`mtrue - M = 5 log10(d / 10)`
    if there is line-of-sight extinction
    :math:`mobs = mtrue + A`
    :math:`mobs - M = 5 log10(d / 10) + A`
    :math:`true - M = 5 log10(d / 10) - A`

    """
    if not obs:
        A *= -1

    return (5 * MAG) * (np.log10(d.to_value(PC)) - 1) + A


# /def


@quantity_io(DM=MAG, assume_annotation_units=True)
def distanceModulus_distance(DM: MAG, **kw) -> Any:
    r"""Distance Modulus.

    .. math::

        DM = 5 log10(d / 10) -> d = 10^{\frac{DM}{5}+1}

    Parameters
    ----------
    DM: scalar, array
        in magnitudes
        if Quantity, pass as distance.to_value('mag')

    Returns
    -------
    distance: scalar, array
        in parsecs
        no units attached

    """
    return np.power(10.0, np.divide(DM, 5.0 * MAG) + 1) * PC


# /def


# TODO assume_annotation_units = T/F?
@quantity_io(
    arg=("length", MAG),
    A=MAG,
    assume_annotation_units=True,
    assumed_units={"A": MAG},
)
def distanceModulus(arg, A=0 * MAG, obs=True, **kw) -> Any:
    r"""Distance Modulus.

    .. math::

        DM = 5 log10(d / 10) + A

    Parameters
    ----------
    d: array_like, optional
        no units to parsecs
    A: Quantity array_like, optional
        extinction in magnitudes
        (default :math:`0 \rm{mag}`)
    obs: bool
        (default True goes to :math:`mobs - M`)
        whether to return (:math:`mobs - M`) or (:math:`mtrue - M`)
        .. note:: don't change unless specifically required

    Returns
    -------
    DM: Quantity array_like
        default MAG

    Notes
    -----
    :math:`mtrue - M = 5 log10(d / 10)`
    if there is line-of-sight extinction
    :math:`mobs = mtrue + A`
    :math:`mobs - M = 5 log10(d / 10) + A`
    :math:`true - M = 5 log10(d / 10) - A`

    """
    if get_physical_type(arg) == "length":
        if not obs:
            A *= -1

        return (5 * MAG) * (np.log10(arg.to_value(PC)) - 1) + A
        # return distanceModulus_magnitude(arg, A=A, obs=obs,
        #                                  _skip_decorator=True)

    else:
        return np.power(10.0, np.divide(arg, 5.0 * MAG) + 1) * PC
        # return distanceModulus_distance(arg, _skip_decorator=True)


# /def


##############################################################################
# Parallax


@quantity_io(d="length")
def parallax_angle(d: PC, **kw) -> Any:
    """Compute parallax angle."""
    return np.arctan(1 * AU / d)


# /def

# --------------------------------------------------------------------------


@quantity_io(p="angle")
def parallax_distance(p: DEG, **kw) -> Any:
    """Compute parallax distance."""
    return 1 * AU / np.tan(p)


# /def

# --------------------------------------------------------------------------


@quantity_io(arg=("angle", "length"))
def parallax(arg, **kw) -> Any:
    """Parallax."""
    if get_physical_type(arg) == "angle":
        return parallax_distance(arg)
    elif get_physical_type(arg) == "length":
        return parallax_angle(arg)
    else:
        raise TypeError(f"{arg} must have units of distance or angle")


# /def


##############################################################################
# Angular Separation


@quantity_io(doff="length", dto="length")
def max_angular_separation(doff, dto, **kw) -> Any:
    """Maximum angular separation.

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
    return np.fabs(np.arctan(np.divide(doff, dto))) * RAD


# /def


##############################################################################
# Docs
