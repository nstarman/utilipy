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
import numpy as np
from functools import wraps


##############################################################################
# CODE

class idxDecorator():
    """Decorator to control whether to return bool array or indices.

    for functions which return bool arrays
    adds *as_ind* as a kwarg to decorated function

    Parameters
    ----------
    func : function or None, optional
        (defualt None)
        the decorated function
        optional so idxDecorator can act as a decorator factory (see example)
    as_ind : bool, optional
        (default False)
        whether to return bool array or the indices (where(bool array == True))
        sets the default behavior for the wrapped fnction *func*


    Notes
    -----
    Add `as_ind` to the function signature and docstring.

    Returns
    -------
    if func is None:
        self : instance of idxDecorator
            a decorator than can be applied to functions
    else:
        self(func) : function
            the decorated function

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

    def __new__(cls, func=None, as_ind=False):
        """Make new instance of idxDecorator.

        if no function, return decorator generator
        else return decorated function

        does not pass to __init__ after

        """
        # making instance of self
        self = super().__new__(cls)

        # if no function, return decorator generator
        # else return decorated function
        if func is not None:       # decorator generator
            self.__init__(as_ind=as_ind)
            return self(func)
        # else
        return self
        # /def

    def __init__(self, func=None, as_ind=False):
        """Initialize decorator class."""
        # adding as_ind parameter default
        self.as_ind = as_ind
    # /return

    def __call__(self, wrapped_func):
        """Decorator."""
        # function wrapper

        @wraps(wrapped_func)
        def wrapper(*args, as_ind=self.as_ind, **kwargs):

            return_ = wrapped_func(*args, **kwargs)

            if as_ind:  # return indices
                return np.where(np.asarray(return_) == True)
            # else
            return return_
        # /def

        # wrapper.__doc__ = wrapped_func.__doc__
        # TODO modify wrapped func documentation to include as_ind
        return wrapper
    # /def
# /class

##############################################################################
# END
