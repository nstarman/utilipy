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


def test_utilipyWarning():
    """Test utilipyWarning."""
    self = unittest.TestCase()
    with self.assertWarns(exceptions.utilipyWarning):
        warnings.warn("utilipyWarning", exceptions.utilipyWarning)

    return


# /def


def test_utilipyWarningVerbose():
    """Test utilipyWarningVerbose."""
    self = unittest.TestCase()
    with self.assertWarns(exceptions.utilipyWarningVerbose):
        warnings.warn(
            "utilipyWarningVerbose", exceptions.utilipyWarningVerbose
        )

    return


# /def


# --------------------------------------------------------------------------


##############################################################################
# END
