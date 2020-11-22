# -*- coding: utf-8 -*-

"""Test data_util :mod:`~utilipy.data_utils.decorators`."""


__all__ = [
    "test_make_shuffler",
    "test_intermix_arrays",
]


##############################################################################
# IMPORTS

# THIRD PARTY
import numpy as np

# PROJECT-SPECIFIC
from utilipy.data_utils import utils

##############################################################################
# PARAMETERS

x = np.arange(2)
y = np.arange(2) + 2

z = np.c_[x, y].T


##############################################################################
# TESTS
##############################################################################


def test_make_shuffler():
    """Test :func:`~utilipy.data_utils.utils.shuffle`."""
    arr = np.arange(100)

    shuffler, undo = utils.make_shuffler(len(arr))

    # shuffling an identity index array yields the shuffler
    assert all((arr[shuffler] - shuffler) == 0.0)

    # unshuffling the shuffler is the identity index array
    assert all(shuffler[undo] == arr)

    # unshufffling works
    assert all(arr[shuffler][undo] == arr)

    return


# /def


# ------------------------------------------------------------------------


def test_intermix_arrays():
    """Test :func:`~utilipy.data_utils.utils.intermix_arrays`."""
    x = np.arange(5)
    y = np.arange(5, 10)
    z = np.arange(10, 15)
    xx = np.c_[x, y]
    yy = np.c_[z, np.arange(15, 20)]

    # Mix single scalar array
    m = utils.intermix_arrays(x)
    expected = np.array([0, 1, 2, 3, 4])

    assert np.all(m == expected)

    # Mix two scalar arrays
    m = utils.intermix_arrays(x, y)
    expected = np.array([0, 5, 1, 6, 2, 7, 3, 8, 4, 9])

    assert np.all(m == expected)

    # Mix multiple scalar arrays
    m = utils.intermix_arrays(x, y, z)
    expected = np.array([0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14])

    assert np.all(m == expected)

    # Mix single ND array
    m = utils.intermix_arrays(xx)
    expected = np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])

    assert np.all(m == expected)

    # Mix two ND arrays
    m = utils.intermix_arrays(xx, yy)
    expected = np.array(
        [
            [0, 10, 1, 11, 2, 12, 3, 13, 4, 14],
            [5, 15, 6, 16, 7, 17, 8, 18, 9, 19],
        ]
    )

    assert np.all(m == expected)

    # Axis arguments
    m = utils.intermix_arrays(xx, yy, axis=0)
    expected = np.array(
        [
            [0, 10, 1, 11, 2],
            [12, 3, 13, 4, 14],
            [5, 15, 6, 16, 7],
            [17, 8, 18, 9, 19],
        ]
    )

    assert np.all(m == expected)


# /def


##############################################################################
# END
