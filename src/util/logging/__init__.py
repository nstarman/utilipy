#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : logging initialization file
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""initialization file for logging
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### Imports

## General
import logging

## Custom
try:
    import loguru

except ImportError as e:
    _LOGURU = False
    print(e)
    print('using standard logging instead')

    from ._logfile_logger import LogFile as LoggerFile  # TODO better name

else:
    _LOGURU = True
    from ._logfile_loguru import LogFile as LoggerFile  # TODO better name


from ._logfile_print import LogFile

## Project-Specific


##############################################################################
# Code
