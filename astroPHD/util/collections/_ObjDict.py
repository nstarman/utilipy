#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ObjDict
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""initialization file for util
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### IMPORTS

## General
from collections import OrderedDict

## Project-Specific
from ..pickle import dump as _dump, load as _load


##############################################################################
### CODE

class ObjDict(OrderedDict):
    """ObjDict
    a basic dictionary-like object intended to store information.
    instantiated with a name (str)
    supports __getattr__ as a redirect to __getitem__.

    Parameters
    ----------
    name: str
        the name of the object
    **kw
        items for ObjDict

    Examples
    --------
    obj = ObjDict('NAME', a=1, b=2)
    print(obj.name, obj.a, obj['b'])
    >> NAME, 1, 2
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
    # /def

    # ----------------------------------
    # item get / set

    def __getitem__(self, keys, _as_generator=False):
        """
        Parameters
        ----------
        keys: str, list of str
            the keys into ObjDict
            if str: just the value from key-value pair
            if list: list of values
        _as_generator: bool  (default False)
            whether to return as a generator
            only if keys is a list

        Returns
        -------
        value(s): anything
            if str: just the value from key-value pair
            if list: list of values
            if _as_generator: generator for list

        Examples
        --------
        obj = ObjDict('NAME', a=1, b=2)
        print(obj['a'])
        >> 1, [NAME, 2]
        print(obj['name', 'b'])
        >> [NAME, 2]
        """
        if isinstance(keys, str):  # single key
            return super().__getitem__(keys)
        else:  # multiple keys
            if _as_generator:  # return generator
                return(OrderedDict.__getitem__(self, k) for k in keys)
            return [OrderedDict.__getitem__(self, k) for k in keys]
    # /def

    # ----------------------------------
    # attribute get / set
    # redirects to item get / set

    def __setattr__(self, key, value):
        self[key] = value
    # /def

    def __getattr__(self, key):
        return self[key]
    # /def

    # ----------------------------------
    # Printing

    def __repr__(self):
        if self.name == '':
            return super().__repr__()
        else:
            return self.name + super().__repr__().replace('ObjDict', '')
    # /def

    # ----------------------------------

    def values(self, *names):
        if not names:
            return super().values()
        else:
            return [self[k] for k in names]
    # /def

    def items(self, *names):
        if not names:
            return super().items()
        else:
            return {k: self[k] for k in names}.items()
    # /def

    def subset(self, *names):
        if not names:
            return self
        else:
            return {k: self[k] for k in names}
    # /def

    def keyslist(self):
        return list(self.keys())
    # /def

    # ----------------------------------
    # Serialize (I/O)

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

    # ----------------------------------

# /class


##############################################################################
### END
