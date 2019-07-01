#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Standard Import File
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
"""


##############################################################################
### IMPORTS

## General

## Custom
# from .. import ObjDict, LogFile

## Project-Specific

##############################################################################
### PARAMETERS

# _LOGFILE = LogFile(header=False)  # PrintLog, which is compatible with LogFile


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

    # autoreload extensions
    get_ipython().magic('load_ext autoreload')

    # set autoreload type
    get_ipython().magic(f'autoreload {1}')

    return
# /def


##############################################################################

# def aimport(module:str, autoreload:bool=True):  # FIXME
#     """jupyter magic aimport

#     Parameters
#     ----------
#     module : list of strs
#         the modules to be imported
#     autoreload : bool, optional  (default True)
#         whether the imported module is marked for autoreloading
#     """
#     assert isinstance(autoreload, bool)

#     if not autoreload:
#         module = '-' + module

#     get_ipython().magic(f'aimport {module}')

#     return
# # /def


# # ----------------------------------------------------------------------------

# def aimports(*modules, autoreload:bool=True):  # FIXME
#     """jupyter magic multiple aimport

#     Parameters
#     ----------
#     *modules : list of strs
#         the modules to be imported
#     autoreload : bool, list, optional  (default True)
#         whether the imported modules are marked for autoreloading
#         if its a list, it must be the same length as **modules*
#     """
#     if autoreload in (True, False):
#         autoreload = [autoreload] * len(modules)
#     elif len(autoreload) == len(modules):
#         pass
#     else:
#         raise ValueError('len(autoreload) != len(modules)')

#     for module in modules:
#         aimport(module, autoreload=autoreload)

#     return
# # /def

##############################################################################
### END
