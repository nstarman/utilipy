#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ipython initialization file
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""dictionaries
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
import numpy as np

from collections import OrderedDict
from collections.abc import ItemsView, ValuesView, KeysView, MappingView

## Project-Specific

###############################################################################
### Classes


# +--------------------------------------------------------------------------+
#                                  IndexDict
# +--------------------------------------------------------------------------+

class IndexDict(OrderedDict):
    """An integer-keyed dictarionary

    The order of the keys and the keys each encode information
    for example:
        the keys encode the order added to IndexDict
        the key order encodes the time-order of the values

    Added/Modifed Methods
    ---------------------
    .__getitem__
    .__setitem__
    .set
    .__getstate__
    .__setstate__
    .copy
    .move_to_start
    .add_to_start
    .keyslist
    .valueslist
    .itemslist
    .maxkey
    .minkey
    .indmax
    .indmin
    .prepend
    .append
    """

    # +------------------------------+
    # Get / Set:
    def __getitem__(self, keys):
        r"""
        Keys Options
        ------------
        **No slices  (except slice(None))
        int: item from key (integer key)
        Ellipsis, None, slice(None): self
        tuple: multidimensional slice
            equiv to self[key0][key1, key2, ...]
        other array:
            return indexdict with these keys
            equive to IndexDict([self[k] for k in keys])
        can combine:
            ex: [(key00, key01, ..), key1, key2, ...]
            equiv to IndexDict([self[k][key1, key2, ...] for k in keys[0]])

        Returns
        -------
        value for key, IndexDict for keys
        """

        # single key
        if np.isscalar(keys):  # get key by order number
            return super().__getitem__(keys)

        elif keys in (Ellipsis, None, slice(None)):
            return self

        # multidimensional
        elif isinstance(keys, tuple):  # multidim
            if np.isscalar(keys[0]):  # single IndexDict key
                # self[key0][key1, key2, ...]
                return super().__getitem__(keys[0])[keys[1:]]
            elif keys[0] in (Ellipsis, None, slice(None)):
                keys0 = self.keys()
            else:  # many IndexDict keys
                # [(key00, key01, ..), key1, key2, ...]
                keys0 = keys[0]

            if len(keys) == 2:  # necessary b/c most [] can't use tuples
                return IndexDict([(k,  self[k][keys[1]]) for k in keys0])
            else:
                return IndexDict([(k,  self[k][keys[1:]]) for k in keys0])

        # not multidimensional
        else: # return indexdict
            # [self[k] for k in keys]
            return IndexDict([(k,  self[k]) for k in keys])
    # /def

    def __setitem__(self, key, value):
        r"""
        Arguments
        ---------
        key: int
            only accepts integer keys
        value: anything
        """
        if not isinstance(key, int):
            raise ValueError('key is not int')
        super().__setitem__(key, value)
        # self._ind = key  # update current index
    # /def

    def set(self, key, value):
        r"""
        Arguments
        ---------
        key: int
            only accepts integer keys
        value: anything
        """
        self.__setitem__(key, value)
    # /def

    # +------------------------------+
    # Move / Add @ positions

    def move_to_start(self, key):
        r"""move to start of OrderedDict

        Arguments
        ---------
        key: int
            only accepts integer keys
        """
        super().move_to_end(key, last=False)
    # /def

    def add_to_start(self, key, value):
        r"""add item @ start of OrderedDict

        Arguments
        ---------
        key: int
            only accepts integer keys
        value: anything
        """
        self[key] = value  # adding
        self.move_to_start(key)  # moving
    # /def

    # move_to_end
    # add_to_end

    # +------------------------------+
    # Serialize:
    def __getstate__(self):
        """get state = self.items()"""
        return self.items()
    # /def

    def __setstate__(self, state):
        """set state from .items()"""
        for i, v in state:
            self.set(i, v)
    # /def

    def copy(self):
        """return copy of self
        uses self.__class__
        """
        instance = super().__new__(self.__class__)
        instance.__init__(self.items())
        return instance

    ###########  List Methods  ################
    def keyslist(self, ind=None):
        r"""list of keys (instead of odict_view)"""
        if ind in (None, Ellipsis):
            ind = slice(None)
        return list(self.keys())[ind]

    def valueslist(self, ind=None):
        r"""array of values (instead of odict_view)"""
        if ind in (None, Ellipsis):
            ind = slice(None)
        return list(self.values())[ind]

    def itemslist(self, ind=None):
        r"""array of items() (instead of odict_view)"""
        if ind in (None, Ellipsis):
            ind = slice(None)
        return list(self.items())[ind]

    # +---------- indmax/min ----------+
    @property
    def curkey(self):
        r"""maximum key  # TODO confirm
        generally most recent key
        """
        return max(self.keyslist())

    @property
    def maxkey(self):
        r"""maximum key
        generally most recent key
        """
        return max(self.keyslist())

    @property
    def minkey(self):
        r"""minimum key
        generally 0
        """
        return min(self.keyslist())

    @property
    def indmax(self):
        r"""last key/index in list"""
        return self.keyslist(-1)
    # /def

    @property
    def indmin(self):
        r"""first key/index in list"""
        return self._bounds.keyslist(0)
    # /def

    # +---------- pre/append ----------+
    def _aprependkey(self, _zeroind):
        try:  # add after maxkey
            key = self.maxkey + 1
        except IndexError:  # need to add starting value
            key = _zeroind
        return key
    # /def

    def prepend(self, value, _zeroind=0):
        r"""add value to start of IndexDict
        """
        key = self._aprependkey(_zeroind)
        self.add_to_start(key, value)
    # /def

    def append(self, value, _zeroind=0):
        r"""add value to end of IndexDict
        """
        key = self._aprependkey(_zeroind)
        self[key] = value
    # /def

    def __eq__(self, other):
        """test for equality
        """
        try:  # single item
            return super().__eq__(other)
        except ValueError:  # many keys, some are arrays
            tests = []
            for k1, k2 in zip(self.values(), other.values()):
                try:
                    tests.append(all(k1 == k2))
                except ValueError: # not array
                    tests.append(k1 == k2)
            return tests
    # /def

# -------------------------------------------------------------------------
