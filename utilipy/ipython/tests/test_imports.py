# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.ipython.imports`."""


__all__ = ["test_imports"]


##############################################################################
# IMPORTS

# THIRD PARTY
import pytest

# PROJECT-SPECIFIC
from utilipy import imports

##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


def test__all__():
    """Test everything in  ``__all__`` is there."""
    for obj in imports.__all__:
        assert hasattr(imports, obj)


# /def


# -------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_imports():
    """Test :class:`~utilipy.ipython.imports`."""


# /def


# -------------------------------------------------------------------


##############################################################################
# END
