#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : select
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""Selection Functions

METHODS
-------
.box
.circle
.ellipse
.inRange
.ioRange
.outRange
"""

__author__ = "Nathaniel Starkman"

#############################################################################
### IMPORTS

## General
import numpy as np

## Project-Specific
from ..util.decorator.idx_decorator import idxDecorator
from ..util.decorator.dtype_decorator import ndarrayDecorator


#############################################################################
## Functions

# @ndarrayDecorator(inargs=[0, 1])  # ensuring x, rng are arrays
def _inRange(x, rng, lbi=True, ubi=False):
    """helper function for inRange

    Parameters
    ----------
    x   : array
        the array on which to test for membership in the range
        supports multiple dimension
    rng : array
        the range. (lower, upper)
        when applied to ND array, must match the number of rows
        ex : for x [NxM], rng must be [Nx2]
    lbi : bool  (default True)
        Lower Bound Inclusive, whether to be inclusive on the lower bound
    ubi : bool  (default False)
        Upper Bound Inclusive, whether to be inclusive on the upper bound

    Returns
    -------
    idx: bool array
        bool index array
        shape matches *x*

    Examples
    --------
    >> x = array([[ 0,  1],
                  [10, 11]])
    >> rng = [[0, 3], [9, 11]]
    >> _inRange(x, rng)
       array([[True, True s],
              [True, False]])
    """

    if len(x.shape) == 1:  # 1D

        if lbi and ubi:  # both true
            return (rng[0] <= x) & (x <= rng[1])
        elif lbi:  # only lbi is true
            return (rng[0] <= x) & (x < rng[1])
        elif ubi:  # only ubi is true
            return (rng[0] < x) & (x <= rng[1])
        else:  # neither true
            return (rng[0] < x) & (x < rng[1])

    else:  # ND

        # iterate over rows
        out = np.zeros_like(x, dtype=bool)
        for i, (row, lu) in enumerate(zip(x, rng)):
            out[i, :] = _inRange(row, lu, lbi=lbi, ubi=ubi)

        return out
# /def


# -----------------------------------------------------------------------------

@idxDecorator
def inRange(*args, rng=None, lbi=True, ubi=False):
    """multidimensional box selection

    Parameters
    ----------
    args : list
        either list of values along each dimension or list of values & bounds
        the input type depends on rng
    rng : None, list    (default None)
        if rng is not None:
            for domains x
            args = [[x1], [x2], ...]
            rng =   [1st [lower, upper],
                     2nd [lower, upper],
                     ...]
        else:
            args are the lists
            list of (x, [lower, upper])
    lbi : bool  (default True)
        Lower Bound Inclusive, whether to be inclusive on the lower bound
    ubi : bool  (default False)
        Upper Bound Inclusive, whether to be inclusive on the upper bound
    as_ind : bool  (default False)
        whether to return bool array or the indices (where(bool array == True))
        sets the default behavior for the wrapped fnction *func*


    Returns
    -------
    inrange : bool ndarray
        boolean array to select values in box selection

    upcoming
    --------
    allow lbi & rbi to be lists, matching args, for individual adjustment
    """
    # Compare
    # If args contains lists of [list, [low, up]]
    if rng is None:
        rowbool = np.array([_inRange(v, lu, lbi=lbi, ubi=ubi)
                            for v, lu in args])
        numtrues = len(args)

    # If args and low,up are in separate lists
    else:

        # if only one arg
        if len(args) == 1:
            # args = (args[0], )
            rng = (rng, )

        rowbool = np.array([_inRange(v, lu, lbi=lbi, ubi=ubi)
                            for v, lu in zip(args, rng)])
        numtrues = len(args)

    # now getting where all the dimensions are inside the bounds
    # collapses column to 1 row
    # check where all rows=True for each collapsed column
    allbool = rowbool.sum(axis=0)
    inrange = (allbool == numtrues)

    return inrange
# /def


# box as proxy to inRange
# inBox = inRange


# -----------------------------------------------------------------------------

@idxDecorator
def outRange(*args, rng=None, lbi=False, ubi=True):
    """multidimensional box exclusion
    equivelent to ~inRange

    Parameters
    ----------
    args : list
        either list of values along each dimension or list of values & bounds
        the input type depends on rng
    rng : None, list    (default None)
        if rng is not None:
            for domains x
            args = [[x1], [x2], ...]
            rng =   [1st [lower, upper],
                     2nd [lower, upper],
                     ...]
        else:
            args are the lists
            list of (x, [lower, upper]
    lbi : bool  (default False)
        Lower Bound Inclusive, whether to be inclusive on the lower bound
    ubi : bool  (default True)
        Upper Bound Inclusive, whether to be inclusive on the upper bound
    as_ind : bool  (default False)
        whether to return bool array or the indices (where(bool array == True))
        sets the default behavior for the wrapped fnction *func*

    Returns
    -------
    outrange : bool ndarray
        boolean array to select values outside box selection

    Planned
    -------
    allow lbi & rbi to be lists, matching args, for individual adjustment
    """
    outrange = ~inRange(*args, rng=rng, lbi=lbi, ubi=ubi)
    return outrange
# /def


# -----------------------------------------------------------------------------

@idxDecorator
def ioRange(incl=None, excl=None, rng=None):
    """Supports inRange and outRange

    Parameters
    ----------
    incl : list
        list of inRange args
    excl : list
        list of notinRange args
    rng : list
        concatenated list of (not)inRange rng
        must be in orgder of [*inRange rng, *notinRange rng]
    as_ind : bool  (default False)
        whether to return bool array or the indices (where(bool array == True))
        sets the default behavior for the wrapped fnction *func*

    Returns
    -------
    out : bool ndarray
        boolean array to select values inside / outside box selection
    """
    # Nothing passed. Raise error
    if (incl is None) & (excl is None):
        raise ValueError('incl and excl are None')
    # Only inclusion passed
    elif excl is None:
        out = inRange(*incl, rng=rng)
    # Only exclusion passed
    elif incl is None:
        out = outRange(*excl, rng=rng)
    # Both inclustion and exclusion
    else:
        inclrng = rng[:len(incl)] if rng is not None else None
        exclrng = rng[len(incl):] if rng is not None else None
        out = inRange(*incl, rng=inclrng) & outRange(*excl, rng=exclrng)

    return out
# /def


# -----------------------------------------------------------------------------

@idxDecorator
def ellipse(*x, x0=0., dx=1.):
    """elliptical selection of data in many dimensions

    sel = np.sqrt(((x - x0) / dx)**2 + ...) < 1

    Parameters
    ----------
    *x: m x (n, 1) arrays
    x0: scalar, (m, 1) array   (default = 0.)
        the center position of each x.
        can broadcast a scalar to apply to all
    dx: scalar, (m, 1) array   (default = 0.)
        the radius in each dimension
    as_ind : bool  (default False)
        whether to return bool array or the indices (where(bool array == True))
        sets the default behavior for the wrapped fnction *func*

    Returns
    -------
    sel: bool
        bool array selecting data w/in ellipse
    """

    shape = (len(x[0]), len(x))

    x0 = np.broadcast_to(x0, shape).T  # reshape x0 correctly
    dx = np.broadcast_to(dx, shape).T  # reshape x0 correctly

    arr = np.divide(np.subtract(x, x0), dx)

    return np.sqrt(np.sum(np.square(arr), axis=0)) < 1
# /def


# -----------------------------------------------------------------------------

@idxDecorator
def circle(*x, x0=0., radius=1.):
    """circular selection of data in many dimensions

    sel = np.sqrt(((x - x0) / radius)**2 + ...) < 1

    Parameters
    ----------
    *x: m x (n, 1) arrays
    x0: scalar, (m, 1) array   (default = 0.)
        the center position of each x.
        can broadcast a scalar to apply to all
    dx: scalar
        the radius
    as_ind : bool  (default False)
        whether to return bool array or the indices (where(bool array == True))
        sets the default behavior for the wrapped fnction *func*

    Returns
    -------
    sel: bool
        bool array selecting data w/in circle
    """
    return ellipse(*x, x0=x0, dx=radius)
# /def

#############################################################################
### END
