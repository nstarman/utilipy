# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Dictionaries
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring
"""Dictionary-style Classes.

Routine Listings
----------------
ReadOnlyDictionaryWrapper

"""

__author__ = "Nathaniel Starkman"
__credit__ = """
    ReadOnlyDictionaryWrapper: https://stackoverflow.com/a/28452633
"""

__all__ = ["ReadOnlyDictionaryWrapper"]


###############################################################################
# IMPORTS

# GENERAL
from collections.abc import Mapping

# CUSTOM

# PROJECT-SPECIFIC


###############################################################################
# CODE
###############################################################################


class ReadOnlyDictionaryWrapper(Mapping):
    """Read-Only Dictionary.

    Warning, the contained dictionary can be modified

    """

    def __init__(self, data):
        """__init__."""
        self._data = data

    # /def

    def __getitem__(self, key):
        """__getitem__."""
        return self._data[key]

    # /def

    def __len__(self):
        """__len__."""
        return len(self._data)

    # /def

    def __iter__(self):
        """__iter__."""
        return iter(self._data)

    # /def


# /class


# --------------------------------------------------------------------------

###############################################################################
# END
