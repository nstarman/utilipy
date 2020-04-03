# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : galpy_imports
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Base set of imports for the galpy code.

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


##############################################################################
# HELPER FUNCTIONS

from utilipy.config import __config__
from utilipy.decorators.docstring import (
    _set_docstring_import_file_helper,
    _import_file_docstring_helper,
)


##############################################################################
# IMPORTS

import time

# ------------------------

try:

    from galpy import __version__

    # time.sleep(0.2)

except ImportError:

    import warnings

    warnings.warn("Cannot import galpy")

else:

    import galpy

    # potential
    from galpy import potential
    from galpy.potential import MWPotential2014

    # orbit
    from galpy.orbit import Orbit

    # util
    from galpy.util import bovy_conversion, bovy_coords

    from galpy.util import galpyWarning

# /if

##############################################################################
# Printing Information


@_set_docstring_import_file_helper("galpy", __doc__)  # doc from __doc__
def galpy_imports_help():
    """Help for galpy base imports."""
    doc = _import_file_docstring_helper(galpy_imports_help.__doc__)
    print(doc)


# /def


if __config__.getboolean("verbosity", "verbose-imports"):
    galpy_imports_help()

##############################################################################
# END
