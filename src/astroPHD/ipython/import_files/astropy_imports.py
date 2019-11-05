#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : astropy_imports
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Base set of imports for the astropy code.

Notes
-----
calls `quantity_support`

Returns
-------
astropy
astropy:
    units->u,
    coordinates->coords, SkyCoord,
    table.Table, QTable
    visualization.quantity_support, astropy_mpl_style

References
----------
Astropy citation: [1]_

.. [1] Astropy Collaboration et al., 2018, AJ, 156, 123

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

# Astropy
import astropy

from astropy import units as u             # units TODO replace with mine
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

@_set_docstring_import_file_helper('astropy', __doc__)  # doc from __doc__
def astropy_imports_help():
    """Help for extended base imports."""
    _import_file_docstring_helper(astropy_imports_help.__doc__)  # formatting
# /def


if __config__.getboolean('verbosity', 'verbose-imports'):
    astropy_imports_help()

##############################################################################
# END
