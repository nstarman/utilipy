# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_amuse
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""test functions for astropy imports."""

__author__ = "Nathaniel Starkman"


##############################################################################


def test_import_astropy():
    """Test _inRange."""
    from utilipy.imports import astropy_imports as imports

    imports.astropy
    imports.u
    imports.coords
    imports.SkyCoord
    imports.Table, imports.QTable
    imports.quantity_support, imports.astropy_mpl_style

    return


# /def


##############################################################################
# END
