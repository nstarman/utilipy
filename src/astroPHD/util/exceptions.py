# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : PBH_in_galaxy
# AUTHOR  : Nathaniel Starkman
# PROJECT : Eridanus_PBH
#
# ----------------------------------------------------------------------------

# Docstring
"""Warnings and Exceptions.

code modified from galpy.

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL
from typing import Any
import warnings

# PROJECT-SPECIFIC
from .config import __config__


##############################################################################
# PARAMETERS

_SHOW_WARNINGS: bool = __config__.getboolean("verbosity", "warnings")

###############################################################################
# CODE
###############################################################################


class astroPHDWarning(Warning):
    """astroPHDWarning."""

    pass


# /class


# ----------------------------------------------------------------------------


class astroPHDWarningVerbose(Warning):
    """astroPHDWarningVerbose."""

    pass


# /class


# ----------------------------------------------------------------------------


def _warning(
    message: Any,
    category: type = astroPHDWarning,
    filename: str = "",
    lineno: int = -1,
    file: None = None,
    line: None = None,
):
    if issubclass(category, astroPHDWarning):
        if not issubclass(category, astroPHDWarningVerbose) or _SHOW_WARNINGS:
            print("astroPHDWarning: " + str(message))
    else:
        print(warnings.formatwarning(message, category, filename, lineno))


##############################################################################
# END
