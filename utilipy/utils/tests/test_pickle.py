# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.utils.pickle`."""


__all__ = [
    "test_config",
    "Test_dump",
    "test_dump_many",
    "test_load",
]


##############################################################################
# IMPORTS

# BUILT-IN
import tempfile

# THIRD PARTY
import numpy as np
import pytest

# PROJECT-SPECIFIC
from utilipy.tests.helper import BaseClassDependentTests
from utilipy.utils import pickle

##############################################################################
# PARAMETERS

objs = {
    int: 1,
    float: 0.2,
    list: [1, 2],
    tuple: (3, 4),
    dict: {"a": 1, "b": 2},
    np.ndarray: np.array([1, 2, 3, 4, 5]),
}

##############################################################################
# TESTS
##############################################################################


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


class Test_dump(BaseClassDependentTests, klass=pickle.dump):
    """Test `~utilipy.utils.pickle.dump`."""

    @pytest.mark.parametrize("obj", objs)
    @staticmethod
    def test_can_dump_objs(obj):
        """Test can dump a few different objects. Unpickle later."""
        # temporary file
        with tempfile.NamedTemporaryFile() as fname:

            pickle.dump(obj, fname=fname)

    # /def

    @pytest.mark.skipif(not pickle.HAS_DILL, reason="`dill` not installed.")
    @pytest.mark.parametrize("obj", objs)
    @staticmethod
    def test_use_dill(obj):
        """Test can dump a few different objects with dill."""
        # temporary file
        with tempfile.NamedTemporaryFile() as fname:

            pickle.dump(obj, fname=fname, use_dill=True)

    # /def

    @pytest.mark.skipif(pickle.HAS_DILL, reason="`dill` installed.")
    @staticmethod
    def test_fail_use_dill():
        """Test failed use of dill.

        Skip if has dill, since want it to fail.
        """
        # expect error
        with pytest.raises(ValueError):

            # make temporary file
            with tempfile.NamedTemporaryFile() as fname:

                pickle.dump([1, 2, 3], fname=fname, use_dill=True)

    # /def


# /class

# --------------------------------------------------------------------------


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


##############################################################################
# END
