# -*- coding: utf-8 -*-
# see LICENSE.rst

"""astroPHD."""

__author__ = "Nathaniel Starkman"

__all__ = []


##############################################################################
# IMPORTS

# Packages may add whatever they like to this file, but
# should keep this content at the top.
from ._astropy_init import *   # noqa

# PROJECT-SPECIFIC
# import top level packages
from . import (
    astronomy,
    constants,
    data_utils,
    decorators,
    extern,
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
