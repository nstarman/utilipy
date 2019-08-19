#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ipython initialization file
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""initialization file for jupyter notebook functions

TODO:
determine which backend and figure_format to use automatically
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.debugger import set_trace
from IPython.display import (
    display,               # display is a better print
    Latex, Markdown       # for printing LaTeX or Markdown strings
)

## Project-Specific
from ..util.logging import LogPrint, LogFile

from .printing import (
    printmd, printMD,     # markdown printing
    printltx, printLaTeX  # LaTeX printing
)

from .autoreload import set_autoreload, aimport
from .imports import run_imports, import_from_file
from .notebook import add_raw_code_toggle
from .plot import configure_matplotlib


##############################################################################
### SETUP

# Running Imported Functions
InteractiveShell.ast_node_interactivity = "all"
configure_matplotlib(backend='inline', figure_format='retina')


##############################################################################
### CODE

def reference():
    """
    TODO
    """

    print("""
    """)

    return
# /def


##############################################################################
### Printing Information

# print("""Imported:
#     IPython:display.display, .Latex, .Markdown
#            .core.interactiveshell.InteractiveShell
#                 .debugger.set_trace
#
#     astroPHD.util.logging.LogPrint, .LogFile
#             .ipython.autoreload.set_autoreload, aimport
#                     .imports.run_imports, import_from_file
#                     .notebook.add_raw_code_toggle
#                     .plot.configure_matplotlib
#                     .printing.printmd, printMD, printltx, printLaTeX
# """)


##############################################################################
### END
