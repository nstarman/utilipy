# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : logfile_print
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""LogPrint function for logging to the console."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

from typing import Any, Union, Optional


##############################################################################
# LogPrint


class LogPrint(object):
    """A basic logger wrapper for print."""

    def __init__(
        self,
        verbose: int = 0,
        sec_div: str = "-",
        header: Union[str, bool, None] = None,
        show_header: bool = True,
        # for compatibility
        **kw: Any,
    ) -> None:
        """Initialize LogPrint.

        start the file header (just printing)

        """
        super().__init__()

        # keeping input arguments
        self.verbose = verbose
        self.sec_div = sec_div

        # making file header
        if header is not False:
            if header in {None, True}:
                header = ""
            elif isinstance(header, str):
                if header[-1] != " ":  # making sure ends in space
                    header += " "
            else:
                raise TypeError

            self.write(f"{header}Log:", endsection="=", print=show_header)
        return

    # /def

    # ------------------------------------------------------------------------

    @classmethod
    def open(
        cls,
        verbose: int = 0,
        sec_div: str = "-",
        header: Union[bool, None, str] = None,
        show_header: bool = True,
        **kw: Any,
    ) -> Any:
        """Open LogPrint.

        TODO
        ----
        kw absorbs all extra kwargs to be consistent with LogFile

        """
        return cls(
            verbose=verbose,
            sec_div=sec_div,
            header=header,
            show_header=show_header,
        )

    # /def

    @classmethod
    def open_to_write(
        cls,
        verbose: int = 0,
        sec_div: str = "-",
        header: Union[bool, None, str] = None,
        show_header: bool = True,
        **kw: Any,
    ) -> Any:
        """open_to_write.

        TODO
        ----
        **kw absorbs all extra kwargs to be consistent with LogFile

        """
        return cls(
            verbose=verbose,
            sec_div=sec_div,
            header=header,
            show_header=show_header,
        )

    # /def

    @classmethod
    def open_to_read(cls) -> Any:
        """Open a logfile to read.

        this class uses ``open``, not a more extensive logger, like ``logging``

        The arguments filename - opener are all for ``open``

        """
        return cls()

    # /def

    # ------------------------------------------------------------------------

    def print(
        self, *text: str, start: str = "", sep: str = " ", end: str = "\n"
    ) -> None:
        r"""Wrap-function for print.

        Parameters
        ----------
        text: str
            the text to print
        sep: str  (default ' ')
            the separater for print
        end: str  (default '\n')
            the end for print

        """
        print(start, end="")
        print(*text, sep=sep, end=end)
        return

    # /def

    def _write(self, *string, start="", sep=" ", end="\n") -> None:
        """Writer method.

        this is implemented solely to be overwritten by child classes

        """
        pass

    # /def

    def _print_and_write(self, *string, start="", sep=" ", end="\n") -> None:
        """Help method to print and call _write.

        this is implemented solely to be overwritten by child classes

        """
        self.print(*string, start=start, sep=sep, end=end)  # printing
        self._write(*string, start=start, sep=sep, end=end)  # writing
        return

    # /def

    def newsection(self, title=None, div=None, print=True) -> None:
        """Make new section.

        Parameters
        ----------
        div: str, None  (default None)
            the divider
            None -> sec_div from initialization

        """
        if title is None:
            title = ""

        if div is None:  # get default divider if custom one not provided
            div = self.sec_div

        full_div = div * int(79 / len(div))  # round out to full line length

        if print:
            self._print_and_write(
                full_div, title, start="\n", sep="\n", end="\n"
            )
        else:
            self._write(full_div, title, start="\n", sep="\n", end="\n\n")
        return

    # /def

    def write(
        self,
        *text: str,
        start: str = "",
        sep: str = " ",
        end: str = "\n",
        startsection: Union[bool, str] = False,
        endsection: Union[bool, str] = False,
        print: bool = True,
    ) -> None:
        r"""Print text.

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
        return

    # /def

    def record(
        self,
        *text: str,
        start: str = "",
        sep: str = " ",
        end: str = "\n",
        startsection: Union[bool, str] = False,
        endsection: Union[bool, str] = False,
    ) -> None:
        """Redirects to write, which goes to print.

        this is implemented solely for compatibility with LogFile

        """
        self.write(
            *text,
            start=start,
            sep=sep,
            end=end,
            startsection=startsection,
            endsection=endsection,
            print=False,
        )
        return

    # /def

    # ------------------------------------------------------------------------

    def report(
        self,
        *msgs: str,
        verbose: Optional[int] = None,
        print: bool = True,
        write: bool = True,
        start_at: int = 1,
        **kw: Any,
    ) -> None:
        """Report function whose message is determined by `verbose`.

        Parameters
        ----------
        msgs : str
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
            what level of verbosity is the first `msg`
            ex: report('test', start_at=3) means 'test' is at verbose=3
        kw:
            kwargs for self.write or self.print

        """
        if verbose is None:
            verbose = self.verbose

        if verbose < start_at:  # below starting verbosity
            msg = None
        elif verbose - start_at >= len(msgs):  # above / at last message
            msg = msgs[-1]
        else:  # inside message options
            msg = msgs[verbose - start_at]

        if str(msg) == "":
            msg = None  # catching null messages

        if msg is not None:
            if write:
                self.write(msg, print=print, **kw)
            else:
                self.print(msg, **kw)
        return

    # /def

    # ------------------------------------------------------------------------

    def close(self) -> None:
        """Close the non-existent file.

        implemented solely to be overwritten by child classes.

        """
        pass

    # /def

    @classmethod
    def read_log(
        cls,
        filename: str,
        buffering: int = -1,
        encoding: Any = None,
        errors: Any = None,
        newline: Any = None,
        closefd: bool = True,
        opener: None = None,
    ) -> str:
        """Read and print out a previous log

        Parameters
        ----------
        filename: str
            the file name / path at which to save this log
        ...

        TODO
        ----
        what should this return?

        """
        file = open(
            filename,
            mode="r",
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
        )
        log = file.read()

        print(log)
        return log

    # /def


# /class

##############################################################################
# END
