# -*- coding: utf-8 -*-
# see LICENSE.rst

"""The `utilipy` Package.

Welcome to utilipy, a collection of useful python codes. This is a centralized
repository for non project-specific code. There are modules for making
advanced decorators, interfacing with IPython environments, miscellaneous
astronomical functions, data utilities, making fitting libraries
inter-operable, improving astropy units and quantity-enabled functions, and
much more.

Routine Listings
----------------
`help`
    `utilipy` help function. Online search or offline overview.

`online_help`
    Search the online `utilipy` documentation for the given query.

`wraps`
    overrides the default ``functools.wraps``, adding signature and docstring
    features.

`LogFile`
    Class for basic logger that can both print and record to a file.

`ObjDict`
    Expanded dictionary with better slicing and attribute-style access.
    Use sparingly. Intended for rapid prototyping since it is NOT a high
    performance object.

References
----------
Zenodo [1]_, Astropy [2]_

.. [1] nstarman. (2020, March 23). nstarman/astroPHD: astropy_template (Version
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
    "LogFile",
    "ObjDict",
    "wraps",
    "config",
    "help",
    "online_help",
]


##############################################################################
# IMPORTS

# Packages may add whatever they like to this file, but
# should keep this content at the top.
# (sets the __version__)
from ._astropy_init import *  # noqa
from ._astropy_init import __version__  # noqa


# GENERAL

from typing import Optional


# PROJECT-SPECIFIC

# configuration
from . import config

# import commonly used functions
from .utils.logging import LogFile
from .utils.collections import ObjDict
from .utils.functools import wraps

# import packages into top-level namespace
from . import (  # noqa
    astro,
    constants,
    data_utils,
    decorators,
    extern,
    imports,
    ipython,
    math,
    plot,
    scripts,
    units,
    utils,
)
from . import astro  # noqa, separated b/c alias


#############################################################################
# HELP FUNCTIONS


def online_help(query: Optional[str] = None):
    """Search the online `utilipy` documentation for the given query.

    Opens the results in the default web browser.
    Requires an active Internet connection.

    Parameters
    ----------
    query : str
        The search query.

    """
    from urllib.parse import urlencode
    import webbrowser

    version = __version__
    if "dev" in version:
        version = "latest"
    else:
        version = "v" + version

    if query is None:  # query is empty
        _query = ""
    else:
        _query: str = urlencode({"q": query})

    url = "https://utilipy.readthedocs.io/en/{}/search.html?{}".format(
        version, _query
    )

    webbrowser.open(url)

    return


# /def


def help(query=None, online: bool = False):
    """`utilipy` help function.

    Parameters
    ----------
    query : str, optional
        The search query.
    online : bool, optional
        Whether to open the online help or just print some help
        documentation (default)

    See Also
    --------
    online_help

    """
    if type == "online":
        return online_help(query=query)

    print("This function is a work in progress")

    print("".join(["-"] * 79))
    ipython.help()

    return


# /def


#############################################################################
# __ALL__

__all_top_imports__ = (
    "astro",
    "astro",
    "constants",
    "data_utils",
    "decorators",
    "extern",
    "imports",
    "ipython",
    "math",
    "plot",
    "scripts",
    "units",
    "utils",
)

__all__ += list(__all_top_imports__)


#############################################################################
# END
