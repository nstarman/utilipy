# -*- coding: utf-8 -*-

"""Warnings and Exceptions."""

__author__ = "Nathaniel Starkman"

__all__ = [
    "conf",
    # warning classes
    "utilipyWarning",
    "utilipyWarningVerbose",
    # functions
    "showwarning",
]

##############################################################################
# IMPORTS

# BUILT-IN
import sys
import typing as T
import warnings

# THIRD PARTY
from astropy import config as _config
from astropy.utils.exceptions import AstropyWarning

#############################################################################
# CONFIGURATION


class Conf(_config.ConfigNamespace):
    """Configuration parameters for :mod:`~utilipy.utils.exceptions`."""

    verbose_warnings = _config.ConfigItem(
        True,
        description="When True, use verbose `utilipy` warnings",
        cfgtype="boolean(default=True)",
    )


conf = Conf()


###############################################################################
# CODE
###############################################################################


class utilipyWarning(AstropyWarning):
    """:mod:`~utilipy` package warning."""


# /class


# ----------------------------------------------------------------------------


class utilipyWarningVerbose(utilipyWarning):
    """Verbose :mod:`~utilipy` warning.

    If used, the warning is verbose, regardless of the `conf` setting.

    """


# /class


# ----------------------------------------------------------------------------
# override built-in showwarning


def showwarning(
    message: T.Any,
    category: type = utilipyWarning,
    filename: str = "",
    lineno: int = -1,
    file: None = None,
    line: None = None,
):
    """Override :func:`~warnings.showwarning`.

    showwarning docs

        Write a warning to a file. The default implementation calls
        :func:`~warnings.formatwarning`(`message`, `category`, `filename`,
        `lineno`, `line`) and writes the resulting string to file, which
        defaults to :func:`~sys.stderr`. You may replace this function with
        any callable by assigning to :func:`~warnings.showwarning`. line is a
        line of source code to be included in the warning message; if line is
        not supplied, :func:`~warnings.formatwarning` will try to read the
        line specified by `filename` and `lineno`.

    Parameters
    ----------
    message : Any
    category : type, optional
    filename : str, optional
    lineno : int, optional
    file : file-type or None, optional
    line : str or None, optional

    """
    if file is None:
        file = sys.stderr

    # Three conditions for a non-verbose warning:
    #   1) utilipyWarning (or subclass)
    #   2) NOT utilipyWarningVerbose
    #   3) verbosity setting is OFF
    if (
        issubclass(category, utilipyWarning)
        and not issubclass(category, utilipyWarningVerbose)
        and not conf.verbose_warnings
    ):
        print(
            "utilipyWarning: " + str(message),
            file=file,
            flush=True,
        )

    # Normal warnings
    else:
        print(
            warnings.formatwarning(
                message=message,
                category=category,
                filename=filename,
                lineno=lineno,
                line=line,
            ),
            file=file,
            flush=True,
        )


# /def

warnings.showwarning = showwarning


##############################################################################
# END
