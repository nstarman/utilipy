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

# scipy
scipy

tqdm.tqdm_notebook -> tqdm


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
from tqdm import tqdm_notebook as tqdm

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

import logging                                    # for logging
from src.util.logging import LogFile, LoggerFile  # custom logging

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
IPython: display, Latex, Markdown, set_trace, printmd, printltx
""")
