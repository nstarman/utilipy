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

## Project-Specific
sys.path.insert(0, '../../src')


##############################################################################
### Parameters & Setup

# General
_PLOT = True                                # Plot the output

# Log file
_LOGFILE = open('./log.txt', 'w')
_VERBOSE = 0                                # Degree of verbosity

# ----------------------------------------------------------------------------
### Setup


##############################################################################
### Running the Script

_LOGFILE.write('Log \nthis is info')

##############################################################################
### Closing
_LOGFILE.close()
