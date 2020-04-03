# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : frozen unit set
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Frozen Constants, sourced from Astropy.



References
----------
References [#]_.

.. [#] Astropy Collaboration et al., 2018, AJ, 156, 123.

"""

__author__ = "Nathaniel Starkman"
__credits__ = ["astropy"]


__all__ = [
    "FrozenConstants",
    "frozen",
]


###############################################################################
# IMPORTS

from . import data
from .. import units as u


###############################################################################
# CODE
###############################################################################


class FrozenConstants:
    """Frozen Constants.

    Attributes
    ----------
    __all_constants__: frozenset
    and all contents

    """

    # def __setattr__(self, name, value):
    #     """Attributes are locked. Only permit in __all_constants__."""
    #     if name in data.__all_constants__:
    #         super().__setattr__(name, value)
    #     return

    # # /def

    def __getitem__(self, name):
        """Get attribute as item."""
        return getattr(self, name)

    # /def

    def __init__(self):
        """Initialize Frozen Constants.

        Set __all_constants__ and all contained constants

        """
        self.__all_constants__ = data.__all_constants__

        C = data.read_constants()

        for name in data.__all_constants__:
            setattr(self, name, C[name]["value"] * u.Unit(C[name]["unit"]))

    # /def


# /class


###############################################################################
# Values

frozen = FrozenConstants()


###############################################################################
# END
