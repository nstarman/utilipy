#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
"""Docstring

#############################################################################

Copyright (c) # TODO

#############################################################################
Planned Features


"""

#############################################################################
# Imports

from collections.abc import MutableSequence
from collections import OrderedDict

# Custom Packages
from .multi import parallel_map

#############################################################################
# Code


class AstrObj(OrderedDict):
    """
    A basic object intended to store information on astronomical objects.
    Instantiated with a name (str)"""

    # def __new__(cls, name):
    #     self = super(AstrObj, cls).__new__(cls)
    #     self.name = name

    def __init__(self, name, **kw):
        super().__init__()
        self.name = name
        for key, value in kw.items():
            self[key] = value

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, *keys):
        if isinstance(keys[0], str):
            return super().__getitem__(keys[0])
        else:
            return [OrderedDict.__getitem__(self, key) for key in keys[0]]

    def keyslist(self):
        return list(self.keys())


class Objects(MutableSequence):
    """Holds many
    [SkyCoord, SkyCoord, ...]
    Can perform operations on many different skycoords simultaneously

    # TODO? change to use __new__ so can change docstring
    """

    # def __new__(cls, *args, name='Objects', **kwargs):

    #     cls.__call__.__doc__ = """
    #     """

    #     self = super(Objects, cls).__new__(cls)

    #     self._args = args
    #     self._argsclass = args[0].__class__

    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    #     return self

    def __init__(self, *args, **kw):
        """all SkyCoords must have the same attributes
        """
        super().__init__()

        self._args = args
        self._argsclass = args[0].__class__

        for key, value in kw.items():
            setattr(self, key, value)
    # /def

    # +-------- get / set / del / insert - item --------+
    def __getitem__(self, index):
        return self._args[index]
    # /def

    def __setitem__(self, index, value):
        self._args[index] = value
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

    # +-------- Pickling --------+
    def __getstate__(self):
        return (self._args, self._argsclass, )  # TODO get all the attributes
    #     return self.__dict__
    # /def

    def __setstate__(self, state):
        self._args = state[0]
        self._argsclass = state[1]
          # TODO set all the attributes
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
