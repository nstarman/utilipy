# -*- coding: utf-8 -*-

"""Typing library utilities."""

__author__ = "Nathaniel Starkman"


__all__ = [
    # numpy
    "array_like",
    # Astropy
    "TableType",
    "FrameOptionsType",
]


###############################################################################
# IMPORTS

# BUILT-IN

import typing as T
from typing import *  # NOQA


# THIRD PARTY

import numpy as np
from astropy import table, coordinates as coord, units as u


###############################################################################
# CODE
###############################################################################

#####################################################################
# Numpy


array_like = T.TypeVar("array_like", np.array, list, tuple, T.Sequence)
"""Array-like types compatible with [numpy]_'s "array-like".

References
----------
.. [numpy] Travis E, Oliphant. A guide to NumPy: Trelgol Publishing, (2006).

Examples
--------

    >>> sc: FrameOptionsType = SkyCoord()
    >>> isinstance(sc, SkyCoord)
    True

"""


#####################################################################
# Astropy

FrameOptionsType = T.TypeVar(
    "FrameOptionsType", str, coord.BaseCoordinateFrame, coord.SkyCoord
)
"""Astropy [astropy]_ frame-like types.

Subclasses of BaseCoordinateFrame or SkyCoord.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> sc: FrameOptionsType = SkyCoord()
    >>> isinstance(sc, SkyCoord)
    True

"""

TableType = T.TypeVar("TableType", table.Table, table.QTable)
"""Astropy [astropy]_ Table-types.

Subclasses of Table, QTable.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> tbl: TableType = QTable()
    >>> isinstance(tbl, Table)
    True

"""

UnitableType = T.TypeVar("UnitableType", u.Unit, u.Quantity, str)
"""Types that work with Astropy [astropy]_ Unit().

Subclasses of Unit, Quantity.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> x: UnitableType = 10 * u.km
    >>> isinstance(x, u.Quantity)
    True

"""


###############################################################################
# END
