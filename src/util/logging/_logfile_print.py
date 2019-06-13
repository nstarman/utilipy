#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : logging
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""functions for logging
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS


##############################################################################
### PRINTLOG

class PrintLog(object):
    """a basic logger wrapper for print
    """

    def __init__(self, verbose=0, sec_div='-', header=None, show_header=True):
        """Initialize PrintLog
        start the file header (just printing)
        """
        super().__init__()

        # keeping input arguments
        self.verbose = verbose
        self.sec_div = sec_div

        # making file header
        # header = False skips the header
        # header = None, True makes a blank heaader
        if header is not False:
            if header in (None, True):
                header = ''

            self.write(f"{header} Log:", endsection='=', print=show_header)
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
        this is implemented solely to be overwritten by child classes
        """
        pass
    # /def

    def _print_and_write(self, *string, start='', sep=' ', end='\n'):
        """helper method to print and call _write
        this is implemented solely to be overwritten by child classes
        """
        self.print(*string, start=start, sep=sep, end=end)   # printing
        self._write(*string, start=start, sep=sep, end=end)  # writing
    # /def

    def newsection(self, title=None, div=None, print=True):
        """make new section

        Parameters
        ----------
        div: str, None  (default None)
            the divider
            None -> sec_div from initalization
        """
        if title is None:
            title = ''

        if div is None:  # get default divider if custom one not provided
            div = self.sec_div

        full_div = div * int(79 / len(div))  # round out to full line length

        if print:
            self._print_and_write(full_div, title, start='\n', sep='\n', end='\n')
        else:
            self._write(full_div, title, start='\n', sep='\n', end='\n\n')
    # /def

    def write(self, *text, start='', sep=' ', end='\n',
              startsection=False, endsection=False, print=True):
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
                self.newsection(div=startsection, print=print)
            else:
                self.newsection(print=print)

        if print:
            self._print_and_write(*text, start=start, sep=sep, end=end)
        else:
            self._write(*text, start=start, sep=sep, end=end)

        if endsection is not False:
            if isinstance(endsection, str):
                self.newsection(div=endsection, print=print)
            else:
                self.newsection(print=print)
    # /def

    def record(self, *text, start='', sep=' ', end='\n',
               startsection=False, endsection=False):
        """redirects to write, which goes to print
        this is implemented solely for compatibility
        """
        self.write(*text, start=start, sep=sep, end=end,
                   startsection=startsection, endsection=endsection,
                   print=False)
    # /def

    def verbort(self, *msgs, verbose=None, print=True, write=True,
                start_at=1, **kw):
        """a report function whose message is determined by the *verbose*

        Parameters
        ----------
        *msgs : str(s)
            the verbosity-ordered messages
            blank messages can be <None>, not only ''
        verbose : int, optional
            which message to record
            None (default) uses self.verbose (default = 0, unless specified)
        print : bool
            whether to print, or just record
        write : bool
            whether to write to logger file
            write redirects to print in this class
        start_at : int
            what level of verbosity is the first *msg*
            ex: verbort('test', start_at=3) means 'test' is at verbose=3
        **kw: kwargs for self.write or self.print
        """

        if verbose is None:
            verbose = self.verbose

        if verbose < start_at:                 # below starting verbosity
            msg = None
        elif verbose - start_at >= len(msgs):  # above / at last message
            msg = msgs[-1]
        else:                                   # inside message options
            msg = msgs[verbose - start_at]

        if str(msg) == '':
            msg = None  # catching null messages

        if msg is not None:
            if write:
                self.write(msg, print=print, **kw)
            else:
                self.print(msg, **kw)
    # /def

    def close(self):
        """close the non-existent file
        this is implemented solely to be overwritten by child classes
        """
        pass
    # /def

    @classmethod
    def read_log(cls, filename, buffering=-1, encoding=None,
                 errors=None, newline=None, closefd=True, opener=None):
        """read and print out a previous log

        Parameters
        ----------
        filename: str
            the file name / path at which to save this log
        ...

        TODO
        what should this return?
        """
        file = open(filename, mode='r', buffering=buffering, encoding=encoding,
                    errors=errors, newline=newline, closefd=closefd,
                    opener=opener)
        log = file.read()

        print(log)
        return log
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
         NOT ALLOWED '+' open a disk file for updating (reading and writing)

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
        if mode == '+':
            raise ValueError('+ not allowed')

        if filename is None:
            return PrintLog(verbose=verbose, sec_div=sec_div, header=header)
        else:
            self = super().__new__(cls)
            return self
    # /def

    def __init__(self, filename, verbose=0, mode='w', sec_div='-',
                 header=None, show_header=True,
                 buffering=-1, encoding=None, errors=None, newline=None,
                 closefd=True, opener=None):
        """LogFile
        set the filename and make the file
        """
        # section divider and srart file header
        # not at start b/c needs .file for .write to work
        super().__init__(verbose=verbose, sec_div=sec_div, header=False)

        # keeping input arguments
        self.filename = filename

        # the file
        self.file = open(
            filename, mode=mode, buffering=buffering, encoding=encoding,
            errors=errors, newline=newline, closefd=closefd, opener=opener
        )

        if mode == 'r':
            return

        # making file header
        if header is False:
            self.write(f"{''} Log:", endsection='=', print=False)
        else:
            if header in (None, True):
                header = ''
            self.write(f"{header} Log:", endsection='=')
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

    # def _print_and_write(self, *string, start='', sep=' ', end='\n'):
    #     """helper method to print and call _write
    #     """
    #     self.print(*string, start=start, sep=sep, end=end)  # printing
    #     self._write(*string, start=start, sep=sep, end=end)  # writing
    # # /def

    def write(self, *text, start='', sep=' ', end='\n',
              startsection=False, endsection=False, print=True):
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
                      print=print)
    # /def

    def record(self, *text, start='', end='\n',
               startsection=False, endsection=False):
        """same as write, but doesn't print as well as write to file
        """
        super().record(*text, start=start, end=end,
                       startsection=startsection, endsection=endsection)
    # /def

    def verbort(self, *msgs, verbose=None, print=True, write=True,
                start_at=1, **kw):
        """a report function whose message is determined by the *verbose*

        Parameters
        ----------
        *msgs : str(s)
            the verbosity-ordered messages
            blank messages can be <None>, not only ''
        verbose : int, optional
            which message to record
            None (default) uses self.verbose (default = 0, unless specified)
        print : bool
            whether to print, or just record
        write : bool
            whether to write to logger file
        start_at : int
            what level of verbosity is the first *msg*
            ex: verbort('test', start_at=3) means 'test' is at verbose=3
        **kw: kwargs for self.write or self.print
        """
        super().verbort(*msgs, verbose=verbose, print=print, write=write,
                        start_at=start_at, **kw)
    # /def

    def close(self):
        """close the file
        """
        print('closing file')
        self.file.close()
    # /def
# /class


##############################################################################
### DONE
