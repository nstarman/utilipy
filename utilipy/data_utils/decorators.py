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

import sys
from typing import Any, Union, Callable, Optional
from typing_extensions import Literal
import numpy as np


# PROJECT-SPECIFIC

from ..utils import functools


##############################################################################
# PARAMETERS

# Windows prints numpy differently. Numpy outputs need to be ignored.
# TODO, a better platform-specific fix for numpy.
if sys.platform.startswith("win"):
    __doctest_skip__ = ["idxDecorator"]


##############################################################################
# CODE
##############################################################################


def idxDecorator(
    function: Optional[Callable] = None,
    *,
    as_ind: Union[bool, Literal["flatten"]] = False,
    _doc_fmt: Optional[dict] = None,  # ibid
    _doc_style: Union[str, Callable, None] = None,  # ibid
) -> Callable:
    """Control whether to return boolean array or indices.

    for functions which return bool arrays
    adds `as_ind` as a kwarg to decorated function

    Parameters
    ----------
    function : types.Callable or None, optional
        (default None)
        the function to be decoratored
        if None, then returns decorator to apply.
    as_ind : bool of "flatten", optional
        (default False)
        whether to return bool array or indices
        (``where(bool array == np.True_)``)
        if "flatten", flattens a nested list with only 1 element
        ie ([0], ) -> [0]
        sets the default behavior for the wrapped function `func`

    Returns
    -------
    wrapper : types.Callable
        wrapper for function
        includes the original function in a method `.__wrapped__`

    Other Parameters
    ----------------
    _doc_fmt : dict, optional
        docstring formatter
        argument into utilipy.functools.wraps
    _doc_style : str or Callable, optional
        docstring style
        argument into utilipy.functools.wraps

    Notes
    -----
    Adds `as_ind`, `_flatten` and other parameters to the function
    signature and docstring.

    Examples
    --------
    Use the Standard Decorator:

    >>> x = np.array([0, 2])
    >>> @idxDecorator
    ... def func1(x):
    ...     return x < 1

    calling normally
    >>> func1(x) # doctest: +SKIP
    array([ True, False], dtype=bool))

    using added kwarg
    >>> func1(x, as_ind=True)
    (array([0]),)

    and flattening
    >>> func1(x, as_ind="flatten")
    array([0])

    Set a Different Default:

    >>> @idxDecorator(as_ind=True)
    ... def func2(x):
    ...     return x < 1

    >>> func2(x)
    (array([0]),)

    >>> func2(x, as_ind=False) # doctest: +SKIP
    array([ True, False])

    Making a New Decorator:

    >>> trueidxdec = idxDecorator(as_ind="flatten")
    >>> @trueidxdec
    ... def func3(x):
    ...     return x < 1
    >>> func3(x)
    array([0])
    >>> func3(x, as_ind=False) # doctest: +SKIP
    array([ True, False])

    Wrapping Existing Functions

    >>> def func(x):
    ...     return x < 1
    >>> newfunc = idxDecorator(func, as_ind=True)
    >>> newfunc(x)
    (array([0]),)
    >>> newfunc(x, as_ind=False) # doctest: +SKIP
    array([ True, False])

    """
    if function is None:  # allowing for optional arguments
        return functools.partial(idxDecorator, as_ind=as_ind)

    @functools.wraps(function, _doc_fmt=_doc_fmt, _doc_style=_doc_style)
    def wrapper(*args: Any, as_ind: bool = as_ind, **kwargs: Any) -> Any:
        """Docstring for wrapper.

        Other Parameters
        ----------------
        as_ind : bool or "flatten", optional
            (default {as_ind})
            whether to return a boolean array, or array of indices.

        """
        return_ = function(*args, **kwargs)

        # determine whether to return indices or bool array
        if as_ind:  # works for bool or full str

            # get the indices
            return_ = np.where(np.asarray(return_) == np.True_)

            # determine whether to return as-is, or flatten
            if as_ind == "flatten":
                if len(return_) == 1:  # nested list with only 1 element
                    return return_[0]
                else:  # not a valid option
                    raise ValueError
            # do not flatten
            else:
                return return_

        # return a bool array
        else:
            return return_

    # /def

    return wrapper


# /def


##############################################################################
# END
