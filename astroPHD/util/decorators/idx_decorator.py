#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : boolean to index decorator
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
"""


##############################################################################
### IMPORTS

## General
import numpy as np
from functools import wraps

## Project-Specific


##############################################################################
### CODE

class idxDecorator():
    """decorator to control whether to return bool array or indices
    for functions which return bool arrays
    adds *as_ind* as a kwarg to decorated function

    Parameters
    ----------
    func : function or None, optional  (defualt None)
        the decorated function
        optional so idxDecorator can act as a decorator factory (see example)
    as_ind : bool, optional  (default False)
        whether to return bool array or the indices (where(bool array == True))
        sets the default behavior for the wrapped fnction *func*


    Parameters Added to Function
    ----------------------------
    as_ind : bool  (default False)
        if true: return np.where(bool array == True)

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
            return x < 1

    >>> func1(x)  # calling normally
    [True, False]
    >>> func1(as_ind=True)  # using added kwarg
    array([0])

    Set a Different Default:

    >>> @idxDecorator(as_ind=True)
    >>> def func2(x):
            return x < 1

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
        """make new instance of idxDecorator
        if no function, return decorator generator
        else return decorated function

        does not pass to __init__ after
        """
        # making instance of self
        self = super().__new__(cls)

        # adding as_ind parameter default
        self.as_ind = as_ind

        # if no function, return decorator generator
        # else return decorated function
        if func is None:       # decorator generator
            return self
        else:                  # decorated function
            return self(func)  
        # /def

    def __call__(self, wrapped_func):
        # function wrapper

        @wraps(wrapped_func)
        def wrapper(*args, as_ind=self.as_ind, **kwargs):

            return_ =  np.asarray(wrapped_func(*args, **kwargs))
            
            if as_ind:  # return indices
                return np.where(return_ == True)
            else:       # return bool array
                return return_
        # /def

        wrapper.__doc__ = wrapped_func.__doc__
        # TODO modify wrapped func documentation to include as_ind
        return wrapper
    # /def

##############################################################################
### END