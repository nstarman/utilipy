# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""Setup for :mod:`~utilipy.ipython`."""


###############################################################################
# IMPORTS

from __future__ import absolute_import

# BUILT-IN
import typing as T

# THIRD PARTY
from astropy import config as _config

###############################################################################
# CODE
###############################################################################


class Conf(_config.ConfigNamespace):
    """Configuration parameters for `utilipy.ipython`."""

    # AST

    ast_node_interactivity = _config.ConfigItem(
        "all",
        description="AST node interactivity.",
        cfgtype="string(default='all')",
    )

    # Matplotlib

    ipython_matplotlib_backend = _config.ConfigItem(
        "inline",
        description="Configure IPython matplotlib backend.",
        cfgtype="string(default='inline')",
    )

    ipython_matplotlib_figure_format = _config.ConfigItem(
        "retina",
        description="Configure IPython matplotlib figure format.",
        cfgtype="string(default='retina')",
    )


conf = Conf()
# /class


###############################################################################
# INFO


__all__: T.List[str] = [
    "conf",  # configuration instance
]


###############################################################################
# END
