# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : select
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Selection Functions.

Routine Listings
----------------
- box
- circle
- ellipse
- inRange
- ioRange
- outRange

Examples
--------
do some examples here

TODO
----
more tests for ND arrays as inputs

"""

#############################################################################
# IMPORTS

# General
import numpy as np

# Project-Specific
from ..util.decorators import idxDecorator, ndarrayDecorator


#############################################################################
# Functions

def _inRange(x, rng, lbi=True, ubi=False):
    """`inRange` helper function.

    Parameters
    ----------
    x : array_like
        the array on which to test for membership in the range
        supports multiple dimension
    rng : list
        the range (lower, upper)
        when applied to ND array, must match the number of rows
        ex : for x [NxM], rng must be [Nx2]
    lbi : bool
        (default True)
        Lower Bound Inclusive, whether to be inclusive on the lower bound
    ubi : bool
        (default False)
        Upper Bound Inclusive, whether to be inclusive on the upper bound

    Returns
    -------
    idx: bool array
        bool index array
        shape matches `x`

    Examples
    --------
    >>> x = array([[ 0,  1],
    ...            [10, 11]])
    >>> rng = [[0, 3], [9, 11]]
    >>> _inRange(x, rng)
    array([[True, True], [True, False]])

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

@idxDecorator()
def inRange(*args, rng=Ellipsis, lbi=True, ubi=False):
    """Multidimensional box selection.

    Parameters
    ----------
    args : list
        list of values along each dimension
        must be the same length
    rng : list
        (default Ellipsis)
        the domain for each argument in `args`::

            args = [[x1], [x2], ...]
            rng =   [1st [lower, upper],
                     2nd [lower, upper],
                     ...]
    lbi : bool
        (default True)
        Lower Bound Inclusive, whether to be inclusive on the lower bound
    ubi : bool
        (default False)
        Upper Bound Inclusive, whether to be inclusive on the upper bound
    as_ind : bool  (default False)
        whether to return bool array or the indices (where(bool array == True))
        sets the default behavior for the wrapped fnction *func*

    Returns
    -------
    inrange : bool ndarray
        boolean array to select values in box selection

    See Also
    --------
    outRange :  multidimensional box exclusion
    ioRange : `inRange` and `outRange` combined

    Examples
    --------
    list of args:

    >>> x = np.arange(5)
    >>> y = np.arange(5) + 10
    >>> inRange(x, y, rng=[[0, 3], [10, 15]])
    array([ True,  True,  True, False, False])

    multidimensional arg:

    >>> x = array([[ 0,  1], [10, 11]])
    >>> rng = [[0, 3], [9, 11]]
    >>> inRange(x, rng=rng)
    array([[True, True ], [True, False]])

    TODO
    ----
    allow lbi & rbi to be lists, matching args, for individual adjustment

    """
    if rng is None:
        raise ValueError()

    # if only one arg
    if len(args) == 1:
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

@idxDecorator()
def outRange(*args, rng=None, lbi=False, ubi=True):
    """Multidimensional box exclusion.

    equivelent to ~inRange

    Parameters
    ----------
    args : list
        either list of values along each dimension or list of values & bounds
        the input type depends on `rng`
    rng : None or list
        (default None)
        if rng is not None::

            args = [[x1], [x2], ...]
            rng =   [1st [lower, upper],
                     2nd [lower, upper],
                     ...]

        else, args are the list of (x, [lower bound, upper. bound])
    lbi : bool
        (default False)
        Lower Bound Inclusive, whether to be inclusive on the lower bound
    ubi : bool
        (default True)
        Upper Bound Inclusive, whether to be inclusive on the upper bound
    as_ind : bool
        (default False)
        whether to return bool array or the indices (where(bool array == True))
        sets the default behavior for the wrapped fnction *func*

    Returns
    -------
    outrange : ndarray of bool or ndarray of int
        boolean array to select values outside box selection
        if as_ind, then index array of same

    TODO
    ----
    allow `lbi` & `rbi` to be lists, matching `args`, for individual adjustment

    """
    outrange = ~inRange(*args, rng=rng, lbi=lbi, ubi=ubi)
    return outrange
# /def


# -----------------------------------------------------------------------------

@idxDecorator
def ioRange(incl=None, excl=None, rng=None):
    """Supports inRange and outRange.

    Parameters
    ----------
    incl : array_like
        args into `inRange`
    excl : array_like
        args into `outRange`
    rng : array_like
        concatenated list of (in)outRange rng
        must be in orgder of [inRange rng, outRange rng]
    as_ind : bool
        (default False)
        whether to return bool array or the indices (``where(bool array == True``))
        sets the default behavior for the wrapped function

    Returns
    -------
    out : ndarray of bool or ndarray of ints
        boolean array to select values inside / outside box selection
        if as_ind, then index array of same

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
    r"""Elliptical selection of data in many dimensions.

    Supports selection with variable center and radius::

        np.sum((x[i] - x0[i]) / dx[i])^2) < 1^2

    Parameters
    ----------
    x: m x (n, 1) array_like
        values along each dimension
    x0: scalar or (m, 1) array
        (default = 0.)
        the center position of each x.
        can broadcast a scalar to apply to all
    dx: scalar or (m, 1) array
        (default = 0.)
        the radius in each dimension
    as_ind : bool
        (default False)
        whether to return bool array or the indices (``where(bool array == True)``)
        sets the default behavior for the wrapped fnction *func*

    Returns
    -------
    sel: array_like of bool
        bool array selecting data w/in ellipse
        if as_ind is True, then array_like of indices

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
    """Circular selection of data in many dimensions.

    Elliptical selection with fixed radius::

        np.sum((x[i] - x0[i]) / radius)^2) < 1^2

    Parameters
    ----------
    x: (m x (n, 1)) arrays
        values along each dimension
    x0: scalar, (m, 1) array
        (default = 0.)
        the center position of each x.
        can broadcast a scalar to apply to all
    dx: scalar
        the radius
    as_ind : bool  (default False)
        whether to return bool array or the indices (``where(bool array == True``))
        sets the default behavior for the wrapped function

    Returns
    -------
    sel: array_like of bool
        bool array selecting data w/in circle
        if as_ind is True, then array_like of indices

    See Also
    --------
    ellipse : elliptical selection

    """
    return ellipse(*x, x0=x0, dx=radius)
# /def

#############################################################################
# END
