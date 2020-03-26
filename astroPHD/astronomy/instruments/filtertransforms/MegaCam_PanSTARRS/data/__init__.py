# -*- coding: utf-8 -*-
# see LICENSE.rst

# ----------------------------------------------------------------------------
#
# TITLE   : data
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

"""Data Management.

Often data is packaged poorly and it can be difficult to understand how
the data should be read.
DON`T PANIC.
This module provides functions to read the contained data.

Routine Listings
----------------

"""

__author__ = "Nathaniel Starkman"


# __all__ = [
#     ""
# ]


###############################################################################
# IMPORTS

# GENERAL

import os
from astropy.table import QTable


###############################################################################
# PARAMETERS

DATA_PATH: str = os.path.dirname(os.path.realpath(__file__))
# DATA_PATH = DATA_PATH + '/' if not DATA_PATH.endswith('/') else DATA_PATH

###############################################################################
# CODE
###############################################################################


def read_MegaCamGen1_from_PS1():

    data = QTable(QTable.read(
        os.path.join(DATA_PATH, "MegaCamGen1_from_PS1.ecsv"),
        format="ascii.ecsv",
    ))
    data.add_index("name")

    return data


# /def

# ------------------------------------------------------------------------


###############################################################################
# END
