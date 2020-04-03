# -*- coding: utf-8 -*-
# see LICENSE.rst

# ----------------------------------------------------------------------------
#
# TITLE   : data
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Data Management.

Often data is packaged poorly and it can be difficult to understand how
the data should be read.
DON`T PANIC.
This module provides functions to read the contained data.

Routine Listings
----------------
read_MegaCamGen1_from_PS1

Todo
----
figure out how to use get_pkg_data_fileobj

"""

__author__ = "Nathaniel Starkman"


# __all__ = [
#     ""
# ]


###############################################################################
# IMPORTS

# GENERAL

from astropy.table import QTable
from astropy.utils.data import get_pkg_data_filename


###############################################################################
# PARAMETERS

_PACKAGE = "utilipy.astro.instruments.filtertransforms.MegaCam_PanSTARRS.data"

###############################################################################
# CODE
###############################################################################


def read_MegaCamGen1_from_PS1():
    """Read MegaCamGen1_from_PS1 data."""
    fpath = get_pkg_data_filename(
        "MegaCamGen1_from_PS1.ecsv", package=_PACKAGE
    )
    return QTable.read(fpath, format="ascii.ecsv")


# /def

# ------------------------------------------------------------------------


###############################################################################
# END
