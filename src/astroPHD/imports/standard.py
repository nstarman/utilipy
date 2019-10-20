#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Standard Import File
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""standard import file.
imports:

GENERAL
-------
os, sys  # operating system
time
pdb
warnings

numpy -> np
scipy


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
.util.logging.LogFile

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
# warnings.filterwarnings('ignore', RuntimeWarning)

# Numpy
import numpy as np  # numerical python
import scipy        # scientific python

## Custom
# import logging                            # for logging
from astroPHD.util.logging import LogFile  # custom loggin

# +---------------------------------------------------------------------------+
# Astropy

import astropy

from astropy import units as u             # units
from astropy import coordinates as coords  # coordinates

from astropy.coordinates import SkyCoord   # SkyCoord
from astropy.table import Table, QTable    # table data structure

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
from matplotlib import cm
from matplotlib import colors



##############################################################################
### Running Imported Functions

# astropy changes
quantity_support()
plt.style.use(astropy_mpl_style)


##############################################################################
### Cleaning Up

# cleaning up
# del quantity_support, astropy_mpl_style


##############################################################################
### Printing Information

_import = {
    base: "os, sys, time, pdb, warnings,"
    "      numpy -> np, scipy,"
    "      tqdm_notebook -> tqdm",
    astropy: "astropy, .units->u, .coordinates->coords, .SkyCoord, .Table, .QTable",
    plot: "starkplot->plt, .mpl_decorator"
    "      matplotlib->mpl, .colors, .cm",
    logging: ".LogFile"
}

if __name__ == "__main__":

    print("""Imported:
    Base: os, sys, time, pdb, warnings,
          numpy -> np, scipy,
          tqdm_notebook -> tqdm
    Astropy: astropy, .units->u, .coordinates->coords, .SkyCoord, .Table, .QTable
    Plot: starkplot->plt, .mpl_decorator
          matplotlib->mpl, .colors, .cm
    Logging: .LogFile
    IPython: display, Latex, Markdown, set_trace,
             printmd, printMD, printltx, printLaTeX,
             configure_matplotlib,
             set_autoreload  #, aimport, aimports
    """)

##############################################################################
### End