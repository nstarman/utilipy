# -*- coding: utf-8 -*-

"""Math Core Functions."""

__author__ = "Nathaniel Starkman"


__all__ = [
    "quadrature",
]


##############################################################################
# IMPORTS

# BUILT-IN

import typing as T


# THIRD PARTY

import numpy as np


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


# ----------------------------------------------------------------------------


# def logsumexp(a: Sequence, axis: int = 0) -> Sequence:
#     """Logsumexp.

#     Parameters
#     ----------
#     a : array-like
#     axis : int
#         the summation axis

#     Returns
#     -------
#     array-like

#     References
#     ----------
#     code modified from galpy

#     """
#     minarr = np.amax(a, axis=axis)

#     if axis == 1:
#         minarr = np.reshape(minarr, (a.shape[0], 1))
#     if axis == 0:
#         minminarr = np.tile(minarr, (a.shape[0], 1))
#     elif axis == 1:
#         minminarr = np.tile(minarr, (1, a.shape[1]))
#     elif axis is None:
#         minminarr = np.tile(minarr, a.shape)
#     else:
#         raise NotImplementedError("logsumexp' not implemented for axis > 2")

#     if axis == 1:
#         minarr = np.reshape(minarr, (a.shape[0]))

#     return minarr + np.log(np.sum(np.exp(a - minminarr), axis=axis))


# /def


###############################################################################
# END
