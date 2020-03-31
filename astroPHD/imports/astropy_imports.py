# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : astropy_imports
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

"""Base set of imports for the astropy code.

Notes
-----
calls `quantity_support`

Routine Listings
----------------
Astropy: imports

    - units->u,
    - coordinates->coords, SkyCoord,
    - table.Table, QTable
    - visualization.quantity_support, astropy_mpl_style

References
----------
.. [#] Astropy Collaboration et al., 2018, AJ, 156, 123.

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# HELPER FUNCTIONS

from astroPHD.config import __config__
from astroPHD.decorators.docstring import (
    _set_docstring_import_file_helper,
    _import_file_docstring_helper,
)


##############################################################################
# IMPORTS

# Astropy
import astropy

from astropy import units as u  # units TODO replace with mine
from astropy import coordinates as coords  # coordinates

from astropy.coordinates import SkyCoord
from astropy.table import Table, QTable  # table data structure

# Allowing quantities in matplotlib
from astropy.visualization import quantity_support, astropy_mpl_style


##############################################################################
# Cleaning Up

# astropy changes to matplotlib
quantity_support()


##############################################################################
# Printing Information


@_set_docstring_import_file_helper("astropy", __doc__)  # doc from __doc__
def astropy_imports_help():
    """Help for extended base imports."""
    doc = _import_file_docstring_helper(astropy_imports_help.__doc__)
    print(doc)


# /def


if __config__.getboolean("verbosity", "verbose-imports"):
    astropy_imports_help()

##############################################################################
# END
