# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : galpy_imports
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Base set of imports for :mod:`~galpy`.

Routine Listings
----------------
Galpy : imports

    - potential, .MWPotential2014
    - galpy.orbit.Orbit
    - galpy.util: bovy_conversion, bovy_coords

References
----------
Galpy reference [#]_.

.. [#] galpy: A Python Library for Galactic Dynamics, Jo Bovy (2015),
    Astrophys. J. Supp., 216, 29 (arXiv/1412.3451)

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "galpy_imports_help",
]


##############################################################################
# HELPER FUNCTIONS

# PROJECT-SPECIFIC
from utilipy.imports import conf
from utilipy.utils import make_help_function

##############################################################################
# IMPORTS

try:

    import galpy

except ImportError:

    import warnings

    warnings.warn("Cannot import galpy")

else:

    # potential
    from galpy import potential
    from galpy.potential import MWPotential2014

    # orbit
    from galpy.orbit import Orbit

    # util
    from galpy.util import bovy_conversion, bovy_coords

    from galpy.util import galpyWarning

    __all__ += [
        # modules
        "galpy",
        # functions
        "potential",
        "MWPotential2014",
        "Orbit",
        "bovy_conversion",
        "bovy_coords",
        "galpyWarning",
    ]

# /if

##############################################################################
# Printing Information

galpy_imports_help = make_help_function(
    "galpy", __doc__, look_for="Routine Listings"
)


if conf.verbose_imports:
    galpy_imports_help()


##############################################################################
# END
