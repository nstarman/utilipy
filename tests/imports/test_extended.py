#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_extended
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""test functions for extended imports."""

__author__ = "Nathaniel Starkman"


##############################################################################

def test_import_extended():
    """Test _inRange."""
    from astroPHD.imports import extended as imports

    imports.norm
    imports.binned_stats

    return
# /def


##############################################################################
# END
