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
"""**DOCSTRING**
"""

__author__ = "Nathaniel Starkman"
# __copyright__ = "Copyright 2018, "
# __credits__ = [""]
# __license__ = "GPL3"
# __version__ = "0.0.0"
# __maintainer__ = "Nathaniel Starkman"
# __email__ = "n.starkman@mail.utoronto.ca"
# __status__ = "Production"


##############################################################################
### IMPORTS

## General

## Custom

## Project-Specific

##############################################################################
### PARAMETERS


##############################################################################
### CODE

def current_file_directory(__file__):
    s = __file__.split('/')
    s = '/'.join(s[:-1])
    return s

##############################################################################
### END
