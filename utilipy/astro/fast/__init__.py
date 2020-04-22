# -*- coding: utf-8 -*-

"""Fast astro functions.

.. todo::

    Implement in C via mypyc

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    # magnitudes
    "apparent_to_absolute_magnitude",
    "absolute_to_apparent_magnitude",
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

# PROJECT-SPECIFIC

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

##############################################################################
# END
