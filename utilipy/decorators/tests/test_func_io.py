# -*- coding: utf-8 -*-

"""Tests for `~utilipy.decorators.func_io`."""


__all__ = [
    "test_store_function_input",
    "test_add_folder_backslash",
    "test_random_generator_from_seed",
]


##############################################################################
# IMPORTS

# BUILT-IN
import functools
import inspect

# THIRD PARTY
import numpy as np
import pytest

# PROJECT-SPECIFIC
from utilipy.decorators import func_io

##############################################################################
# CODE
##############################################################################


def test_store_function_input():
    """Test :func:`~utilipy.decorators.func_io.store_function_input`."""
    # Inputs

    x, y = 1, 2

    # ----------
    # decorate by function call

    def test_func(x, y):
        """Test Function.

        Parameters
        ----------
        x, y : float

        """
        return x, y

    # /def

    # Store inputs
    store_func = func_io.store_function_input(
        test_func, store_inputs=True, _doc_style="numpy", _doc_fmt={}
    )
    res, inputs = store_func(x, y)  # pylint: disable=E1121

    assert res == (x, y)
    assert isinstance(inputs, inspect.BoundArguments)
    assert inputs.args == (x, y)

    # Don't store inputs
    no_store_func = func_io.store_function_input(
        test_func, store_inputs=False, _doc_style="numpy", _doc_fmt={}
    )
    res = no_store_func(x, y)  # pylint: disable=E1121

    assert res == (x, y)

    # ----------
    # decorate by pie-syntax

    @func_io.store_function_input  # all defaults
    def store_pie_func(x, y):
        """Test Function.

        Parameters
        ----------
        x, y : float

        """
        return x, y

    # /def

    res, inputs = store_pie_func(x, y)

    assert res == (x, y)
    assert isinstance(inputs, inspect.BoundArguments)
    assert inputs.args == (x, y)

    # ----------
    # decorate by called pie-syntax

    @func_io.store_function_input(store_inputs=True)  # just explicitly
    def store_pie_func2(x, y):
        """Test Function.

        Parameters
        ----------
        x, y : float

        """
        return x, y

    # /def

    res, inputs = store_pie_func2(x, y)

    assert res == (x, y)
    assert isinstance(inputs, inspect.BoundArguments)
    assert inputs.args == (x, y)


# /def


# -------------------------------------------------------------------


def test_add_folder_backslash():
    """Test :func:`~utilipy.decorators.func_io.add_folder_backslash`."""
    # ----------
    # decorate by function call

    def test_func(x, path):
        return path

    # /def

    args = (None, "~/Documents")

    # call as-is
    assert test_func(*args) == "~/Documents"

    # call decorated
    wrapped_func = func_io.add_folder_backslash(test_func, arguments=["path"])
    assert wrapped_func(*args) == "~/Documents/"  # pylint: disable=E1121

    # for str argument
    wrapped_func = func_io.add_folder_backslash(test_func, arguments="path")
    assert wrapped_func(*args) == "~/Documents/"  # pylint: disable=E1121

    # ----------
    # decorate by pie-syntax

    @func_io.add_folder_backslash(arguments=["path"])
    def wrapped_pie_func(x, path):
        return path

    assert wrapped_pie_func(None, "~/Documents") == "~/Documents/"
    assert wrapped_pie_func.__wrapped__(None, "~/Documents") == "~/Documents"


# /def


# -------------------------------------------------------------------


def _assert_LofLeq(list1, list2):
    """Assert nested lists are equal."""
    assert all(
        all(l1 == l2) if isinstance(l1, np.ndarray) else (l1 == l2)
        for l1, l2 in zip(list1, list2)
    )


def test_random_generator_from_seed():
    """Test :func:`~utilipy.decorators.func_io.random_generator_from_seed`."""
    exp = np.random.RandomState(0).get_state()
    # ----------
    # decorate by function call

    def test_func(x, random):
        return random

    # /def

    args = (None, 0)

    # call as-is
    assert test_func(*args) == 0

    # call decorated
    wrapped_fn = func_io.random_generator_from_seed(test_func)
    _assert_LofLeq(wrapped_fn(*args).get_state(), exp)  # pylint: disable=E1121

    # call wrapped partial
    wrapper = func_io.random_generator_from_seed()
    assert isinstance(wrapper, functools.partial)
    wrapped_fn = wrapper(test_func)
    _assert_LofLeq(wrapped_fn(*args).get_state(), exp)

    # call with str seed_names argument
    wrapped_fn = func_io.random_generator_from_seed(
        test_func, seed_names="random"
    )
    _assert_LofLeq(wrapped_fn(*args).get_state(), exp)  # pylint: disable=E1121

    # call with incorrect seed_names argument
    wrapped_fn = func_io.random_generator_from_seed(
        test_func, seed_names="not_here"
    )
    assert wrapped_fn(*args) == 0  # pylint: disable=E1124

    # call with strict input typing
    wrapped_fn = func_io.random_generator_from_seed(
        test_func, raise_if_not_int=True
    )
    with pytest.raises(TypeError):
        wrapped_fn(None, 0.1)  # pylint: disable=E1124

    # ----------
    # decorate by pie-syntax

    @func_io.random_generator_from_seed(seed_names="rng")
    def wrapped_pie_func(x, rng):
        return rng

    _assert_LofLeq(wrapped_pie_func(None, 0).get_state(), exp)


# /def

##############################################################################
# END
