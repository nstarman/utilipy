# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : math
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Math."""

__author__ = "Nathaniel Starkman"

###############################################################################
# IMPORTS

# General
import numpy as np

# Project-Specific


###############################################################################
# CODE

def quadrature(*args, axis=0):
    """Return arguments summed in quadrature."""
    if len(args) == 0:
        raise ValueError
    if len(args) == 1:
        args = args[0]
    return np.sqrt(np.sum(np.square(args), axis=axis))
# /def


# ----------------------------------------------------------------------------


def logsumexp(arr, axis=0):
    """Logsumexp.

    Faster?
    code modified from galpy

    """
    minarr = np.amax(arr, axis=axis)
    if axis == 1:
        minarr = np.reshape(minarr, (arr.shape[0], 1))
    if axis == 0:
        minminarr = np.tile(minarr, (arr.shape[0], 1))
    elif axis == 1:
        minminarr = np.tile(minarr, (1, arr.shape[1]))
    elif axis is None:
        minminarr = np.tile(minarr, arr.shape)
    else:
        raise NotImplementedError(
            "logsumexp' not implemented for axis > 2")
    if axis == 1:
        minarr = np.reshape(minarr, (arr.shape[0]))
    return minarr + np.log(np.sum(np.exp(arr - minminarr), axis=axis))
# /def


###############################################################################
# END
