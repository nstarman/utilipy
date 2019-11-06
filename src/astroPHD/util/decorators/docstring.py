# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : docstring
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Docstring decorators."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General
import inspect
import functools

# Project-Specific
from .decoratorbaseclass import DecoratorBaseClass


##############################################################################
# CODE
##############################################################################

# def _get_returns_section(module_doc: str):

#     ind = module_doc.find('Returns')
#     end_ind = ind + module_doc[ind:].find('---')  # finding next section

#     doc = module_doc[ind:end_ind]  # get section (+ next header)
#     doc = doc.split('\n')[:-2]  # strip next header
#     doc = '\n'.join(doc)  # rejoin with indent

#     return doc
# # /def


def _set_docstring_import_file_helper(name: str, module_doc: str):
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
    ind = module_doc.find('Returns') + 2 * 7 + 2  # skip 'Returns' & line
    end_ind = ind + module_doc[ind:].find('---')  # finding next section

    doc = module_doc[ind:end_ind]  # get section (+ next header)
    doc = doc.split('\n')[:-2]  # strip next header
    doc[0] = '    ' + doc[0]  # indent 1st line
    doc = '\n    '.join(doc)  # rejoin with indent

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        # /def
        wrapper.__doc__ += f'\n\n{name}_imports:\n{doc}'
        return wrapper
    # /def
    return decorator
# /def


def _import_file_docstring_helper(docstring):
    """Help from import file helper function."""
    doc = docstring.split('\n')  # split on lines
    doc = '\n'.join(doc[1:])  # join all after 1st line
    doc = inspect.cleandoc(doc)  # clean up
    print(doc)
# /def


##############################################################################

class replace_docstring(DecoratorBaseClass):
    """Replace a function docstrin."""

    def _doc_func(self, docstring):
        return self.docstring

    def __call__(self, wrapped_function):
        """Construct a function wrapper."""
        @functools.wraps(wrapped_function)
        def wrapper(*func_args, **func_kwargs):
            return wrapped_function(*func_args, **func_kwargs)
        # /def

        return super().__call__(wrapper)
    # /def


set_docstring = replace_docstring

##############################################################################
# END
