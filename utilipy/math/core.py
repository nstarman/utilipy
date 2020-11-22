# -*- coding: utf-8 -*-

"""Math Core Functions."""

__author__ = "Nathaniel Starkman"


__all__ = [
    "quadrature",
    # quantity functions
    "as_quantity",
    "qsquare",
    "qnorm",
    "qarange",
]


##############################################################################
# IMPORTS

# BUILT-IN
import typing as T
import warnings

# THIRD PARTY
import numpy as np
from astropy.units import Quantity
from numpy.linalg import norm

##############################################################################
# IMPORTS

_NUMPY_VERSION = [
    int(v) for i, v in enumerate(np.__version__.split(".")) if i < 3
]
if (_NUMPY_VERSION[0] <= 1) and (_NUMPY_VERSION[1] <= 16):  # v1.16
    warnings.warn(
        (
            "Need to set the environment variable "
            "NUMPY_EXPERIMENTAL_ARRAY_FUNCTION=1"
        )
    )


###############################################################################
# CODE
###############################################################################


def quadrature(*args: T.Tuple[T.Sequence], axis: int = 0) -> T.Sequence:
    """Return arguments summed in quadrature.

    ::

        sqrt(sum(square(args), axis=axis))

    Parameters
    ----------
    args: Sequence
    axis: int
        the summation axis, default 0.

    Returns
    -------
    array-like

    """
    if len(args) == 0:
        raise ValueError
    if len(args) == 1:
        args = args[0]

    return np.sqrt(np.sum(np.square(args), axis=axis))


# /def


#####################################################################
# Quantity Functions


def as_quantity(arg):
    """Convert argument to a Quantity (or raise NotImplementedError).

    from :mod:`~astropy.utils`.

    Returns
    -------
    Quantity
        not copied, quantity subclasses passed through.

    Raises
    ------
    NotImplementedError
        if Quantity() fails

    """
    try:
        return Quantity(arg, copy=False, subok=True)
    except Exception:
        raise NotImplementedError


# /def

# -------------------------------------------------------------------


def qsquare(*args, **kw):
    """Quantity, Squared.

    Parameters
    ----------
    *args : Quantity
        passed, as tuple, to :func:`~as_quantity`
    **kw
        arguments into :func:`~numpy.square`

    Returns
    -------
    Quantity
        not copied, quantity subclasses passed through.

    Raises
    ------
    NotImplementedError
        if :func:`~as_quantity` fails

    """
    return np.square(as_quantity(args), **kw)


# /def

# -------------------------------------------------------------------


def qnorm(*args, **kw):
    """Quantity, Normed.

    Parameters
    ----------
    *args : Quantity
        passed, as tuple, to :func:`~as_quantity`
    **kw
        arguments into :func:`~numpy.linalg.norm`

    Returns
    -------
    Quantity
        not copied, quantity subclasses passed through.

    Raises
    ------
    NotImplementedError
        if :func:`~as_quantity` fails

    """
    return norm(as_quantity(args), **kw)


# /def


# -------------------------------------------------------------------


def qarange(start, stop, step, unit=None):
    """:func:`~numpy.arange` for Quantities."""
    if unit is None:
        unit = step.unit

    arng = np.arange(
        start.to_value(unit), stop.to_value(unit), step.to_value(unit)
    )

    return arng * unit


# /def


# -------------------------------------------------------------------


###############################################################################
# END
