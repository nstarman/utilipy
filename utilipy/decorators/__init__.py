# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Decorators
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Decorators."""


__all__ = [
    # defined here
    "store_function_input",
    "add_folder_backslash",
    # baseclass
    "DecoratorBaseClass",
    "classy_decorator",
    # data-type decorators
    "dtypeDecorator",
    "dtypeDecoratorMaker",
    "intDecorator",
    "floatDecorator",
    "strDecorator",
    "boolDecorator",
    "ndarrayDecorator",
    "ndfloat64Decorator",
]

##############################################################################
# IMPORTS

# GENERAL

from astropy.utils.decorators import sharedmethod  # replaces semistaticmethod


# PROJECT-SPECIFIC

from ..utils import functools
from ..utils.functools import wraps
from ..utils import inspect

# base class
from .baseclass import DecoratorBaseClass, classy_decorator

# data-type decorators
from .func_io import (
    store_function_input,
    add_folder_backslash,
    # dtype
    dtypeDecorator,
    dtypeDecoratorMaker,
    # standard types
    intDecorator,
    floatDecorator,
    strDecorator,
    boolDecorator,
    # numpy
    ndarrayDecorator,
    ndfloat64Decorator,
)

# top-level
from . import baseclass, docstring, func_io


##############################################################################
# END
