#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_extended
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""test functions for extended imports."""


##############################################################################
# IMPORTS

# GENERAL

import warnings

warnings.simplefilter("ignore", RuntimeWarning)


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
