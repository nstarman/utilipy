# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : base_imports
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Base set of imports.

Routine Listings
----------------
Base: imports

    - os, sys, time, pdb, warnings,
    - numpy -> np, scipy,
    - tqdm -> TQDM, tqdm, .tqdm_notebook -> tqdmn

IPython: imports

    - display, Latex, Markdown, set_trace,
    - printmd, printMD, printltx, printLaTeX,
    - set_autoreload, aimport,
    - run_imports, import_from_file,
    - add_raw_code_toggle

utilipy: imports

    - LogFile
    - ObjDict

References
----------
SciPy references are [#]_ and [#]_.

NumPy references are [#]_ and [#]_.

IPython reference is [#]_.

Matplotlib reference is [#]_.

.. [#] Travis E. Oliphant, "Python for Scientific Computing", Computing in
   Science & Engineering, 9, 10-20 (2007), DOI:10.1109/MCSE.2007.58
   http://scitation.aip.org/content/aip/journal/cise/9/3/10.1109/MCSE.2007.58.

.. [#] K. Jarrod Millman and Michael Aivazis, "Python for Scientists and
   Engineers", Computing in Science & Engineering, 13, 9-12 (2011),
   DOI:10.1109/MCSE.2011.36
   http://scitation.aip.org/content/aip/journal/cise/13/2/10.1109/MCSE.2011.36.

.. [#] Travis E, Oliphant. A guide to NumPy, USA: Trelgol Publishing, (2006).

.. [#] Stéfan van der Walt, S. Chris Colbert and Gaël Varoquaux.
   "The NumPy Array: A Structure for Efficient Numerical Computation",
   Computing in Science & Engineering, 13, 22-30 (2011),
   DOI:10.1109/MCSE.2011.37
   http://scitation.aip.org/content/aip/journal/cise/13/2/10.1109/MCSE.2011.37.

.. [#] Fernando Pérez, Brian E. Granger, "IPython: A System for Interactive
   Scientific Computing", Computing in Science and Engineering, vol. 9,
   no. 3, pp. 21-29, May/June 2007, doi:10.1109/MCSE.2007.53.
   URL: https://ipython.org.

.. [#] John D. Hunter, Matplotlib: A 2D Graphics Environment, Computing in
   Science & Engineering, 9, 90-95 (2007), DOI:10.1109/MCSE.2007.55
   http://scitation.aip.org/content/aip/journal/cise/9/3/10.1109/MCSE.2007.55.

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "base_imports_help",
]


##############################################################################
# PARAMETERS

from utilipy.config import __config__
from utilipy.decorators.docstring import (
    _set_docstring_import_file_helper,
    _import_file_docstring_helper,
)


##############################################################################
# IMPORTS

# +---------------------------------------------------------------------------+
# Basic

import os
import sys  # operating system
import time  # timing
import pdb  # debugging
import warnings  # warning

# Numpy
import numpy as np  # numerical python
import scipy  # scientific python

# TODO implement when no TqdmExperimentalWarning
# from tqdm.autonotebook import tqdm
import tqdm as TQDM
from tqdm import tqdm as tqdm, tqdm_notebook as tqdmn


# CUSTOM

from utilipy.utils import ObjDict  # custom dictionary-like object
from utilipy.utils.logging import LogFile  # LoggerFile  # custom logging


# +--------------------------------------------------------------------------+
# IPython

try:

    _HAS_IPYTHON: bool = False

    get_ipython()

    if get_ipython() is None:  # double checking
        raise NameError

except NameError:

    pass

else:

    _HAS_IPYTHON = True

    from IPython.core.interactiveshell import InteractiveShell
    from IPython.core.debugger import set_trace
    from IPython.display import (
        display,  # display is a better print
        Latex,
        Markdown,  # for printing LaTeX or Markdown strings
    )

    # %run runs in the main namespace, so need to run as 'src.', not '.''
    from utilipy.ipython import (
        printmd,
        printMD,  # markdown printing
        printltx,
        printLaTeX,  # LaTeX printing
        set_autoreload,
        aimport,  # imports
        run_imports,
        import_from_file,  # imports
        add_raw_code_toggle,  # notebook
    )


##############################################################################
# Running Imported Functions

if _HAS_IPYTHON:

    InteractiveShell.ast_node_interactivity = "all"


##############################################################################
# Printing Information


@_set_docstring_import_file_helper("base", __doc__)  # doc from __doc__
def base_imports_help():
    """Help for Matplotlib base imports."""
    doc = _import_file_docstring_helper(base_imports_help.__doc__)
    print(doc)


# /def


if __config__.getboolean("verbosity", "verbose-imports"):
    base_imports_help()

##############################################################################
# END
