# -*- coding: utf-8 -*-

"""astro functions where the arguments are SkyCoords."""

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


#############################################################################
# IMPORTS

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


#############################################################################
# END
