# -*- coding: utf-8 -*-

"""Utilities."""


__all__ = [
    # modules
    "collections",
    "logging",
    "exceptions",
    "functools",
    "inspect",
    "metaclasses",
    "pickle",
    "string",
    "typing",
    # classes and functions
    "LogPrint",
    "LogFile",
    "ObjDict",
    "WithDocstring",
    "WithMeta",
    "WithReference",
    "temporary_namespace",
    "make_help_function",
]

__all_top_imports__ = (  # TODO deprecate
    "collections",
    # "doc_parse_tools",
    "logging",
    "exceptions",
    "functools",
    "inspect",
    "metaclasses",
    "pickle",
    "string",
    "typing",
)


##############################################################################
# IMPORTS

# BUILT-IN

from contextlib import contextmanager
from types import ModuleType
import typing as T


# THIRD PARTY

from astropy.utils.data import find_current_module


# PROJECT-SPECIFIC

from .logging import LogPrint, LogFile
from .collections import ObjDict, WithDocstring, WithMeta, WithReference

# import modules
from . import (
    collections,
    # doc_parse_tools,
    logging,
    exceptions,
    functools,
    inspect,
    metaclasses,
    pickle,
    string,
    typing,
)


##############################################################################
# CODE
##############################################################################


@contextmanager
def temporary_namespace(module: ModuleType, keep: T.List[str] = []):
    """Temporary Namespace within ``with`` statement.

    1. Stores keys in ``__dict__`` (determined by ``__name__``)
    2. Enters ``with`` statement
    3. Deletes all new keys in ``__dict__`` except those specified in `keep`

    Parameters
    ----------
    module : module
        ``sys.modules[__name__]`` of module calling from.

        .. todo::

            not need to pass any module information. infer.

    keep : list, optional
        list of (str) variable names to keep.

    Yields
    ------
    module : module
        the specified module, for accessing namespace

    """
    # sys.modules[__name__]
    original_namespace: list = list(module.__dict__.keys())
    try:
        yield module
    finally:
        keys: tuple = tuple(module.__dict__.keys())
        to_keep: list = original_namespace + keep

        n: str
        for n in keys:
            if n not in to_keep:
                del module.__dict__[n]
        # /for
    # /try


# /def


# -------------------------------------------------------------------


def make_help_function(
    name: str,
    module: T.Union[None, ModuleType, str] = None,
    look_for: T.Optional[str] = None,  # "Routine Listings",
    doctitle: T.Optional[str] = None,
) -> T.Callable:
    """Set docstring from module Returns section.

    Takes a helper function for a module and adds the content of the modules'
    `look_for` section. Currently only works on numpy-style docstring.

    Parameters
    ----------
    name: str
        name of function. Add "_help".
    module:
        Module
    look_for : str, optional
        The section to look for (default None)
        The section name "Routine Listings" is replaced by "Returns"
    doctitle : str, optional

    Returns
    -------
    decorator : Callable
        decorator function to change the wrapped function's docstring.

    Notes
    -----
    .. todo::

        separate the imports help function from the general helps function.
        the general help function should be similar to the find_api_page
        in astropy and the help function in the utilipy init.

    """
    if module is None:
        mod_name = find_current_module(1).__name__
        module_doc = module.__doc__
    elif isinstance(module, ModuleType):
        module_doc = module.__doc__
        mod_name = module.__name__
    elif isinstance(module, str):
        module_doc = module
        mod_name = find_current_module(2).__name__

    if look_for is None:
        doc = module_doc

    elif isinstance(look_for, str):
        ind = module_doc.find(look_for) + 2 * len(look_for) + 2
        end_ind = ind + module_doc[ind:].find("---")  # finding next section

        doc = module_doc[ind:end_ind]  # get section (+ next header)
        doc = "\n".join(doc.split("\n")[:-2])  # strip next header

        if look_for == "Routine Listings":  # skip 'Routine Listings' & line
            Name = name.capitalize()
            doc = f"\n{Name} Returns\n{'-'*(len(name) + 1)}-------\n" + doc

    else:
        raise TypeError

    # TODO with FunctionType in types
    def help_function():
        print(doc)

    help_function.__name__ = f"{name}_help"
    help_function.__module__ = mod_name
    help_function.__doc__ = f"Help for {doctitle or name}."
    # /def

    return help_function


# /def


##############################################################################
# END
