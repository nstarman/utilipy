#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : lmfit
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""decorators for converting scipy residual functions to lmfit functions

TODO redo with my decorator method
"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General
from wrapt import ObjectProxy

# Custom
# from .. import ObjDict, LogFile

# Project-Specific

##############################################################################
# PARAMETERS

# _LOGFILE = LogFile(header=False)  # LogPrint, compatible with LogFile


##############################################################################
# CODE

class scipy_residual_to_lmfit(ObjectProxy):
    """decorator to make scipy residual functions compatible with lmfit
    (see https://lmfit.github.io/lmfit-py/fitting.html)

    Parameters
    ----------
    var_order : list of strs
        the variable order used by lmfit
        the strings are the names of the lmfit parameters
        must be in the same order as the scipy residual function

    Returns
    -------
    scipy_residual_to_lmfit : class
        internally constructed class

    Notes
    -----
    the function can be called as normal
    add a .lmfit function for use in lmfit minimizations
    see https://lmfit.github.io/lmfit-py/fitting.html
    ex:
        @scipy_residual_to_lmfit(['amp', 'phase', 'freq', 'decay'])
        def residual(vars, x, data, eps_data):
            amp, phase, freq, decay = vars
            ...
            return res

    TODO
    - since using ObjectProxy, make it compatible with bound functions
      see https://wrapt.readthedocs.io/en/latest/wrappers.html#function-wrappers
    """

    def __new__(cls, func=None, var_order: list=None):
        """
        """
        if var_order is None:
            raise ValueError('var_order cannot be None')

        self = super().__new__(cls)  # inherit class information

        # assigning documentation as function documentation
        self.__doc__ = func.__doc__

        # allowing scipy_residual_to_lmfit to act as a decorator
        if func is None:
            return self.decorator(var_order)
        return self
    # /def

    @classmethod
    def decorator(cls, var_order: list):
        """TODO
        """
        # @functools.wraps(cls)  # not needed when using ObjectProxy
        def wrapper(func):
            """scipy_residual_to_lmfit wrapper"""
            return cls(func, var_order=var_order)
        # /def

        return wrapper
    # /def

    def __init__(self, func, var_order: list):
        super().__init__(func)  # inializing function into wrapt.ObjectProxy
        self.var_order = var_order
        return
    # /def

    def lmfit(self, params, *args, **kwargs):
        vars = [params[n].value for n in self.var_order]
        return self.__wrapped__(vars, *args, **kwargs)
    # /def
# /class


##############################################################################
# END
