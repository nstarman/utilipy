# -*- coding: utf-8 -*-

"""Astropy Units. Extended.

provides full drop-in replacement for astropy units.

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    # top-level
    "amuse",
    "composite",
    "core",
    "decorators",
    "full_amuse",
    # core
    "quantity_return_",
    "ExpandedUnitType",
    # decorators
    "quantity_output",
    "quantity_io",
    # "QuantityInputOutput",
]


#############################################################################
# IMPORTS

# THIRD-PARTY

from astropy.units import *  # for drop-in use, parts will be overridden
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

# units to add
from .amuse import *
from .composite import *

# more stuff
from .core import quantity_return_, ExpandedUnitType
from .decorators import quantity_output, quantity_io, QuantityInputOutput

# Import modules into top-level directory
from . import amuse, composite, core, decorators, full_amuse


# THIRD-PARTY


#############################################################################
# CLEANUP

# try:  # TODO not need to delete b/c stub file.
#     del add_enabled_equivalencies
# except Exception:
#     pass


#############################################################################
# __ALL__

# if hasattr(astropy.units, "__all__"):
#     __all__ += astropy.units.__all__
# else:
#     pass
# #     __all__ += list(dir(astropy.units))

# __all__ += _added_units.__all__
# # __all__ += decorators.__all__


##############################################################################
# END
