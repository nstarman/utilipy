#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : autoreload
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""functions for working with autoreload extension
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General

## Custom
from ..util.logging import LogPrint

## Project-Specific

##############################################################################
### PARAMETERS

_LOGFILE = LogPrint(header=False, verbose=0)

get_ipython().magic('load_ext autoreload')  # autoreload extensions


##############################################################################
### CODE

def set_autoreload(reload_type:int=1):
    """global imports setting

    Parameters
    ----------
    reload_type : int
        0: Disable automatic reloading.
        1: Reload all modules imported with %aimport every time
           before executing the Python code typed.
        2: Reload all modules (except those excluded by %aimport)
           every time before executing the Python code typed.
    """

    # set autoreload type
    get_ipython().magic(f'autoreload {reload_type}')

    _LOGFILE.write(f'set autoreload to {reload_type}')

    return
# /def


##############################################################################


def aimport(*modules, autoreload: (bool, list, tuple)=True):  # TODO support any list
    """jupyter magic aimport

    Parameters
    ----------
    *modules : list of strs
        the modules to be imported
    autoreload : bool, list, optional  (default True)
        whether the imported modules are marked for autoreloading
        if its a list, it must be the same length as **modules*
    """
    # making autoreload compatible with modules
    if isinstance(autoreload, bool):
        autoreload = [autoreload] * len(modules)
    elif len(autoreload) == len(modules):  # any list
        pass
    else:
        raise ValueError('len(autoreload) != len(modules)')

    for module, reload_type in zip(modules, autoreload):
        # testing correct data types
        assert isinstance(module, str)
        assert isinstance(autoreload, bool)

        if not reload_type:
            module = '-' + module  # mark for not autoreloading

        # import
        get_ipython().magic(f'aimport {module}')

    return
# /def


##############################################################################
### END
