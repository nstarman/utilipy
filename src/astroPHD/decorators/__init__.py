#!/usr/bin/env python# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : decorator initialization file
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""initialization file for util.decorators."""

##############################################################################
# IMPORTS

# GENERAL

# PROJECT-SPECIFIC
from ..util import functools
from ..util.functools import wraps
from ..util import inspect

# base class
from .decoratorbaseclass import DecoratorBaseClass, classy_decorator

# data-type decorators
from .dtype_decorator import (
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

# bool array to index decorator
from .idx_decorator import idxDecorator


##############################################################################


def store_function_input(
    function=None, *, store_inputs=True, _doc_style="numpy", _doc_fmt=None
):
    """Docstring for decorator.

    Description of this decorator

    Parameters
    ----------
    function : types.FunctionType or None, optional
        the function to be decoratored
        if None, then returns decorator to apply.
    _get_inputs : bool, optional
        whether to return all the inputs to the function as a dictionary

    Returns
    -------
    wrapper : types.FunctionType
        wrapper for function
        does a few things
        includes the original function in a method `.__wrapped__`

    Other Parameters
    ----------------
    _doc_style: str or formatter, optional
        default 'numpy'
        parameter to `astroPHD.wraps`
    _doc_fmt: dict, optional
        default None
        parameter to `astroPHD.wraps`

    """
    if function is None:  # allowing for optional arguments
        return functools.partial(
            store_function_input,
            store_inputs=store_inputs,
            _doc_style=_doc_style,
            _doc_fmt=_doc_fmt,
        )

    sig = inspect.signature(function)

    @wraps(function, _doc_style=_doc_style, _doc_fmt=_doc_fmt)
    def wrapper(*args, store_inputs=store_inputs, **kw):
        """Wrapper docstring.

        Parameters
        ----------
        prints information about function
        store_inputs: bool
            whether to store function inputs in a BoundArguments instance
            default {store_inputs}

        """
        return_ = function(*args, **kw)
        if store_inputs:
            inputs = sig.bind_partial(*args, **kw)
            return return_, inputs
        else:
            return return_

    # /def

    return wrapper


# /def


##############################################################################
# END
