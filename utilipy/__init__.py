# -*- coding: utf-8 -*-
# see LICENSE.rst

"""The `utilipy` Package on import.

Welcome to utilipy, a collection of useful python codes. This is a centralized
repository for non project-specific code. There are modules for making
advanced decorators, interfacing with IPython environments, data utilities,
making fitting libraries inter-operable, and much more.


References
----------
Zenodo [1]_, Astropy [2]_

.. [1] nstarman. (2020, March 23). nstarman/utilipy: astropy_template (Version
    astropy_template). Zenodo. http://doi.org/10.5281/zenodo.3724822
.. [2] Astropy Collaboration et al., 2018, AJ, 156, 123.


Examples
--------

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
    "extern",
    "imports",
    "math",
    "plot",
    "scripts",
    "utils",
    # functions
    "data_graph",
    "LogFile",
    "ObjDict",
    "wraps",
    "lookup",
    "online_help",
    "reload_config",
]

__all_top_imports__ = (  # TODO deprecate
    "data_utils",
    "decorators",
    "extern",
    "imports",
    "math",
    "plot",
    "scripts",
    "utils",
)


##############################################################################
# IMPORTS

# -----------------------------------------------
# keep this content at the top. (sets the __version__)
from ._astropy_init import *  # noqa: F401, F403  # isort:skip
from ._astropy_init import __version__  # noqa  # isort:skip

# -----------------------------------------------

# BUILT-IN
import typing as T

# THIRD PARTY
import astropy.config as config
from astropy.utils.misc import find_api_page

# PROJECT-SPECIFIC
from . import math  # noqa
from . import data_utils, decorators, extern, imports, plot, scripts, utils
from .data_utils import data_graph
from .utils.collections import ObjDict
from .utils.functools import wraps
from .utils.logging import LogFile

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


def online_help(query: T.Union[None, str, T.Any] = None, version=__version__):
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

    Examples
    --------
    To do a specific search of `utilipy`'s docs, use the ``online_help``
    function. If you don't have a specific query, that's fine too,
    `utilipy` will open the general search page.

    As an example, here we query RTD for the documentation on `LogFile`.

        >>> import utilipy
        >>> utilipy.online_help(query="LogFile") # doctest: +SKIP

    The same can be accomplished with the general `help` function.

        >>> import utilipy
        >>> utilipy.help(query="LogFile", online=True) # doctest: +SKIP

    See Also
    --------
    :func:`~utilipy.help`

    """
    # first get version to search
    if "dev" in version:
        version = "latest"
    else:
        version = version if version.startswith("v") else "v" + version

    # look up objects
    if not isinstance(query, str) and query is not None:
        if version == "latest":
            version = None
        return find_api_page(query, version=version, openinbrowser=True)

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


# -------------------------------------------------------------------


@decorators.code_dev.indev
def lookup(query: T.Optional[str] = None, online: bool = False):
    """*Utilipy* help function. Online search or offline overview.

    Parameters
    ----------
    query : str, optional
        The search query.
    online : bool, optional
        Whether to open the online help or just print some help
        documentation (default)

    Examples
    --------
    A search of `utilipy`'s online docs.

        >>> import utilipy
        >>> utilipy.help(query="LogFile", online=True) # doctest: +SKIP

    See Also
    --------
    :func:`~utilipy.online_help`

    """
    if online:
        return online_help(query=query, version="latest")
    # else:

    print("This function is a work in progress")

    print("".join(["-"] * 79))
    ipython.help()

    return


# /def


#############################################################################
# END
