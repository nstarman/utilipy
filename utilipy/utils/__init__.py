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
    "misc",
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

# PROJECT-SPECIFIC

from .logging import LogPrint, LogFile
from .collections import ObjDict, WithDocstring, WithMeta, WithReference
from .misc import temporary_namespace, make_help_function

# import modules
from . import (
    collections,
    # doc_parse_tools,
    logging,
    exceptions,
    functools,
    inspect,
    metaclasses,
    misc,
    pickle,
    string,
    typing,
)


##############################################################################
# CODE
##############################################################################


##############################################################################
# END
