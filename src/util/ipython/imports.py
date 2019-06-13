#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Standard Import File
# AUTHOR  : Nathaniel Starkman
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""standard import file.
imports:

GENERAL
-------
os, sys  # operating system
time
pdb
warnings

numpy -> np
scipy

tqdm.tqdm_notebook -> tqdm_nb


ASTROPY
-------
astropy
.units -> u
.coordinates -> coords
    .SkyCoord
.table.Table, QTable
.visualization.quantity_support, astropy_mpl_style

**also does:
quantity_support()
plt.style -> astropy_mpl_style


PLOTTING
--------
starkplot -> plt
.mpl_decorator

matplotlib -> mpl
.colors
.cm

Logging
-------
logging
.util.logging.LogFile, LoggerFile

Misc
-------
.util.ObjDict

IPYTHON
-------
display, Latex, Markdown, set_trace,
printmd, printltx

**also does:
%matplotlib inline
%config InlineBackend.figure_format = 'retina'
InteractiveShell.ast_node_interactivity = "all"
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### Imports

# +---------------------------------------------------------------------------+
# Basic

import os, sys                        # operating system
import time                           # timing
import pdb                            # debugging
import warnings                       # warning
# warnings.filterwarnings('ignore', RuntimeWarning)

# Numpy
import numpy as np  # numerical python
import scipy        # scientific python

# +------------------------+
# from tqdm.autonotebook import tqdm  # TODO implement when no TqdmExperimentalWarning
from tqdm import tqdm_notebook as tqdm_nb

# +---------------------------------------------------------------------------+
# Astropy
import astropy

from astropy import units as u             # units TODO replace with mine
from astropy import coordinates as coords  # coordinates

from astropy.coordinates import SkyCoord
from astropy.table import Table, QTable  # table data structure

# Allowing quantities in matplotlib
from astropy.visualization import quantity_support, astropy_mpl_style

# +---------------------------------------------------------------------------+
# Plotting

try:
    import starkplot as plt
except ImportError as e:
    warnings.warn('Cannot import starkplot, using matplotlib.pyplot instead.' +
                  '\nmpl_decorator will not work.')
    from matplotlib import pyplot as plt
else:
    from starkplot import mpl_decorator

import matplotlib as mpl
from matplotlib import colors
from matplotlib import cm

# +--------------------------------------------------------------------------+
# IPython Magic

# %run runs in the main namespace, so need to run as 'src.', not '.''
from src.util.ipython import (
    display, Latex, Markdown,
    set_trace,
    printmd, printltx
)
# this also does: %matplotlib inline,
#                 %config InlineBackend.figure_format = 'retina'
#                 InteractiveShell.ast_node_interactivity = "all"

# +--------------------------------------------------------------------------+
# Logging

from src.util.logging import (
    logging,                          # standard logging
    LogFile,                          # custom minimal logging
    LoggerFile                        # custom extended logger
)

# +--------------------------------------------------------------------------+
# Custom Functions
from src.util import ObjDict

##############################################################################
### Running Imported Functions

# astropy changes
quantity_support()
plt.style.use(astropy_mpl_style)

# cleaning up
# del quantity_support, astropy_mpl_style

##############################################################################
### Priting Information

print("""Imported:
Base: os, sys, time, pdb, warnings, numpy -> np, scipy
Astropy: astropy, .units->u, .coordinates->coords, .SkyCoord, .Table, .QTable
Plot: starkplot->plt, .mpl_decorator
      matplotlib->mpl, .colors, .cm
Logging: logging, .LogFile, .LoggerFile
Misc: ObjDict
IPython: display, Latex, Markdown, set_trace, printmd, printltx
""")
