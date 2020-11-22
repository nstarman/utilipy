#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.decorators.func_io.dtype_decorator`."""


##############################################################################
# IMPORTS

# THIRD PARTY
import numpy as np
import pytest

# PROJECT-SPECIFIC
from utilipy.decorators.func_io import dtypeDecorator

##############################################################################
# PARAMETERS

x = 1
y = 2.2
z = [3, 4.4]
u, uu = "5", "5.5"
v = False
w = np.array([7, 8.8])


##############################################################################
# dtypeDecorator


def test_dtypeDecorator_blank():
    """Test no-conversion mode of dtypeDecorator."""
    # defining function
    @dtypeDecorator()
    def func(x):
        return x

    # /def

    assert func(x) == x
    assert func(y) == y
    assert func(z) == z
    assert func(u) == u
    assert func(uu) == uu
    assert func(v) == v
    assert (func(w) == w).all()

    return


# /def


def test_dtypeDecorator_python_scalars():
    """Test standard use of dtypeDecorator."""
    # defining function
    @dtypeDecorator(in_dtype=[(0, int)], out_dtype=[(0, float)])
    def func(x):
        assert isinstance(x, int)
        return x

    # /def

    assert isinstance(func(x), float)
    assert isinstance(func(y), float)

    # should fail
    with pytest.raises(TypeError):
        assert isinstance(func(z), float)

    assert isinstance(func(u), float)

    with pytest.raises(ValueError):
        assert isinstance(func(uu), float)

    assert isinstance(func(v), float)

    with pytest.raises(TypeError):
        assert isinstance(func(w), float)

    return


# /def


# def test_dtypeDecorator_numpy_arrays():
#     """test standard use of dtypeDecorator
#     """
#     # TODO
# # /def


# def test_dtypeDecorator_single_arg():
#     """
#     """
#
#     @dtypeDecorator(inargs=(0, int))
#     def func(x):
#         return x
#
#     # TODO test
#
#     @dtypeDecorator(outargs=(0, int))
#     def func(x):
#         return x
#
#     # TODO test
#
#     @dtypeDecorator(inargs=(0, int), outargs=(1, int))
#     def func(x, y):
#         return x, y
#
#     # TODO test
#
#     return
# # /def


# def test_dtypeDecorator_string_arg():
#     """
#     """
#
#     @dtypeDecorator(inargs=('all', int))
#     def func(x):
#         return x
#
#     # TODO test
#
#     @dtypeDecorator(outargs=('all', int))
#     def func(x):
#         return x
#
#     # TODO test
#
#     @dtypeDecorator(inargs=('all', int), outargs=('all', float))
#     def func(x, y):
#         return x, y
#
#     # TODO test
#
#     return
# # /def


# --------------------------------------------------------------------------


##############################################################################
# END
