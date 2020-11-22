# -*- coding: utf-8 -*-

"""Selection Functions.

Examples
--------
do some examples here

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "inRange",
    "outRange",
    "ioRange",
    "ellipse",
    "circle",
]


#############################################################################
# IMPORTS

# BUILT-IN
import typing as T

# THIRD PARTY
import numpy as np

# PROJECT-SPECIFIC
from .decorators import idxDecorator
from utilipy.utils.typing import EllipsisType

#############################################################################
# Functions


def _inRange(
    x: np.array, rng: T.Sequence, lbi: bool = True, ubi: bool = False
) -> np.array:
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
    >>> x = np.array([[ 0,  1],
    ...               [10, 11]])
    >>> rng = [[0, 3], [9, 11]]
    >>> _inRange(x, rng) # doctest: +SKIP
    array([[ True,  True],
           [ True, False]])

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


@idxDecorator(_doc_style="numpy")
def inRange(
    *args: T.Union[np.array, T.Sequence],
    rng: T.Union[T.Sequence, EllipsisType] = Ellipsis,
    lbi: bool = True,
    ubi: bool = False
) -> np.array:
    """Multidimensional box selection.

    Parameters
    ----------
    args : Sequence
        list of values along each dimension
        must be the same length
        can be same-shaped ND arrays, each treated as a series of rows.
    rng : Sequence or Ellipsis, optional
        (default Ellipsis)
        the domain for each argument in `args`::

            args = [[x1], [x2], ...]
            rng =   [1st [lower, upper],
                     2nd [lower, upper],
                     ...]

        if each 'xn' is multidimensional
    lbi : bool, optional
        (default True)
        Lower Bound Inclusive, whether to be inclusive on the lower bound
    ubi : bool, optional
        (default False)
        Upper Bound Inclusive, whether to be inclusive on the upper bound
    as_ind : bool, optional
        (default False)
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
        >>> inRange(x, y, rng=[[0, 3], [10, 15]]) # doctest: +SKIP
        array([ True,  True,  True, False, False])

    multidimensional arg:

        >>> x = np.array([[ 0,  1], [10, 11]])
        >>> rng = [[0, 3], [9, 11]]
        >>> inRange(x, rng=rng) # doctest: +SKIP
        array([[ True,  True],
               [ True, False]])

    .. todo::

        allow lbi & rbi to be lists, matching args, for individual adjustment

    """
    # if only one arg
    if len(args) == 1:
        rng = (rng,)

    rowbool = np.array(
        [_inRange(v, lu, lbi=lbi, ubi=ubi) for v, lu in zip(args, rng)]
    )

    numtrues = len(args)

    # now getting where all the dimensions are inside the bounds
    # collapses column to 1 row
    # check where all rows=True for each collapsed column
    allbool = rowbool.sum(axis=0)
    inrange = allbool == numtrues

    return inrange


# /def


# -----------------------------------------------------------------------------


@idxDecorator(_doc_style="numpy")
def outRange(
    *args: T.Union[np.array, T.Sequence],
    rng: T.Union[T.Sequence, EllipsisType] = Ellipsis,
    lbi: bool = True,
    ubi: bool = False
) -> np.array:
    """Multidimensional box exclusion.

    equivelent to ~inRange

    Parameters
    ----------
    args : Sequence
        either list of values along each dimension or list of values & bounds
        the input type depends on `rng`
    rng : Ellipsis or Sequence, optional
        (default Ellipsis)
        if rng is not Ellipsis::

            args = [[x1], [x2], ...]
            rng =   [1st [lower, upper],
                     2nd [lower, upper],
                     ...]

        else, args are the list of (x, [lower bound, upper. bound])
    lbi : bool, optional
        (default False)
        Lower Bound Inclusive, whether to be inclusive on the lower bound
    ubi : bool, optional
        (default True)
        Upper Bound Inclusive, whether to be inclusive on the upper bound
    as_ind : bool, optional
        (default False)
        whether to return bool array or the indices (where(bool array == True))
        sets the default behavior for the wrapped fnction *func*

    Returns
    -------
    outrange : ndarray of bool or ndarray of int
        boolean array to select values outside box selection
        if as_ind, then index array of same

    .. todo::

        allow `lbi` & `rbi` to be lists, matching `args`, for indiv adjustment

    """
    return ~inRange(*args, rng=rng, lbi=lbi, ubi=ubi)


# /def


# -----------------------------------------------------------------------------


@idxDecorator(_doc_style="numpy")
def ioRange(
    incl: T.Union[None, tuple, np.array] = None,
    excl: T.Union[None, tuple, np.array] = None,
    rng: T.Union[T.Sequence, EllipsisType] = Ellipsis,
) -> np.array:
    """Supports inRange and outRange.

    Parameters
    ----------
    incl : array_like, optional
        args into `inRange`
        must be a tuple if many args, not a tuple else
    excl : array_like, optional
        args into `outRange`
        must be a tuple if many args, not a tuple else
    rng : Sequence or Ellipsis, optional
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
        raise ValueError("incl and excl are None")
    # Only inclusion passed
    elif excl is None:
        if isinstance(incl, tuple):
            out = inRange(*incl, rng=rng)
        else:
            out = inRange(incl, rng=rng)
    # Only exclusion passed
    elif incl is None:
        if isinstance(excl, tuple):
            out = outRange(*excl, rng=rng)
        else:
            out = outRange(excl, rng=rng)
    # Both inclusion and exclusion
    else:
        if isinstance(incl, tuple):
            inclrng = rng[: len(incl)] if rng is not ... else ...
            out = inRange(*incl, rng=inclrng)
        else:
            inclrng = rng[: np.shape(incl)[0] - 1] if rng is not ... else ...
            if len(inclrng) == 1:
                inclrng = inclrng[0]
            out = inRange(incl, rng=inclrng)

        if isinstance(excl, tuple):
            exclrng = rng[len(excl) :] if rng is not ... else ...
            out &= outRange(*excl, rng=exclrng)
        else:
            exclrng = rng[np.shape(excl)[0] - 1 :] if rng is not ... else ...
            if len(exclrng) == 1:
                exclrng = exclrng[0]
            out &= outRange(excl, rng=exclrng)

    return out


# /def


# -----------------------------------------------------------------------------


@idxDecorator(_doc_style="numpy")
def ellipse(
    *x: T.Union[np.array, T.Sequence],
    x0: T.Union[float, T.Sequence] = 0.0,
    dx: T.Union[float, T.Sequence] = 1.0
) -> np.array:
    r"""Elliptical selection of data in many dimensions.

    Supports selection with variable center and radius::

        np.sum((x[i] - x0[i]) / dx[i])^2) < 1^2

    Parameters
    ----------
    x: m x (n, 1) array_like
        values along each dimension
    x0: scalar or (m, 1) array, optional
        (default = 0.)
        the center position of each x.
        can broadcast a scalar to apply to all
    dx: scalar or (m, 1) array, optional
        (default = 0.)
        the radius in each dimension

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


@idxDecorator(_doc_style="numpy")
def circle(
    *x: T.Union[np.array, T.Sequence],
    x0: T.Union[float, T.Sequence] = 0.0,
    radius: T.Union[float, T.Sequence] = 1.0
) -> np.array:
    """Circular selection of data in many dimensions.

    Elliptical selection with fixed radius::

        np.sum((x[i] - x0[i]) / radius)^2) < 1^2

    where the summation is over the dimensions.

    Parameters
    ----------
    x : array_like
        shape (m x (n, 1))
        values along each dimension
    x0 : array_like, optional
        scalar or (m, 1) array
        the center position of each x, [default 0.]
        can broadcast a scalar to apply to all
    radius : float, optional
        the radius

    Returns
    -------
    sel : array_like of bool
        bool array selecting data within circle
        if as_ind is True, then array_like of indices

    """
    return ellipse(*x, x0=x0, dx=radius)


# /def

#############################################################################
# END
