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
    - coordinates->coords, SkyCoord,
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
    # "quantity_support",
    "astropy",
    "u",
    "coords",
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

from utilipy.imports import conf
from utilipy.utils import make_help_function


##############################################################################
# IMPORTS

import astropy

from astropy import units as u  # units TODO replace with mine
from astropy import coordinates as coords  # coordinates

from astropy.coordinates import SkyCoord
from astropy.table import Table, QTable  # table data structure

from astropy.visualization import quantity_support, astropy_mpl_style

# modeling
from astropy import modeling
from astropy.modeling import models, fitting

if float(astropy.__version__[:3]) > 4.1:
    from astropy.modeling import custom_model

    __all__ += ("custom_model",)


##############################################################################
# Cleaning Up

# astropy changes to matplotlib
quantity_support()


##############################################################################
# Printing Information

astropy_imports_help = make_help_function(
    "astropy", __doc__, look_for="Routine Listings"
)


if conf.verbose_imports:
    astropy_imports_help()


##############################################################################
# END
