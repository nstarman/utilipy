# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""Setup for :mod:`~utilipy.imports`."""


###############################################################################
# IMPORTS

from __future__ import absolute_import

# BUILT-IN
import typing as T
from contextlib import contextmanager

# THIRD PARTY
from astropy import config as _config

###############################################################################
# CODE
###############################################################################


class Conf(_config.ConfigNamespace):
    """Configuration parameters for `utilipy.imports`."""

    verbose_imports = _config.ConfigItem(
        True,
        description="imports import verbosity configuration",
        cfgtype="boolean(default=True)",
    )


conf = Conf()
# /class


# -------------------------------------------------------------------


@contextmanager
def use_import_verbosity(verbosity: T.Optional[bool] = None):
    """Set import verbosity only inside a with block.

    Wrapper for conf.set_temp('verbose_imports', verbosity).

    Parameters
    ----------
    verbosity : bool, Optional
        the import verbosity, None (default) doesn't change value.

    Yields
    ------
    :class:`~utilipy.imports.conf`

    """
    with conf.set_temp("verbose_imports", verbosity):  # use existing system.
        yield conf

    return


# /def


###############################################################################
# INFO


__all__ = [
    "conf",  # configuration instance
    "use_import_verbosity",  # contextmanager
]


###############################################################################
# END
