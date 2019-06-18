#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : inspect
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkython
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
from inspect import getfullargspec
from collections import namedtuple

## Custom
from . import ObjDict, LogFile

## Project-Specific

##############################################################################
### PARAMETERS

# _LOGFILE = LogFile(header=False)  # PrintLog, which is compatible with LogFile


##############################################################################
### Types

FullerArgSpec = namedtuple('FullerArgSpec',
                           ['args', 'defaultargs', 'argdefaults', 'varargs',
                            'kwonlyargs', 'kwonlydefaults', 'varkw',
                            'annotations'])


##############################################################################
### Functions

def getfullerargspec(func):
    """getfullerargspec

    fullargspec with separation of mandatory and optional arguments
    adds *defargs* which corresponds *defaults*

    Parameters
    ----------
    func : function
        the function to inspect

    Returns
    -------
    FullerArgSpec : namedtuple
        args             : the mandatory arguments
        defargs          : arguments with defaults
        defaults         : dictionary of defaults to defargs
        varargs          : variable arguments (*args)
        kwonlyargs       : key-word only arguments
        kwonlydefaults   : key-word only argmunent defaults
        varkw            : variable key-word arguments (**kwargs)
        annotations      : function annotations
    """
    spec = getfullargspec(func)

    if spec.defaults is not None:

        args = spec.args[:-len(spec.defaults)]
        defargs = spec.args[-len(spec.defaults):]
        defaults = {k: v for k, v in zip(defargs, spec.defaults)}

    else:
        args = spec.args
        defargs = None
        defaults = None

    return FullerArgSpec(args, defargs, defaults, spec.varargs,
                         spec.kwonlyargs, spec.kwonlydefaults, spec.varkw,
                         spec.annotations)
# /def


# --------------------------------------------------------------------------

##############################################################################
### END
