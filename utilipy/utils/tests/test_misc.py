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
from utilipy.utils import misc

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


def test_temporary_namespace():  # TODO FIX
    """Test :func:`~utilipy.utils.misc.temporary_namespace`."""
    x = 1
    y = 2

    with misc.temporary_namespace(locals(), keep=["a"]):
        locals()["a"] = 3  # TODO FIX
        locals()["b"] = 4

    assert x, y == (1, 2)
    assert locals()["a"] == 3

    with pytest.raises(AssertionError):
        assert "b" in locals()


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

    assert help_function.__name__ == "test_help"
    assert help_function.__module__ == "null_module"
    assert help_function.__doc__ == "Help for test.\n\n" + _doc


# /def


##############################################################################
# END
