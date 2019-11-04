#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   :
# AUTHOR  : Nathaniel Starkman
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**

TODO
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
from IPython import get_ipython
import warnings

## Project-Specific


##############################################################################
### CODE

def configure_matplotlib(backend: str='inline', figure_format: str='retina'):
    """Configure matplotlib jupyter magic.

    Parameters
    ----------
    backend : str, optional  (defualt 'inline')
        set the matplotlib backend

    """
    if get_ipython() is None:
        warnings.warn('not in an IPython environment,'
                      'cannot configure matplotlib')
        return

    from IPython.terminal.pt_inputhooks import UnknownBackend

    try:
        # set matplotlib backend
        get_ipython().magic(f"matplotlib {backend}")

    except UnknownBackend:
        warnings.warn('not a valid backed. Please try again.')

    else:
        # set the resolution
        get_ipython().magic("config InlineBackend.figure_format"
                            f"='{figure_format}'")

    return
# /def

##############################################################################
### END
