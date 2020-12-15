# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.utils.pickle`."""


__all__ = [
    "test_dump",
    "test_save",
    "test_dump_many",
    "test_load",
    "test_load_many",
]


##############################################################################
# IMPORTS

# THIRD PARTY
import pytest

# PROJECT-SPECIFIC
from utilipy.utils import pickle

##############################################################################
# Tests


def test_config():
    """Test `~utilipy.utils.pickle.conf`.

    .. todo::

        A unified method of testing configs

    """
    assert pickle.conf.use_dill is False

    with pickle.conf.set_temp("use_dill", True):
        assert pickle.conf.use_dill is True


# /def


# --------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_dump():
    """Test :func:`~utilipy.utils.pickle.dump`."""
    assert False, pickle


# /def


@pytest.mark.skip(reason="TODO")
def test_save():
    """Test :func:`~utilipy.utils.pickle.save`."""
    assert False


# /def


@pytest.mark.skip(reason="TODO")
def test_dump_many():
    """Test :func:`~utilipy.utils.pickle.dump_many`."""
    assert False


# /def


# --------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_load():
    """Test :func:`~utilipy.utils.pickle.load`."""
    assert False


# /def


@pytest.mark.skip(reason="TODO")
def test_load_many():
    """Test :func:`~utilipy.utils.pickle.load_many`."""
    assert False


# /def


##############################################################################
# END
