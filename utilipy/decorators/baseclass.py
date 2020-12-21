# -*- coding: utf-8 -*-

"""Base class for decorators.

Most decorators are function-based. A function-based decorator is reasonably
flexible, even permitting default values to be set dynamically. By using
`~utilipy.utils.functools.wraps` in :mod:`~utility.utils.functools` these
function-based decorators may can also merge the decorator and function
signatures and docstrings.

.. code-block:: python

    def template_decorator(function=None, *, kw1=None, kw2=None):
        '''Decorator Docstring.

        Parameters
        ----------
        function : Callable or None, optional
            the function to be decoratored
            if None, then returns decorator to apply.
        kw1, kw2 : Any, optional
            keyword only arguments
            sets the wrapper's default values.

        Returns
        -------
        wrapper : Callable
            wrapper for `function`
            includes the original function in a method ``.__wrapped__``

        '''
        if function is None: # allowing for optional arguments
            return functools.partial(template_decorator, kw1=k1, kw2=kw2)

        @utilipy.wraps(function, _doc_style='numpy')
        def wrapper(*args, kw1=kw1, kw2=kw2, kw3="kw3", **kw):
            '''wrapper docstring.

            Parameters
            ----------
            kw1, kw2 : Any, optional
                default {kw1}, {kw2}
            kw3 : str, optional
                default {kw3}

            '''
            # do stuff here
            return_ = function(*args, **kw)
            # and here
            return return_

        return wrapper

For most purposes decorators of these sorts are sufficient. However, there are
a number of limitations inherent to a function-based approach. A more general
architecture is possible using classes. As example, ``TemplateDecorator``
is nearly equivalent to the previously defined ``template_decorator``.

.. code-block:: python

    class TemplateDecorator():

        def __new__(cls, function=None, *, kw1=None, kw2=None):
            self = super().__new__(cls)  # make instance
            if function is not None:  # this will return a wrapped function
                return self(function, kw1=kw1, kw2=kw2)
            else:  # this will return a function wrapper
                return self

        def __init__(self, kw1=None, kw2=None):
            self.kw1 = kw1
            self.kw2 = kw2

        def __call__(self, function, kw1=None, kw2=None):
            '''Construct a function wrapper.'''
            kw1 = self.kw1 if kw1 is None else kw1
            kw2 = self.kw2 if kw2 is None else kw2

            @utilipy.wraps(function)
            def wrapper(*args, kw1=kw1, kw2=kw2, kw3="kw3", **kw):
                '''wrapper docstring.

                Parameters
                ----------
                kw1, kw2 : Any, optional
                    default {kw1}, {kw2}
                kw3 : str, optional
                    default {kw3}

                '''
                # do stuff here
                return_ = function(*args, **kw)
                # and here
                return return_

            return wrapper

An important difference between ``template_decorator`` and
``TemplateDecorator`` happens at creation. If template decorator is
created with


"""

__author__ = "Nathaniel Starkman"


__all__ = [
    # decorators
    "DecoratorBaseMeta",
    "DecoratorBaseClass",
    "classy_decorator",
    # utility
    "_placeholders",
]


##############################################################################
# IMPORTS

# BUILT-IN
import copy
import typing as T
from abc import abstractmethod
from collections import namedtuple

# PROJECT-SPECIFIC
from utilipy.utils import functools, inspect
from utilipy.utils.string import FormatTemplate

##############################################################################
# Parameters

_placeholders: tuple = (inspect._empty, inspect._void, inspect._placehold)


class kwargs:  # FIXME: temporary fix for Sphinx
    pass


##############################################################################
# CODE
##############################################################################

# ----------------------------------------------------------------------------
# MetaClass


class DecoratorBaseMeta(type):
    """Meta-class for decorators.

    This metaclass is pretty specific for DecoratorBaseClass and should
    probably not be used in other contexts.

    This metaclass:

    - creates `__kwdefaults__`, copying from `__base_kwdefaults__`.
    - makes a named-tuple class for read-only versions of `__kwdefaults__`
    - stores the original class and call docs
    - formats the class docstrings with the `__kwdefaults__`

    """

    def __new__(cls: type, name: str, bases: tuple, dct: dict):
        """Set properties for new decorator class.

        define an `__init__` method and store original docs

        Parameters
        ----------
        name : str
        bases : tuple
        dct : dictionary

        """
        # --------------------------------------------------
        # __base_kwdefaults__ -> __kwdefaults__

        dct["__kwdefaults__"] = dct["__base_kwdefaults__"].copy()

        dct["_kwd_namedtuple"] = namedtuple(
            "kwdefaults", dct["__kwdefaults__"].keys()
        )

        # --------------------------------------------------
        # store original docs
        # with None -> ''
        dct["_orig_classdoc_"] = FormatTemplate(
            copy.copy(dct.get("__doc__", None)) or ""
        )
        dct["_orig_calldoc_"] = FormatTemplate(
            copy.copy(dct["__call__"].__doc__) or ""
        )

        # formatting class docstring
        # needs to be done here for the first class declaration
        # later edits are handled in DecoratorBaseClass by `__new__`
        dct["__doc__"]: str = dct["_orig_classdoc_"].safe_substitute(
            **dct["__kwdefaults__"]
        )

        # ------------------------
        # 1) change call's signature
        #   - add a variable positional argument (\*args)
        #   - promote any positional arguments with defaults
        #     (except *function*) to keyword only arguments
        #   - substitue the values of `__kwdefaults__` as the default values
        #     for key-word arguments with a placehold value
        #     (_empty, _void, _placehold)

        callsig: inspect.FullerSignature
        callsig = inspect.fuller_signature(dct["__call__"])

        # store whether has kwargs, for use in ``callwrapper``
        has_kwargs = callsig.index_var_keyword

        # next check if have a var_positional argument
        # promoting default-valued positional arguments to kwargs
        callsig = callsig.add_var_positional_parameter(index=2)
        callsig = callsig.add_var_keyword_parameter(name="kwargs")

        # replacing defaults if in __base_kwdefaults__
        i: int
        name: str
        param: inspect.Parameter
        for i, (name, param) in enumerate(callsig.parameters.items()):
            # only keyword-only args (most since added var_positional)
            if (name in dct["__kwdefaults__"]) and (  # yup
                param.kind == inspect.KEYWORD_ONLY
            ):  # key-word
                callsig = callsig.modify_parameter(
                    i, default=dct["__kwdefaults__"][name]
                )

        # updating __call__ from callsig
        attr: str
        for attr in functools.SIGNATURE_ASSIGNMENTS:
            try:
                value = getattr(callsig, attr)
            except AttributeError:
                pass
            else:
                setattr(dct["__call__"], attr, value)

        # ------------------------
        # 2) Wrap __call__ so can use without parenthesis
        #   - store __call__
        #   - change function default to None

        # store original call function   # TODO fix copy_function
        dct["__orig_call__"]: T.Callable = functools.copy_function(
            dct["__call__"]
        )
        dct["__orig_call__"].__kwdefaults__: dict = dct[
            "__call__"
        ].__kwdefaults__
        # dct["__orig_call__"].__signature__ = callsig.signature

        # change function default to None
        # not doing it before to preserve __orig_call__
        try:
            callsig = callsig.modify_parameter(
                1, default=None, kind=inspect.POSITIONAL_OR_KEYWORD
            )
        except ValueError:  # already has a default
            pass

        dct["_callsig"]: inspect.Signature = callsig

        # make wrapper
        def callwrapper(
            self, function: T.Callable = None, *args: T.Any, **kwargs: T.Any
        ):
            self = self.new(
                **kwargs
            )  # TODO extract __kwdefaults__ dict from this

            # update kwargs to carry over to __orig_call__
            if has_kwargs is False:  # no kwargs, can only use existing
                nkw: dict = (self._callsig.__kwdefaults__ or {}).copy()
            else:  # can pass everything along
                nkw: dict = (self.__kwdefaults__ or {}).copy()
            nkw.update(kwargs)

            # allow calling without parenthesis
            if function is None:
                return functools.partial(self.__orig_call__, **nkw)
            else:
                return self.__orig_call__(function, *args, **nkw)

        # /def

        callwrapper.__kwdefaults__: dict = dct["__kwdefaults__"].copy()
        # /def

        # overwrite __call__ with wrapped function
        # TODO fix update_wrapper
        dct["__call__"]: T.Callable = functools.update_wrapper(
            callwrapper,
            dct["__orig_call__"],
            signature=callsig,
            docstring=dct["_orig_calldoc_"].safe_substitute(
                **dct["__kwdefaults__"]
            ),
        )
        dct["__call__"].__kwdefaults__: dict = dct["__kwdefaults__"].copy()

        # ------------------------

        # create and return object
        return type.__new__(cls, name, bases, dct)

    # /def

    def __init__(cls: type, name: str, bases: tuple, dct: dict):
        """__init__ method for MetaClass.

        Sets up docstring inheritance.

        References
        ----------
        The docstring inheritance method is modified from
        astropy's InheritDocstrings metaclass

        .. todo::

            replace with better doc_inheritance from custom_inherit

        """
        # ---------------------
        # docstring inheritance

        # find public methods
        def is_public_member(key: str):
            return (
                key.startswith("__") and key.endswith("__") and len(key) > 4
            ) or not key.startswith("_")

        # /def

        # add docstring to methods
        key: str
        val: T.Any
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
    """Base Class for Decorators.

    Parameters
    ----------
    function : Callable, optional
    kwargs : dict, optional
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

    __base_kwdefaults__: dict = {}

    @property
    def kwdefaults(self: type):
        """__kwdefaults__ named tuple."""
        return self._kwd_namedtuple(**self.__kwdefaults__)

    # /def

    def __new__(
        cls: type, function: T.Optional[T.Callable] = None, **kwargs: T.Any
    ):
        """Make new DecoratorBaseClass.

        Parameters
        ----------
        function : Collable, optional
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
        key: str
        for key in kwargs.keys():
            if key not in attr_keys:
                raise ValueError("")

        # update __kwdefaults__ from kwargs
        self.__kwdefaults__ = self.__base_kwdefaults__.copy()
        self.__kwdefaults__.update(kwargs)

        # --------------------
        # format docstrings
        # done here for all the non-first class creation (see metaclass)

        self.__doc__: str = self._orig_classdoc_.safe_substitute(
            **self.__kwdefaults__
        )

        self.__call__.__func__.__doc__: str
        self.__call__.__func__.__doc__ = self._orig_calldoc_.safe_substitute(
            **self.__kwdefaults__
        )

        # --------------------
        # format __call__ signature

        # replacing defaults if in __kwdefaults__
        for i, (name, param) in enumerate(self._callsig.parameters.items()):
            # only keyword-only args (most since added var_positional)
            if (
                (name in self.__kwdefaults__)  # yup
                and (param.kind == inspect.KEYWORD_ONLY)  # key-word
                # and (param.default in _placeholders)  # no default!
            ):
                self._callsig = self._callsig.modify_parameter(
                    i, default=self.__kwdefaults__[name]
                )
        # /for

        # set signature and defaults
        self.__call__.__func__.__signature__ = self._callsig.signature
        self.__call__.__func__.__kwdefaults__ = self.__kwdefaults__

        # print(self._callsig.parameters.values())
        # print(self.__call__.__func__.__signature__)
        # print(self.__call__.__func__.__kwdefaults__)

        # --------------------

        if function is not None:  # this will return a wrapped function
            return self(function)
        else:  # this will return a function wrapper
            return self

    # /def

    def __getitem__(self: type, name: str):
        """Get item from kwdefaults."""
        return self.__kwdefaults__[name]

    # /def

    def __setitem__(self: type, name: str, value: T.Any):
        """Set kwdefaults item."""
        self.__kwdefaults__[name] = value

    # /def

    def as_decorator(
        self: type,
        wrapped_function: T.Optional[T.Callable] = None,
        **kwdefaults: T.Any
    ):
        """Make decorator.

        Parameters
        ----------
        wrapped_function : Callable
        kwdefaults
            update the decorator default values

        Returns
        -------
        Callable or type
            function if called with the function (Decorator(function))
            type if no function provided, i.e. pie syntax

        """
        decorator: type = self.new(**kwdefaults)

        if wrapped_function is not None:  # return a wrapped function
            return decorator(wrapped_function)
        # else return a function wrapper
        return decorator

    # /def

    def new(self: type, **kw):
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

        TODO
        ----
        figure out how help(self) can correctly display __kwdefaults__

        """
        # get and update defaults
        kwdefaults: dict = self.__kwdefaults__.copy()
        kwdefaults.update(**kw)
        # make new class, updating defaults
        # TODO use new so override class docstring and recall metaclass
        return self.__class__(function=None, **kwdefaults)

    # /def

    @abstractmethod
    def __call__(self: type, function: T.Callable):
        @functools.wraps(function)
        def wrapper(*func_args: T.Any, **func_kwargs: T.Any):
            return function(*func_args, **func_kwargs)

        # /def

        return wrapper

    # /def


# /class


# ----------------------------------------------------------------------------
# Turn a Function into a Decorator


def classy_decorator(decorator_function: T.Callable = None):
    """Convert decorated functions to classes.

    Parameters
    ----------
    decorator_function: Callable
        The decorator function

    Returns
    -------
    Decorator: DecoratorBaseClass
        class version of `decorator_function`, using the `DecoratorBaseClass`

    """
    if decorator_function is None:  # allowing for optional arguments
        return functools.partial(classy_decorator)

    signature: inspect.FullerSignature
    signature = inspect.fuller_signature(decorator_function)
    signature = signature.prepend_parameter(  # add in self
        inspect.Parameter("self", inspect.POSITIONAL_ONLY)
    )
    # key-word defaults from function
    kwd: dict = inspect.getfullerargspec(decorator_function).kwonlydefaults

    def mycall(
        self: type, wrapped_function: T.Callable, *args: T.Any, **kwargs: T.Any
    ):
        return decorator_function(wrapped_function, *args, **kwargs)

    # /def

    class Decorator(DecoratorBaseClass):

        __base_kwdefaults__: dict = kwd

        # /def
        __call__: T.Callable = functools.makeFunction(
            mycall.__code__,
            mycall.__globals__,
            name="__call__",
            signature=signature,
            docstring=decorator_function.__doc__,
            closure=mycall.__closure__,
        )

    # /class

    # set docstring
    Decorator.__doc__: str = FormatTemplate(
        (decorator_function.__doc__ or "")
    ).safe_substitute(**kwd)
    Decorator.__name__ = decorator_function.__name__

    return Decorator()


# /def


##############################################################################
# END
