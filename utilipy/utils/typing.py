# -*- coding: utf-8 -*-

"""Typing library utilities."""

__all__ = [
    # compat
    "OrderedDictType",
    "EllipsisType",
    # numpy
    "array_like",
    # Astropy
    "CoordinateRepresentationType",
    "CoordinateDifferentialType",
    "CoordinateType",
    "FrameOptionsType",
    "TableType",
    "UnitableType",
    "DistanceType",
    "AngleType",
    "ModelType",
    "FittableModelType",
]


###############################################################################
# IMPORTS

# BUILT-IN
import typing as T
from typing import *  # noqa

# THIRD PARTY
import astropy.coordinates as coord
import astropy.units as u
import numpy as np
from astropy import table
from astropy.modeling.core import CompoundModel, FittableModel, Model

###############################################################################
# CODE
###############################################################################

OrderedDictType = T.OrderedDict
EllipsisType = type(Ellipsis)


#####################################################################
# Numpy


array_like = T.TypeVar("array_like", np.ndarray, list, tuple, T.Sequence)
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

CoordinateRepresentationType = T.TypeVar(
    "RepresentationType",
    coord.BaseRepresentation,
    coord.BaseRepresentationOrDifferential,
)
"""Astropy [astropy]_ representation types.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

"""


CoordinateDifferentialType = T.TypeVar(
    "RepresentationType",
    coord.BaseDifferential,
    coord.BaseRepresentationOrDifferential,
)
"""Astropy [astropy]_ representation types.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

"""


# -------------------------------------------------------------------

CoordinateType = T.TypeVar(
    "CoordinateType", coord.BaseCoordinateFrame, coord.SkyCoord
)
"""Astropy [astropy]_ coordinate frame-like types.

Subclasses of BaseCoordinateFrame or SkyCoord.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> sc: CoordinateType = SkyCoord()
    >>> isinstance(sc, SkyCoord)
    True

"""

FrameOptionsType = T.TypeVar("FrameOptionsType", str, CoordinateType)
"""Astropy [astropy]_ frame-like types.

Subclasses of BaseCoordinateFrame or SkyCoord, or a string.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> sc: FrameOptionsType = SkyCoord()
    >>> isinstance(sc, SkyCoord)
    True

"""

# -------------------------------------------------------------------

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

# -------------------------------------------------------------------

UnitableType = T.TypeVar("UnitableType", u.Unit, u.Quantity, str)
"""Types that work with Astropy [astropy]_ :class:`~astropy.units.Unit`.

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

UnitType = T.TypeVar("UnitType", u.UnitBase, u.Unit)
""":class:`~astropy.units.Unit` Type [astropy]_.

Subclasses of Unit.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> unit: UnitType = u.km
    >>> isinstance(x, u.Unit)
    True

"""

QuantityType = T.TypeVar("QuantityType", u.Quantity, u.SpecificTypeQuantity)
"""Types for :class:`~astropy.units.Quantity`[astropy]_ .

Subclasses of Distance, Quantity.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> x: QuantityType = 10 * u.km
    >>> isinstance(x, u.Quantity)
    True

"""

DistanceType = T.TypeVar("DistanceType", coord.Distance, u.Quantity)
"""Types for :class:`~astropy.coordinates.Distance`[astropy]_ .

Subclasses of Distance, Quantity.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> x: DistanceType = 10 * u.km
    >>> isinstance(x, u.Quantity)
    True

"""


AngleType = T.TypeVar("DistanceType", coord.Angle, u.Quantity)
"""Types for :class:`~astropy.coordinates.Angle`[astropy]_ .

Subclasses of Angle, Quantity.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> x: DistanceType = 10 * u.deg
    >>> isinstance(x, u.Quantity)
    True

"""

# -------------------------------------------------------------------

ModelType = T.TypeVar("ModelType", Model, CompoundModel)
"""Astropy :class:`~astropy.modeling.Model` Types [astropy]_.

Subclasses of Model, CompoundModel.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> from astropy.modeling.models import Model, Gaussian1D
    >>> x: ModelType = Gaussian1D()
    >>> isinstance(x, Model)
    True

"""

FittableModelType = T.TypeVar("ModelType", FittableModel, CompoundModel)
"""Astropy :class:`~astropy.modeling.FittableModel` Types [astropy]_.

Subclasses of FittableModel, CompoundModel.
Note that not all CompoundModels are fittable, but this can't be checked.

References
----------
.. [astropy] Astropy Collaboration et al., 2018, AJ, 156, 123.

Examples
--------

    >>> from astropy.modeling.models import Model, Gaussian1D
    >>> x: ModelType = Gaussian1D()
    >>> isinstance(x, Model)
    True

"""


###############################################################################
# END
