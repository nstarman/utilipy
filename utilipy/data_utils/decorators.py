# -*- coding: utf-8 -*-

"""`data_util` decorators."""


##############################################################################
# IMPORTS

# BUILT-IN
import sys
import typing as T

# THIRD PARTY
import numpy as np
from typing_extensions import Literal

# PROJECT-SPECIFIC
from utilipy.utils import functools

##############################################################################
# PARAMETERS

# Windows prints numpy differently. Numpy outputs need to be ignored.
# TODO: a better platform-specific fix for numpy.
if sys.platform.startswith("win"):
    __doctest_skip__ = ["idxDecorator"]


##############################################################################
# CODE
##############################################################################


def idxDecorator(
    function: T.Optional[T.Callable] = None,
    *,
    as_ind: T.Union[bool, Literal["flatten"]] = False,
    _doc_fmt: T.Optional[dict] = None,  # ibid
    _doc_style: T.Union[str, T.Callable, None] = None,  # ibid
) -> T.Callable:
    """Control whether to return boolean array or indices.

    for functions which return bool arrays
    adds `as_ind` as a kwarg to decorated function

    Parameters
    ----------
    function : Callable, optional
        (default None)
        the function to be decoratored
        if None, then returns decorator to apply.
    as_ind : bool or "flatten", optional
        (default False)
        whether to return bool array or indices
        (``where(bool array == np.True_)``)
        if "flatten", flattens a nested list with only 1 element
        ie ([0], ) -> [0]
        sets the default behavior for the wrapped `function`

    Returns
    -------
    wrapper : Callable
        wrapper for `function`
        includes the original function in a method ``.__wrapped__``

    Other Parameters
    ----------------
    _doc_fmt : dict, optional
        docstring formatter
        argument into :func:`~utilipy.utils.functools.wraps`
    _doc_style : str or Callable, optional
        docstring style
        argument into :func:`~utilipy.utils.functools.wraps`

    Notes
    -----
    Adds `as_ind` and other parameters to the function signature and docstring.

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
        return functools.partial(
            idxDecorator,
            as_ind=as_ind,
            _doc_fmt=_doc_fmt,
            _doc_style=_doc_style,
        )

    @functools.wraps(function, _doc_fmt=_doc_fmt, _doc_style=_doc_style)
    def wrapper(
        *args: T.Any, as_ind: bool = as_ind, **kwargs: T.Any
    ) -> T.Sequence:
        """Index-decorator wrapper docstring, overwritten by `function`.

        Other Parameters
        ----------------
        as_ind : bool or "flatten", optional
            (default {as_ind})
            whether to return a boolean array, or array of indices.

        Raises
        ------
        `~ValueError`
            if `as_ind` is "flatten" and cannot be flattened (len > 1)

        """
        # Step 1: call function
        bool_arr = function(*args, **kwargs)

        # Step 2:  determine whether to return indices or bool array
        if as_ind:  # works for bool or full str
            # get the indices
            inds = np.nonzero(np.asarray(bool_arr) == np.True_)

            # determine whether to return as-is, or flatten
            if as_ind == "flatten":
                if len(inds) == 1:  # nested list with only 1 element
                    return inds[0]
                else:  # not a valid option
                    raise ValueError
            else:  # do not flatten
                return inds

        # return a bool array
        return bool_arr

    # /def

    return wrapper


# /def


##############################################################################
# END
