# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   :
# AUTHOR  :
# PROJECT :
#
# ----------------------------------------------------------------------------

"""**DOCSTRING**.

description

Routine Listings
----------------

"""

__author__ = ""
# __copyright__ = "Copyright 2019, "
# __credits__ = [""]
# __license__ = ""
# __version__ = "0.0.0"
# __maintainer__ = ""
# __email__ = ""
# __status__ = "Production"

# __all__ = [
#     ""
# ]


##############################################################################
# IMPORTS

# GENERAL
import sys
import warnings
import argparse
from typing import Optional

# CUSTOM

from utilipy import LogFile

# PROJECT-SPECIFIC


##############################################################################
# PARAMETERS

# General
_PLOT = True  # Plot the output

# Log file
_VERBOSE = 0  # Degree of verbosity
_LOGFILE = LogFile.open(
    f"./{__file__}.log", header="script", verbose=_VERBOSE  # File  # script header
)  # setting as default


##############################################################################
# CODE
##############################################################################


class ClassName(object):
    """Docstring for ClassName."""

    def __init__(self, arg):
        """Initialize class."""
        super().__init__()
        self.arg = arg


# /class


# ------------------------------------------------------------------------


def function():
    """Docstring."""
    pass


# /def


##############################################################################
# Command Line
##############################################################################


def make_parser(inheritable=False):
    """Expose parser for ``main``.

    Parameters
    ----------
    inheritable: bool
        whether the parser can be inherited from (default False).
        if True, sets ``add_help=False`` and ``conflict_hander='resolve'``

    Returns
    -------
    parser: ArgumentParser

    """
    parser = argparse.ArgumentParser(
        description="",
        add_help=~inheritable,
        conflict_handler="resolve" if ~inheritable else "error",
    )

    return parser


# /def


# ------------------------------------------------------------------------


def main(args: Optional[list] = None, opts: Optional[argparse.Namespace] = None):
    """Script Function.

    Parameters
    ----------
    args : list, optional
        an optional single argument that holds the sys.argv list,
        except for the script name (e.g., argv[1:])
    opts : Namespace, optional
        pre-constructed results of parsed args
        if not None, used ONLY if args is None

    """
    if opts is not None and args is None:
        pass
    else:
        if opts is not None:
            warnings.warn("Not using `opts` because `args` are given")
        parser = make_parser()
        opts = parser.parse_args(args)

    return


# /def


# ------------------------------------------------------------------------

if __name__ == "__main__":

    main(args=None, opts=None)  # all arguments except script name

# /if


##############################################################################
# END

_LOGFILE.close()
