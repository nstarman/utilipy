# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : astronat imports
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Base set of imports for :mod:`~astronat`.

Only imports if astronat is installed

Routine Listings
----------------
astronat : imports

    - constants, dynamics, units, utils
    - reload_config -> astronat_reload_config
    - online_help -> astronat_online_help
    - help -> astronat_help

References
----------
Plotly reference [#]_.

.. [#] plotly: Collaborative data science, Plotly Technologies (2015),
    (https://plot.ly)

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "astronat_imports_help",
    # modules
    "constants",
    "dynamics",
    "units",
    "utils",
    # functions
    "astronat_reload_config",
    "astronat_online_help",
    "astronat_help",
    "TableList",
    "QTableList",
    "TablesList",
]


##############################################################################
# HELPER FUNCTIONS

from utilipy.imports import conf
from utilipy.utils import make_help_function


##############################################################################
# IMPORTS

try:

    import astronat

except ImportError:

    import warnings

    warnings.warn("Cannot import astronat")

else:

    # modules
    from astronat import constants, dynamics, units, utils

    # functions
    from astronat import (
        reload_config as astronat_reload_config,
        online_help as astronat_online_help,
        help as astronat_help,
    )

    from astronat.utils.table import TableList, QTableList, TablesList


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
