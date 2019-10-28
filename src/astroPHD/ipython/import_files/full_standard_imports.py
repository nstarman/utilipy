#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""full standard import file.

GENERAL
-------
os, sys  # operating system
time
pdb
warnings

numpy -> np
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
.cm
.colors

Logging
-------
logging
.util.logging.LogFile

Misc
-------
.util.ObjDict

IPYTHON
-------
display, Latex, Markdown, set_trace,
printmd, printMD, printltx, printLaTeX
set_autoreload, # aimport, aimports
configure_matplotlib

**also does:
%matplotlib inline
%config InlineBackend.figure_format = 'retina'
InteractiveShell.ast_node_interactivity = "all"
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
from astroPHD.util import ObjDict  # custom dictionary-like object
from astroPHD.util.logging import LogFile  #, LoggerFile  # custom logging

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
except ImportError:
    warnings.warn('Cannot import starkplot, using matplotlib.pyplot instead.' +
                  '\nmpl_decorator will not work.')
    from matplotlib import pyplot as plt
else:
    from starkplot import mpl_decorator

import matplotlib as mpl
from matplotlib import cm, colors

# +--------------------------------------------------------------------------+
# IPython Magic

from IPython.core.interactiveshell import InteractiveShell

from astroPHD.ipython.autoreload import set_autoreload, aimport
from astroPHD.ipython.plot import configure_matplotlib

# %run runs in the main namespace, so need to run as 'src.', not '.''
from astroPHD.ipython import (
    display, Latex, Markdown,
    set_trace,
    printmd, printMD,
    printltx, printLaTeX
)
# this also does: %matplotlib inline,
#                 %config InlineBackend.figure_format = 'retina'
#                 InteractiveShell.ast_node_interactivity = "all"

##############################################################################
### Running Imported Functions

InteractiveShell.ast_node_interactivity = "all"

configure_matplotlib(backend='inline', figure_format='retina')

# astropy changes
quantity_support()
plt.style.use(astropy_mpl_style)


##############################################################################
### Cleaning Up

# # cleaning up
# del InteractiveShell
# del quantity_support, astropy_mpl_style


##############################################################################
### Printing Information

# print("""Imported:
# Base: os, sys, time, pdb, warnings,
#       numpy -> np, scipy,
#       tqdm_notebook -> tqdm
# Astropy: astropy, .units->u, .coordinates->coords, .SkyCoord, .Table, .QTable
# Plot: starkplot->plt, .mpl_decorator
#       matplotlib->mpl, .colors, .cm
# Logging: .LogFile
# Misc: ObjDict
# IPython: display, Latex, Markdown, set_trace,
#          printmd, printMD, printltx, printLaTeX,
#          configure_matplotlib,
#          set_autoreload, aimport(s)
# """)

##############################################################################
### END
