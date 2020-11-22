# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : plotly imports
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Base set of imports for :mod:`~plotly`.

Only imports if plotly is installed

Routine Listings
----------------
plotly : imports

    - plotly
    - express -> px
    - graph_objs -> go
    - io -> pio
    - subplots -> make_subplots

plotly_imports_help


References
----------
Plotly reference [#]_.

.. [#] plotly: Collaborative data science, Plotly Technologies (2015),
    (https://plot.ly)

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "plotly_imports_help",
    "HAS_PLOTLY",
]


##############################################################################
# HELPER FUNCTIONS

# PROJECT-SPECIFIC
from utilipy.imports import conf
from utilipy.utils import make_help_function

##############################################################################
# IMPORTS

try:

    import plotly

except ImportError:
    import warnings

    warnings.warn("Cannot import plotly")

    HAS_PLOTLY: bool = False

else:

    HAS_PLOTLY: bool = True

    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio
    from plotly.subplots import make_subplots

    __all__ += ["plotly", "px", "go", "pio", "make_subplots"]

# /if


##############################################################################
# Printing Information

plotly_imports_help = make_help_function(
    "plotly", __doc__, look_for="Routine Listings"
)


if conf.verbose_imports:
    plotly_imports_help()


##############################################################################
# END
