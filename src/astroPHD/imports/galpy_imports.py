# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : galpy_imports
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
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

from astroPHD.util.config import __config__
from astroPHD.util.decorators.docstring import (
    _set_docstring_import_file_helper,
    _import_file_docstring_helper
)



##############################################################################
# IMPORTS

if __name__ == '__main__':  # protect if galpy not installed

    import galpy

    # potential
    from galpy import potential
    from galpy.potential import MWPotential2014

    # orbit
    from galpy.orbit import Orbit

    # util
    from galpy.util import bovy_conversion, bovy_coords

# /if

##############################################################################
# Printing Information

@_set_docstring_import_file_helper('galpy', __doc__)  # doc from __doc__
def galpy_imports_help():
    """Help for galpy base imports."""
    _import_file_docstring_helper(galpy_imports_help.__doc__)  # formatting
# /def


if __config__.getboolean('verbosity', 'verbose-imports'):
    galpy_imports_help()

##############################################################################
# END
