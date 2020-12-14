# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : astropy_imports
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Base set of imports for :mod:`~astropy`.

Notes
-----
calls `quantity_support`

Routine Listings
----------------
Astropy: imports

    - units->u,
    - coordinates->coord, SkyCoord,
    - table.Table, QTable
    - visualization.quantity_support, astropy_mpl_style

References
----------
Astropy [#]_

.. [#] Astropy Collaboration et al., 2018, AJ, 156, 123.

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "astropy_imports_help",
    "astropy",
    "u",
    "const",
    "coord",
    "cosmology",
    "SkyCoord",
    "Table",
    "QTable",
    "astropy_mpl_style",
    # modeling
    "modeling",
    "models",
    "fitting",
]


##############################################################################
# HELPER FUNCTIONS

# THIRD PARTY
import astropy
import astropy.constants as const
import astropy.coordinates as coord
import astropy.cosmology as cosmology
import astropy.units as u
from astropy import modeling
from astropy.coordinates import SkyCoord
from astropy.modeling import fitting, models
from astropy.table import QTable, Table
from astropy.visualization import (
    astropy_mpl_style,
    quantity_support,
    time_support,
)

# PROJECT-SPECIFIC
from utilipy.imports import conf
from utilipy.utils import make_help_function

##############################################################################
# Cleaning Up

# astropy changes to matplotlib
quantity_support()
time_support()


##############################################################################
# Printing Information

astropy_imports_help = make_help_function(
    "astropy", __doc__, look_for="Routine Listings"
)


if conf.verbose_imports:
    astropy_imports_help()


##############################################################################
# END
