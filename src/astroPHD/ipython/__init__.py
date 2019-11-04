#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ipython initialization file
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""initialization file for IPython envionments.

Methods
-------
autoreload:
    set_autoreload: set the notebook's autoreload state for modules
    aimport: import a module with autoreload options
imports:
    import_from_file
    run_imports
    import_base, import_extended, import_astropy, import_matplotlib
    aimport from .autoreload
notebook:
    add_raw_code_toggle
plot:
    configure_matplotlib
printing:
    printmd / printMD
    printHTML
    printltx / printLaTeX

Returns
-------
IPython
    get_ipython
    core.interactiveshell.InteractiveShell
        .debugger.set_trace
    display.display, Latex, Markdown, HTML
astroPHD
    ipython.autoreload.set_autoreload, aimport
           .imports.run_imports, import_from_file
           .notebook.add_raw_code_toggle
           .plot.configure_matplotlib
           .printing.printmd, printMD, printltx, printLaTeX
    util.logging.LogPrint, LogFile

Info
----
will set the display setting to all output lines
and set the matplotlib backend to inline with retina resolution
`InteractiveShell.ast_node_interactivity = "all"`
`configure_matplotlib(backend='inline', figure_format='retina')`

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.debugger import set_trace
from IPython.display import (
    display,        # display is a better print
    Latex,          # for printing LaTeX
    Markdown, HTML  # for printing Markdown & HTML
)

# Project-Specific
from ..util.logging import LogPrint, LogFile

from .autoreload import set_autoreload, aimport
from .imports import run_imports, import_from_file
from .notebook import add_raw_code_toggle
from .plot import configure_matplotlib
from .printing import (
    printmd, printMD,     # markdown printing
    printltx, printLaTeX  # LaTeX printing
)


##############################################################################
# SETUP

# Running Imported Functions
InteractiveShell.ast_node_interactivity = "all"

try:
    get_ipython()
except NameError:
    import warnings
    warnings.warn('cannot call get_ipython! this module is pretty much useless')
else:
    if get_ipython() is not None:
        configure_matplotlib(backend='inline', figure_format='retina')


##############################################################################
# CODE

def help():
    """Help for ipython module.

    Returns
    -------
    IPython:display.display, .Latex, .Markdown
           .core.interactiveshell.InteractiveShell
                .debugger.set_trace

    astroPHD.util.logging.LogPrint, .LogFile
            .ipython.autoreload.set_autoreload, aimport
                    .imports.run_imports, import_from_file
                    .notebook.add_raw_code_toggle
                    .plot.configure_matplotlib
                    .printing.printmd, printMD, printltx, printLaTeX

    Methods
    -------
    autoreload:
        set_autoreload: set the notebook's autoreload state for modules
        aimport: import a module with autoreload options

    imports:
        import_from_file
        run_imports
        import_base, import_extended, import_astropy, import_matplotlib
        aimport from .autoreload

    notebook:
        add_raw_code_toggle

    plot:
        configure_matplotlib

    printing:
        printmd / printMD
        printHTML
        printltx / printLaTeX

    """
    print(__doc__)
    return
# /def


##############################################################################
# Printing Information

# if .astrophd_profile.printhelp:
#     print("""Imported:
#         IPython:display.display, .Latex, .Markdown
#                .core.interactiveshell.InteractiveShell
#                     .debugger.set_trace

#         astroPHD.util.logging.LogPrint, .LogFile
#                 .ipython.autoreload.set_autoreload, aimport
#                         .imports.run_imports, import_from_file
#                         .notebook.add_raw_code_toggle
#                         .plot.configure_matplotlib
#                         .printing.printmd, printMD, printltx, printLaTeX
#     """)


##############################################################################
# END
