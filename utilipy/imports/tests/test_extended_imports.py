# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.imports.extended_imports`."""


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
