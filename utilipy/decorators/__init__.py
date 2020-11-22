# -*- coding: utf-8 -*-


"""Decorators."""


__all__ = [
    # modules
    "baseclass",
    "docstring",
    "func_io",
    "code_dev",
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
    # convenience
    "functools",
    "inspect",
    "wraps",
]


##############################################################################
# IMPORTS

# PROJECT-SPECIFIC
from ..utils import functools, inspect
from ..utils.functools import wraps
from . import baseclass, code_dev, docstring, func_io
from .baseclass import DecoratorBaseClass, classy_decorator
from .func_io import (
    boolDecorator,
    dtypeDecorator,
    dtypeDecoratorMaker,
    floatDecorator,
    intDecorator,
    ndarrayDecorator,
    ndfloat64Decorator,
    store_function_input,
    strDecorator,
)

from .func_io import add_folder_backslash  # dtype; standard types; numpy

##############################################################################
# END
