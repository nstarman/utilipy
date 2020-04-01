# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : numpy Parse tools
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring
"""Docstring inheritance-style implementations.

To implement your own inheritance file, simply write a function to this template:

.. code-block:: python
    :linenos:

    def your_style(prnt_doc, child_doc, method='replace'):
        '''Merges parent and child docstrings

        Parameters
        ----------
        prnt_cls_doc: Optional[str]
        child_doc: Optional[str]
        method: Union[Literal["merge"], Literal["replace"]]

        Returns
        ------
        Optional[str]
            The merged docstring that will be utilized.

        '''
        return final_docstring


and log this using `custom_inherit.add_style(your_style)`. To permanently save
your function, define your function within custom_inherit/_style_store.py, and
log it in custom_inherit.style_store.__all__. Your style will then be
available as 'your_style' (i.e. whatever you named the function).

Routine Listings
----------------
parent
numpy
reST
google
numpy_napoleon

References
----------
The code source [1]_.

.. [1] https://github.com/rsokl/custom_inherit

TODO
----
https://stackoverflow.com/a/41083968


"""

__author__ = "Ryan Soklaski"
__license__ = "MIT"
__version__ = "2.2.2"
__email__ = "https://github.com/rsokl/custom_inherit"

# All built-in styles must be logged in the __all__ field.
__all__ = ["parent", "numpy", "reST", "google", "numpy_napoleon"]


###############################################################################
# IMPORTS

# GENERAL
from typing import Union
from typing_extensions import Literal

# PROJECT-SPECIFIC
from .napoleon_parse_tools import (
    merge_google_napoleon_docs,
    merge_numpy_napoleon_docs,
)
from .numpy_parse_tools import merge_numpy_docs
from .rest_parse_tools import merge_rest_docs


###############################################################################
# CODE
###############################################################################


def parent(
    prnt_doc: Union[str, None], child_doc: Union[str, None], method="replace"
):
    """Documentation strings are inherited if not overridden.

    Wherever the docstring for a child-class' attribute (or for the class
    itself) is `None`, inherit the corresponding docstring from the parent.

    Parameters
    ----------
    prnt_sec: Optional[str]
        The docstring section from the parent's attribute.
    child_sec: Optional[str]
        The docstring section from the child's attribute.
    method: {replace}, optional
        'replace' (only option) parent with child sections, if exists.

    *NOTE* As of Python 3.5, this is the default behavior of the built-in
    function inspect.getdoc

    """
    return child_doc if child_doc is not None else prnt_doc


# /def


def numpy(
    prnt_doc: Union[str, None],
    child_doc: Union[str, None],
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
):
    """Merges numpy-styled docstrings from the parent and child.

    Specifically, any docstring section that appears in the parent's docstring
    that is not present in the child's is inherited. Otherwise, the child's
    docstring section is utilized. An exception to this is if the parent
    docstring contains a "Raises" section, but the child's attribute's
    docstring contains a "Returns" or "Yields" section instead. In this
    instance, the "Raises" section will not appear in the inherited docstring.

    Any whitespace that can be uniformly removed from a docstring's second line
    and onwards is removed. Sections in the resulting docstring will be
    separated by a single blank line.

    For details on the numpy docstring style, see:
    https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

    Parameters
    ----------
    prnt_sec: Optional[str]
        The docstring section from the parent's attribute.
    child_sec: Optional[str]
        The docstring section from the child's attribute.
    method: {merge, replace}, optional
        'merge' merges the sections.
        'replace' (default) parent with child sections, if exists.

    Examples
    --------
        - parent's docstring:

            ''' Parent's line

                Parameters
                ----------
                x: int
                    description of x
                y: Union[None, int]
                    description of y

                Raises
                ------
                NotImplemented Error

            '''

        - child's docstring:

            ''' Child's line

                Returns
                -------
                int

                Notes
                -----
                notes blah blah

            '''

        - docstring that is ultimately inherited:

            ''' Child's line

                Parameters
                ----------
                x: int
                    description of x
                y: Union[None, int]
                    description of y

                Returns
                -------
                int

                Notes
                -----
                notes blah blah

            '''

    """
    return merge_numpy_docs(prnt_doc, child_doc, method=method)


# /def


def reST(
    prnt_doc: Union[str, None],
    child_doc: Union[str, None],
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
):
    """Merge two reST-style docstrings into a single docstring.

    Given the reST-style docstrings from a parent and child's attributes, merge the docstring
    sections such that the child's section is used, wherever present, otherwise the parent's
    section is used.

    Sections are delimited by any type of reST section title. For more details, see:
    http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections

    Any whitespace that can be uniformly removed from a docstring's second line and onwards is
    removed. Sections in the resulting docstring will be separated by a single blank line.

    Parameters
    ----------
    prnt_sec: Optional[str]
        The docstring section from the parent's attribute.
    child_sec: Optional[str]
        The docstring section from the child's attribute.
    method: {merge, replace}, optional
        'merge' merges the sections.
        'replace' (default) parent with child sections, if exists.

    Examples
    --------
      parent - ''' Header1
                   -------
                   parent's content for Header 1
                       - indented material
                   Header2
                   ~~~~~~~
                   content for Header2

               '''

      child -  ''' Front-matter
                   ~~~~~~~~~
                   NewHeader
                   ~~~~~~~~~
                   content for NewHeader

                   Header2
                   +++++++
                   child's content for Header2

               '''

      merged - ''' Front-matter

                   Header1
                   -------
                   content for Header 1
                       - indented material

                   Header2
                   +++++++
                   child's content for Header2

                   ~~~~~~~~~
                   NewHeader
                   ~~~~~~~~~
                   content for NewHeader

               '''
    """
    return merge_rest_docs(prnt_doc, child_doc, method=method)


# /def


def numpy_napoleon(
    prnt_doc: Union[str, None],
    child_doc: Union[str, None],
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
):
    """Behaves identically to the 'numpy' style, but abides by the docstring sections
    specified by the "Napoleon" standard.

    For more info regarding the Napoleon standard, see:
    http://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html#docstring-sections

    Parameters
    ----------
    prnt_sec: Optional[str]
        The docstring section from the parent's attribute.
    child_sec: Optional[str]
        The docstring section from the child's attribute.
    method: {merge, replace}, optional
        'merge' merges the sections.
        'replace' (default) parent with child sections, if exists.

    Examples
    --------
        - parent's docstring:

            ''' Parent's line

                Keyword Arguments
                -----------------
                x: int
                    description of x
                y: Union[None, int]
                    description of y

                Raises
                ------
                NotImplemented Error

            '''

        - child's docstring:

            ''' Child's line

                Returns
                -------
                int

                Notes
                -----
                notes blah blah

            '''

        - docstring that is ultimately inherited:

            ''' Child's line

                Keyword Arguments
                -----------------
                x: int
                    description of x
                y: Union[None, int]
                    description of y

                Returns
                -------
                int

                Notes
                -----
                notes blah blah

            '''

    """
    return merge_numpy_napoleon_docs(prnt_doc, child_doc, method=method)


# /def


def google(
    prnt_doc: Union[str, None],
    child_doc: Union[str, None],
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
):
    """Merge google-styled docstrings by the "Napoleon" standard.

    Specifically, any docstring section that appears in the parent's docstring
    that is not present in the child's is inherited. Otherwise, the child's
    docstring section is utilized. An exception to this is if the parent
    docstring contains a "Raises" section, but the child's attribute's
    docstring contains a "Returns" or "Yields" section instead. In this
    instance, the "Raises" section will not appear in the inherited docstring.

    Any whitespace that can be uniformly removed from a docstring's second line
    and onwards is removed. Sections in the resulting docstring will be
    separated by a single blank line.

    For more info regarding the Napoleon standard, see:
    http://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html#docstring-sections

    For details on the google docstring style, see:
    http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html#example-google

    Parameters
    ----------
    prnt_sec: Optional[str]
        The docstring section from the parent's attribute.
    child_sec: Optional[str]
        The docstring section from the child's attribute.
    method: {merge, replace}, optional
        'merge' merges the sections.
        'replace' (default) parent with child sections, if exists.

    Examples
    --------
        - parent's docstring:

            ''' Parent's line

                Args:
                    x: int
                        description of x
                    y: Union[None, int]
                        description of y

                Raises:
                    NotImplemented Error

            '''

        - child's docstring:

            ''' Child's line

                Returns:
                    int

                Notes:
                    notes blah blah

            '''

        - docstring that is ultimately inherited:

            ''' Child's line

                Parameters:
                    x: int
                        description of x
                    y: Union[None, int]
                        description of y

                Returns:
                    int

                Notes:
                    notes blah blah

            '''

    """
    return merge_google_napoleon_docs(prnt_doc, child_doc, method=method)


# /def

##############################################################################
# END
