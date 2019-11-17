# -*- coding: utf-8 -*-

# Docstring and MetaData
"""Degree Decorator."""

__author__ = "Nathaniel Starkman"

#############################################################################
# IMPORTS

# GENERAL
import numpy as np
from functools import wraps

# PROJECT-SPECIFIC
from .._domain_factory import domain_factory


#############################################################################
# CODE
#############################################################################

def degreeDecorator(inDegrees=[], outDegrees=[], roof=False):
    """Decorator to transform angles from and to degrees if necessary

    Arguments
    ---------
    inDegrees: list
        list specifitying indices of angle arguments
        ex: [index, index, ...]
        can also include domain information with the index
            (index, lower, upper), where upper > lower
            domain must be in radians
        ex: [index, (index, lower, upper), ...]
    outDegrees: list
        same as inDegrees, but for function return

    HISTORY:

       ____-__-__ - Written - Bovy
       2019-03-02 - including domainDecorator & speedups - Nathaniel Starkman (UofT)

    """
    # speedup if no domain adjustments
    if all(map(np.isscalar, [*inDegrees, *outDegrees])):
        # (modified) old degree decorator
        def wrapper(func):
            @wraps(func)
            def wrapped(*args, **kwargs):
                isdeg = kwargs.get('degree', False)
                # PRE
                if isdeg:
                    args = [arg * np.pi / 180 if i in inDegrees else arg
                            for i, arg in enumerate(args)]

                # CALLING
                out = func(*args, **kwargs)

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

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            isdeg = kwargs.get('degree', False)

            # PRE
            newargs = list(args)
            for i, f in indegs:  # adjusting domain of in args
                if isdeg:  # deg -> rad
                    newargs[i] = f(args[i] * np.pi / 180.)
                else:  # already rad
                    newargs[i] = f(args[i])

            # CALLING
            out = func(*newargs, **kwargs)

            # POST
            for i, f in outdegs:
                if isdeg:
                    out[:, i] = f(out[:, i]) * 180 / np.pi
                else:
                    out[:, i] = f(out[:, i])

            return out
        # /def
        return wrapped
    # /def
    return wrapper
# /def
