#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Standard Import File
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
# Plotting

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import cm, colors

# +--------------------------------------------------------------------------+
# IPython Magic

from astroPHD.ipython.plot import configure_matplotlib


##############################################################################
### Running Imported Functions

configure_matplotlib(backend='inline', figure_format='retina')


##############################################################################
### Printing Information

print("""Imported from Matplotlib:
    pyplot->plt
    matplotlib->mpl, .colors, .cm
    configure_matplotlib
""")


##############################################################################
### END
