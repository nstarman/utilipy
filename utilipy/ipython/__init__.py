# -*- coding: utf-8 -*-

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

utilipy: modules and functions

    - ipython

        - autoreload.set_autoreload, aimport
        - .imports.run_imports, import_from_file
        - .notebook.add_raw_code_toggle
        - .plot.configure_matplotlib
        - .printing.printmd, printMD, printltx, printLaTeX

    - utils.logging.LogPrint, LogFile

Notes
-----
will set the display setting to all output lines
and set the matplotlib backend to inline with retina resolution
`InteractiveShell.ast_node_interactivity = "all"`
`configure_matplotlib(backend='inline', figure_format='retina')`

References
----------
IPython [#]_

.. [#] Fernando Pérez, Brian E. Granger, IPython: A System for Interactive
    Scientific Computing, Computing in Science and Engineering, vol. 9,
    no. 3, pp. 21-29, May/June 2007, doi:10.1109/MCSE.2007.53.
    URL: https://ipython.org

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "help",
    # "get_ipython",
    # "InteractiveShell",
    # "set_trace",
    # "display",
    # "Latex",
    # "Markdown",
    # "HTML",
    "set_autoreload",
    "aimport",
    "run_imports",
    "import_from_file",
    "add_raw_code_toggle",
    "printMD",
    "printLTX",
]


##############################################################################
# IMPORTS

# GENERAL

from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.debugger import set_trace
from IPython.display import (
    display,  # display is a better print
    Latex,  # for printing LaTeX
    Markdown,
    HTML,  # for printing Markdown & HTML
)


# PROJECT-SPECIFIC

from ..utils.logging import LogPrint, LogFile
from ..config import __config__
from ..decorators.docstring import _set_docstring_import_file_helper

from .autoreload import set_autoreload, aimport
from .imports import run_imports, import_from_file
from .notebook import add_raw_code_toggle
from .plot import configure_matplotlib
from .printing import (
    printMD,  # Markdown printing
    printLTX,  # LaTeX printing
)


##############################################################################
# PARAMETERS

try:
    get_ipython()
    if get_ipython() is None:  # double checking
        raise NameError
except NameError:
    _HAS_IPY: bool = False
else:
    _HAS_IPY: bool = True


if _HAS_IPY:

    # Running Imported Functions
    InteractiveShell.ast_node_interactivity = "all"

    configure_matplotlib(backend="inline", figure_format="retina")


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
