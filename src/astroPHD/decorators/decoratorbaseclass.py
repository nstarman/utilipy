#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Docstring and Metadata
"""Base class for decorators"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General

# Project-Specific

##############################################################################
# CODE

class DecoratorBaseClass():
    """DecoratorBaseClass."""

    @staticmethod
    def _doc_func(docstring):
        return docstring

    def __new__(cls, func=None, **kwargs):
        """
        this is a quick and dirty method for class-based decorator creation
        it is generically better to do this with a classmethod like
        @classmethod
        as_decorator(cls, func=None, ...):
            all the same code as here
        """
        # make instance
        self = super().__new__(cls)

        # wrapper control:
        if func is not None:  # this will return a wrapped function
            # pass all arguments and kwargs to init
            # since __init__ is will not be called
            self.__init__(func, **kwargs)
            return self(func)
        else:  # this will return a function wrapper
            # for when using as a @decorator
            # __init__ will be automatically called after this
            return self
    # /def

    def __init__(self, func=None, **kwargs):
        """
        these are stored to be used inside of __call__
        they are not normally passed to the wrapped_function
        """
        super().__init__()

        # store all values passed to __init__
        for k, v in kwargs.items():
            setattr(self, k, v)

        # call __post_init__
        self.__post_init__()

        return
    # /def

    def __post_init__(self):
        """"""
        pass
    # /def

    def _edit_docstring(self, wrapper):
        """Edit docstring."""

        # docstring
        # if wrapper.__doc__ is not None:
        #     wrapper.__doc__ = self._doc_func(wrapper.__doc__)
        wrapper.__doc__ = self._doc_func(wrapper.__doc__)

        # storing extra info
        # wrapper._doc_func = self._doc_func

        return wrapper
    # /def


    def __call__(self, wrapper):
        """"""
        return self._edit_docstring(wrapper)
    # /def 

# /class

##############################################################################
# END
