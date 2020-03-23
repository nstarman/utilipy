# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : constants
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""constants.

Astropy constants, with frozen version for reproducibility

float versions of the constants accessible through `values` module
this includes frozen version for reproducibility
to access frozen verion, set `frozen-constants=True` in astropy config


References
----------
References [#]_.

.. [#] Astropy Collaboration et al., 2018, AJ, 156, 123.

"""

__author__ = "Nathaniel Starkman"

##############################################################################
# IMPORTS

# GENERAL
from astropy.constants import *

# PROJECT-SPECIFIC
from . import values
from .values import ConstantsValues, default_values


#############################################################################
# END
