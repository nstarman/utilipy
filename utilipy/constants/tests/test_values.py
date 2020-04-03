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

from .._frozen import frozen as frozenconstants
from .. import values, data


##############################################################################
# TESTS
##############################################################################


def test_ConstantsValues():
    """Test ConstantsValues class."""
    # ----------------------------
    # Frozen

    f = values.ConstantsValues(frozen=True)

    assert f.from_frozen is True

    _names = set(data.__all_constants__)
    _names.update({"c_ms", "c_kms", "AU_to_pc", "pc_to_AU"})
    assert f._names == _names

    # standard constants
    C = frozenconstants

    for name in data.__all_constants__:
        assert getattr(f, name) == C[name].value

    # __getitem__
    assert f[name] == C[name].value

    # ----------------------------
    # Not Frozen

    # TODO

    return


# /def


# ------------------------------------------------------------------------


def test_values():
    """Test `values`."""
    f = values.values

    assert f.from_frozen is True

    _names = set(data.__all_constants__)
    _names.update({"c_ms", "c_kms", "AU_to_pc", "pc_to_AU"})
    assert f._names == _names

    # standard constants
    C = frozenconstants

    for name in data.__all_constants__:
        assert getattr(f, name) == C[name].value

    # __getitem__
    assert f[name] == C[name].value

    return


# /def


# ------------------------------------------------------------------------


##############################################################################
# END
