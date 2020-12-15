# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.utils.exceptions`."""


__all__ = [
    "test_utilipyWarning",
    "test_utilipyWarningVerbose",
]


##############################################################################
# IMPORTS

# BUILT-IN
import sys
import tempfile
import unittest
import warnings

# PROJECT-SPECIFIC
from utilipy.utils import exceptions

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


def test_showwarning():
    """Test :func:`~utilipy.utils.exceptions._showwarning`."""
    # First test UserWarning
    with tempfile.NamedTemporaryFile(mode="w+") as tmp:

        exceptions.showwarning(
            message="\ntest",
            category=UserWarning,
            filename=tmp.name,
            lineno=-1,
            file=tmp,  # redirect to file, not stdout
            line=None,
        )

        tmp.seek(0)  # rewind file

        lines = tmp.readlines()
        i = 1 if sys.version_info.minor > 6 else 3

        assert lines[i] == "test\n", lines

    # /with

    # Test utilipyWarning non-verbose warning
    # have to make a temporary file
    # turn off the verbosity, and pass a utilipyWarning
    with tempfile.NamedTemporaryFile(mode="w+") as tmp:

        with exceptions.conf.set_temp("verbose_warnings", False):

            exceptions.showwarning(
                message="test",
                category=exceptions.utilipyWarning,
                filename=tmp.name,
                lineno=-1,
                file=tmp,  # redirect to file, not stdout
                line=None,
            )

            tmp.seek(0)  # rewind file

            assert tmp.readline() == "utilipyWarning: test\n", tmp.readline()

        # /with

    # /with


# /def


##############################################################################
# END
