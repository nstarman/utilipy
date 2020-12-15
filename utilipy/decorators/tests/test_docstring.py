# -*- coding: utf-8 -*-

"""Test contents of :mod:`~utilipy.decorators.docstring`."""

__all__ = [
    "test_set_docstring_for_import_func",
]


##############################################################################
# IMPORTS

# PROJECT-SPECIFIC
from . import _null_imports
from utilipy.decorators import docstring

##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


def test_set_docstring_for_import_func():
    """Test :func:`~utilipy.decorators.docstring.set_docstring_for_import_func`."""

    @docstring.set_docstring_for_import_func(
        "tests/_null_imports.py",
        package="utilipy.decorators",
        section="Routine Listings",
    )
    def null_imports_func():
        return

    # /def

    assert null_imports_func.__doc__ == "Nothing."

    _null_imports


# /def


# -------------------------------------------------------------------


##############################################################################
# END
