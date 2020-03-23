#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   :
# AUTHOR  : Nathaniel Starkman
# PROJECT :
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Utils for paths."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL
from typing import Union
from pathlib import Path

# PROJECT-SPECIFIC


##############################################################################
# PARAMETERS


##############################################################################
# CODE


def get_absolute_path(path: Union[str, Path]) -> Union[str, Path]:
    """Get absolute path."""
    return Path(path).resolve()


# /def


def parent_file_directory(path: Union[str, Path]) -> Union[str, Path]:
    """Parent file directory."""
    return Path(path).parent


# /def

##############################################################################
# END
