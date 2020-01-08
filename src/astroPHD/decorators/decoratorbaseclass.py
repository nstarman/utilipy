# -*- coding: utf-8 -*-

# Docstring and Metadata
"""Base class for decorators."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL
import abc
import copy
import inspect
from typing import Any, Union, Callable, Optional

# PROJECT-SPECIFIC
from ..util.functools import wraps, partial
from ..util.string import FormatTemplate


##############################################################################
# CODE
##############################################################################

# ----------------------------------------------------------------------------
# MetaClass


class DecoratorBaseMeta(type):
    """MetaClass for decorators.

    Ensures a decorator has an __init__ method,
    with a docstring from __call__ if not set.

    """

    def __new__(cls, name, bases, dct):
        """Set properties for new decorator class.

        define an init method and store original docs

        Parameters
        ----------
        cls : type
        name : str
        bases : tuple
        dct : dictionary

        """
        # # add function to class
        # if "__init__" not in dct:

        #     # define __init__ so always have an __init__ method
        #     # and can overwrite the docstring from __call__
        #     def __init__(self, *args, **kwargs):
        #         return

        #     dct["__init__"] = __init__

        # # /if

        # store original docs
        # with None -> ''
        dct["_orig_classdoc_"] = FormatTemplate(
            copy.copy(dct.get("__doc__", None)) or ""
        )
        # dct['_orig_initdoc_'] = copy.copy(dct['__init__'].__doc__)
        # dct['_orig_calldoc_'] = copy.copy(dct['__call__'].__doc__)

        # format class docstring
        # have to do in __new__ so that don't get class & instance docstrings
        if "__kwdefaults__" not in dct:
            dct["__kwdefaults__"] = {}
        dct["__doc__"] = dct["_orig_classdoc_"].safe_substitute(**dct["__kwdefaults__"])

        # create and return object
        return type.__new__(cls, name, bases, dct)

    # /def

    def __init__(cls, name, bases, dct):
        """__init__ method for MetaClass.

        Sets up docstring inheritance.

        References
        ----------
        The docstring inheritance method is modified from
        astropy's InheritDocstrings metaclass

        """
        # ---------------------
        # docstring inheritance

        # find public methods
        def is_public_member(key):
            return (
                key.startswith("__") and key.endswith("__") and len(key) > 4
            ) or not key.startswith("_")

        # /def

        # add docstring to methods
        for key, val in dct.items():
            # check is public function without a docstring
            if (
                (inspect.isfunction(val) or inspect.isdatadescriptor(val))
                and is_public_member(key)
                and val.__doc__ is None
            ):

                # traverse MRO
                for base in cls.__mro__[1:]:
                    super_method = getattr(base, key, None)
                    if super_method is not None:
                        val.__doc__ = super_method.__doc__
                        break
                # /for
        # /for

        # ---------------------

        super().__init__(name, bases, dct)

        return

    # /def


# /class


# ----------------------------------------------------------------------------
# Base Class


class DecoratorBaseClass(metaclass=DecoratorBaseMeta):
    """A class-based implementation of simple_mod_decorator."""

    # @property
    # def __kwdefaults__(self):
    #     """__kwdefaults__."""
    #     return self.__base_kwdefaults__

    # @__kwdefaults__.setter
    # def __kwdefaults__(self, value):
    #     self.__base_kwdefaults__ =

    __kwdefaults__ = {}

    def __new__(cls, function=None, **kwargs):
        """Make new decorator instance.

        Parameters
        ----------
        kwargs : dict
            attributes

        Returns
        -------
        type
            function if called with the function (Decorator(function))
            type if no function provided, i.e. pie syntax

        Raises
        ------
        ValueError
            if a kwarg not supported, i.e. not in __kwdefaults__

        """
        self = super().__new__(cls)  # make instance

        # --------------------
        # assign to class

        attr_keys = self.__kwdefaults__.keys()  # get defaults

        # check keys are valid
        for key in kwargs.keys():
            if key not in attr_keys:
                raise ValueError("")

        # update __kwdefaults__ from kwargs
        self.__kwdefaults__.update(kwargs)

        # --------------------
        # format docstrings

        # TODO allow for partial formatting

        self.__doc__ = self._orig_classdoc_.safe_substitute(**self.__kwdefaults__)
        # self.__call__.__func__.__doc__ = self._orig_calldoc_.format(**self.__kwdefaults__)

        # --------------------

        if function is not None:  # this will return a wrapped function
            return self(function)
        else:  # this will return a function wrapper
            return self

    # /def

    def __getitem__(self, name):
        """Get item from kwdefaults."""
        return self.__kwdefaults__[name]

    # /def

    def __setitem__(self, name, value):
        """Set kwdefaults item."""
        self.__kwdefaults__[name] = value

    # /def

    def as_decorator(self, wrapped_function=None, **kwdefaults):
        """Make decorator.

        Parameters
        ----------
        wrapped_function : types.FunctionType

        Returns
        -------
        types.FunctionType or type
            function if called with the function (Decorator(function))
            type if no function provided, i.e. pie syntax

        """
        decorator = self.new(**kwdefaults)

        if wrapped_function is not None:  # return a wrapped function
            return decorator(wrapped_function)
        # else return a function wrapper
        return decorator

    # /def

    def new(self, **kw):
        """Make a new decorator from current decorator.

        Inherits properties from current decorator.
        Can be overwritten.

        Parameters
        ----------
        kw: dict
            key, value pairs for the kwdefaults

        Returns
        -------
        type
            new decorator with updated properties

        """
        # get and update defaults
        kwdefaults = self.__kwdefaults__.copy()
        kwdefaults.update(**kw)
        # make new class, updating defaults
        return self.__class__(**kwdefaults)

    # /def

    @abc.abstractmethod
    def __call__(self, wrapped_function):
        """Construct a function wrapper.

        This function must be overwritten.

        """
        @wraps(wrapped_function)
        def wrapper(*func_args, **func_kwargs):
            return_ = wrapped_function(*func_args, **func_kwargs)
            return return_

        # /def

        return wrapper

    # /def


# /class


# ----------------------------------------------------------------------------
# Turn a Function into a Decorator


def classy_decorator(decorator_function=None):
    """Convert decorated functions to classes.

    Parameters
    ----------
    decorator_function: types.FunctionType
        The decorator function

    Returns
    -------
    Decorator: DecoratorBaseClass
        class version of `decorator_function`, using the `DecoratorBaseClass`

    """
    if decorator_function is None:  # allowing for optional arguments
        return partial(classy_decorator)

    # key-word defaults from function
    kwd = inspect.getfullargspec(decorator_function).kwonlydefaults

    # TODO rename decorator as function name
    class Decorator(DecoratorBaseClass):

        __kwdefaults__ = kwd

        def __call__(self, wrapped_function):
            return decorator_function(wrapped_function)

        # /def

    # /class

    Decorator.__doc__ = FormatTemplate(decorator_function.__doc__).safe_substitute(**kwd)

    return Decorator()


# /def


# ----------------------------------------------------------------------------
# DEPRECATED

# class DecoratorBaseClass:
#     """DecoratorBaseClass."""

#     @staticmethod
#     def _doc_func(docstring: str) -> str:
#         return docstring

#     def __new__(cls, func: Optional[Callable] = None, **kwargs: Any) -> object:
#         """__new__.

#         this is a quick and dirty method for class-based decorator creation
#         it is generically better to do this with a classmethod like

#         @classmethod
#         as_decorator(cls, func=None, ...):
#             all the same code as here

#         """
#         # make instance
#         self = super().__new__(cls)

#         # wrapper control:
#         if func is not None:  # this will return a wrapped function
#             # pass all arguments and kwargs to init
#             # since __init__ is will not be called
#             self.__init__(func, **kwargs)
#             return self(func)
#         else:  # this will return a function wrapper
#             # for when using as a @decorator
#             # __init__ will be automatically called after this
#             return self

#     # /def

#     def __init__(self, func: Optional[Callable] = None, **kwargs: Any) -> None:
#         """__init__.

#         these are stored to be used inside of __call__
#         they are not normally passed to the wrapped_function

#         """
#         super().__init__()

#         # store all values passed to __init__
#         for k, v in kwargs.items():
#             setattr(self, k, v)

#         # call __post_init__
#         self.__post_init__()

#         return

#     # /def

#     def __post_init__(self) -> None:
#         """__post_init__."""
#         pass

#     # /def

#     def _edit_docstring(self, wrapper: Callable) -> Callable:
#         """Edit docstring."""

#         # docstring
#         # if wrapper.__doc__ is not None:
#         #     wrapper.__doc__ = self._doc_func(wrapper.__doc__)
#         wrapper.__doc__ = self._doc_func(wrapper.__doc__)

#         # storing extra info
#         # wrapper._doc_func = self._doc_func

#         return wrapper

#     # /def

#     def __call__(self, wrapper: Callable) -> Callable:
#         """__call__."""
#         return self._edit_docstring(wrapper)

#     # /def


# # /class

##############################################################################
# END
