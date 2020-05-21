# -*- coding: utf-8 -*-
# see LICENSE.rst

"""The `utilipy` Package.

Welcome to utilipy, a collection of useful python codes. This is a centralized
repository for non project-specific code. There are modules for making
advanced decorators, interfacing with IPython environments, data utilities,
making fitting libraries inter-operable, and much more.

Routine Listings
----------------
`help`
    *utilipy* help function. Online search or offline overview.

`online_help`
    Search the online *utilipy* documentation for the given query.

`wraps`
    overrides the default :func:`~functools.wraps`, adding signature
    and docstring features.

`LogFile`
    Class for basic logger that can both print and record to a file.

`ObjDict`
    Expanded dictionary with better slicing and attribute-style access.
    Use sparingly. Intended for rapid prototyping since it is NOT a high
    performance object.

References
----------
Zenodo [1]_, Astropy [2]_

.. [1] nstarman. (2020, March 23). nstarman/utilipy: astropy_template (Version
    astropy_template). Zenodo. http://doi.org/10.5281/zenodo.3724822
.. [2] Astropy Collaboration et al., 2018, AJ, 156, 123.


Examples
--------

help
^^^^

To do a specific search of `utilipy`'s docs, use the ``online_help`` function.
If you don't have a specific query, that's fine too,
`utilipy` will open the general search page.

As an example, here we query RTD for the documentation on `LogFile`.

    >>> import utilipy
    >>> utilipy.online_help(query="LogFile") # doctest: +SKIP

The same can be accomplished with the general `help` function.

    >>> import utilipy
    >>> utilipy.help(query="LogFile", online=True) # doctest: +SKIP

"""

__author__ = "Nathaniel Starkman"

__all__ = [
    # modules
    "data_utils",
    "decorators",
    "imports",
    "ipython",
    "math",
    "plot",
    "scripts",
    "utils",
    # functions
    "data_graph",
    "LogFile",
    "ObjDict",
    "wraps",
    "help",
    "online_help",
    "reload_config",
]


##############################################################################
# IMPORTS

# Packages may add whatever they like to this file, but
# should keep this content at the top.
# (sets the __version__)
from ._astropy_init import *  # noqa
from ._astropy_init import __version__  # noqa


# THIRD PARTY

import astropy.config as config


# PROJECT-SPECIFIC

from .utils import typing as T
from .utils.logging import LogFile
from .utils.collections import ObjDict
from .utils.functools import wraps

from .data_utils import data_graph

# import packages into top-level namespace
from . import (  # noqa
    data_utils,
    decorators,
    imports,
    ipython,
    math,
    plot,
    scripts,
    utils,
)


#############################################################################
# PARAMTERS

__all_top_imports__ = (  # TODO deprecate
    "data_utils",
    "decorators",
    "imports",
    "ipython",
    "math",
    "plot",
    "scripts",
    "utils",
)


#############################################################################
# CONFIG FUNCTIONS


def reload_config():
    """Reload utilipy configuration.

    See Also
    --------
    :mod:`~astropy.config`

    """
    config.reload_config("utilipy")


# /def


#############################################################################
# HELP FUNCTIONS


def online_help(query: T.Union[None, str, T.Any] = None):
    """Search the online documentation for the given query.

    Opens the results in the default web browser.
    Requires an active internet connection.

    Parameters
    ----------
    query : str, object, optional
        The search query for `RTD <https://utislipy.readthedocs.io>`_.
        None (default) or "" is an empty search.
        If an object, uses :func:`~astropy.utils.misc.find_api_page`
        to find the correct API page.

    """
    # first get version to search
    version = __version__
    if "dev" in version:
        version = "latest"
    else:
        version = "v" + version

    if not isinstance(query, str) and query is not None:
        if version == "latest":
            version = None
        find_api_page(query, version=version, openinbrowser=True)
        return
    # else:

    from urllib.parse import urlencode
    import webbrowser

    # process the query
    if query is None:  # empty query, empty search
        query = ""
    else:  # encode the query
        query: str = urlencode({"q": query})

    url = f"https://utilipy.readthedocs.io/en/{version}/search.html?{query}"

    webbrowser.open(url)


# /def


@decorators.code_dev.indev
def help(query: T.Optional[str] = None, online: bool = False):
    """utilipy help function.

    Parameters
    ----------
    query : str, optional
        The search query.
    online : bool, optional
        Whether to open the online help or just print some help
        documentation (default)

    """
    if online:
        return online_help(query=query)
    # else:

    print("This function is a work in progress")

    print("".join(["-"] * 79))
    ipython.help()

    return


# /def


#############################################################################
# END
