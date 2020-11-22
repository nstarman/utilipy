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
# import modules
from . import inspect  # doc_parse_tools,
from . import (
    collections,
    exceptions,
    functools,
    logging,
    metaclasses,
    misc,
    pickle,
    string,
    typing,
)
from .collections import ObjDict, WithDocstring, WithMeta, WithReference
from .logging import LogFile, LogPrint
from .misc import make_help_function, temporary_namespace

##############################################################################
# CODE
##############################################################################


##############################################################################
# END
