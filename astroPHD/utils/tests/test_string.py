# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE  : test util/string
#
# ----------------------------------------------------------------------------

"""tests for util/string.py."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

# PROJECT-SPECIFIC

from .. import string


##############################################################################
# Tests


def test_FormatTemplate():
    """Test FormatTemplate.

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
