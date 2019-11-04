#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : initialization file
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Initialization file for astronomy."""

##############################################################################
# IMPORTS

# General


# Project-Specific
from .. import units

from . import fast, instruments, main, sc

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
# END
