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
"""
## General
pathlib, .Path

## Custom
get_absolute_path
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
import pathlib
from pathlib import Path

## Custom

## Project-Specific


##############################################################################
### PARAMETERS


##############################################################################
### CODE

def get_absolute_path(path:str) -> Path:
    """
    """

    return Path(path).resolve()
# /def


def parent_file_directory(path:str) -> Path:
    """
    """

    path = Path(path)
    return path.parent
# /def

##############################################################################
### END
