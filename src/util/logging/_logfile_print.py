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
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### Imports

# General
# from _io import TextIOWrapper

# Project-Specific


##############################################################################
### PrintLog

class PrintLog(object):
    """a basic logger wrapper for print
    """

    def __init__(self, verbose=0, sec_div='-', header=None,):
        """Initialize PrintLog
        start the file header (just printing)
        """
        super().__init__()

        # keeping input arguments
        self.verbose = verbose
        self.sec_div = sec_div

        # making file header
        if header is None:
            header = 'PrintLog'
        self.write(f"{header} Log:", endsection='=')
    # /def

    def print(self, *text, start='', sep=' ', end='\n'):
        r"""wrapper for print

        Parameters
        ----------
        text: str
            the text to print
        sep: str  (default ' ')
            the separater for print
        end: str  (default '\n')
            the end for print
        """
        print(start, end='')
        print(*text, sep=sep, end=end)
    # /def

    def _write(self, *string, start='', sep=' ', end='\n'):
        r"""writer method
        redirects to .print
        this is implemented solely to be overwritten by child classes
        """
        self.print(*string, start=start, sep=sep, end=end)
    # /def

    def _print_and_write(self, *string, start='', sep=' ', end='\n'):
        """helper method to print and call _write
        this is implemented solely to be overwritten by child classes
        """
        self.print(*string, start=start, sep=sep, end=end)  # printing
    # /def

    def newsection(self, div=None):
        """make new section

        Parameters
        ----------
        div: str, None  (default None)
            the divider
            None -> sec_div from initalization
        """
        if div is None:  # get default divider if custom one not provided
            div = self.sec_div

        full_div = div * int(79 / len(div))  # round out to full line length

        self._print_and_write(full_div, start='\n', end='\n\n')
    # /def

    def write(self, *text, start='', sep=' ', end='\n',
              startsection=False, endsection=False, _print=True):
        """print text

        TODO implement sep method for write

        Parameters
        ----------
        text: str
            the text to write & print
        start: str  (default '')
            start to print
        sep: str  (default ' ')
            the separater for print
        end: str  (default '\n')
            the end for print
        startsection: bool  (default False)
            whether to start a new section before writing
        endsection:  bool  (default False)
        """

        if startsection is not False:
            if isinstance(startsection, str):
                self.newsection(div=startsection)
            else:
                self.newsection()

        if _print:
            self._print_and_write(*text, start=start, sep=sep, end=end)
        else:
            self._write(*text, start=start, sep=sep, end=end)

        if endsection is not False:
            if isinstance(endsection, str):
                self.newsection(div=endsection)
            else:
                self.newsection()
    # /def

    def record(self, *text, start='', end='\n',
               startsection=False, endsection=False):
        """redirects to write, which goes to print
        this is implemented solely for compatibility
        """
        self.write(*text, start=start, sep=sep, end=end,
                   startsection=startsection, endsection=endsection,
                   _print=False)
    # /def

    def verbort(self, *msgs, verbose=None, _print=True, _write=True,
                _start_at=1,
                **kw):
        """a report function whose message is determined by the *verbose*

        Parameters
        ----------
        *msgs : str(s)
            the verbosity-ordered messages
            blank messages can be <None>, not only ''
        verbose : int, optional
            which message to record
            None (default) uses self.verbose (default = 0, unless specified)
        _print : bool
            whether to print, or just record
        _write : bool
            whether to write to logger file
            write redirects to print in this class
        _start_at : int
            what level of verbosity is the first *msg*
            ex: verbort('test', _start_at=3) means 'test' is at verbose=3
        **kw: kwargs for self.write or self.print
        """
        if verbose is None:
            verbose = self.verbose

        if verbose >= len(msgs):
            verbose = len(msgs) - 1

        msg = msgs[verbose]
        if msg is None: msg = ''

        if _write:
            self.write(msg, _print=_print, **kw)
        else:
            self.print(msg, **kw)
    # /def

    def close(self):
        """close the non-existent file
        this is implemented solely to be overwritten by child classes
        """
        pass
    # /def

# /class


##############################################################################
### LogFile


class LogFile(PrintLog):
    """a basic logger which can both print and record to a file
    ** this class uses `open', not a more extensive logger, like `logging'

    The arguments filename - opener are all for `open`
    their descriptions are in
        https://docs.python.org/3/library/functions.html#open

    Parameters
    ----------
    filename : str, optional
        the file name / path at which to save this log
        If no filename, makes a PrintLog() instead
    mode : str  (default 'w')
        recommend either 'w' or 'a'
    sec_div : str
        the section divider used in `newsection'
    header : None, str  (default None)
        the header for the file
        None -> filename
    ...

    Notes
    -----
    mode options:
        'r' open for reading
        'w' open for writing, truncating the file first
        'x' open for exclusive creation, failing if the file already exists
        'a' open for writing, appending to the end of the file if it exists
        'b' binary mode
        't' text mode
        '+' open a disk file for updating (reading and writing)

    Inherited Methods
    -----------------
    .print
    .newsection
    .write  (reimplemented for docstring)
    .record  (reimplemented for docstring)
    .verbort  (reimplemented for docstring)

    Overwritten Methods
    -------------------
    ._write: writes to file
    ._print_and_write: prints and writes
    """

    def __new__(cls, filename=None, verbose=0, mode='w',
                sec_div='-', header=None,
                buffering=-1, encoding=None, errors=None, newline=None,
                closefd=True, opener=None):
        """New LogFile
        If no filename, makes a PrintLog instead
        """
        if filename is None:
            return PrintLog(verbose=verbose, sec_div=sec_div, header=header)
        else:
            self = super().__new__(cls)
            return self


    def __init__(self, filename, verbose=0, mode='w', sec_div='-', header=None,
                 buffering=-1, encoding=None, errors=None, newline=None,
                 closefd=True, opener=None):
        """LogFile
        set the filename and make the file
        """

        # keeping input arguments
        self.filename = filename

        # the file
        self.file = open(
            filename, mode=mode, buffering=buffering, encoding=encoding,
            errors=errors, newline=newline, closefd=closefd, opener=opener
        )

        # section divider and srart file header
        # not at start b/c needs .file for .write to work
        super().__init__(verbose=verbose, sec_div=sec_div, header=header)
    # /def

    @classmethod
    def open(cls, filename, verbose=0, mode='w', sec_div='-', header=None,
             buffering=-1, encoding=None, errors=None, newline=None,
             closefd=True, opener=None):
        """a basic logger which can both print and record to a file
        ** this class uses `open', not a more extensive logger, like `logging'

        The arguments filename - opener are all for `open`
        their descriptions are in
            https://docs.python.org/3/library/functions.html#open

        Parameters
        ----------
        filename: str
            the file name / path at which to save this log
        mode: str  (default 'w')
            recommend either 'w' or 'a'
        sec_div: str
            the section divider used in `newsection'
        header : None, str  (default None)
            the header for the file
            None -> filename
        ...

        Notes
        -----
        mode options:
            'r' open for reading
            'w' open for writing, truncating the file first
            'x' open for exclusive creation, failing if file already exists
            'a' open for writing, appending to the end of file if it exists
            'b' binary mode
            't' text mode
            '+' open a disk file for updating (reading and writing)
        """
        return cls(filename, verbose=verbose, mode=mode, sec_div=sec_div, header=header,
                   buffering=buffering, encoding=encoding, errors=errors,
                   newline=newline, closefd=closefd, opener=opener)
    # /def

    @classmethod
    def open_to_write(cls, filename, verbose=0, mode='w', sec_div='-', header=None,
                      buffering=-1, encoding=None, errors=None, newline=None,
                      closefd=True, opener=None):
        """a basic logger which can both print and record to a file
        ** this class uses `open', not a more extensive logger, like `logging'

        The arguments filename - opener are all for `open`
        their descriptions are in
            https://docs.python.org/3/library/functions.html#open

        Parameters
        ----------
        filename: str
            the file name / path at which to save this log
        mode: str  (default 'w')
            recommend either 'w' or 'a'
            cannot be 'r'
        sec_div: str
            the section divider used in `newsection'
        header : None, str  (default None)
            the header for the file
            None -> filename
        ...

        Notes
        -----
        mode options:
            'w' open for writing, truncating the file first
            'x' open for exclusive creation, failing if file already exists
            'a' open for writing, appending to the end of file if it exists
            'b' binary mode
            't' text mode
            '+' open a disk file for updating (reading and writing)
        """
        if mode == 'r':
            raise ValueError('mode must be set to write')

        return cls(filename, verbose=verbose, mode=mode, sec_div=sec_div, header=header,
                   buffering=buffering, encoding=encoding, errors=errors,
                   newline=newline, closefd=closefd, opener=opener)
    # /def

    @classmethod
    def open_to_read(cls, filename, buffering=-1, encoding=None,
                     errors=None, newline=None, closefd=True, opener=None):
        """a basic logger which can both print and record to a file
        ** this class uses `open', not a more extensive logger, like `logging'

        The arguments filename - opener are all for `open`
        their descriptions are in
            https://docs.python.org/3/library/functions.html#open

        Parameters
        ----------
        filename: str
            the file name / path at which to save this log
        ...
        """
        return cls(filename, mode='r', buffering=buffering, encoding=encoding,
                   errors=errors, newline=newline, closefd=closefd,
                   opener=opener)
    # /def

    def __getattr__(self, name):
        """redirect non-defined attributes to self.file
        """
        return getattr(self.file, name)
    # /def

    def _write(self, *string, start='', sep=' ', end='\n'):
        r"""writer method
        this is used by all write methods
        implemented so it can be overriden easily
        **Note: end='' does nothing. Write automatically does '\n'
        """
        if len(string) == 0:  # checking there is a string
            raise ValueError('needs a value')

        self.file.write(start)  # start

        # write to file
        if len(string) == 1:
            self.file.write(str(string[0]) + end)

        else:
            for s in string[:-1]:
                self.file.write(str(s) + sep)
            self.file.write(str(s) + end)
    # /def

    def _print_and_write(self, *string, start='', sep=' ', end='\n'):
        """helper method to print and call _write
        """
        self.print(*string, start=start, sep=sep, end=end)  # printing
        self._write(*string, start=start, sep=sep, end=end)  # writing
    # /def

    def write(self, *text, start='', sep=' ', end='\n',
              startsection=False, endsection=False, _print=True):
        """Write string to stream and print it to output.

        Parameters
        ----------
        text: str
            the text to write & print
        start: str  (default '')
            start to print
        sep: str  (default ' ')
            the separater for print
        end: str  (default '\n')
            the end for print
        startsection: bool  (default False)
            whether to start a new section before writing
        endsection:  bool  (default False)
        """

        super().write(*text, start=start, sep=sep, end=end,
                      startsection=startsection, endsection=endsection,
                      _print=_print)
    # /def

    def record(self, *text, start='', end='\n',
           startsection=False, endsection=False):
        """same as write, but doesn't print as well as write to file
        """
        super().record(*text, start=start, end=end,
                       startsection=startsection, endsection=endsection)
    # /def

    def verbort(self, *msgs, verbose=None, _print=True, _write=True,
                _start_at=1, **kw):
        """a report function whose message is determined by the *verbose*

        Parameters
        ----------
        *msgs : str(s)
            the verbosity-ordered messages
            blank messages can be <None>, not only ''
        verbose : int, optional
            which message to record
            None (default) uses self.verbose (default = 0, unless specified)
        _print : bool
            whether to print, or just record
        _write : bool
            whether to write to logger file
        _start_at : int
            what level of verbosity is the first *msg*
            ex: verbort('test', _start_at=3) means 'test' is at verbose=3
        **kw: kwargs for self.write or self.print
        """
        super().verbort(*msgs, verbose=verbose,
                        _print=_print, _write=_write,
                        **kw)
    # /def

    def close(self):
        """close the file
        """
        print('closing file')
        self.file.close()
    # /def
# /class


# --------------------------------------------------------------------------
