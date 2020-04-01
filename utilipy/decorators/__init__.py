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

from typing import Callable, Dict, Any

from astropy.utils.decorators import sharedmethod  # replaces semistaticmethod


# PROJECT-SPECIFIC

from ..utils import functools
from ..utils.functools import wraps
from ..utils import inspect

# base class
from .baseclass import DecoratorBaseClass, classy_decorator

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
# from .idx_decorator import idxDecorator


##############################################################################


def store_function_input(
    function: Callable = None,
    *,
    store_inputs: bool = True,
    _doc_style: str = "numpy",
    _doc_fmt: Dict[str, Any] = {}
):
    """Store Function Inputs.

    Store the function inputs as a BoundArguments.

    Parameters
    ----------
    function : Callable or None, optional
        the function to be decoratored
        if None, then returns decorator to apply.
    store_inputs : bool, optional
        whether to return all the inputs to the function as a dictionary

    Returns
    -------
    wrapper : Callable
        wrapper for function
        does a few things
        includes the original function in a method `.__wrapped__`

    Other Parameters
    ----------------
    _doc_style: str or formatter, optional
        default 'numpy'
        parameter to `utilipy.wraps`
    _doc_fmt: dict, optional
        default None
        parameter to `utilipy.wraps`

    """
    if function is None:  # allowing for optional arguments
        return functools.partial(
            store_function_input,
            store_inputs=store_inputs,
            _doc_style=_doc_style,
            _doc_fmt=_doc_fmt,
        )

    sig = inspect.fuller_signature(function)
    _doc_fmt["wrapped_function"] = function.__name__

    @wraps(function, _doc_style=_doc_style, _doc_fmt=_doc_fmt)
    def wrapper(*args, store_inputs: bool = store_inputs, **kw):
        """Wrapper docstring.

        Parameters
        ----------
        store_inputs: bool
            whether to store function inputs in a BoundArguments instance
            default {store_inputs}

        Returns
        -------
        inputs: BoundArguments
            the inputs to ``{wrapped_function}``
            only returned if `store_inputs` is True
            other returned values are in now in a tuple

        """
        return_ = function(*args, **kw)

        if store_inputs:
            inputs = sig.bind_partial(*args, **kw)  # make BoundArguments
            inputs.apply_defaults()  # get default values from function
            return return_, inputs
        else:
            return return_

    # /def

    return wrapper


# /def


# ------------------------------------------------------------------------


def add_folder_backslash(
    function=None, *, arguments=[], _doc_style="numpy", _doc_fmt={}
):
    """Add backslashes to str arguments.

    For use in ensuring directory filepaths end in '/'

    Parameters
    ----------
    function : Callable or None, optional
        the function to be decoratored
        if None, then returns decorator to apply.
    arguments : list of strings, optional
        arguments to which to append '/', if not already present
        strings are names of arguments

    Returns
    -------
    wrapper : Callable
        wrapper for function
        does a few things
        includes the original function in a method `.__wrapped__`

    Other Parameters
    ----------------
    _doc_style: str or formatter, optional
        default 'numpy'
        parameter to `utilipy.wraps`
    _doc_fmt: dict, optional
        default None
        parameter to `utilipy.wraps`

    """
    if function is None:  # allowing for optional arguments
        return functools.partial(
            add_folder_backslash,
            arguments=arguments,
            _doc_style=_doc_style,
            _doc_fmt=_doc_fmt,
        )

    @wraps(function, _doc_style=_doc_style, _doc_fmt=_doc_fmt)
    def wrapper(*args, **kw):
        """Wrapper docstring.

        Parameters
        ----------
        store_inputs: bool
            whether to store function inputs in a BoundArguments instance
            default {store_inputs}

        TODO
        ----
        need to do by inspect, since can pass args as kwargs

        """
        args = list(args)
        for itm in arguments:
            if isinstance(itm, int):
                # print('TODO fix')
                if not args[itm].endswith("/"):
                    args[itm] = args[itm] + "/"
            elif isinstance(itm, str):
                if not kw[itm].endswith("/"):
                    kw[itm] = kw[itm] + "/"
            else:
                raise TypeError("elements of `args` must be int or str")

        return function(*args, **kw)

    # /def

    return wrapper


# /def


##############################################################################
# END
