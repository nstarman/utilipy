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

## General
from collections import OrderedDict

## Custom
from .logging import LogFile, LoggerFile

## Project-Specific
from .pickle import dump as _dump, load as _load


##############################################################################
### CODE

class ObjDict(OrderedDict):
    """ObjDict
    a basic dictionary-like object intended to store information.
    instantiated with a name (str)
    supports __getattr__ as a redirect to __getitem__.

    """

    def __init__(self, name='', **kw):
        """__init__
        initialize with a name for the container and kwargs for the dict
        # the name is stored in the dictionary as well
        """
        super().__init__()

        object.__setattr__(self, 'name', name)

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

    def __repr__(self):
        if self.name == '':
            return super().__repr__()
        else:
            return self.name + super().__repr__().replace('ObjDict', '')

    def values(self, *names):
        if not names:
            return super().values()
        else:
            return [self[k] for k in names]

    def items(self, *names):
        if not names:
            return super().items()
        else:
            return {k: self[k] for k in names}.items()

    def subset(self, *names):
        if not names:
            return self
        else:
            return {k: self[k] for k in names}

    def keyslist(self):
        return list(self.keys())

    # +-------- Serialize --------+
    def __reduce__(self):
        return (self.__class__,
                (self.name, ),
                OrderedDict(self.items()))

    def __setstate__(self, state):
        for key, value in state.items():
            self[key] = value
    # /def

    def dump(self, fname, protocol=None, *, fopt='b', fix_imports=True):
        _dump(self, fname, protocol=protocol, fopt=fopt,
              fix_imports=fix_imports)
    # /def

    def save(self, fname, protocol=None, *, fopt='b', fix_imports=True):
        self.dump(fname, protocol=protocol, fopt=fopt, fix_imports=fix_imports)
    # /def

    @staticmethod
    def load(fname, *, fopt='b', fix_imports=True, encoding='ASCII',
             errors='strict'):
        self = _load(fname, fopt=fopt, fix_imports=fix_imports,
                     encoding=encoding, errors=errors)
        return self
    # /def
# /class

# --------------------------------------------------------------------------
