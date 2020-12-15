# -*- coding: utf-8 -*-

"""Tests for module :mod:`~utilipy.decorators.code_dev`."""

__all__ = [
    "test_DevelopmentWarning",
    "test_BetaDevelopmentWarning",
    "test_indev_doc",
    "test_indev_func_message",
    "test_indev_decorator_func",
    "test_indev_decorator_class",
]


##############################################################################
# IMPORTS

# BUILT-IN
import warnings

# THIRD PARTY
import pytest

# PROJECT-SPECIFIC
from utilipy.decorators import code_dev as cdev

##############################################################################
# CODE
##############################################################################

#####################################################################
# Warnings


def test_DevelopmentWarning():
    """Test `~utilipy.decorators.code_dev.DevelopmentWarning`."""
    with pytest.warns(cdev.DevelopmentWarning):

        warnings.warn(cdev.DevelopmentWarning())

    # /with


# /def


# -------------------------------------------------------------------


def test_BetaDevelopmentWarning():
    """Test `~utilipy.decorators.code_dev.BetaDevelopmentWarning`."""
    with pytest.warns(cdev.BetaDevelopmentWarning):

        warnings.warn(cdev.BetaDevelopmentWarning())

    # /with


# /def


#####################################################################
# Indev


def test_indev_doc():
    """Test :func:`~utilipy.decorators.code_dev.indev_doc`."""
    old_doc = """Short Summary.

    Parameters
    ----------
    x, y : float

    Returns
    -------
    None

    """

    message = "test code dev"

    new_doc = cdev.indev_doc(old_doc=old_doc, message=message)

    expected_doc = (
        "Short Summary.\n\n"
        "    .. versionchanged:: indev\n\n        test code dev\n\n"
        "    Parameters\n    ----------\n    x, y : float\n\n"
        "    Returns\n    -------\n    None"
    )

    assert new_doc == expected_doc


# /def


# -------------------------------------------------------------------


def test_indev_func_message():
    """Test :func:`~utilipy.decorators.code_dev.indev` function message."""
    # test function
    def _func():
        """Short Summary."""

    # /dev

    indev_func = cdev.indev(
        message=_func,
        name="",
        alternative="",
        todo="",
        obj_type=None,
        warning_type=cdev.DevelopmentWarning,
    )

    assert indev_func.__wrapped__ == _func

    expected_doc = (
        "Short Summary.\n\n"
        "    .. versionchanged:: indev\n\n"
        "        The _func function is in development "
        "and may be added in a future version.\n\n"
    )

    assert indev_func.__doc__ == expected_doc


# /def


# -------------------------------------------------------------------


def test_indev_decorator_func():
    """Test :func:`~utilipy.decorators.code_dev.indev` function message."""
    # --------------

    @cdev.indev()
    def func():
        """Short Summary."""
        return "result"

    # /dev

    assert hasattr(func, "__wrapped__")
    assert func() == func.__wrapped__() == "result"

    assert func.__wrapped__.__doc__ == "Short Summary."
    assert func.__doc__ == (
        "Short Summary.\n\n"
        "    .. versionchanged:: indev\n\n"
        "        The func function is in development "
        "and may be added in a future version.\n\n"
    )

    with pytest.warns(cdev.DevelopmentWarning):
        warnings.warn(func())
    # /with

    # --------------

    @cdev.indev(message="indev message")
    def func():
        """Short Summary."""

    # /dev

    assert func.__doc__ == (
        "Short Summary.\n\n"
        "    .. versionchanged:: indev\n\n"
        "        indev message\n\n"
    )

    # --------------

    @cdev.indev(name="new_name")
    def func():
        """Short Summary."""

    # /dev

    assert func.__doc__ == (
        "Short Summary.\n\n"
        "    .. versionchanged:: indev\n\n"
        "        The new_name function is in development "
        "and may be added in a future version.\n\n"
    )

    # --------------

    @cdev.indev(alternative="alternative")
    def func():
        """Short Summary."""

    # /dev

    assert func.__doc__ == (
        "Short Summary.\n\n"
        "    .. versionchanged:: indev\n\n"
        "        The func function is in development "
        "and may be added in a future version.\n"
        "        Use alternative instead.\n\n"
    )

    # --------------

    @cdev.indev(todo="test")
    def func():
        """Short Summary."""

    # /dev

    assert func.__doc__ == (
        "Short Summary.\n\n"
        "    .. versionchanged:: indev\n\n"
        "        The func function is in development "
        "and may be added in a future version.\n"
        "        TODO: test\n\n"
    )

    # --------------

    @cdev.indev(warning_type=cdev.BetaDevelopmentWarning)
    def func():
        """Short Summary."""

    # /dev

    assert func.__doc__ == (
        "Short Summary.\n\n"
        "    .. versionchanged:: indev\n\n"
        "        The func function is in development "
        "and may be added in a future version.\n\n"
    )

    with pytest.warns(cdev.BetaDevelopmentWarning):
        warnings.warn(func())
    # /with

    # --------------

    @cdev.indev(obj_type="FUNCTION")
    def func():
        """Short Summary."""

    # /dev

    assert func.__doc__ == (
        "Short Summary.\n\n"
        "    .. versionchanged:: indev\n\n"
        "        The func FUNCTION is in development "
        "and may be added in a future version.\n\n"
    )

    # --------------

    @cdev.indev(warning_type=UserWarning)
    def func():
        """Short Summary."""

    # /dev

    with pytest.warns(UserWarning):
        warnings.warn(func())
    # /with


# /def


# -------------------------------------------------------------------


def test_indev_decorator_class():
    """Test :func:`~utilipy.decorators.code_dev.indev` class.

    Don't need to a lot of tests on the docstring, as these are covered
    by both :func:`~utilipy.decorators.code_dev.tests.test_indev_doc` and
    :func:`~utilipy.decorators.code_dev.tests.test_indev_decorator_func`.

    """
    # ----------------

    @cdev.indev()
    class Class(object):
        """docstring for Class."""

        def __init__(self):
            """Short Summary."""
            super(Class, self).__init__()

    # /class

    assert Class.__doc__ == (
        "docstring for Class.\n\n"
        "    .. versionchanged:: indev\n\n"
        "        The Class class is in development "
        "and may be added in a future version.\n\n"
    )

    assert hasattr(Class.__init__, "__wrapped__")

    assert Class.__init__.__wrapped__.__doc__ == "Short Summary."

    with pytest.warns(cdev.DevelopmentWarning):
        warnings.warn(Class())
    # /with


# /def

##############################################################################
# END
