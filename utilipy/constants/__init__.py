# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : constants
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Astropy Constants.

Astropy constants, with a frozen version for reproducibility.

float versions of the constants accessible through `values` module
this includes frozen version for reproducibility
to access frozen version, set `frozen-constants=True` in utilipy config


References
----------
References [#]_.

.. [#] Astropy Collaboration et al., 2018, AJ, 156, 123.

"""

__author__ = "Nathaniel Starkman"

__all__ = [
    "frozen",
    "FrozenConstants",
    "default_values",
    "ConstantsValues",
]


##############################################################################
# IMPORTS

# GENERAL

from astropy import constants
from astropy.constants import *


# PROJECT-SPECIFIC

from ._frozen import FrozenConstants, frozen
from .values import ConstantsValues, values as default_values

# import top level packages
from . import (
    values,
    _frozen,
)


##############################################################################
# __ALL__

__all_top_imports__ = ("values", "_frozen")

__all__ += list(__all_top_imports__)
# __all__ += (
#     constants.__all__
#     if hasattr(constants, "__all__")
#     else list(dir(constants))
# )


#############################################################################
# END
