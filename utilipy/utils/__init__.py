# -*- coding: utf-8 -*-

"""Utilities."""

__author__ = "Nathaniel Starkman"


__all__ = [
    "LogPrint",
    "LogFile",
    "ObjDict",
    "collections",
    "doc_parse_tools",
    "logging",
    "exceptions",
    "functools",
    "inspect",
    "metaclasses",
    "pickle",
    "string",
    "temporary_namespace",
    "typing",
]


##############################################################################
# IMPORTS

# BUILT-IN

from contextlib import contextmanager
from typing import List
from types import ModuleType


# PROJECT-SPECIFIC

from .logging import LogPrint, LogFile
from .collections import ObjDict

# import top level packages
from . import (
    collections,
    doc_parse_tools,
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
# __ALL__

__all_top_imports__ = (
    "collections",
    "doc_parse_tools",
    "logging",
    "metaclasses",
)

__all__ += list(__all_top_imports__)


##############################################################################
# CODE
##############################################################################


@contextmanager
def temporary_namespace(module: ModuleType, keep: List[str] = []):
    """Temporary Namespace within ``with`` statement

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
