#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : unit decorators
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Units Util."""

__author__ = "Nathaniel Starkman"

##############################################################################
# IMPORTS

# GENERAL
from typing import Any, Union, Sequence

# astropy
from astropy.units.core import Unit, IrreducibleUnit

from astropy.utils.decorators import wraps
from astropy.utils.misc import isiterable


###############################################################################
# CODE
###############################################################################


def unit_output(
    res: Any,
    unit: Unit = None,
    to_value: bool = False,
    equivalencies: Sequence = [],
    decompose: Union[bool, Sequence] = False,
) -> Any:
    """Control return of Quantities.

    Parameters
    ----------
    res: Quantity, optional
        the result
    unit: Unit, optional
        sets the unit for the returned `res`
        if None, returns `res` unchanged, unless `to_value` is used
        if '', decomposes
    to_value: bool, optional
        whether to return ``.to_value(unit)``
        see Astropy.units.Quantity.to_value
    equivalencies: list, optional
        equivalencies for ``.to()`` and ``.to_value()``
        only used if `unit' to `to_value` are not None/False
    decompose: bool or list, optional
        unit decomposition
        default, False

        * bool: True, False for decomposing.
        * list: bases for ``.decompose(bases=[])``

            will first decompose, then apply `unit`, `to_value`, `equivalencies`

        Decomposing then converting wastes time, since
        ``.to(unit, equivalencies)`` internally does conversions.
        The only use for combining `decompose` with other `unit_output`
        parameters is with::

            unit=None, to_value=True, equivalencies=[], decompose=`bool or [user bases here]'

        since this will decompose to desired bases then return the value in those bases

        .. note::

            **experimental feature:**
            for things which are not (astropy.unit.Unit, astropy.unit.core.IrreducibleUnit),
            tries wrapping in ``Unit()``. This would normally return an error, but now
            allows for conversions such as:

            >>> x = 10 * u.km * u.s
            >>> bases = [u.Unit(2 * u.km), u.s]
            >>> x.decompose(bases=bases) # doctest: +SKIP
            <Quantity 5.0 2 km s>

    Returns
    -------
    res:
        function output, converted / decomposed / evaluated to desired units

    Raises
    ------
    ValueError
        if unit not astropy compatible
    astropy.units.UnitConversionError
        if conversion not legit

    Examples
    --------
    How to apply in a function directly

    >>> def example_function(x, **kw):
    ...     return unit_output(x, unit=kw.get('unit', None),
    ...                        to_value=kw.get('to_value', False),
    ...                        equivalencies=kw.get('equivalencies', []),
    ...                        decompose=kw.get('decompose', []))
    >>> example_function(10*u.km, unit=u.m, to_value=True)
    10000.0

    """
    # fast check to do nothing
    if (
        (unit is None)
        & (to_value is False)
        & (equivalencies == [])
        & (decompose is False)
    ):
        return res

    # First decomposing
    if decompose is False:
        pass
    elif decompose is True:
        res = res.decompose()
    elif decompose:  # decompose is NOT empty list
        clss = (Unit, IrreducibleUnit)
        bases = [
            Unit(x) if not issubclass(x.__class__, clss) else x
            for x in decompose
        ]
        res = res.decompose(bases=bases)

    # Now Converting
    if (unit is None) and (to_value is False):  # nothing required
        return res
    elif to_value is True:  # return value
        return res.to_value(unit, equivalencies)
    return res.to(unit, equivalencies)


# /def


###############################################################################
# END
