# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Docstring Parsing Tools
# PROJECT : Adapted for utilipy
#
# ----------------------------------------------------------------------------

"""Docstring Parsing Tools.

Docstring inheritance-style implementations.

To implement your own inheritance file, simply write a function that fits the template

.. code-block:: python

    def your_style(prnt_doc, child_doc):
        ''' Merges parent and child docstrings

            Parameters
            ----------
            prnt_cls_doc: Optional[str]
            child_doc: Optional[str]

            Returns
            ------
            Optional[str]
                The merged docstring that will be utilized.'''
        return final_docstring

and log this using `custom_inherit.add_style(your_style)`.
To permanently save your function

1. define your function within custom_inherit/_style_store.py
2. log it in custom_inherit.style_store.__all__.

Your style will then be available as 'your_style'
(i.e. whatever you named the function).

Routine Listings
----------------
merge_numpy_docs
merge_rest_docs
merge_numpy_napoleon_docs
merge_google_napoleon_docs

"""

__author__ = "Ryan Soklaski"
__license__ = "MIT"
__version__ = "2.2.2"
__email__ = "https://github.com/rsokl/custom_inherit"

__all__ = [
    "merge_numpy_docs",
    "merge_rest_docs",
    "merge_numpy_napoleon_docs",
    "merge_google_napoleon_docs",
]


##############################################################################
# IMPORTS

# PROJECT-SPECIFIC

from .napoleon_parse_tools import (
    merge_google_napoleon_docs,
    merge_numpy_napoleon_docs,
)
from .numpy_parse_tools import merge_numpy_docs
from .rest_parse_tools import merge_rest_docs

from . import _style_store


###############################################################################
# CODE
###############################################################################


def _check_style_function(style_func):
    out = style_func("", "")
    if not isinstance(out, str) and out is not None:
        raise TypeError
    return None


# /def


class _DocMergeStore:
    """A dictionary-like object that stores the docstring styles available

    Only callable objects with the signature::

        f(Optional[str], Optional[str]) -> Optional[str]

    can be stored. If f is a valid callable, then _DocMergeStore()[f] -> f.

    """

    def __init__(self, *args, **kwargs):
        self._store = dict()
        self.update(*args, **kwargs)

    # /def

    def __repr__(self):
        return repr(self._store)

    # /def

    def __str__(self):
        out_str = "The available stored styles are: "
        styles = "\n".join("\t- " + style for style in sorted(self.keys()))
        return "\n".join((out_str, styles))

    # /def

    def __setitem__(self, style_name, style_func):
        """Make available a new function for merging a 'parent' and 'child' docstring.

        Parameters
        ----------
        style_name : Any
            The identifier of the style being logged
        style_func: Callable[[Optional[str], Optional[str]], Optional[str]]
            The style function that merges two docstrings into a single docstring."""
        try:
            _check_style_function(style_func)
        except TypeError:
            raise TypeError(
                "The style store only stores callables of the form: "
                "\n\tstyle_func(Optional[str], Optional[str]) -> Optional[str]"
            )
        self._store[style_name] = style_func

    # /def

    def __getitem__(self, item):
        """Given a valid style-ID, retrieve a stored style.

        If a valid function (callable) is supplied, return it in place.

        Parameters
        ----------
        item : Union[Any, Callable[Optional[str], Optional[str]], Optional[str]]
            A valid style-ID or style-function.

        """
        try:
            return self._store[item]
        except KeyError:
            try:
                _check_style_function(item)
                return item
            except (TypeError, ValueError):
                raise TypeError(
                    "Either a valid style name or style-function must be specified"
                )

    # /def

    def keys(self):
        """ D.keys() -> a set-like object providing a view on D's keys"""
        return self._store.keys()

    # /def

    def pop(self, *args):
        """D.pop(k[,d]) -> v, remove specified key and return the corresponding value.

        If key is not found, d is returned if given,
        otherwise KeyError is raised.

        """
        if len(args) < 3:
            return self._store.pop(*args)
        else:
            raise TypeError(
                "pop expected at most 2 arguments, got {}".format(len(args))
            )

    # /def

    def update(self, *args, **kwargs):
        """D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.

        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]

        """
        if len(args) > 1:
            raise TypeError(
                "update expected at most 1 arguments, got %d" % len(args)
            )

        for key, value in dict(*args, **kwargs).items():
            self[key] = value

    # /def

    def values(self):
        """D.values() -> an object providing a view on D's values."""
        return self._store.values()

    # /def

    def items(self):
        """D.items() -> a set-like object providing a view on D's items"""
        return self._store.items()

    # /def


# /def

##############################################################################


store = _DocMergeStore(
    [(key, getattr(_style_store, key)) for key in _style_store.__all__]
)

##############################################################################


def add_style(style_name, style_func):
    """Make available a new function for merging a 'parent' and 'child' docstring.

    Parameters
    ----------
    style_name : Any
        The identifier of the style being logged
    style_func: Callable[[Optional[str], Optional[str]], Optional[str]]
        The style function that merges two docstrings into a single docstring.

    """
    store[style_name] = style_func


# /def


def remove_style(style):
    """ Remove the specified style from the style store.

    Parameters
    ----------
    style: Any
        The inheritance-scheme style ID to be removed.

    """
    if style in store:
        store.pop(style)


# /def


##############################################################################
# END
