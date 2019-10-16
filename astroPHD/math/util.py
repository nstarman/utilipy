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
"""

__author__ = "Nathaniel Starkman"
# __copyright__ = "Copyright 2018, "
# __credits__ = [""]
# __license__ = "GPL3"
# __version__ = "0.0.0"
# __maintainer__ = "Nathaniel Starkman"
# __email__ = "n.starkman@mail.utoronto.ca"
# __status__ = "Production"


##############################################################################
### IMPORTS

## General
import numpy as np

## Project-Specific


##############################################################################
### CODE

def quadrature(*args, axis=0):
    r"""return arguments summed in quadrature
    """
    if len(args) == 0:
        raise ValueError
    if len(args) == 1:
        args = args[0]
    return np.sqrt(np.sum(np.square(args), axis=axis))


# --------------------------------------------------------------------------

##############################################################################
### END
