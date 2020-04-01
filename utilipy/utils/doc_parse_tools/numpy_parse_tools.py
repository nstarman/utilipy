# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : numpy Parse tools
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring
"""Numpy parse tools.

routines to parse docstrings according to the Napoleon format specifications.
code sourced from [1]_, but modified to merge, not replace, docstring sections.


Routine Listings
----------------
merge_numpy_docs
    Merge two numpy-style docstrings into a single docstring

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

__all__ = ["merge_numpy_docs"]


###############################################################################
# IMPORTS

# GENERAL
from collections import OrderedDict
from inspect import cleandoc

import typing
from typing import Union
from typing_extensions import Literal


###############################################################################
# CODE
###############################################################################


def parse_numpy_doc(doc):
    """Extract the text from the sections of a numpy-formatted docstring.

    Parameters
    ----------
    doc: Union[str, None]

    Returns
    -------
    OrderedDict[str, Union[None,str]]
        The extracted numpy-styled docstring sections.

    """
    doc_sections = OrderedDict(
        [
            ("Short Summary", None),
            ("Deprecation Warning", None),
            ("Attributes", None),
            ("Extended Summary", None),
            ("Parameters", None),
            ("Returns", None),
            ("Yields", None),
            ("Other Parameters", None),
            ("Raises", None),
            ("See Also", None),
            ("Notes", None),
            ("References", None),
            ("Examples", None),
        ]
    )

    if not doc:
        return doc_sections

    doc = cleandoc(doc)
    lines = iter(doc.splitlines())

    key = "Short Summary"
    body = []
    while True:
        try:
            line = next(lines).rstrip()
            if line in doc_sections:
                doc_sections[key] = "\n".join(body).rstrip() if body else None
                body = []
                key = line
                next(lines)  # skip section delimiter
            else:
                body.append(line)
        except StopIteration:
            doc_sections[key] = "\n".join(body)
            break

    return doc_sections


# /def


def merge_section(
    key: str,
    prnt_sec: Union[str, None],
    child_sec: Union[str, None],
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
) -> Union[str, None]:
    """Synthesize a output numpy docstring section.

    Parameters
    ----------
    key: str
        The numpy-section being merged.
    prnt_sec: Optional[str]
        The docstring section from the parent's attribute.
    child_sec: Optional[str]
        The docstring section from the child's attribute.
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

    if key == "Short Summary":
        header = ""
    else:
        header = "\n".join((key, "".join("-" for i in range(len(key))), ""))

    if method == "replace":
        body = prnt_sec if child_sec is None else child_sec
    elif method == "merge":
        # TODO more intelligent merge strategy,
        # respecting arg vs kwarg order, overriding repeated args, etc.
        if prnt_sec is None:
            body = child_sec or ""
        elif child_sec is None:
            body = prnt_sec or ""
        else:
            body = prnt_sec + "\n" + child_sec

    return header + body


# /def


def merge_all_sections(
    prnt_sctns: typing.MutableMapping[str, Union[None, str]],
    child_sctns: typing.MutableMapping[str, Union[None, str]],
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
) -> Union[str, None]:
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
            key, prnt_sctns[key], child_sctns[key], method=method
        )
        if sect is not None:
            doc.append(sect)

    return "\n\n".join(doc) if doc else None


# /def


def merge_numpy_docs(
    prnt_doc: Union[str, None] = None,
    child_doc: Union[str, None] = None,
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
) -> Union[str, None]:
    """Merge two numpy-style docstrings into a single docstring.

    Given the numpy-style docstrings from a parent and child's attributes,
    merge the docstring sections such that the child's section is used,
    wherever present, otherwise the parent's section is used.

    Any whitespace that can be uniformly removed from a docstring's second line
    and onwards is removed. Sections will be separated by a single blank line.

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
    return merge_all_sections(
        parse_numpy_doc(prnt_doc), parse_numpy_doc(child_doc), method=method
    )


# /def


###############################################################################
# END
