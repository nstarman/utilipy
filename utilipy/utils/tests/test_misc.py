# -*- coding: utf-8 -*-

"""Test contents of :mod:`~utilipy.utils.misc`."""

__all__ = [
    "test_temporary_namespace",
    "test_make_help_function",
]


##############################################################################
# IMPORTS

# THIRD PARTY

import pytest


# PROJECT-SPECIFIC

from .. import misc


##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


@pytest.mark.skip()
def test_temporary_namespace():
    """Test :func:`~utilipy.utils.misc.temporary_namespace`."""
    x = 1
    y = 2

    with misc.temporary_namespace(None, keep=["a",]):
        a = 3
        b = 4

    assert x, y == (1, 2)
    assert a == 3
    # assert "a" in test_temporary_namespace.__dict__
    # with pytest.raises(AssertionError):
    #     assert "b" in test_temporary_namespace.__dict__


# /def


# -------------------------------------------------------------------


@pytest.mark.skip()
def test_make_help_function():
    """Test :func:`~utilipy.utils.misc.make_help_function`."""
    pass


# /def


##############################################################################
# END
