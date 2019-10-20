#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : 
# AUTHOR  : Nathaniel Starkman
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""docstring decorators
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
import functools

## Project-Specific
from .decoratorbaseclass import DecoratorBaseClass


##############################################################################
### CODE

class replace_docstring(DecoratorBaseClass):
    """Replace a function docstring withf
    """

    def _doc_func(self, docstring):
        return self.docstring

    def __call__(self, wrapped_function):
        """Construct a function wrapper."""
        @functools.wraps(wrapped_function)
        def wrapper(*func_args, **func_kwargs):
            return wrapped_function(*func_args, **func_kwargs)
        # /def

        return super().__call__(wrapper)
    # /def
        

##############################################################################
### END