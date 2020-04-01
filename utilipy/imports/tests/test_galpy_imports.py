#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_galpy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""test functions for galpy imports."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL
try:
    import galpy
except ImportError:
    _do_galpy_import = False
else:
    _do_galpy_import = True

##############################################################################


def test_import_galpy():
    """Test galpy imports when not in IPython environment"""
    if _do_galpy_import:

        from utilipy.imports import galpy_imports as imports

        imports.galpy
        imports.potential
        imports.MWPotential2014
        imports.Orbit
        imports.bovy_conversion, imports.bovy_coords

    return


# /def


##############################################################################
# END
