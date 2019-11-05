# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : matplotlib_imports
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
r"""Base set of imports for matplotlib.

Returns
-------
Matplotlib:
    pyplot->plt
    matplotlib->mpl, .colors, .cm
astroPHD:
    ipython.plot.configure_matplotlib

References
----------
Matplotlib reference is [1]_

.. [1] John D. Hunter. Matplotlib: A 2D Graphics Environment, Computing in
    Science & Engineering, 9, 90-95 (2007), DOI:10.1109/MCSE.2007.55
    http://scitation.aip.org/content/aip/journal/cise/9/3/10.1109/MCSE.2007.55

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# HELPER FUNCTIONS

from astroPHD.util.config import __config__
from astroPHD.util.decorators.docstring import (
    _set_docstring_import_file_helper,
    _import_file_docstring_helper
)


##############################################################################
# IMPORTS

# +---------------------------------------------------------------------------+
# Plotting

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import cm, colors

from mpl_toolkits.mplot3d import Axes3D  # 3D plotting

# +--------------------------------------------------------------------------+
# IPython Magic

from astroPHD.ipython.plot import configure_matplotlib


##############################################################################
# Running Imported Functions

configure_matplotlib(backend='inline', figure_format='retina')


##############################################################################
# Printing Information

@_set_docstring_import_file_helper('Matplotlib', __doc__)  # doc from __doc__
def matplotlib_imports_help():
    """Help for Matplotlib base imports."""
    _import_file_docstring_helper(matplotlib_imports_help.__doc__)  # format
# /def


if __config__.getboolean('verbosity', 'verbose-imports'):
    matplotlib_imports_help()


##############################################################################
# END
