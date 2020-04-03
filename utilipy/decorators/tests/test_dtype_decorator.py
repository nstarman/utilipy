#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_dtype_decorator
#
# ----------------------------------------------------------------------------

"""Test functions for dtype_decorator."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

import numpy as np


# PROJECT-SPECIFIC

from utilipy.decorators.func_io import (
    dtypeDecorator,
    # dtypeDecoratorMaker,
    # # standard types
    # intDecorator,
    # floatDecorator,
    # strDecorator,
    # boolDecorator,
    # # numpy
    # ndarrayDecorator,
    # ndfloat64Decorator,
)


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
    try:
        assert isinstance(func(z), float)
    except TypeError:
        pass
    else:
        raise AssertionError("func([3, 4.4]) should have failed")

    assert isinstance(func(u), float)

    try:
        assert isinstance(func(uu), float)
    except ValueError:
        pass
    else:
        raise AssertionError("func('5.5') should have failed")

    assert isinstance(func(v), float)

    try:
        assert isinstance(func(w), float)
    except TypeError:
        pass
    else:
        raise AssertionError("func(np.array([7, 8.8])) should have failed")


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
