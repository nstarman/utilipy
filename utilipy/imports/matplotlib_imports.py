# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : matplotlib_imports
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Base set of imports for :mod:`~matplotlib`.

Routine Listings
----------------
Matplotlib: imports

    - pyplot->plt
    - matplotlib->mpl, .cm, .colors
    - mpl_toolkits.mplot3d.Axes3D

utilipy: imports

    - ipython.plot.configure_matplotlib

References
----------
Matplotlib reference [#]_.

.. [#] John D. Hunter. Matplotlib: A 2D Graphics Environment, Computing in
    Science and Engineering, 9, 90-95 (2007), DOI:10.1109/MCSE.2007.55
    http://scitation.aip.org/content/aip/journal/cise/9/3/10.1109/MCSE.2007.55

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "mpl",
    "plt",
    "cm",
    "colors",
    # "Axes3D",
    "matplotlib_imports_help",
]


##############################################################################
# HELPER FUNCTIONS

# THIRD PARTY
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm, colors

# PROJECT-SPECIFIC
from utilipy.imports import conf
from utilipy.utils import make_help_function

# from mpl_toolkits.mplot3d import Axes3D


# +--------------------------------------------------------------------------+
# IPython Magic

try:

    _HAS_IPYTHON = False

    get_ipython()

    if get_ipython() is None:  # double checking
        raise NameError

except NameError:

    pass

else:

    _HAS_IPYTHON = True

    from utilipy.ipython.plot import configure_matplotlib

    __all__ += [
        "configure_matplotlib",
    ]  # TODO add when no IPython


##############################################################################
# Running Imported Functions

if _HAS_IPYTHON:

    configure_matplotlib(backend="inline", figure_format="retina")


##############################################################################
# Printing Information

matplotlib_imports_help = make_help_function(
    "matplotlib", __doc__, look_for="Routine Listings"
)


if conf.verbose_imports:
    matplotlib_imports_help()


##############################################################################
# END
