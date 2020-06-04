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


##############################################################################
# END
