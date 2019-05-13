#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : logging
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""functions for logging

TODO use a decorator for setting docstrings
TODO allow no filename and it acts like print
TODO allow write to not print
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### Imports

# General
# from _io import TextIOWrapper

# Project-Specific


##############################################################################
### Code

class LogFile(object):
    """a basic logger which can both print and record to a file
    ** this class uses `open', not a more extensive logger, like `logging'

    The arguments filename - opener are all for `open`
    their descriptions are in
        https://docs.python.org/3/library/functions.html#open

    INPUT
    -----
    filename: str
        the file name / path at which to save this log
    mode: str  (default 'w')
        recommend either 'w' or 'a'
    ...
    sec_div: str
        the section divider used in `newsection'

    NOTES
    -----
    mode options:
        'r' open for reading
        'w' open for writing, truncating the file first
        'x' open for exclusive creation, failing if the file already exists
        'a' open for writing, appending to the end of the file if it exists
        'b' binary mode
        't' text mode
        '+' open a disk file for updating (reading and writing)
    """

    def __init__(self, filename, mode='w', buffering=-1, encoding=None,
                 errors=None, newline=None, closefd=True, opener=None,
                 sec_div='-'):
        """Initialize LogFile
        set the filename and make the file
        start the file header (both printing and writing)
        """
        super().__init__()

        # keeping input arguments
        self.filename = filename
        self.sec_div = sec_div

        # the file
        self.file = open(
            filename, mode='w', buffering=buffering, encoding=encoding,
            errors=errors, newline=newline, closefd=closefd, opener=opener
        )

        # making file header
        self.write(f'{filename} Log:\n\n', endsection='=')
    # /def

    @classmethod
    def open(cls, filename, mode='w', buffering=-1, encoding=None,
             errors=None, newline=None, closefd=True, opener=None):
        """
        """
        return cls(filename, mode=mode, buffering=buffering,
                   encoding=encoding, errors=errors, newline=newline,
                   closefd=closefd, opener=opener)
    # /def

    @classmethod
    def open_to_write(cls, filename, mode='w', buffering=-1, encoding=None,
                      errors=None, newline=None, closefd=True, opener=None):
        if mode == 'r':
            raise ValueError('mode must be set to write')
        return cls(filename, mode=mode, buffering=buffering,
                   encoding=encoding, errors=errors, newline=newline,
                   closefd=closefd, opener=opener)
    # /def

    @classmethod
    def open_to_read(cls, filename, buffering=-1, encoding=None,
                     errors=None, newline=None, closefd=True, opener=None):
        return cls(filename, mode='r', buffering=buffering,
                   encoding=encoding, errors=errors, newline=newline,
                   closefd=closefd, opener=opener)
    # /def

    def __getattr__(self, name):
        """redirect non-defined attributes to self.file
        """
        return getattr(self.file, name)
    # /def

    def print(self, text, sep=' ', end='\n'):
        """wrapper for print
        """
        print(text, sep=sep, end=end)
    # /def

    def _write(self, string):
        """writer method
        this is used by all write methods
        implemented so it can be overrode easily
        """
        self.file.write(string)
    # /def

    def newsection(self, div=None):
        """make new section
        div: divider
        """
        if div is None:
            div = self.sec_div
        self._write('\n' + div * 79 + '\n\n')
    # /def

    def write(self, text, start='', sep=' ', end='\n',
              startsection=False, endsection=False):
        """Write string to stream.
        Returns the number of characters written (which is always equal to
        the length of the string).
        """
        print(text, sep=sep, end=end)
        if startsection is not False:
            if isinstance(startsection, str):
                self.newsection(div=startsection)
            else:
                self.newsection()

        self._write(start + str(text) + end)

        if endsection is not False:
            if isinstance(endsection, str):
                self.newsection(div=endsection)
            else:
                self.newsection()
    # /def

    def record(self, text, start='', end='\n',
               startsection=False, endsection=False):
        """same as write, but doesn't print as well
        """
        if startsection:
            self.newsection()

        self._write(start + str(text) + end)

        if endsection:
            self.newsection()
    # /def

    def close(self):
        print('closing file')
        self.file.close()
    # /def
# /class


# --------------------------------------------------------------------------
