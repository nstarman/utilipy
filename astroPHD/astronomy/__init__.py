#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : initialization file
# AUTHOR  : 
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""initialization file for __________
"""

__author__ = ""
# __copyright__ = "Copyright 2018, "
# __credits__ = [""]
# __license__ = "GPL3"
# __version__ = "0.0.0"
# __maintainer__ = ""
# __email__ = ""
# __status__ = "Production"

##############################################################################
### IMPORTS

## General


## Project-Specific
from . import fast, filtertransforms, instruments, main, sc, util

from .main.functions import (
    # distance modulus
    distanceModulus_magnitude, distanceModulus_distance,
    distanceModulus,
    # parallax
    parallax_angle, parallax_distance, parallax,
    # angular separation
    max_angular_separation
)


##############################################################################
### END
