# -*- coding: utf-8 -*-

"""initialization file for astro.main"""

__author__ = "Nathaniel Starkman"


__all__ = [
    # distance modulus
    "distanceModulus_magnitude",
    "distanceModulus_distance",
    "distanceModulus",
    # parallax
    "parallax_angle",
    "parallax_distance",
    "parallax",
    # angular separation
    "max_angular_separation",
]


##############################################################################
# IMPORTS

# GENERAL

# PROJECT-SPECIFIC
from .functions import (
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
