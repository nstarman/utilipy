# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : docstring
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Docstring decorators.

Routine Listings
----------------
`format_doc`
    Astropy's Format Docstring Function

"""

__author__ = "Nathaniel Starkman"


# __all__ = [
#     "format_doc",
# ]


##############################################################################
# IMPORTS

import inspect
import functools

from typing import Any, Callable, Optional


##############################################################################
# CODE
##############################################################################

##############################################################################
# Format Doc

# TODO figure out automodapi's :allowed-package-names: so don't
# need this jerry-rigged method

from astropy.utils.decorators import format_doc as _format_doc


def format_doc(
    docstring: Optional[str], *args: Any, **kwargs: Any
) -> Callable:
    """Astropy's Format Docstring Function."""
    return _format_doc(docstring, *args, **kwargs)


format_doc.__doc__ = _format_doc.__doc__


##############################################################################


def _set_docstring_import_file_helper(
    name: Optional[str], module_doc: str
) -> Callable:
    """Set docstring from module Returns section.

    takes a helper function for a module and adds the content of the modules'
    `Returns` section.

    Parameters
    ----------
    name: str
        name of importer
    module_doc: str
        docstring of import module

    """
    look_for = "Routine Listings"
    ind = (
        module_doc.find(look_for) + 2 * len(look_for) + 2
    )  # skip 'Routine Listings' & line
    end_ind = ind + module_doc[ind:].find("---")  # finding next section

    doc = module_doc[ind:end_ind]  # get section (+ next header)
    doc = "\n".join(doc.split("\n")[:-2])  # strip next header

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # /def
        wrapper.__doc__ += f"\n\nReturns\n-------\n{doc}"
        return wrapper

    # /def
    return decorator


# /def


def _import_file_docstring_helper(docstring: str) -> str:
    """Help from import file helper function."""
    doc = docstring.split("\n")  # split on lines
    doc = "\n".join(doc[1:])  # join all after 1st line
    doc = inspect.cleandoc(doc)  # clean up
    return doc


# /def


##############################################################################
# END
