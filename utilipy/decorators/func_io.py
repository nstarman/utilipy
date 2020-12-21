# -*- coding: utf-8 -*-

"""Function Input and Output Decorators."""

__all__ = [
    "store_function_input",
    "add_folder_backslash",
    "random_generator_from_seed",
    "dtypeDecoratorMaker",
]


##############################################################################
# IMPORTS

# BUILT-IN
import typing as T

# THIRD PARTY
import numpy as np

# PROJECT-SPECIFIC
from utilipy.utils import functools, inspect
from utilipy.utils.typing import EllipsisType

##############################################################################
# CODE
##############################################################################


def store_function_input(
    function: T.Callable = None,
    *,
    store_inputs: bool = True,
    _doc_style: str = "numpy",
    _doc_fmt: T.Dict[str, T.Any] = {},
):
    """Store Function Inputs.

    Store the function inputs as a BoundArguments.

    Parameters
    ----------
    function : T.Callable or None, optional
        the function to be decoratored
        if None, then returns decorator to apply.
    store_inputs : bool, optional
        whether to return all the inputs to the function as a dictionary

    Returns
    -------
    wrapper : T.Callable
        Wrapper for `function` that can store function inputs
        in a BoundArguments instance.
        Includes the original function in a method `.__wrapped__`

    Other Parameters
    ----------------
    _doc_style: str or formatter, optional
        default 'numpy'
        parameter to `utilipy.wraps`
    _doc_fmt: dict, optional
        default None
        parameter to `utilipy.wraps`

    """
    if function is None:  # allowing for optional arguments
        return functools.partial(
            store_function_input,
            store_inputs=store_inputs,
            _doc_style=_doc_style,
            _doc_fmt=_doc_fmt,
        )

    sig = inspect.fuller_signature(function)
    _doc_fmt["wrapped_function"] = function.__name__

    @functools.wraps(function, _doc_style=_doc_style, _doc_fmt=_doc_fmt)
    def wrapper(*args, store_inputs: bool = store_inputs, **kw):
        """Wrapper docstring.

        Parameters
        ----------
        store_inputs: bool
            whether to store function inputs in a `~inspect.BoundArguments`
            instance default {store_inputs}

        Returns
        -------
        inputs: `~inspect.BoundArguments`
            the inputs to ``{wrapped_function}``
            only returned if `store_inputs` is True
            other returned values are in now in a tuple

        """
        return_ = function(*args, **kw)

        if store_inputs:  # make and return BoundArguments
            inputs = sig.bind_partial_with_defaults(*args, **kw)
            return return_, inputs
        else:
            return return_

    # /def

    return wrapper


# /def


# -------------------------------------------------------------------


def add_folder_backslash(
    function=None,
    *,
    arguments: T.List[T.Union[str, int]] = [],
    _doc_style="numpy",
    _doc_fmt={},
):
    """Add backslashes to str arguments.

    For use in ensuring directory file-paths end in '/', when
    ``os.join`` just won't do.

    Parameters
    ----------
    function : T.Callable or None, optional
        the function to be decoratored
        if None, then returns decorator to apply.
    arguments : list of string or int, optional
        arguments to which to append '/', if not already present
        strings are names of arguments.
        Can also be int, which only applies to args.

    Returns
    -------
    wrapper : T.Callable
        wrapper for function
        does a few things
        includes the original function in a method ``.__wrapped__``

    Other Parameters
    ----------------
    _doc_style: str or formatter, optional
        default 'numpy'
        parameter to `~utilipy.wraps`
    _doc_fmt: dict, optional
        default None
        parameter to `~utilipy.wraps`

    Examples
    --------
    For modifying a single argument

    >>> @add_folder_backslash(arguments='path')
    ... def func(path):
    ...     return path
    >>> func("~/Documents")
    '~/Documents/'

    When several arguments need modification.

    >>> @add_folder_backslash(arguments=('path1', 'path2'))
    ... def func(path1, path2):
    ...     return (path1, path2)
    >>> func("~/Documents", "~Desktop")
    ('~/Documents/', '~Desktop/')

    """
    if isinstance(arguments, (str, int)):  # recast as tuple
        arguments = (arguments,)

    if function is None:  # allowing for optional arguments
        return functools.partial(
            add_folder_backslash,
            arguments=arguments,
            _doc_style=_doc_style,
            _doc_fmt=_doc_fmt,
        )

    sig = inspect.signature(function)

    @functools.wraps(function, _doc_style=_doc_style, _doc_fmt=_doc_fmt)
    def wrapper(*args, **kw):
        """Wrapper docstring.

        Parameters
        ----------
        store_inputs: bool
            whether to store function inputs in a BoundArguments instance
            default {store_inputs}

        """
        # bind args & kwargs to function
        ba = sig.bind_partial(*args, **kw)
        ba.apply_defaults()

        for name in arguments:  # iter through args
            # first check it's a string
            if not isinstance(ba.arguments[name], (str, bytes)):
                continue
            else:
                str_type = type(ba.arguments[name])  # get string type

            backslash = str_type("/")  # so we can work with any type

            if isinstance(name, int):  # only applies to args
                if not ba.args[name].endswith(backslash):
                    ba.args[name] += backslash
            elif isinstance(name, str):  # args or kwargs
                if not ba.arguments[name].endswith(backslash):
                    ba.arguments[name] += backslash
            else:
                raise TypeError("elements of `args` must be int or str")

        return function(*ba.args, **ba.kwargs)

    # /def

    return wrapper


# /def


#####################################################################


def random_generator_from_seed(
    function: T.Callable = None,
    seed_names: T.Union[str, T.Sequence[str]] = ("random", "random_seed"),
    generator: T.Callable = np.random.RandomState,
    raise_if_not_int: bool = False,
):
    """Function decorator to convert random seed to random number generator.

    Parameters
    ----------
    function : types.FunctionType or None (optional)
        the function to be decoratored
        if None, then returns decorator to apply.
    seed_names : list (optional)
        possible parameter names for the random seed
    generator : ClassType (optional)
        ex :class:`numpy.random.default_rng`, :class:`numpy.random.RandomState`

    raise_if_not_int : bool (optional, keyword-only)
        raise TypeError if seed argument is not an int.

    Returns
    -------
    wrapper : types.FunctionType
        wrapper for function
        converts random seeds to random number generators before calling.
        includes the original function in a method `.__wrapped__`

    Raises
    ------
    TypeError
        If `raise_if_not_int` is True and seed argument is not an int.

    """
    if isinstance(seed_names, str):  # correct a bare string to list
        seed_names = (seed_names,)

    if function is None:  # allowing for optional arguments
        return functools.partial(
            random_generator_from_seed,
            seed_names=seed_names,
            generator=generator,
        )

    sig = inspect.signature(function)
    pnames = tuple(sig.parameters.keys())

    @functools.wraps(
        function,
        _doc_fmt={"seed_names": seed_names, "random_generator": generator},
    )
    def wrapper(*args, **kw):
        """Wrapper docstring, added to Function.

        Notes
        -----
        T.Any argument in {seed_names} will be interpreted as a random seed,
        if it is an integer, and will be converted to a random number generator
        of type {random_generator}.

        """
        ba = sig.bind_partial(*args, **kw)
        ba.apply_defaults()

        # go through possible parameter names for the random seed
        # if it is a parameter and the value is an int, change to RandomState
        for name in seed_names:  # iterate through possible
            if name in pnames:  # see if present
                if isinstance(ba.arguments[name], int):  # seed -> generator
                    ba.arguments[name] = generator(ba.arguments[name])
                elif raise_if_not_int:
                    raise TypeError(f"{name} must be <int>")
                else:  # do not replace
                    pass
        # /for

        return function(*ba.args, **ba.kwargs)

    # /def

    return wrapper


# /def


#####################################################################
# DataType Decorators


class dtypeDecorator:
    """Ensure arguments are type *dtype*.

    Parameters
    ----------
    func : function, optional
        function to decorate
    inargs : list
        [(index, dtype), ...]

    outargs : list
        [(index, dtype), ...]

    these arguments, except func, should be specified by key word
    if inargs is forgotten and func is not a function, then func is
    assumed to be inargs.

    """

    def __new__(
        cls,
        func: T.Optional[T.Callable] = None,
        in_dtype: T.Any = None,
        out_dtype: T.Any = None,
    ):
        """New dtypeDecorator."""
        self = super().__new__(cls)  # making instance of self

        # correcting if forgot to specify in_dtype and no function
        # in this case, *in_dtype* is stored in *func*
        # need to do func->None, inarags<-func, and out_dtype<-in_dtype
        if not isinstance(func, T.Callable):
            # moving arguments 'forward'
            out_dtype = in_dtype
            in_dtype = func
            func = None

        # allowing for wrapping with calling the class
        if func is not None:
            self.__init__(in_dtype, out_dtype)
            return self(func)
        # else:
        return self

    # /def

    def __init__(
        self, in_dtype: T.Any = None, out_dtype: T.Any = None
    ) -> None:
        """Initialize dtypeDecorator."""
        super().__init__()

        # in_dtype
        # TODO check in_dtype is list of lists
        self._in_dtype = in_dtype

        # out_dtype
        # TODO check out_dtype is list of lists
        self._out_dtype = out_dtype

        return

    # /def

    def __call__(self, wrapped_func: T.Callable) -> T.Callable:
        """Make Decorator.

        Parameters
        ----------
        wrapped_func: Callable
            function to be wrapped

        """
        # make wrapper
        @functools.wraps(wrapped_func)
        def wrapper(*args: T.Any, **kw: T.Any) -> T.Any:
            # making arguments self._dtype
            if self._in_dtype is None:  # no conversion needed
                return_ = wrapped_func(*args, **kw)
            elif len(args) == 0:
                return_ = wrapped_func(**kw)
            elif len(args) == 1:
                # TODO better
                if len(self._in_dtype) != 1 or self._in_dtype[0][0] != 0:
                    raise IndexError("too many indices")
                arg = self._in_dtype[0][1](args[0])
                return_ = wrapped_func(arg, **kw)
            else:
                args = list(args)  # allowing modifications
                for i, dtype in self._in_dtype:
                    args[i] = dtype(args[i])  # converting to desired dtype`
                return_ = wrapped_func(*args, **kw)

            # POST
            if self._out_dtype is None:  # no conversion needed
                pass
            else:
                if not np.isscalar(return_):
                    return_ = list(return_)  # allowing modifications
                    for i, dtype in self._out_dtype:
                        # converting to desired dtype
                        return_[i] = dtype(return_[i])
                else:
                    if len(self._out_dtype) != 1:  # TODO do this check?
                        raise ValueError("out_dtype has too many indices")
                    return_ = self._out_dtype[0][1](return_)

            return return_

        # /def
        return wrapper

    # /def


# /class

# -------------------------------------------------------------------

# define class
class dtypeDecoratorBase:
    """Ensure arguments are type `dtype`.

    Parameters
    ----------
    func : function (optional)
        function to decorate
    inargs : Ellipsis or iterable or slice or None (optional)
        - None (default), does nothing
        - Ellipsis: converts all arguments to dtype
        - iterable: convert arguments at index specified in iterable
            ex: [0, 2] converts arguments 0 & 2
        - slice: convert all arguments specified by slicer
    outargs : Ellipsis or iterable or slice or None (optional)
        - None (default), does nothing
        - iterable: convert arguments at index specified in iterable
            ex: [0, 2] converts arguments 0 & 2
        - slice: convert all arguments specified by slicer
        - Ellipsis : convert all arguments

    these arguments, except func, should be specified by key word.
    if inargs is forgotten and func is not a function, then func is
    assumed to be inargs.

    Examples
    --------
    >>> intDecorator = dtypeDecoratorMaker(int)
    >>> @intDecorator(inargs=[0, 1], outargs=2)
    ... def func(x, y, z):
    ...     return x, y, z, (x, y, z)
    ... # /def
    >>> print(func(1.1, 2.2, 3.3))
    (1, 2, 3, (1, 2, 3.3))

    """

    def __init_subclass__(cls, dtype: T.Any = None):
        """Initialize subclass & store dtype."""
        super().__init_subclass__()
        cls._dtype = dtype

    # /def

    @property
    def dtype(self):
        """Get dtype. read-only access."""
        return self._dtype

    # /def

    def __new__(
        cls,
        func: T.Callable = None,
        inargs: T.Union[EllipsisType, slice, T.Iterable, None] = None,
        outargs: T.Union[EllipsisType, slice, T.Iterable, None] = None,
    ):
        self = super().__new__(cls)  # making instance of self

        # correcting if forgot to specify inargs and did not provide a func
        # in this case, *inargs* is stored in *func*
        # need to do func->None, inarags<-func, and outargs<-inargs
        if not isinstance(func, T.Callable):
            # moving arguments 'forward'
            outargs = inargs
            inargs = func
            func = None

        # allowing for wrapping with calling the class
        if func is not None:
            # need to initialize b/c not returning `self`
            self.__init__(inargs, outargs)
            return self(func)
        else:
            return self

    # /def

    def __init__(
        self,
        inargs: T.Union[EllipsisType, slice, T.Iterable, None] = None,
        outargs: T.Union[EllipsisType, slice, T.Iterable, None] = None,
    ) -> None:
        super().__init__()

        # inargs
        if inargs is Ellipsis:  # convert all
            self._inargs = slice(None)
        else:
            self._inargs = inargs

        # TODO validate inputs

        # outargs
        if outargs is Ellipsis:
            self._outargs = slice(None)
        elif np.isscalar(outargs):
            self._outargs = [outargs]
        else:
            self._outargs = outargs

    # /def

    def __call__(self, wrapped_func: T.Callable) -> T.Callable:
        """Wrap function.

        Works by making a wrapper which will convert input and
        output arguments to the specified data type.

        Parameters
        ----------
        wrapped_func : callable
            Function to wrap.

        """
        sig = inspect.signature(wrapped_func)

        @functools.wraps(wrapped_func)
        def wrapper(*args: T.Any, **kwargs: T.Any) -> T.Any:

            ba = sig.bind_partial(*args, **kwargs)
            ba.apply_defaults()

            # PRE
            # making arguments self._dtype
            if self._inargs is None:  # no conversion needed
                pass
            elif isinstance(self._inargs, slice):
                # converting inargs to list of indices
                lna = len(ba.args)

                inkeys = tuple(ba.arguments.keys())[:lna][self._inargs]
                inargs = tuple(range(lna))[self._inargs]

                # converting to desired dtype
                for k, i in zip(inkeys, inargs):
                    ba.arguments[k] = self._dtype(ba.args[i])
            else:  # any iterable

                lna = len(ba.args)
                argkeys = tuple(ba.arguments.keys())

                for i in self._inargs:
                    if isinstance(i, int):  # it's for args
                        ba.arguments[argkeys[i]] = self._dtype(args[i])
                    else:  # isinstance(i, str)
                        ba.arguments[i] = self._dtype(ba.arguments[i])

            # /PRE

            return_ = wrapped_func(*ba.args, **ba.kwargs)

            # POST
            # no conversion needed
            if self._outargs is None or not isinstance(return_, tuple):
                return return_
            # slice
            elif isinstance(self._outargs, slice):
                iterable = tuple(range(len(return_)))[self._outargs]
            else:
                iterable = self._outargs

            return_ = list(return_)

            for i in iterable:
                return_[i] = self._dtype(return_[i])

            return tuple(return_)
            # /POST

        # /def

        return wrapper

    # /def


# /class


# -------------------------------------------------------------------


def dtypeDecoratorMaker(dtype: T.Any):
    """Function to make a dtype decorator.

    Parameters
    ----------
    dtype : type
        intended data type

    Returns
    -------
    dtypeDecorator : decorator class
        a decorator which can convert input and output arguments
        to the intended datatype

    Examples
    --------
    >>> intDecorator = dtypeDecoratorMaker(int)
    >>> @intDecorator(inargs=[0, 1], outargs=2)
    ... def func(x, y, z):
    ...     return x, y, z, (x, y, z)
    >>> x, y, z, orig = func(1.1, 2.2, 3.3)
    >>> print(x, y, z, orig)  # z->int before returned
    1 2 3 (1, 2, 3.3)

    """
    # make subclass
    class dtypeDecorator(dtypeDecoratorBase, dtype=dtype):
        pass

    # /class

    dtypeDecorator.__name__ = f"{dtype}Decorator"

    return dtypeDecorator


# /def


#############################################################################
# MAKING DECORATORS

intDecorator = dtypeDecoratorMaker(int)
floatDecorator = dtypeDecoratorMaker(float)
strDecorator = dtypeDecoratorMaker(str)
boolDecorator = dtypeDecoratorMaker(bool)

ndarrayDecorator = dtypeDecoratorMaker(np.ndarray)
ndfloat64Decorator = dtypeDecoratorMaker(np.float64)


#############################################################################
# END
