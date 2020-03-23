# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : initialization file
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""initialization file for units."""

__author__ = "Nathaniel Starkman"

#############################################################################
# IMPORTS

# GENERAL

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

##############################################################################
# END
