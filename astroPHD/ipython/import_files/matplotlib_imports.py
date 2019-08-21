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

from astroPHD.ipython.plot import configure_matplotlib


##############################################################################
### Running Imported Functions

configure_matplotlib(backend='inline', figure_format='retina')


##############################################################################
### Printing Information

print("""Imported from Matplotlib:
    starkplot->plt, .mpl_decorator
    matplotlib->mpl, .colors, .cm
""")


##############################################################################
### END
