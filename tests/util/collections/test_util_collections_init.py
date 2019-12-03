#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE  : test util/collections/__init__
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""tests for util/collections/__init__
"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General
import numpy as np

# Project-Specific
from astroPHD.util import collections


##############################################################################
# Tests

def test_imported():
    """test standard use of idxDecorator
    """
    from astroPHD.util.collections._ObjDict import ObjDict

    # using added kwarg
    assert collections.ObjDict is ObjDict

    return
# /def


# --------------------------------------------------------------------------


##############################################################################
# END
