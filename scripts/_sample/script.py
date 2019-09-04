#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   :
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""script: **DOCSTRING**
WARN: a version using the python logger is under development
"""

__author__ = "AUTHOR"

##############################################################################
### Imports

## General
import os, sys, time, pdb, copy
# import numpy as np

## Astropy
# from astropy import units as u

## Custom

## Project-Specific
sys.path.insert(0, '../../')
from src.util.logging import LogFile


##############################################################################
### Parameters & Setup

# General
_PLOT = True                                # Plot the output

# Log file
_VERBOSE = 0  # Degree of verbosity
_LOGFILE = LogFile.open(f'./{__file__}.log',  # File
                        header='script',  # script header
                        verbose=_VERBOSE)  # setting as default


# ----------------------------------------------------------------------------
### Setup


##############################################################################
### Running the Script

_LOGFILE.write('Log this info', 'and this', 'and this', sep='__')

##############################################################################
### Closing
_LOGFILE.close()
