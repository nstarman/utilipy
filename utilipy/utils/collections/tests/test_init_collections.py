# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE  : test util/collections/__init__
#
# ----------------------------------------------------------------------------

"""tests for util/collections/__init__
"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

# import numpy as np


# PROJECT-SPECIFIC

from ... import collections


##############################################################################
# Tests


def test_imported():
    """test standard use of idxDecorator
    """
    from utilipy.utils.collections._ObjDict import ObjDict

    # using added kwarg
    assert collections.ObjDict is ObjDict

    return


# /def


# --------------------------------------------------------------------------


##############################################################################
# END
