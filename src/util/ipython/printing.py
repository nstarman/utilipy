#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : iPython printing
# AUTHOR  : Nathaniel Starkman
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""functions for enhanced printing in an iPython environment
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### Imports

# General
from IPython.display import display
from IPython.display import Latex, Markdown  # display is a better print

# Project-Specific


##############################################################################
# Code

def printmd(s, color=None, size=None, bold=False, italic=False,
            fontweight=None, fontstyle=None):
    """print in markdown
    uses <span>

    INPUT
    -----
    s: str
        the string to print
    color:  str  (default None)
        sets the 'style:color'
        for color names see https://www.w3schools.com/tags/ref_colornames.asp
        or can supply hex value
    size: int  (default None)
        sets the 'style:font-size' in px
    bold: bool  (default False)
        shortcut to fontweight='bold'
        *fontweight* takes precedence
    italic: bool  (default False)
        shortcut to fontstyle='italic'
        *fontstyle* takes precedence
    fontweight: str, int  (default None)
        sets the 'style:font-weight'
        str options: 'normal', 'bold', 'lighter', 'bolder'
        int options: 0-1000
    fontstyle: str  (default None)
        sets the 'style:font-style'
        see https://www.w3schools.com/cssref/pr_font_font-style.asp
        str options: normal, italic, oblique, initial, inherit
    """
    # doing style
    styleattrs = []
    if color is not None:
        styleattrs.append(f'color:{color}')
    if size is not None:
        styleattrs.append(f'font-size:{size}px')
    # if textalign is not None:  # FIXME doesn't work in jupyter-lab
    #    styleattrs.append(f'text-align:{textalign}')

    if fontweight is not None:
        styleattrs.append(f'font-weight:{fontweight}')
    elif bold:
        styleattrs.append('font-weight:bold')

    if fontstyle is not None:
        styleattrs.append(f'font-style:{fontstyle}')
    elif italic:
        styleattrs.append('font-style:italic')

    # TODO: add more options

    style = "style='{}'".format(';'.join(styleattrs))

    string = f"<span {style}>{s}</span>"
    display(Markdown(string))
# /def


# ----------------------------------------------------------------------------


def printltx(s):
    """print in latex

    INPUT
    -----
    s: str
        the s to print
    """
    # TODO: add more options
    display(Latex(s))
# /def
