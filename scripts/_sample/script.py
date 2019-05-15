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
"""script: **DOCSTRING**
WARN: a version using the python logger is under development
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### Imports

## General
import os, sys, time, pdb, copy
# import numpy as np

## Astropy
# from astropy import units as u

## Custom
sys.path.insert(0, '../../')
# from src.util.logging import LogFile
from src.util.logging._logfile_loguru import LogFile

## Project-Specific


##############################################################################
### Parameters & Setup

# General
_PLOT = True                                # Plot the output

# Log file
_LOGFILE = LogFile.open('./log.txt', 'w',   # File
                        header='script')
_VERBOSE = 0                                # Degree of verbosity

# ----------------------------------------------------------------------------
### Setup


##############################################################################
### Running the Script

_LOGFILE.write('Log \nthis is info')

_LOGFILE.info('Log this info', 'and this', 'and this', sep='__')

##############################################################################
### Closing
_LOGFILE.close()
