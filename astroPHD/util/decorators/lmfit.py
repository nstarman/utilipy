#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : lmfit
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkython
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""decorators for converting scipy residual functions to lmfit functions
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
from wrapt import ObjectProxy

## Custom
# from .. import ObjDict, LogFile

## Project-Specific

##############################################################################
### PARAMETERS

# _LOGFILE = LogFile(header=False)  # PrintLog, compatible with LogFile


##############################################################################
### CODE

def scipy_residual_to_lmfit(var_order:list):
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
            def res
    
    TODO:
    - make this a class so that it supports
      scipy_residual_to_lmfit(func, var_order)
      then it can be used to replace functions like
      func = scipy_residual_to_lmfit(func, var_order)
    - since using ObjectProxy, make it compatible with bound functions
      see https://wrapt.readthedocs.io/en/latest/wrappers.html#function-wrappers
    - not have to define a class inside this function
    """

    class scipy_residual_to_lmfit(ObjectProxy):
        """

        Parameters
        ----------
        wrapped : function

        defaulted
        ---------
        var_order : list
            the variable order used by lmfit
        """

        def __init__(self, wrapped):
            super().__init__(wrapped)
            self.var_order = var_order
            return
        # /def

        def __call__(self, vars, *args, **kwargs):
            return self.__wrapped__(vars, *args, **kwargs)
        # /def

        def lmfit(self, params, *args, **kwargs):
            vars = [params[n].value for n in self.var_order]
            return self.__wrapped__(vars, *args, **kwargs)
        # /def
    
    return scipy_residual_to_lmfit
# /def


##############################################################################
### END
