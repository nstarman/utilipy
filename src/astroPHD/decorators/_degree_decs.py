# -*- coding: utf-8 -*-

# Docstring and MetaData
"""Degree Decorator."""

__author__ = "Nathaniel Starkman"

#############################################################################
# IMPORTS

# GENERAL
from typing import Any, Union, Callable
import numpy as np
from functools import wraps

# PROJECT-SPECIFIC
from ..util._domain_factory import domain_factory


#############################################################################
# CODE
#############################################################################

def degreeDecorator(inDegrees: list=[], outDegrees: list=[],
                    roof: bool=False) -> Callable:
    """Decorator to transform angles from and to degrees if necessary

    Parameters
    ----------
    inDegrees: list
        list specifitying indices of angle arguments
        ex: [index, index, ...]
        can also include domain information with the index
            (index, lower, upper), where upper > lower
            domain must be in radians
        ex: [index, (index, lower, upper), ...]
    outDegrees: list
        same as inDegrees, but for function return

    """
    # speedup if no domain adjustments
    if all(map(np.isscalar, [*inDegrees, *outDegrees])):
        # (modified) old degree decorator
        def wrapper(function: Callable) -> Callable:
            @wraps(function)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                isdeg: bool = kwargs.get('degree', False)
                # PRE
                if isdeg:
                    _args: list = [arg * np.pi / 180 if i in inDegrees else arg
                                   for i, arg in enumerate(args)]

                # CALLING
                out = function(*_args, **kwargs)

                # POST
                if isdeg:
                    for i in outDegrees:
                        out[:, i] *= 180. / np.pi
                return out
            # /def
            return wrapped
        # /def
        return wrapper
    # /def

    # else:  # need to adjust domains

    indegs = [(x, lambda x: x) if np.isscalar(x)
              else (x[0], domain_factory(*x[1:], roof=roof))
              for x in inDegrees]
    outdegs = [(x, lambda x: x) if np.isscalar(x)
               else (x[0], domain_factory(*x[1:], roof=roof))
               for x in outDegrees]

    def wrapper(function: Callable):
        @wraps(function)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            isdeg: bool = kwargs.get('degree', False)

            # PRE
            newargs: list = list(args)
            i: int
            func: Callable
            for i, func in indegs:  # adjusting domain of in args
                if isdeg:  # deg -> rad
                    newargs[i] = func(args[i] * np.pi / 180.)
                else:  # already rad
                    newargs[i] = func(args[i])

            # CALLING
            out: Any = function(*newargs, **kwargs)

            # POST
            for i, func in outdegs:
                if isdeg:
                    out[:, i] = func(out[:, i]) * 180 / np.pi
                else:
                    out[:, i] = func(out[:, i])

            return out
        # /def
        return wrapped
    # /def
    return wrapper
# /def

#############################################################################
# END
