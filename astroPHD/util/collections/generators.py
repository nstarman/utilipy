#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : generators
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
from itertools import islice

try:
    from astropy.utils.decorators import wraps
except ImportError as e:
    print("could not import wraps from astropy. using functools' instead")
    from functools import wraps


#############################################################################
### Generator Wrappers

class LenIter(object):
    """
    """

    def __init__(self, iterable, length=None):
        self._iter = iterable
        self._len = length
    # /def

    def __iter__(self):
        return self._iter
    # /def

    def __len__(self):
        if self._len is not None:
            return self._len
        else:
            raise AttributeError('iterator has no len()')
    # /def

    @property
    def shape(self):
        return (self.__len__(), )
    # /def


# -------------------------------------------------------------------------

class LenGen(object):
    r"""generator wrapper with len() support

    based off https://stackoverflow.com/a/7460935

    Arguments
    ---------
    gen: generator (!must return a generator)
    length: the known length of the generator
    args: generator args
    kw: generator kwargs
    """

    def __init__(self, gen, length=None, args=[], kws={}):
        self.gen_func = gen
        self._args = args
        self._kws = kws

        self._len = length
    # /def

    def __iter__(self):
        return self.gen_func(*self._args, **self._kws)
    # /def

    def __call__(self):
        if self._len is not None:
            return LenIter(islice(self.gen_func(*self._args, **self._kws), self._len), self._len)
        else:
            return self.gen_func(*self._args, **self._kws)
        # return islice(self.gen(*self._args, **self._kws), self._len)
    # /def

    def islice(self, *args):
        if len(args) == 0:
            raise ValueError('need to provide a *stop*')
        elif len(args) == 1:
            length = args[0]
        elif len(args) == 2:
            length = args[1] - args[0]
        elif len(args) == 3:
            length = len(np.arange(*args))

        iterable = self.gen_func(*self._args, **self._kws)
        return LenIter(islice(iterable, *args), length)
    # /def

    def __len__(self):
        if self._len is not None:
            return self._len
        else:
            raise AttributeError('___ has no len()')
    # /def

    @property
    def shape(self):
        return (self.__len__(), )
    # /def

# -------------------------------------------------------------------------
