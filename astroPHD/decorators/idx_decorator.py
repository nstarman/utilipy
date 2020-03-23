# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : boolean to index decorator
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""index decorator."""


##############################################################################
# IMPORTS

# GENERAL

from types import FunctionType
from typing import Any, Union, Callable, Optional
import numpy as np

# PROJECT-SPECIFIC

from ..util import functools


##############################################################################
# CODE


def idxDecorator(
    function: Optional[Callable] = None, *, as_ind: bool = False,
    _doc_fmt: Optional[dict] = None,  # ibid
    _doc_style: Union[str, FunctionType, None] = None,  # ibid
) -> Callable:
    """Control whether to return boolean array or indices.

    for functions which return bool arrays
    adds `as_ind` as a kwarg to decorated function

    Parameters
    ----------
    function : types.FunctionType or None, optional
        (default None)
        the function to be decoratored
        if None, then returns decorator to apply.
    as_ind : bool, optional
        (default False)
        whether to return bool array or indices (``where(bool array == True)``)
        sets the default behavior for the wrapped function `func`

    Returns
    -------
    wrapper : types.FunctionType
        wrapper for function
        includes the original function in a method `.__wrapped__`

    Notes
    -----
    Add `as_ind` to the function signature and docstring.

    Examples
    --------
    Use the Standard Decorator:

    >>> @idxDecorator
    >>> def func1(x):
    ...     return x < 1

    >>> func1(x)  # calling normally
    [True, False]
    >>> func1(as_ind=True)  # using added kwarg
    array([0])

    Set a Different Default:

    >>> @idxDecorator(as_ind=True)
    >>> def func2(x):
    ...     return x < 1

    >>> func2(x)  # calling normally
    array([0])
    >>> func2(as_ind=False)  # using added kwarg
    array([True, False])

    Making a New Decorator:

    >>> trueidxdec = idxDecorator(as_ind=True)
    >>> @trueidxdec
    >>> def func3(x):
            return x < 1
    >>> func3(x)  # calling normally
    array([0])
    >>> func3(as_ind=False)  # using added kwarg
    array([True, False])

    Wrapping Existing Functions

    >>> def func(x):
            return x < 1
    >>> newfunc = idxDecorator(func, as_ind=True)
    >>> newfunc(x)
        array([0])
    >>> newfunc(x)
        array([True, False])

    """
    if function is None:  # allowing for optional arguments
        return functools.partial(idxDecorator, as_ind=as_ind)

    @functools.wraps(function, _doc_fmt=_doc_fmt, _doc_style=_doc_style)
    def wrapper(*args: Any, as_ind: bool = as_ind, **kwargs: Any) -> Any:
        """Docstring for wrapper.

        Other Parameters
        ----------------
        as_ind: bool
            (default {as_ind})
            whether to return a boolean array, or array of indices.

        """
        return_ = function(*args, **kwargs)

        if as_ind:  # return indices
            return np.where(np.asarray(return_) == True)
        else:
            return return_

    # /def

    return wrapper


# /def


##############################################################################
# END
