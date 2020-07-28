# -*- coding: utf-8 -*-

"""Test data_util :mod:`~utilipy.data_utils.decorators`."""


__all__ = [
    "test_shuffle",
    "test_get_path_to_file",
]


##############################################################################
# IMPORTS

# THIRD PARTY

import numpy as np
import pytest


# PROJECT-SPECIFIC

from ..utils import shuffle, get_path_to_file


##############################################################################
# PARAMETERS

x = np.arange(2)
y = np.arange(2) + 2

z = np.c_[x, y].T


##############################################################################
# TESTS
##############################################################################


def test_shuffle():
    """Test :func:`~utilipy.data_utils.utils.shuffle`."""
    arr = np.arange(100)

    shuffler, undo = shuffle(len(arr))

    # shuffling an identity index array yields the shuffler
    assert all((arr[shuffler] - shuffler) == 0.0)

    # unshuffling the shuffler is the identity index array
    assert all(shuffler[undo] == arr)

    # unshufffling works
    assert all(arr[shuffler][undo] == arr)


# /def


# ------------------------------------------------------------------------


@pytest.mark.skip("TODO")
def test_get_path_to_file():
    """Test :func:`~utilipy.data_utils.utils.get_path_to_file`."""
    get_path_to_file


# /def


# ------------------------------------------------------------------------


##############################################################################
# END
