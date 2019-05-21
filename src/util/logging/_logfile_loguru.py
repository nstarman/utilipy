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

## General
import sys

# Loguru
from loguru import logger

## Custom
from ._logfile_print import LogFile as _LogFile

## Project-Specific


##############################################################################
### Setup


_READMODES = ('r', )
_WRITEMODES = ('w', 'x', 'a', 'b')
_READWRITEMODES = ('+', )


##############################################################################
### Code

class LogFile(_LogFile):
    """a logger which can both print and record to a file
    ** this class uses loguru, a 3rd party logging package

    The arguments filename - opener are all for `open`
    their descriptions are in
        https://docs.python.org/3/library/functions.html#open

    Parameters
    ----------
    filename : str
        the file name / path at which to save this log
    mode : str  (default 'w')
        recommend either 'w' or 'a'
    sec_div : str
        the section divider used in `newsection'
    header : None, str  (default None)
        the header for the file
        None -> filename
    ...

    # Notes
    # -----
    # mode options:
    #     'r' open for reading
    #     'w' open for writing, truncating the file first
    #     'x' open for exclusive creation, failing if the file already exists
    #     'a' open for writing, appending to the end of the file if it exists
    #     'b' binary mode
    #     't' text mode
    #     '+' open a disk file for updating (reading and writing)
    """

    def __init__(self, filename, mode='w', sec_div='-', header=None,
                 buffering=-1, encoding=None, errors=None, newline=None,
                 closefd=True, opener=None):
        """Initialize LogFile
        set the filename and make the file
        start the file header (both printing and writing)
        """

        # use LogFile from _logfile_print if reading
        # because it requires `open' to read
        if mode not in _WRITEMODES:
            super().__init__(
                filename, mode=mode, sec_div=sec_div, header=header,
                buffering=buffering, encoding=encoding, errors=errors,
                newline=newline, closefd=closefd, opener=opener
            )

        # use loguru
        else:

            # TODO delete old file?

            # keeping input arguments
            self.filename = filename
            self.sec_div = sec_div

            # the file
            config = {
                "handlers": [
                    {"sink": sys.stdout, "format": "{message}"},
                    # {"sink": filename, "format": "{icon} {message}", "serialize": False},
                    {"sink": filename, "format": "{message}", "serialize": False},
                ],
            }
            logger.add(filename)
            logger.configure(**config)

            logger.level('write', no=38, color="<black>")

            # updating levels
            for lvl in ('TRACE', 'DEBUG', 'INFO', 'SUCCESS',
                        'WARNING', 'ERROR', 'CRITICAL'):
                logger.level(lvl, icon=logger.level(lvl).icon + ': ')

            self.file = logger

            # making file header
            if header is None:
                header = filename
            self.write(f"{header} Log:", endsection='=')
    # /def

    def _write(self, *string, start='', sep=' ', end='\n'):
        r"""writer method
        this is used by all write methods
        implemented so it can be overriden easily
        **Note: end='' does nothing. Write automatically does '\n'
        """
        if len(string) == 0:  # checking there is a string
            raise ValueError('needs a value')

        self.file.log('write', start)  # start

        # write to file
        if len(string) == 1:
            self.file.log('write', str(string[0]) + end)

        else:
            for s in string[:-1]:
                self.file.log('write', str(s) + sep)
            self.file.log('write', str(s) + end)
    # /def

    def _print_and_write(self, *string, start='', sep=' ', end='\n'):
        """helper method to print and call _write
        """
        self._write(*string, start=start, sep=sep, end=end)  # writing
    # /def

    def record(self, *text, start='', end='\n',
               startsection=False, endsection=False):
        """same as write, but doesn't print as well as write to file

        TODO write w/out also printing
        """
        self.write(*text, start=start, sep=sep, end=end,
                   startsection=startsection, endsection=endsection)
    # /def

    def close(self):
        print('closing file')
    # /def
# /class


# --------------------------------------------------------------------------
