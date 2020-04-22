# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""Setup for :mod:`~utilipy.constants`."""


###############################################################################
# IMPORTS

# BUILT-IN

from __future__ import absolute_import


# THIRD PARTY

from astropy import config as _config


###############################################################################
# CODE
###############################################################################


class Conf(_config.ConfigNamespace):
    """Configuration parameters for `utilipy.constants`."""

    frozen_constants = _config.ConfigItem(
        True,
        description=(
            "constants set by data file (True), "
            "or by .value on astropy constants at runtime (False)"
        ),
        cfgtype="boolean(default=True)",
    )


# /class


conf = Conf()


###############################################################################
# INFO


__all__ = [
    "conf",  # configuration instance
]


###############################################################################
# END
