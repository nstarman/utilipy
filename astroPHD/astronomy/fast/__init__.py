#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : initialize fast functions
# AUTHOR  : Nathaniel Starkman
# PROJECT : astronat
#
# ----------------------------------------------------------------------------
### Docstring and Metadata
r"""
"""

__author__ = "Nathaniel Starkman"

#############################################################################
### Imports

from .functions import (
    # magnitudes
    apparent_to_absolute_magnitude, absolute_to_apparent_magnitude,
    # distance modulus
    distanceModulus_magnitude, distanceModulus_distance,
    distanceModulus,
    # parallax
    parallax_angle, parallax_distance, parallax,
    # angular separation
    max_angular_separation,
)

#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2018, "
__credits__ = [""]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"

#############################################################################
# Code
