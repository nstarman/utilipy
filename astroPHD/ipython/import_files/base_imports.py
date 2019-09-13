#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Base Import File
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

# +---------------------------------------------------------------------------+
# Basic

import os, sys                        # operating system
import time                           # timing
import pdb                            # debugging
import warnings                       # warning

# Numpy
import numpy as np  # numerical python
import scipy        # scientific python

# TODO implement when no TqdmExperimentalWarning
# from tqdm.autonotebook import tqdm
from tqdm import tqdm_notebook as tqdm

## Custom
from astroPHD.util import ObjDict          # custom dictionary-like object
from astroPHD.util.logging import LogFile  # LoggerFile  # custom logging


# +--------------------------------------------------------------------------+
# IPython Magic

from IPython.core.interactiveshell import InteractiveShell
from IPython.core.debugger import set_trace
from IPython.display import (
    display,               # display is a better print
    Latex, Markdown       # for printing LaTeX or Markdown strings
)

# %run runs in the main namespace, so need to run as 'src.', not '.''
from astroPHD.ipython import (
    printmd, printMD,               # markdown printing
    printltx, printLaTeX,           # LaTeX printing
    set_autoreload, aimport,        # imports
    run_imports, import_from_file,  # imports
    add_raw_code_toggle,            # notebook
)


##############################################################################
### Running Imported Functions

InteractiveShell.ast_node_interactivity = "all"


##############################################################################
### Printing Information

print("""base_imports:
    Base: os, sys, time, pdb, warnings,
          numpy -> np, scipy,
          tqdm_notebook -> tqdm
    Logging: .LogFile
    Misc: ObjDict
    IPython: display, Latex, Markdown, set_trace,
             printmd, printMD, printltx, printLaTeX,
             configure_matplotlib,
             set_autoreload, aimport,
             run_imports, import_from_file,
""")

##############################################################################
### END
