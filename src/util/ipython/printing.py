#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : IPython printing
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""functions for enhanced printing in an iPython environment
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### Imports

## General
from IPython.display import display
from IPython.display import Latex, Markdown  # display is a better print

## Project-Specific


##############################################################################
# Code

def printmd(s, color=None, size=None, bold=False, italic=False,
            fontweight=None, fontstyle=None):
    """print in markdown
    uses <span>

    Parameters
    ----------
    s : str
        the string to print
    color :  str, optional  (default None)
        sets the 'style:color'
        for color names see https://www.w3schools.com/tags/ref_colornames.asp
        or can supply hex value
    size : int, optional  (default None)
        sets the 'style:font-size' in px
    bold : bool, optional  (default False)
        shortcut to fontweight='bold'
        *fontweight* takes precedence
    italic : bool, optional  (default False)
        shortcut to fontstyle='italic'
        *fontstyle* takes precedence
    fontweight : str or int, optional  (default None)
        sets the 'style:font-weight'
        str options: 'normal', 'bold', 'lighter', 'bolder'
        int options: 0-1000
    fontstyle : str, optional (default None)
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


def printltx(s, math=False, equation=False, matrix=False, label=''):
    r"""print in latex

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
        True: 'matrix'
        if str: use that matrix type, like 'bmatrix'
            shortcuts: 'b' -> 'bmatrix'
    label: the label of the equation, etc.
        only used in equation or matrix
    """
    if label == '':
        pass
    else:
        label = r'\label{' + label + '}'

    if isinstance(math, str):
        s = math + s + math
    elif math:  # (True)
        s = '$' + s + '$'

    if equation:
        s = r'\begin{equation}' + label + s + r'\end{equation}'
    elif equation is None:
        s = r'\begin{equation*}' + label + s + r'\end{equation*}'

    if isinstance(matrix, str):
        if matrix == 'b':
            matrix = 'bmatrix'
        s = r'\begin{' + matrix + '}' + label + s + r'\end{' + matrix + '}'
    elif matrix:
        s = r'\begin{matrix}' + label + s + r'\end{matrix}'

    display(Latex(s))
# /def


# ----------------------------------------------------------------------------
