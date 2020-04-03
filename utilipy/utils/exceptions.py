# -*- coding: utf-8 -*-

"""Warnings and Exceptions.

Routine Listings
----------------
utilipyWarning
utilipyWarningVerbose
_warning

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

from typing import Any
import warnings


# PROJECT-SPECIFIC

from ..config import __config__


##############################################################################
# PARAMETERS

try:
    __config__.getboolean("verbosity", "warnings")
except Exception:
    _SHOW_WARNINGS: bool = True
else:
    _SHOW_WARNINGS: bool = __config__.getboolean("verbosity", "warnings")


###############################################################################
# CODE
###############################################################################


class utilipyWarning(Warning):
    """utilipyWarning."""

    pass


# /class


# ----------------------------------------------------------------------------


class utilipyWarningVerbose(Warning):
    """utilipyWarningVerbose."""

    pass


# /class


# ----------------------------------------------------------------------------


def _warning(
    message: Any,
    category: type = utilipyWarning,
    filename: str = "",
    lineno: int = -1,
    file: None = None,
    line: None = None,
):
    if issubclass(category, utilipyWarning):
        if not issubclass(category, utilipyWarningVerbose) or _SHOW_WARNINGS:
            print("utilipyWarning: " + str(message))
    else:
        print(warnings.formatwarning(message, category, filename, lineno))


warnings.showwarning = _warning  # TODO check how this is used


##############################################################################
# END
