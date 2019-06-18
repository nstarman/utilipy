#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : domain factory
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""domain factory
factory function for making domain-restricting functions
"""

__author__ = "Nathaniel Starkman"


#############################################################################
# IMPORTS

import numpy as np


#############################################################################
# CODE

def domain_factory(low, up, roof=False, getnp=False, inf2nan=True):
    r"""

    NAME:

        domain_factory

    PURPOSE:

        factory function for making domain-restricting functions
        it moves everything into the domain
        **note for half-open domains
            ex: [0, infty) will move everything <0 => infty
            Must always be domain_factory(finite, +/- inf, ...)

    INPUT:
        low: <float> lower bound
        up:  <float> upper bound
        roof: <bool>  False -> [floor, roof), True -> (floor, roof]
        getnp: <bool> whether to return # of periods from the domain

    OUTPUT:

        domain_adj: function

    HISTORY:

        2018-03-02 - Written - Nathaniel Starkman (UofT)

    TODO:
        support half-open domains:
            ex: [0, infty) or (-infty, 0]

    """

    def domain_adj(x, roof=roof, numT=0):
        r"""
        x:: angle
        roof:: <bool> False -> [floor, roof), True -> (floor, roof]
        numT:: # of periods from the domain
        """
        dm = np.divmod((x - low), (up - low))
        out = dm[1] + low  # get into correct domain
        if roof:
            try:  # numpy array
                out[out == -low] = up
            except TypeError:  # not numpy
                if out == low:
                    out = up

        if inf2nan:
            try:
                out[np.isinf(out)] = np.NaN
            except TypeError:  # b/c doesn't work on scalars :(
                out = np.NaN if np.isinf(out) else out

        if getnp:
            return out, dm[0]
        else:
            return out + np.nan_to_num((up - low) * numT)

    return domain_adj
# /def

#############################################################################
# DONE
