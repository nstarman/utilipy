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

## Project-Specific


##############################################################################
### CODE

def configure_matplotlib(backend='inline', figure_format='retina'):
    """configure matplotlib jupyter magic

    Parameters
    ----------
    backend : str, optional  (defualt 'inline')
        set the matplotlib backend
    """
    if get_ipython() is None:
        raise Warning('not in an IPython environment,'
                      'cannot configure matplotlib')

    # set matplotlib backend
    get_ipython().magic(f"matplotlib {backend}")

    # set the resolution
    get_ipython().magic("config InlineBackend.figure_format='{figure_format}'")

    return
# /def

##############################################################################
### END
