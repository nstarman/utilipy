# -*- coding: utf-8 -*-
# see LICENSE.rst

# ----------------------------------------------------------------------------
#
# TITLE   : test constants frozen
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Tests."""

__author__ = "Nathaniel Starkman"

# __all__ = [
#     ""
# ]


##############################################################################
# IMPORTS

# GENERAL

import astropy.units as u


# PROJECT-SPECIFIC

from .. import _frozen, data


##############################################################################
# TESTS
##############################################################################


def test_FrozenConstants():
    """Test FrozenConstants class."""
    f = _frozen.FrozenConstants()

    # --------------
    # check has all constants

    assert f.__all_constants__ == data.__all_constants__

    # --------------
    # check equality

    C = data.read_constants()

    name: str
    for name in data.__all_constants__:
        assert getattr(f, name) == C[name]["value"] * u.Unit(C[name]["unit"])

    # --------------
    # check __getitem__

    assert f[name] == C[name]["value"] * u.Unit(C[name]["unit"])

    return


# /def


# ------------------------------------------------------------------------


def test_frozen():
    """Test `frozen`."""
    f = _frozen.frozen
    # --------------
    # check has all constants

    assert f.__all_constants__ == data.__all_constants__

    # --------------
    # check equality

    C = data.read_constants()

    name: str
    for name in data.__all_constants__:
        assert getattr(f, name) == C[name]["value"] * u.Unit(C[name]["unit"])

    # --------------
    # check __getitem__

    assert f[name] == C[name]["value"] * u.Unit(C[name]["unit"])

    return


# /def


# ------------------------------------------------------------------------


##############################################################################
# END
