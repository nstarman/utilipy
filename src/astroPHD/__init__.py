# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : astroPHD initialization file
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Main initialization file."""

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2019, "
__credits__ = [""]
__license__ = "GPL3"
__version__ = "0.1.1"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"

##############################################################################
# IMPORTS

# Project-Specific
# import top level packages
from . import (
    astronomy,
    community,
    constants,
    data_utils,
    decorators,
    fitting,
    imports,
    ipython,
    math,
    plot,
    units,
    util,
)

# import commonly used functions
from .util.logging import LogFile
from .util.collections import ObjDict
from .util.functools import wraps

# configuration
from . import config


#############################################################################
# HELP FUNCTION


def help() -> None:
    """`astroPHD` help function.

    This function is a work in progress

    """
    print("This function is a work in progress")

    print("".join(["-"] * 79))
    ipython.help()

    return None


# /def

#############################################################################
# END
