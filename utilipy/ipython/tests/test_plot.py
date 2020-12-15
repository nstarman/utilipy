# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.ipython.plot`."""


__all__ = ["test_plot"]


##############################################################################
# plot

# THIRD PARTY
import pytest

# PROJECT-SPECIFIC
from utilipy.ipython import plot

##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


def test__all__():
    """Test everything in  ``__all__`` is there."""
    for obj in plot.__all__:
        assert hasattr(plot, obj)


# /def


# -------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_plot():
    """Test :class:`~utilipy.ipython.plot`."""


# /def


# -------------------------------------------------------------------


##############################################################################
# END
