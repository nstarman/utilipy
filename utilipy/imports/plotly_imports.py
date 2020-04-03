# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : plotly imports
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Base set of imports for plotly.

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

__all__ = ["plotly_imports_help"]

##############################################################################
# HELPER FUNCTIONS

from utilipy.config import __config__
from utilipy.decorators.docstring import (
    _set_docstring_import_file_helper,
    _import_file_docstring_helper,
)


##############################################################################
# IMPORTS

try:

    import plotly

except ImportError:

    import warnings

    warnings.warn("Cannot import plotly")

else:

    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio
    from plotly.subplots import make_subplots

# /if


##############################################################################
# Printing Information


@_set_docstring_import_file_helper("plotly", __doc__)  # doc from __doc__
def plotly_imports_help():
    """Help for plotly base imports."""
    doc = _import_file_docstring_helper(plotly_imports_help.__doc__)
    print(doc)
    return


# /def


if __config__.getboolean("verbosity", "verbose-imports"):
    plotly_imports_help()

##############################################################################
# END
