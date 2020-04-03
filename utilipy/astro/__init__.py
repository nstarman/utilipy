#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : initialization file
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Initialization file for astro."""

##############################################################################
# IMPORTS

# General
from astropy.cosmology import default_cosmology

# Project-Specific
from .. import units
from .. import constants

from . import fast, instruments, main, sc

from .main import (
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


##############################################################################
# END
