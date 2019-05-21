#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ipython initialization file
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""initialization file for jupyter notebook functions
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### Imports

## General
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display
from IPython.display import Latex, Markdown  # display is a better print
from IPython.core.debugger import set_trace

## Custom
from .printing import printmd, printltx

## Project-Specific


##############################################################################
### Running

InteractiveShell.ast_node_interactivity = "all"

# configure matplotlib
get_ipython().magic('matplotlib inline')
get_ipython().magic("config InlineBackend.figure_format='retina'")


##############################################################################
### Code
