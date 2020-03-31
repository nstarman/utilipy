#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_extended
#
# ----------------------------------------------------------------------------

"""Test functions for extended imports."""


##############################################################################
# IMPORTS

# GENERAL

# fmt: off
import warnings; warnings.simplefilter("ignore", RuntimeWarning)
# fmt: on


# PROJECT-SPECIFIC

from .. import extended_imports as imports


##############################################################################


def test_import_extended():
    """Test Extended Imports."""
    imports.norm
    imports.binned_stats

    return


# /def


# ------------------------------------------------------------------------


##############################################################################
# END
