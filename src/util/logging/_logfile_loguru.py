#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : logging with loguru
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""functions for logging with loguru

TODO make custom {level} that is blank
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### Imports

# General
import sys

# Loguru
from loguru import logger

# Custom
from ._logfile_print import LogFile as _LogFile

# Project-Specific


##############################################################################
### Setup


_READMODES = ('r', )
_WRITEMODES = ('w', 'x', 'a', 'b')
_READWRITEMODES = ('+', )


##############################################################################
### Code

class LogFile(_LogFile):
    """docstring for LogFile
    """

    def __init__(self, filename, mode='w', buffering=-1, encoding=None,
                 errors=None, newline=None, closefd=True, opener=None,
                 sec_div='-'):

        # use LogFile from _logfile_print if reading
        if mode not in _WRITEMODES:
            super().__init__(
                filename, mode=mode, buffering=buffering, encoding=encoding,
                errors=errors, newline=newline, closefd=closefd, opener=opener,
                sec_div=sec_div
            )

        # use loguru
        else:

            # keeping input arguments
            self.filename = filename
            self.sec_div = sec_div

            # the file
            config = {
                "handlers": [
                    {"sink": sys.stdout, "format": "{time} - {message}"},
                    {"sink": filename, "format": "{level} {message}", "serialize": False},
                ],
            }
            logger.add(filename)
            logger.configure(**config)

            # new_level = logger.level("SNAKY", no=38, color="<yellow>", icon="🐍")

            self.file = logger

            # making file header
            self.write(f'{filename} Log:\n\n', endsection='=')

    def _write(self, str):
        self.file.info(str)
    # /def
# /class


# --------------------------------------------------------------------------
