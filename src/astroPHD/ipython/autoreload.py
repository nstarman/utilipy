#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""functions for working with autoreload extension.

set_autoreload
aimport

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General
from IPython import get_ipython

# Project-Specific
from ..util.logging import LogPrint

##############################################################################
# PARAMETERS

_LOGFILE = LogPrint(header=False, verbose=0)


##############################################################################
# CODE

def set_autoreload(reload_type: int=1):
    """Global imports setting.

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


# TODO support any list
def aimport(*modules, autoreload: (bool, list, tuple)=True):
    """Jupyter magic aimport.

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
        assert isinstance(reload_type, bool)

        if not reload_type:
            module = '-' + module  # mark for not autoreloading

        # import
        get_ipython().magic(f'aimport {module}')

    return
# /def


##############################################################################
# Setting State

if get_ipython() is not None:
    get_ipython().magic('load_ext autoreload')  # autoreload extensions
    set_autoreload(1)

##############################################################################
# END
