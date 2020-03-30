# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE  : test util/exceptions
#
# ----------------------------------------------------------------------------

"""tests for util/exceptions.py."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

import warnings
import unittest


# PROJECT-SPECIFIC

from .. import exceptions


##############################################################################
# Tests


def test_astroPHDWarning():
    """Test astroPHDWarning."""
    self = unittest.TestCase()
    with self.assertWarns(exceptions.astroPHDWarning):
        warnings.warn("astroPHDWarning", exceptions.astroPHDWarning)

    return


# /def


def test_astroPHDWarningVerbose():
    """Test astroPHDWarningVerbose."""
    self = unittest.TestCase()
    with self.assertWarns(exceptions.astroPHDWarningVerbose):
        warnings.warn(
            "astroPHDWarningVerbose", exceptions.astroPHDWarningVerbose
        )

    return


# /def


# --------------------------------------------------------------------------


##############################################################################
# END
