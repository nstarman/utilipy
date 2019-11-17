# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ipython initialization file
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Functions for interacting with the IPython environment.

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
IPython: modules and functions

    - get_ipython
    - core.interactiveshell

        - InteractiveShell
        - .debugger.set_trace

    - display.display, Latex, Markdown, HTML

astroPHD: modules and functions

    - ipython

        - autoreload.set_autoreload, aimport
        - .imports.run_imports, import_from_file
        - .notebook.add_raw_code_toggle
        - .plot.configure_matplotlib
        - .printing.printmd, printMD, printltx, printLaTeX

    - util.logging.LogPrint, LogFile

Notes
-----
will set the display setting to all output lines
and set the matplotlib backend to inline with retina resolution
`InteractiveShell.ast_node_interactivity = "all"`
`configure_matplotlib(backend='inline', figure_format='retina')`

"""

__author__ = "Nathaniel Starkman"

##############################################################################
# PARAMETERS

# from ..decorators.docstring import set_docstring
from astroPHD.util.config import __config__
from astroPHD.decorators.docstring import (
    _set_docstring_import_file_helper
)

_HAS_IPYTHON = False

##############################################################################
# IMPORTS

# General
try:

    get_ipython()

    if get_ipython() is None:  # double checking
        raise NameError

except NameError:

    pass

else:

    _HAS_IPYTHON = True

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

if _HAS_IPYTHON:

    # Running Imported Functions
    InteractiveShell.ast_node_interactivity = "all"

    configure_matplotlib(backend='inline', figure_format='retina')


##############################################################################
# INFORMATION

# @set_docstring(docstring=__doc__)
@_set_docstring_import_file_helper(None, __doc__)  # doc from __doc__
def help():
    """Help for ipython module."""
    print(__doc__)
    return
# /def


##############################################################################
# END
