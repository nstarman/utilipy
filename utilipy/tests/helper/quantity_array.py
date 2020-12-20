# -*- coding: utf-8 -*-

"""PDB and close-to-zero safe element-wise |Quantity| array comparisons.

The Astropy funciton :func:`~astropy.tests.helper.quantity_allclose` has
a few shortcomings:

    - It fails if the argument `a` and `b` are/close to zero
    - pdb diagnostics when the units don't match are really hard

"""

__all__ = [
    "eltwise_quantity_isclose",
    "eltwise_quantity_allclose",
    "eltwise_assert_quantity_isclose",
    "eltwise_assert_quantity_allclose",
]


##############################################################################
# IMPORTS

# BUILT-IN
import typing as T
from itertools import zip_longest

# THIRD PARTY
import astropy.units as u
import numpy as np
from astropy.units.quantity import (
    _unquantify_allclose_arguments as _unquantify,
)

##############################################################################
# PARAMETERS

QuantityType = T.TypeVar("QuantityType", bound=u.Quantity)

##############################################################################
# CODE
##############################################################################


# TODO support argument kwargs
def eltwise_quantity_isclose(
    a,
    b,
    rtol=1e-15,
    atol=None,
    equal_nan=False,
    wrap: T.Union[None, T.Tuple[int, QuantityType]] = None,
):
    """Returns True if two arrays are element-wise equal within a tolerance.

    This is a |Quantity|-aware version of :func:`~numpy.allclose`,
    modified from :mod:`~astropy` to be easier for PDB debugging.

    .. warning::

        This function should only be used when setting up testing.
        Use :func:`~astropy.units.allclose` or
        :func:`~astropy.tests.helper.quantity_allclose`.

    Parameters
    ----------
    wrap : T.Tuple[int, QuantityType], optional

    """
    # Splitting the comparison into a for-loop allows for element-wise
    # comparisons and prevents dropping into sub-functions so we stay in this
    # namespace when in PDB.
    try:
        alen = len(a)
    except TypeError:  # scalar
        a = [a]
        alen = 1

    try:
        blen = len(b)
    except TypeError:  # scalar
        b = [b]
        blen = 1

    assert alen == blen

    try:
        len(rtol)
    except TypeError:  # scalar
        rtol = np.broadcast_to(rtol, blen, subok=True)

    try:
        len(atol)
    except TypeError:  # scalar
        atol = np.broadcast_to(atol, blen, subok=True)

    wrap = wrap if wrap is not None else [wrap]

    close = []
    for x, y, rt, at, wrp in zip_longest(a, b, rtol, atol, wrap):
        if wrp is not None:  # adjust to phase-wrap
            x = np.divmod(x, wrp)[1]  # the "remainder"
            y = np.divmod(y, wrp)[1]

        try:
            x, y, _rt, _at = _unquantify(x, y, rt, at)
        except u.UnitsError as e:
            raise u.UnitsError(e)

        compare = u.isclose(x, y, rtol=_rt, atol=_at, equal_nan=equal_nan)

        close.append(compare)

    return np.array(close)


# /def


# -------------------------------------------------------------------


# TODO support argument kwargs
def eltwise_quantity_allclose(
    a,
    b,
    rtol=1e-15,
    atol=None,
    equal_nan=False,
    wrap: T.Union[None, T.Tuple[int, QuantityType]] = None,
):
    """Returns True if two arrays are element-wise equal within a tolerance.

    This is a |Quantity|-aware version of :func:`~numpy.allclose`,
    modified from :mod:`~astropy` to be easier for PDB debugging.

    .. warning::

        This function should only be used when setting up testing.
        Use :func:`~astropy.units.allclose` or
        :func:`~astropy.tests.helper.quantity_allclose`.

    """
    return np.all(
        eltwise_quantity_isclose(
            a, b, rtol=rtol, atol=atol, equal_nan=equal_nan, wrap=wrap
        )
    )


# /def


# -------------------------------------------------------------------


# TODO support argument kwargs
def eltwise_assert_quantity_isclose(
    a,
    b,
    rtol=1e-15,
    atol=None,
    equal_nan=False,
    wrap: T.Union[None, T.Tuple[int, QuantityType]] = None,
):
    """Returns True if two arrays are element-wise equal within a tolerance.

    This is a |Quantity|-aware version of :func:`~numpy.allclose`,
    modified from :mod:`~astropy` to be easier for PDB debugging.

    .. warning::

        This function should only be used when setting up testing.
        Use :func:`~astropy.units.allclose` or
        :func:`~astropy.tests.helper.quantity_allclose`.

    """
    # Splitting the comparison into a for-loop allows for element-wise
    # comparisons and prevents dropping into sub-functions so we stay in this
    # namespace when in PDB.
    try:
        alen = len(a)
    except TypeError:  # scalar
        a = [a]
        alen = 1

    try:
        blen = len(b)
    except TypeError:
        b = [b]
        blen = 1

    assert alen == blen

    try:
        len(rtol)
    except TypeError:  # scalar
        rtol = np.broadcast_to(rtol, blen, subok=True)

    try:
        len(atol)
    except TypeError:  # scalar
        atol = np.broadcast_to(atol, blen, subok=True)

    wrap = wrap if wrap is not None else [wrap]

    for x, y, rt, at, wrp in zip_longest(a, b, rtol, atol, wrap):
        if wrp is not None:  # adjust to phase-wrap
            x = np.divmod(x, wrp)[1]  # the "remainder"
            y = np.divmod(y, wrp)[1]

        try:
            x, y, _rt, _at = _unquantify(x, y, rt, at)
        except u.UnitsError as e:
            raise u.UnitsError(e)

        assert u.isclose(
            x, y, rtol=_rt, atol=_at, equal_nan=equal_nan
        ), f"{x}, {y} | {_rt}, {_at}"


# /def


# -------------------------------------------------------------------


# TODO support argument kwargs
def eltwise_assert_quantity_allclose(
    a,
    b,
    rtol=1e-15,
    atol=None,
    equal_nan=False,
    wrap: T.Union[None, T.Tuple[int, QuantityType]] = None,
):
    """Raise an assertion if two objects are not equal up to desired tolerance.

    This is a :class:`~astropy.units.Quantity`-aware version of
    :func:`numpy.testing.assert_allclose`,
    modified from :mod:`~astropy` to be easier for PDB debugging.

    .. warning::

        This function should only be used when setting up testing.
        Use :func:`~astropy.tests.helper.assert_quantity_allclose`.

    """
    # Splitting the comparison into a for-loop allows for element-wise
    # comparisons and prevents dropping into sub-functions so we stay in this
    # namespace when in PDB.
    return eltwise_assert_quantity_isclose(
        a, b, rtol=rtol, atol=atol, equal_nan=equal_nan, wrap=wrap
    )


# /def


##############################################################################
# END
