#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : objects
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""initialization file for jupyter notebook functions
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
import numpy as np
from collections import OrderedDict
from collections.abc import MutableSequence

## Custom Packages
from ..multi import parallel_map
from ..pickle import dump as _dump, load as _load

## Project-Specific


#############################################################################
### CODE

class Objects(MutableSequence):
    """Holds many
    Can perform operations on many different objects simultaneously

    # TODO? change to use __new__ so can change docstring
    """

    def __init__(self, *args, **kw):
        """all SkyCoords must have the same attributes
        """
        super().__init__()

        self._args = list(args)
        self._argsclass = args[0].__class__

        for key, value in kw.items():
            setattr(self, key, value)
    # /def

    # +-------- get / set / del / insert - item --------+
    def __getitem__(self, index):
        if np.isscalar(index):  # get key by order number
            return self._args[index]
        elif isinstance(index, ....__class__):
            return self._args
        elif isinstance(index, slice):
            return self._args[index]
        else:
            return [self._args[key] for key in index]

    def __setitem__(self, index, value):
        if np.isscalar(index):  # get key by order number
            self._args[index] = value
        elif isinstance(index, ....__class__):
            self._args = value
        elif isinstance(index, slice):
            raise Exception('not yet implemented')
        else:
            # try broadcasting
            try:
                index.shape
            except AttributeError:  # no shape attribute
                # try using len
                try:
                    len(index)
                except TypeError:
                    vs = value
                else:
                    vs = np.broadcast_to(value, len(index), subok=True)
            else:
                vs = np.broadcast_to(value, index.shape, subok=True)

            # try iterating
            if np.iterable(vs):
                for i, v in zip(index, vs):  # set recursively
                    self[i] = v
            elif np.isscalar(vs):
                print(vs)
                for i in index:  # set recursively
                    self[i] = vs
            else:
                raise Exception("didn't work")
        # /def

    def __delitem__(self, index):
        self._args.pop(index)
    # /def

    def insert(self, index, value):
        self._args.insert(index, value)
    # /def

    # +-------- len --------+

    def __len__(self):
        return len(self._args)
        # /def

    # +-------- Get / Set --------+
    def __getattr__(self, name):
        """
        NAME:
            __getattr__
        PURPOSE:
            get or evaluate an attribute for these SkyCoords
        INPUT:
            name - name of the attribute
        OUTPUT:
            if the attribute is callable, a function to evaluate the attribute for each Orbit; otherwise a list of attributes
        HISTORY:
            Based off .Orbits method from Mathew Bub
            2018-12-01 - last modified - Nathaniel Starkman (UofT)
            2019-02-10 - last modified - Nathaniel Starkman (UofT)
        """

        # getting attribute in a recursion-friendly way
        try:
            attribute = getattr(self._argsclass, name)
        except Exception as e:
            # attribute = object.__getattribute__(self._args[0], name)
            attribute = self._argsclass.__getattr__(self._args[0], name)

        if callable(attribute):
            # TODO can use self._returnfunc?
            def returnfunc(*args, **kwargs):
                return [
                    getattr(arg, name)(*args, **kwargs)
                    for arg in self._args
                ]
            returnfunc.__doc__ = attribute.__doc__
            return returnfunc
        else:
            return [getattr(arg, name) for arg in self._args]
    # /def

    def get(self, name, parallelize=False):
        try:
            attribute = getattr(self._argsclass, name)
        except Exception as e:
            attribute = object.__getattribute__(self._args[0], name)

        if callable(attribute):

            if parallelize:
                def returnfunc(sequence, *args, numcores=None, **kwargs):
                    return parallel_map(
                        sequence, func_args=args, func_kw=kwargs,
                        numcores=None)

            else:
                def returnfunc(*args, **kwargs):
                    return [getattr(arg, name)(*args, **kwargs)
                            for arg in self._args]

            returnfunc.__doc__ = attribute.__doc__

            return returnfunc

        else:
            return [getattr(arg, name) for arg in self._args]
    # /def

    # +-------- Serialize --------+
    def __getstate__(self):
        return self.__dict__
    # /def

    def __setstate__(self, state):
        self.__dict__ = state
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

# -------------------------------------------------------------------------
