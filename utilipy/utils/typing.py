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
from typing import *


# THIRD PARTY

import numpy as np
from astropy import table, coordinates as coords


###############################################################################
# CODE
###############################################################################

#####################################################################
# Numpy


array_like = T.TypeVar("array_like", np.array, list, tuple)


#####################################################################
# Astropy

TableType = T.TypeVar("TableType", table.Table, table.QTable)

FrameOptionsType = T.TypeVar(
    "FrameOptionsType", str, coords.BaseCoordinateFrame, coords.SkyCoord
)


###############################################################################
# END
