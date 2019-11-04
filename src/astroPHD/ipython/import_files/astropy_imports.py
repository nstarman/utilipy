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
"""Base set of imports for the astropy code."""

__author__ = "Nathaniel Starkman"


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

print("""Imported from Astropy:
    astropy, .units->u, .coordinates->coords, .SkyCoord, .Table, .QTable
""")
