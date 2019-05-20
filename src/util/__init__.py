#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : util initialization file
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""initialization file for util
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### Imports

# General
from collections import OrderedDict

# Custom
from .logging import LogFile, LoggerFile

# Project-Specific


##############################################################################

class InfoContainer(OrderedDict):
    """InfoContainer
    a basic dictionary-like object intended to store information.
    instantiated with a name (str)
    supports __getattr__ as a redirect to __getitem__.

    """

    def __init__(self, name='', **kw):
        """__init__
        initialize with a name for the container and kwargs for the dict
        the name is stored in the dictionary as well
        """
        super().__init__()
        self.name = name
        for key, value in kw.items():
            self[key] = value

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, keys):
        if isinstance(keys, str):
            return super().__getitem__(keys)
        else:
            return [OrderedDict.__getitem__(self, key) for key in keys]

    def keyslist(self):
        return list(self.keys())
# /class

# --------------------------------------------------------------------------
