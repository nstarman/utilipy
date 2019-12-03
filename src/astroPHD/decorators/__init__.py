#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : decorator initialization file
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""initialization file for util.decoraytors
"""

##############################################################################
### IMPORTS

## General

## Project-Specific
# data-type decorators
from .dtype_decorator import (
    dtypeDecorator,
    dtypeDecoratorMaker,
    # standard types
    intDecorator,
    floatDecorator,
    strDecorator,
    boolDecorator,
    # numpy
    ndarrayDecorator,
    ndfloat64Decorator,
)

# bool array to index decorator
from .idx_decorator import idxDecorator


##############################################################################
### END
