# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : matplotlib_imports
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Base set of imports for matplotlib.


"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# +---------------------------------------------------------------------------+
# Plotting

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import cm, colors

from mpl_toolkits.mplot3d import Axes3D

# +--------------------------------------------------------------------------+
# IPython Magic

from astroPHD.ipython.plot import configure_matplotlib


##############################################################################
# Running Imported Functions

configure_matplotlib(backend='inline', figure_format='retina')


##############################################################################
# Printing Information

def matplotlib_imports_help():
    """Help for matplotlib base imports.

    Imported from Matplotlib:
        pyplot->plt
        matplotlib->mpl, .colors, .cm
        configure_matplotlib

    """
    print(__doc__)
# /def

from astroPHD.util.config import __config__

if __config__.getboolean('verbose', 'verbose-imports'):
    matplotlib_imports_help()


##############################################################################
# END
