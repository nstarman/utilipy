# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : IPython printing
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""functions for enhanced printing in an IPython environment.

Routine Listings
----------------
printMD
    Print in Markdown.
printLTX, printLaTeX
    Print in LaTeX.

References
----------
Ipython [1]_

.. [1] Fernando Pérez, Brian E. Granger, IPython: A System for Interactive
    Scientific Computing, Computing in Science and Engineering, vol. 9,
    no. 3, pp. 21-29, May/June 2007, doi:10.1109/MCSE.2007.53.
    URL: https://ipython.org

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "printMD",
    "printLTX",
]


##############################################################################
# IMPORTS

from typing import Union, Optional
from IPython.display import display  # display is a better print
from IPython.display import Latex, Markdown  # , HTML


##############################################################################
# CODE
##############################################################################


def printMD(
    s: str,
    color: Optional[str] = None,
    size: Optional[float] = None,
    bold: bool = False,
    italic: bool = False,
    fontweight: Optional[float] = None,
    fontstyle: Optional[str] = None,
    highlight: Optional[str] = None,
):
    """Print in Markdown.

    uses <span>

    Parameters
    ----------
    s : str
        the string to print
    color :  str or None, optional  (default None)
        sets the 'style:color'
        for color names see https://www.w3schools.com/tags/ref_colornames.asp
        or can supply hex value
    size : int, optional  (default None)
        sets the 'style:font-size' in px
    bold : bool, optional
        (default False)
        shortcut to fontweight='bold'
        *fontweight* takes precedence
    italic : bool, optional
        (default False)
        shortcut to fontstyle='italic'
        *fontstyle* takes precedence
    fontweight : str or int, optional
        (default None)
        sets the 'style:font-weight'
        str options: 'normal', 'bold', 'lighter', 'bolder'
        int options: 0-1000
    fontstyle : str or None, optional
        (default None)
        sets the 'style:font-style'
        see https://www.w3schools.com/cssref/pr_font_font-style.asp
        str options: normal, italic, oblique, initial, inherit
    highlight : str or None, optional
        (default None)

    """
    # doing style
    styleattrs = []
    if color is not None:
        styleattrs.append(f"color:{color}")
    if size is not None:
        styleattrs.append(f"font-size:{size}px")
    # if textalign is not None:  # FIXME doesn't work in jupyter-lab
    #    styleattrs.append(f'text-align:{textalign}')

    if fontweight is not None:
        styleattrs.append(f"font-weight:{fontweight}")
    elif bold:
        styleattrs.append("font-weight:bold")

    if fontstyle is not None:
        styleattrs.append(f"font-style:{fontstyle}")
    elif italic:
        styleattrs.append("font-style:italic")

    elif highlight is not None:
        styleattrs.append("background-color:{highlight}")

    # TODO: add more options

    style = "style='{}'".format(";".join(styleattrs))

    string = f"<span {style}>{s}</span>"
    display(Markdown(string))


# /def


# printHTML = printmd


# ----------------------------------------------------------------------------


def printLTX(
    s: str,
    math: Union[str, bool] = False,
    equation: Union[str, bool] = False,
    matrix: Union[str, bool] = False,
    label: str = "",
):
    r"""Print in LaTeX.

    Parameters
    ----------
    s : raw! str
        the s to print
    math : bool, str  (default False)
        whether the whole string should be wrapped in $$
        if str: wrap in that string
    equation: bool, None  (default False)
        whether the whole string should be wrapped in $\equation$
        if None: then '\equation*'
    matrix: bool, str  (default False)
        whether the whole string should be wrapped in $\matrix$
        if str, use that matrix type, like 'bmatrix'
        shortcuts) 'b' -> 'bmatrix'
    label: the label of the equation, etc.
        only used in equation or matrix

    """
    if label == "":
        pass
    else:
        label = r"\label{" + label + "}"

    if isinstance(math, str):
        s = math + s + math
    elif math:  # (True)
        s = "$" + s + "$"

    if equation:
        s = r"\begin{equation}" + label + s + r"\end{equation}"
    elif equation is None:
        s = r"\begin{equation*}" + label + s + r"\end{equation*}"

    if isinstance(matrix, str):
        if matrix == "b":
            matrix = "bmatrix"
        s = r"\begin{" + matrix + "}" + label + s + r"\end{" + matrix + "}"
    elif matrix:
        s = r"\begin{matrix}" + label + s + r"\end{matrix}"

    display(Latex(s))

    return


# /def


##############################################################################
# END
