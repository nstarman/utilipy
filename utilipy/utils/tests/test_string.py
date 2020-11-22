# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.utils.string`."""


__all__ = [
    "test_FormatTemplate",
]


##############################################################################
# IMPORTS

# PROJECT-SPECIFIC
from utilipy.utils import string

##############################################################################
# Tests


def test_FormatTemplate():
    """Test :class:`~utilipy.utils.string.FormatTemplate`.

    both full and partial format

    """
    s = string.FormatTemplate("$a ${b} {c} {b} ${a}")

    # -----------------------------------
    # test full format
    assert s.format(a=1, b=2, c=3) == "1 2 3 2 1"

    # test partial format
    assert s.format(a=1) == "1 ${b} ${c} ${b} 1"

    # -----------------------------------
    # __str__

    assert s.__str__() == "$a ${b} ${c} ${b} ${a}"

    return


# /def


# --------------------------------------------------------------------------


##############################################################################
# END
