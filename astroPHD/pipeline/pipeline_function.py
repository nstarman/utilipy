#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : src initialization
# AUTHOR  : Nathaniel Starkman
# PROJECT : Palomar 5 in Gaia DR2
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""pipeline function

TODO:
- set the documentation for PipelineFunction
- figure out how to dynamically change the docstring for PipelineFunction
  so that it keeps the defaults set by .initialize in the docstring
- change name _func to __wrapped__?
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### IMPORTS

## General
from decorator import decorator
import functools
from types import FunctionType

## Project-Specific
# from .util import ObjDict, LogFile
from ..util.dict_util import split_dictionary
from ..util.inspect import getfullerargspec


###############################################################################
### PARAMETERS

_DOC = """

current call signature : # TODO

Parameters
----------
func : function
    defualt : {func}

"""

# _LOGFILE = LogFile(header=False)  # PrintLog, which is compatible with LogFile


##############################################################################
### CODE

class PipelineFunction(object):
    """

    current call signature : # TODO

    Parameters
    ----------
    func : function
        default : {func}

    outargnames: tuple, None
        the names of the outputs of *func*
        ** only used by next function in a Pipeline **
        mandatory b/c python cannot introspect function returns
        when used in a Pipeline, this is used by *inargnames* of the next
        function, unless otherwise specified / overwritten

    inargnames : dict  # TODO
        ** only used by previous function in a Pipeline **
        for a dictionary of inputs *indict*, *inargnames* maps the keys of
        *indict* to the (kw)args of *func*
        *func* is introspected for the full set of possible keys, anything
        not explicitly remapped by *inargnames* is assumed to be the same.
            ex: for func(x, y, z) & inargnames = dict(x='a')
                now the input to func is assumed to be func(a, y, z)

        *inargnames* cannot remap keys to existing kw(arg) s.t. there are many
        a KeyError will be raised in this case
            ex: for func(x, y, z) & inargnames = dict(x='a')
                this tries to do func(y, y, z), which is not permitted

    """

    def __new__(cls, func, outargnames, inargnames=None, **kw):

        # # catching when this should be a decorator
        # if not isinstance(func, FunctionType):
        #     return cls.decorator(outargnames, inargnames, **kw)

        self = super().__new__(cls)
        # Call function
        # implemented in here to be able to preserve the call signature
        # @decorator
        # def call_func(func, *args, **kwargs):
        #     return func(*args, **kwargs)
        # self.__call__ = call_func(func)
        # Run function
        # self.run.__doc__ = """setting run"""
        # changing documention to reflect
        # TODO do this in a metaclass?
        self.__doc__ = self.__doc__.format(func=func, )

        return self
    # /def

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    @classmethod
    def decorator(cls, outargnames, inargnames=None, **kw):
        # FIXME

        @functools.wraps(cls)  # TODO implement from decorator package?
        def wrap(func):
            return cls(func, outargnames, inargnames, **kw)

        return wrap
    # /def

    def __init__(self, func, outargnames, inargnames=None, **kw):
        # super().__init__(func)
        self._func = func

        self._spec = getfullerargspec(func)  # detailed info on the function

        # inargnames
        if inargnames is None:  # FIXME
            inargnames = {}
        # TODO some check its a dictionary
        self._inargnames = inargnames

        # outargnames
        if outargnames is None:
            outargnames = ()
        elif isinstance(outargnames, str):
            outargnames = (outargnames, )
        # TODO some check its a list or tuple
        self._outargnames = outargnames

        # initialize
        self.initialize(**kw)
        return
    # /def

    def initialize(self, **kw):
        self._defaults = kw
    # /def

    def _split_into_args_kwargs(self, kw):

        kwset = set(kw.keys())
        args = []
        # mandatory arguments
        if self._spec.args is not None:

            # checking all required arguments are present
            argset = set(self._spec.args)
            if not argset.issubset(kwset):
                raise Exception(f'{self._func.__name__} needs argument(s): {argset.difference(kwset)}')
            # ... they are, proceeding
            # splitting out the args and removing the keys from kw
            argsdict, kw = split_dictionary(kw, keys=self._spec.args)
            # adding in args
            args += argsdict.values()

        # default arguments
        if self._spec.defaultargs is not None:
            # getting the defaults
            argdefaults = self._spec.argdefaults
            # overriding with values from **kw
            defargsdict, kw = split_dictionary(kw, keys=self._spec.defaultargs)

            argdefaults.update(defargsdict)
            args += argdefaults.values()

        # variable arguments
        if self._spec.varargs is not None:
            args += kw.pop(self._spec.varargs, ())

        return args, kw
    # /def

    def run(self, **kw):
        """fun the function
        """
        kwd = self._defaults  # TODO check copying is necessary
        kwd.update(kw)

        args, kwargs = self._split_into_args_kwargs(kwd)
        print(args, kwargs)

        res = self._func(*args, **kwargs)

        if len(self._outargnames) == 0:
            return {}
        elif len(self._outargnames) == 1:
            return {self._outargnames[0]: res}
        else:
            assert len(self._outargnames) == len(res)  # TODO as raise? diff is python optimized mode
            return {k: v for k, v in zip(self._outargnames, res)}
    # /def

##############################################################################
### END
