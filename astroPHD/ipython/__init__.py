#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ipython initialization file
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""initialization file for jupyter notebook functions
"""


##############################################################################
### IMPORTS

## General
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display
from IPython.display import Latex, Markdown  # display is a better print
from IPython.core.debugger import set_trace

## Project-Specific
from ..util.paths import current_file_directory as _cfd

from .printing import (
    printmd, printMD,     # markdown printing
    printltx, printLaTeX  # LaTeX printing
)

from .aimport import set_autoreload # , aimport, aimports
from .notebook import add_raw_code_toggle
from .plot import configure_matplotlib


##############################################################################
### CODE


def run_imports(extended=False):
    """runs .imports file using ipython magic

    Imports:
    Base: os, sys, time, pdb, warnings, numpy -> np, scipy
    Astropy: astropy, .units->u, .coordinates->coords, .SkyCoord, .Table, .QTable
    Plot: starkplot->plt, .mpl_decorator
          matplotlib->mpl, .colors, .cm
    Logging: logging, .LogFile, .LoggerFile
    Misc: ObjDict
    IPython: display, Latex, Markdown, set_trace, printmd, printltx
    """

    # running imports file
    get_ipython().magic(f"run {_cfd(__file__)}/imports.py")

    if extended:
        run_extended_imports()

    return
# /def


# ----------------------------------------------------------------------------

def run_extended_imports():
    """runs .extended_imports file using ipython magic

    Imports:
    TODO
    """

    get_ipython().magic(f"run {_cfd(__file__)}/extended_imports.py")

    return
# /def


##############################################################################

def reference():
    """
    TODO
    """

    print("""
    """)

    return
# /def


##############################################################################
### Running

# InteractiveShell.ast_node_interactivity = "all"
# configure_matplotlib()

# del _cfd

##############################################################################
### END
