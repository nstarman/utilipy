# -*- coding: utf-8 -*-

"""Warnings and Exceptions."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# BUILT-IN

import typing as T
import warnings


# THIRD PARTY

from astropy import config as _config


#############################################################################
# PARAMETERS


__all__: T.List[str] = [
    "conf",
    "utilipyWarning",
    "utilipyWarningVerbose",
    "_warning",
]


#############################################################################
# CONFIGURATION


class Conf(_config.ConfigNamespace):
    """Configuration parameters for :mod:`~utilipy.utils.exceptions`."""

    verbose_warnings = _config.ConfigItem(
        False,
        description="When True, use verbose warnings",
        cfgtype="boolean(default=False)",
    )


conf = Conf()


###############################################################################
# CODE
###############################################################################


class utilipyWarning(Warning):
    """:mod:`~utilipy` package warning."""


# /class


# ----------------------------------------------------------------------------


class utilipyWarningVerbose(Warning):
    """Verbose :mod:`~utilipy` warning."""


# /class


# ----------------------------------------------------------------------------


def _warning(
    message: T.Any,
    category: type = utilipyWarning,
    filename: str = "",
    lineno: int = -1,
    file: None = None,
    line: None = None,
):
    if issubclass(category, utilipyWarning):
        if (
            not issubclass(category, utilipyWarningVerbose)
            or conf.verbose_warnings
        ):
            print("utilipyWarning: " + str(message))
    else:
        print(warnings.formatwarning(message, category, filename, lineno))


warnings.showwarning = _warning  # TODO check how this is used


##############################################################################
# END
