#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : logging with loguru
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""functions for logging with loguru
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
import logging

## Project-Specific
from ._LogPrint import LogPrint
# from ._LogFile import LogFile


##############################################################################
### CODE

class LogFileger(LogPrint):
    """docstring for LogFile


    mode : str
        'w' : write new file
        'a' : append to existing file
    """

    def __new__(cls, filename=None, verbose=0, sec_div='-',
                header=None, show_header=True,
                # logging arguments
                # mode='w'
                ):
        """New LogFile
        If no filename, makes a LogPrint instead
        """
        if filename is None:
            return LogPrint(verbose=verbose, sec_div=sec_div,
                            header=header, show_header=show_header)
        # /if

        self = super().__new__(cls)
        return self
    # /def

    def __init__(self, filename=None, verbose=0, sec_div='-',):

        # instantiate without writing
        # section divider and srart file header
        super().__init__(verbose=verbose, sec_div=sec_div, header=False)

        self.filename = filename

        # Verbosity
        # TODO verbosity
        # these are the logger built-in levels
        # verbose = 0 -> not set
        # verbose = 10 -> debug
        # verbose = 20 -> info
        # verbose = 30 -> warning
        # verbose = 40 -> error
        # verbose = 50 -> critical

        # The Logger
        # ----------

        # TODO consistent name with self.file in LogFile
        # TODO logger name different than filename?
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(verbose)

        # filehandler
        fh = logging.FileHandler(filename)
        fh.setLevel(logging.DEBUG)

        # console object
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # # create formatter and add it to the handlers
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # fh.setFormatter(formatter)
        # ch.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    # /def


# /class


# --------------------------------------------------------------------------
