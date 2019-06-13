#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : pickle
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""plotfuncs
"""

__author__ = "Nathaniel Starkman"

#############################################################################
### Imports

import pickle


############################################################################
# Code

def dump(obj, fname, protocol=None, *, fopt='b', fix_imports=True):
    r"""
    """
    with open(fname, 'w' + fopt) as file:
        pickle.dump(obj, file, protocol=protocol, fix_imports=fix_imports)
    return
# /def


def load(fname, *, fopt='b', fix_imports=True, encoding='ASCII',
         errors='strict'):
    r"""pickle load
    """
    with open(fname, 'r' + fopt) as file:
        res = pickle.load(file, fix_imports=fix_imports,
                          encoding=encoding, errors=errors)
    return res
# /def
