# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ReST Parse tools
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring
"""ReST parse tools.

routines to parse docstrings according to the Napoleon format specifications.
code sourced from [1]_, but modified to merge, not replace, docstring sections.


Routine Listings
----------------
merge_rest_docs
    Merge two ReST-style docstrings into a single docstring

References
----------
The code source [1]_.

.. [1] https://github.com/rsokl/custom_inherit

"""

__all__ = ["merge_rest_docs"]


###############################################################################
# IMPORTS

# GENERAL

from collections import OrderedDict
from inspect import cleandoc
from string import punctuation

from typing import Optional, Union, Dict
from typing_extensions import Literal


###############################################################################
# CODE
###############################################################################


def is_delimiter(line: str) -> bool:
    """True if a line consists only of a single punctuation character."""
    return (
        bool(line)
        and (line[0] in punctuation)
        and (line[0] * len(line) == line)
    )


# /def


class Section(object):
    def __init__(self, header: str = None, body: str = None):
        self.header: str = header
        self.body: str = body


# /class


def parse_rest_doc(doc: Union[str, None]) -> Dict[str, Section]:
    """Extract the headers, delimiters, and text from reST-formatted docstrings.

    Parameters
    ----------
    doc: Union[str, None]

    Returns
    -------
    Dict[str, Section]

    """
    doc_sections = OrderedDict([("", Section(header=""))])
    if not doc:
        return doc_sections

    doc = cleandoc(doc)
    lines = iter(doc.splitlines())

    header = ""
    body = []
    section = Section(header=header)
    line = ""

    while True:
        try:
            prev_line = line
            line = next(lines)
            # section header encountered
            if is_delimiter(line) and 0 < len(prev_line) <= len(line):
                # prev-prev-line is overline
                if (
                    len(body) >= 2
                    and len(body[-2]) == len(line)
                    and body[-2][0] == line[0]
                    and is_delimiter(body[-2])
                ):
                    lim = -2
                else:
                    lim = -1

                section.body = "\n".join(body[:lim]).rstrip()
                doc_sections.update([(header.strip(), section)])
                section = Section(header="\n".join(body[lim:] + [line]))
                header = prev_line
                body = []
                line = ""
            else:
                body.append(line)

        except StopIteration:
            section.body = "\n".join(body).rstrip()
            doc_sections.update([(header.strip(), section)])
            break

    return doc_sections


# /def


def merge_rest_docs(
    prnt_doc: Optional[str] = None,
    child_doc: Optional[str] = None,
    method: Union[Literal["merge"], Literal["replace"]] = "replace",
) -> str:
    """See custom_inherit.style_store.reST for details."""
    prnt_sections = parse_rest_doc(prnt_doc)
    child_sections = parse_rest_doc(child_doc)

    header = prnt_sections[""]
    prnt_sections.update(child_sections)
    if not child_sections[""].body:
        prnt_sections[""] = header
        if not header.body:
            prnt_sections.popitem(last=False)

    return "\n\n".join(
        ("\n".join((x.header, x.body)) for x in prnt_sections.values())
    ).lstrip()


# /def


###############################################################################
# END
