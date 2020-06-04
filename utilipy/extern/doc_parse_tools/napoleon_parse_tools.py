# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Napoleon Parse tools
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring
"""Napoleon parse tools.

routines to parse docstrings according to the Napoleon format specifications.
code sourced from [1]_, but modified to merge, not replace, docstring sections.


Routine Listings
----------------
merge_google_napoleon_docs
    Merge two google-style docstrings into a single docstring,
    according to napoleon docstring sections.

merge_numpy_napoleon_docs
    Merge two numpy-style docstrings into a single docstring,
    according to napoleon docstring sections.

References
----------
The code source [1]_.

.. [1] https://github.com/rsokl/custom_inherit

"""

__author__ = "Ryan Soklaski"
__license__ = "MIT"
__version__ = "2.2.2"
__email__ = "https://github.com/rsokl/custom_inherit"

__all__ = ["merge_google_napoleon_docs", "merge_numpy_napoleon_docs"]


###############################################################################
# IMPORTS

# GENERAL
from collections import OrderedDict
from inspect import cleandoc

import typing
from typing import Union, Optional
from typing_extensions import Literal


###############################################################################
# CODE
###############################################################################


def parse_napoleon_doc(doc: Union[str, None], style: str):
    """Extract the text from the sections of a numpy-formatted docstring.

    Parameters
    ----------
    doc: str or None
        The docstring to parse.

    style: str
        'google' or 'numpy'

    Returns
    -------
    OrderedDict[str, Union[None,str]]
        The extracted numpy-styled docstring sections.

    """
    napoleon_sections = [
        "Short Summary",
        "Attributes",
        "Methods",
        "Warning",
        "Note",
        "Parameters",
        "Other Parameters",
        "Keyword Arguments",
        "Returns",
        "Yields",
        "Raises",
        "Warns",
        "See Also",
        "References",
        "Todo",
        "Example",
        "Examples",
    ]

    aliases = {
        "Args": "Parameters",
        "Arguments": "Parameters",
        "Keyword Args": "Keyword Arguments",
        "Return": "Returns",
        "Warnings": "Warning",
        "Yield": "Yields",
    }

    doc_sections = OrderedDict([(key, None) for key in napoleon_sections])

    if not doc:
        return doc_sections

    assert style in ("google", "numpy")

    doc = cleandoc(doc)
    lines = iter(doc.splitlines())

    key = "Short Summary"
    body = []
    while True:
        try:
            line = next(lines).rstrip()
            header = (
                line
                if style == "numpy"
                else (line[:-1] if line.endswith(":") else line)
            )
            if header and (header in doc_sections or header in aliases):
                doc_sections[aliases.get(key, key)] = (
                    "\n".join(body).rstrip() if body else None
                )
                body = []
                key = header
                if style == "numpy":
                    next(lines)  # skip section delimiter
            else:
                body.append(line)
        except StopIteration:
            doc_sections[aliases.get(key, key)] = "\n".join(body)
            break
    return doc_sections


# /def


def merge_section(
    key: str,
    prnt_sec: Union[str, None],
    child_sec: Union[str, None],
    style: str,
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
):
    """Synthesize a output napoleon docstring section.

    Parameters
    ----------
    key: str
        The napoleon-section being merged.
    prnt_sec: Union[str, None]
        The docstring section from the parent's attribute.
    child_sec: Union[str, None]
        The docstring section from the child's attribute.
    style: str
        docstring style format
    method: {merge, replace}, optional
        'merge' merges the sections.
        'replace' (default) parent with child sections, if exists.

    Returns
    -------
    Optional[str]
        The output docstring section.

    """
    if prnt_sec is None and child_sec is None:
        return None

    assert style in ("google", "numpy")

    if key == "Short Summary":
        header = ""
    else:
        if style == "numpy":
            header = "\n".join(
                (key, "".join("-" for i in range(len(key))), "")
            )
        else:
            header = "\n".join((key + ":", ""))

    if method == "replace":
        body = prnt_sec if child_sec is None else child_sec
    elif method == "merge":
        # TODO more intelligent merge strategy,
        # respecting arg vs kwarg order, overriding repeated args, etc.
        body = prnt_sec if child_sec is None else prnt_sec + "\n" + child_sec

    return header + body


# /def


def merge_all_sections(
    prnt_sctns: typing.MutableMapping[str, Union[None, str]],
    child_sctns: typing.MutableMapping[str, Union[None, str]],
    style: str,
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
):
    """Merge the doc-sections of the parent's and child's attribute.

    Parameters
    ----------
    prnt_sctns: OrderedDict[str, Union[None,str]]
    child_sctns: OrderedDict[str, Union[None,str]]
    method: {merge, replace}, optional
        'merge' merges the sections.
        'replace' (default) parent with child sections, if exists.

    Returns
    -------
    str
        Output docstring of the merged docstrings.

    """
    doc = []

    prnt_only_raises = prnt_sctns["Raises"] and not (
        prnt_sctns["Returns"] or prnt_sctns["Yields"]
    )
    if prnt_only_raises and (child_sctns["Returns"] or child_sctns["Yields"]):
        prnt_sctns["Raises"] = None

    for key in prnt_sctns:
        sect = merge_section(
            key, prnt_sctns[key], child_sctns[key], style, method=method
        )
        if sect is not None:
            doc.append(sect)
    return "\n\n".join(doc) if doc else None


# /def


def merge_numpy_napoleon_docs(
    prnt_doc: Optional[str] = None,
    child_doc: Optional[str] = None,
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
):
    """Merge two numpy-style docstrings into one numpy-napolean docstring.

    Given the numpy-style docstrings from a parent and child's attributes,
    merge the docstring sections such that the child's section is used,
    wherever present, otherwise the parent's section is used.

    Any whitespace that can be uniformly removed from a docstring's second line
    and onwards is removed. Sections will be separated by a single blank line.

    Aliased docstring sections are normalized.
    E.g Args, Arguments -> Parameters

    Parameters
    ----------
    prnt_doc: Optional[str]
        The docstring from the parent.
    child_doc: Optional[str]
        The docstring from the child.
    method: {merge, replace}, optional
        'merge' merges the sections.
        'replace' (default) parent with child sections, if exists.

    Returns
    -------
    Union[str, None]
        The merged docstring.

    """
    style = "numpy"
    return merge_all_sections(
        parse_napoleon_doc(prnt_doc, style),
        parse_napoleon_doc(child_doc, style),
        style,
        method=method,
    )


# /def


def merge_google_napoleon_docs(
    prnt_doc: Optional[str] = None,
    child_doc: Optional[str] = None,
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
):
    """Merge two google-style docstrings into one google-napoleon docstring.

    Given the google-style docstrings from a parent and child's attributes,
    merge the docstring sections such that the child's section is used,
    wherever present, otherwise the parent's section is used.

    Any whitespace that can be uniformly removed from a docstring's second line
    and onwards is removed. Sections will be separated by a single blank line.

    Aliased docstring sections are normalized.
    E.g Args, Arguments -> Parameters

    Parameters
    ----------
    prnt_doc: Optional[str]
        The docstring from the parent.
    child_doc: Optional[str]
        The docstring from the child.
    method: {merge, replace}, optional
        'merge' merges the sections.
        'replace' (default) parent with child sections, if exists.

    Returns
    -------
    Union[str, None]
        The merged docstring.

    """
    style = "google"
    return merge_all_sections(
        parse_napoleon_doc(prnt_doc, style),
        parse_napoleon_doc(child_doc, style),
        style,
        method=method,
    )


# /def

###############################################################################
# END
