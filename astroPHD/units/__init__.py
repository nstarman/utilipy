# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : initialization file
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""initialization file for units."""

__author__ = "Nathaniel Starkman"


__all__ = []


#############################################################################
# IMPORTS

# GENERAL

import astropy.units
from astropy.units import *
from astropy.units import (  # explicit imports for mypy compatibility
    # units
    rad,
    deg,
    m,
    AU,
    pc,
    mag,
    # functions
    get_physical_type,
)

# PROJECT-SPECIFIC

from ._added_units import *
from .decorators import *

from . import _added_units, decorators


#############################################################################
# __ALL__

if hasattr(astropy.units, "__all__"):
    __all__ += astropy.units.__all__
else:
    __all__ += list(dir(astropy.units))

__all__ += _added_units.__all__
__all__ += decorators.__all__


##############################################################################
# END
