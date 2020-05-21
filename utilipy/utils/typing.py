# -*- coding: utf-8 -*-

"""Typing library utilities."""

__author__ = "Nathaniel Starkman"
__credits__ = ["typing"]


__all__ = ["array_like"]


###############################################################################
# IMPORTS

# BUILT-IN

import typing as T
from typing import *


# THIRD PARTY

import numpy as np
from astropy import table


###############################################################################
# CODE
###############################################################################

#####################################################################
# Numpy


array_like = T.TypeVar("array_like", np.array, list, tuple)


#####################################################################
# Astropy

TableType = T.TypeVar("TableType", table.Table, table.QTable)


###############################################################################
# END
