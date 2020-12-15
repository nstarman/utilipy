# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.imports.extended_imports`."""


##############################################################################
# IMPORTS

# BUILT-IN
import warnings

# PROJECT-SPECIFIC
from utilipy.imports import extended_imports as imports

##############################################################################
# PARAMETERS

warnings.simplefilter("ignore", RuntimeWarning)

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
