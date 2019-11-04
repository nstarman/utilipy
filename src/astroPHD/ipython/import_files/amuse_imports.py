# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : amuse_imports
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Base set of imports for the AMUSE code."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

if __name__ == '__main__':

    import amuse

    # lab
    from amuse import lab
    from amuse.units import units, constants
    from amuse.couple import bridge


##############################################################################
# INFORMATION

print("""Imported from amuse:
    amuse
    lab
    units
"""
      )


##############################################################################
# END
