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
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### Imports

## General
import os, sys, time, pdb, copy
from loguru import logger
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
# _LOGFILE = open('./log.txt', 'w')           # Log file
_LOGFILE = logging.getLogger(__name__)
_LOGFILE.addHandler(logging.NullHandler())
_LOGFILE.setLevel(logging.INFO)

# logger.basicConfig(filename='./log.txt', level=logging.INFO)
_VERBOSE = 0                                # Degree of verbosity

# ----------------------------------------------------------------------------
### Setup


##############################################################################
### Running the Script

_LOGFILE.info('Logg \n this is info')

##############################################################################
### Closing
# _LOGFILE.close()
