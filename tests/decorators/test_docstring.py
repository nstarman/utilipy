#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_select
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""test functions for data_utils/select
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
# import numpy as np

## Project-Specific
from astroPHD.decorators.docstring import (replace_docstring)


##############################################################################
### PARAMETERS


##############################################################################
### idxDecorator

def test_replace_docstring():
    """Test replace_docstring."""
    class Test(object):
        """Test Class."""

        def __init__(self):
            super(Test, self).__init__()

        def test1():
            """Docstring for test1."""
            pass

        @replace_docstring(docstring=test1.__doc__)
        def test2():
            pass

    assert Test.test2.__doc__ == Test.test1.__doc__

    assert Test().test2.__doc__ == Test().test1.__doc__

    return
# /def


# --------------------------------------------------------------------------


##############################################################################
### END