# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.utils.exceptions`."""


__all__ = [
    "test_utilipyWarning",
    "test_utilipyWarningVerbose",
]


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
    """Test :class:`~utilipy.utils.exceptions.utilipyWarning`."""
    self = unittest.TestCase()
    with self.assertWarns(exceptions.utilipyWarning):
        warnings.warn("utilipyWarning", exceptions.utilipyWarning)

    return


# /def


def test_utilipyWarningVerbose():
    """Test :class:`~utilipy.utils.exceptions.utilipyWarningVerbose`."""
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
