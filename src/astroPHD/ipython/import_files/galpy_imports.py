# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : galpy_imports
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Base set of imports for the galpy code."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

if __name__ == '__main__':

    import galpy

    # potential
    from galpy import potential
    from galpy.potential import MWPotential2014

    # orbit
    from galpy.orbit import Orbit

    # util
    from galpy.util import bovy_conversion, bovy_coords


##############################################################################
# INFORMATION

print("""Imported from galpy:
    potential, .MWPotential2014
    galpy.orbit.Orbit
    galpy.util: bovy_conversion, bovy_coords
""")


##############################################################################
# END
