#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : initialize fast functions
# AUTHOR  : Nathaniel Starkman
# PROJECT : astronat
#
# ----------------------------------------------------------------------------
# Docstring and Metadata
"""Fast astronomy functions.

TODO
----
Implement in C

"""

__author__ = "Nathaniel Starkman"

#############################################################################
# Imports

from .functions import (
    # magnitudes
    apparent_to_absolute_magnitude,
    absolute_to_apparent_magnitude,
    # distance modulus
    distanceModulus_magnitude,
    distanceModulus_distance,
    distanceModulus,
    # parallax
    parallax_angle,
    parallax_distance,
    parallax,
    # angular separation
    max_angular_separation,
)

#############################################################################
# END
