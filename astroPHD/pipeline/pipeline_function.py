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
# import decorator
# import functools
from wrapt import ObjectProxy

## Project-Specific
from ..util.dict_util import split_dictionary
from ..util.inspect import getfullerargspec


##############################################################################
### CODE

class PipelineFunction(ObjectProxy):
    """Node of a Pipeline

    INFO
    ----
    The signature is that of the underlying function
    The defaults for the pipeline can be seen in self._defaults  # TODO better method

    Parameters
    ----------
    func : function

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

    TODO
    ----
    have a register_function_connection
    """

    def __call__(self, *args, **kwargs):
        """pass the call to the function
        """
        return self._func(*args, **kwargs)
    # /def

    def __new__(cls, func=None, outargnames=None, inargnames=None, name=None,
                **kw):
        """
        """
        if outargnames is None:
            raise ValueError('outargnames cannot be None')

        self = super().__new__(cls)  # inherit class information

        # assigning documentation as function documentation
        self.__doc__ = func.__doc__

        # allowing PipelineFunction to act as a decorator
        if func is None:
            return self.decorator(outargnames, inargnames=inargnames,
                                  name=name, **kw)
        return self
    # /def

    @classmethod
    def decorator(cls, outargnames, inargnames=None, name=None, **kw):
        """TODO
        """
        # @functools.wraps(cls)  # not needed when using ObjectProxy
        def wrapper(func):
            """PipelineFunction wrapper"""
            return cls(func, outargnames=outargnames, inargnames=inargnames,
                       name=name, **kw)
        # /def

        return wrapper
    # /def

    def __init__(self, func, outargnames, inargnames=None, name=None, **kw):
        """Node of a Pipeline

        Defaults
        --------
        The defaults for the pipeline can be seen in self._defaults  # TODO better method

        PipelineFunction Parameters
        ---------------------------

        """

        super().__init__(func)  # inializing function into wrapt.ObjectProxy

        # storing function
        self._func = func
        self.name = func.__name__ if name is None else name

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

        # initialize defaults
        self.set_defaults(**kw)
        return
    # /def

    def set_defaults(self, **kw):
        """
        """
        self._defaults = kw
    # /def

    def _split_into_args_kwargs(self, kw):
        """
        """
        kwset = set(kw.keys())
        args = []
        # mandatory arguments
        if self._spec.args is not None:

            # checking all required arguments are present
            argset = set(self._spec.args)
            if not argset.issubset(kwset):
                raise Exception(f'{self._func.__name__} needs argument(s): \
                                  {argset.difference(kwset)}')
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
        kwd = self._defaults.copy()  # copying is necessary

        # mapping keys using _inargnames
        for n1, n2 in self._inargnames.items():
            if n1 in kw:
                kw[n2] = kw.pop(n1)

        kwd.update(kw)

        args, kwargs = self._split_into_args_kwargs(kwd)
        # print(args, kwargs)

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
