#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : domaian decorators
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""initialization file for domain decorators
"""

__author__ = "Nathaniel Starkman"

##############################################################################
# IMPORTS

# GENERAL
from typing import Any, Union, Callable, Sequence

# PROJECT-SPECIFIC
from ..util._domain_factory import domain_factory
from ..util.functools import wraps

#############################################################################
# CODE


def domainDecorator(
    inDomains: Sequence, outDomains: Sequence, roof: bool = False
) -> Callable:
    """Decorator to ensure numbers are in the correct domain.

    Parameters
    ----------
    inDomains:
        (index, (lower, upper)), where upper > lower
        [(0, 0, np.pi), (1, -np.pi/2, np.pi/2),]
    outDomains
    """
    indoms = [(i, domain_factory(*dom, roof=roof)) for i, *dom in inDomains]

    outdoms = [(i, domain_factory(*dom, roof=roof)) for i, *dom in outDomains]

    def wrapper(function: Callable) -> Callable:
        @wraps(function)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            newargs = list(args)
            for i, f in indoms:  # adjusting domain of in-args
                newargs[i] = f(args[i])

            out = function(*newargs, **kwargs)  # falling wrapped func

            for i, f in outdoms:  # adjusting domain of out args
                out[:, i] = f(out[:, i])

            return out

        # /def
        return wrapped

    # /def
    return wrapper


# /def


def domainMapDecorator(
    inDomains: Sequence, outDomains: Sequence, roof: bool = False, usenp: bool = True
) -> Callable:
    """Decorator to ensure numbers are in the correct domain.

    format: (index, (lower, upper)), where upper > lower
    ex: inDomains = [(0, 0, np.pi), (1, (-np.pi/2, np.pi/2)),]

    HISTORY:

       2019-03-02 - Written - Nathaniel Starkman (UofT)

    TODO better name
    """
    indoms = [(i, domain_factory(*dom, roof=roof, getnp=True)) for i, *dom in inDomains]
    nps = [0] * len(inDomains)  # number of periods

    outdoms = [
        (i, domain_factory(*dom, roof=roof, getnp=False)) for i, *dom in outDomains
    ]

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            newargs = list(args)
            for i, f in indoms:  # adjusting domain of in-args
                newargs[i], nps[i] = f(args[i])

            out: Any = func(*newargs, **kwargs)  # falling wrapped func

            if usenp:
                for (i, f), np in zip(outdoms, nps):  # adjusting domain of out args
                    out[:, i] = f(out[:, i], np=np)
            else:
                for i, f in outdoms:  # adjusting domain of out args
                    out[:, i] = f(out[:, i])
            return out

        # /def
        return wrapped

    # /def
    return wrapper


# /def

#############################################################################
# DONE
