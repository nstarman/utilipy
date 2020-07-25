# -*- coding: utf-8 -*-

"""Test contents of :mod:`~utilipy.utils.misc`."""

__all__ = [
    "test_temporary_namespace",
    "test_make_help_function_raises",
]


##############################################################################
# IMPORTS

# BUILT-IN

import types


# THIRD PARTY

import pytest


# PROJECT-SPECIFIC

from .. import misc


##############################################################################
# PARAMETERS

_doc_ = __doc__

_doc = """Docstring

Returns
-------
Nothing.

"""


##############################################################################
# CODE
##############################################################################


@pytest.mark.skip()
def test_temporary_namespace():
    """Test :func:`~utilipy.utils.misc.temporary_namespace`."""
    x = 1
    y = 2

    with misc.temporary_namespace(None, keep=["a",]):
        a = 3
        b = 4

    assert x, y == (1, 2)
    assert a == 3
    # assert "a" in test_temporary_namespace.__dict__
    # with pytest.raises(AssertionError):
    #     assert "b" in test_temporary_namespace.__dict__


# /def


# -------------------------------------------------------------------


def test_make_help_function_raises():
    """Test :func:`~utilipy.utils.misc.make_help_function` Exceptions."""
    with pytest.raises(TypeError):
        misc.make_help_function("test", look_for=Exception)


# /def


def test_make_help_function_find_module():
    """Test :func:`~utilipy.utils.misc.make_help_function` Exceptions."""
    help_function = misc.make_help_function("test", module=None)

    assert help_function.__name__ == "test_help"
    assert help_function.__module__ == "utilipy.utils.tests.test_misc"
    assert help_function.__doc__ == "Help for test.\n\n" + _doc_


# /def


def test_make_help_function_pass_module():
    """Test :func:`~utilipy.utils.misc.make_help_function` Exceptions."""
    module = types.ModuleType("null_module", doc=_doc)

    help_function = misc.make_help_function("test", module=module)

    # import pdb; pdb.set_trace()

    assert help_function.__name__ == "test_help"
    assert help_function.__module__ == "null_module"
    assert help_function.__doc__ == "Help for test.\n\n" + _doc


# /def


##############################################################################
# END
