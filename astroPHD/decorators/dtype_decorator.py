# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : decorators
#
# ----------------------------------------------------------------------------

"""DataType Decorators.

TODO
----
support argument 'all' in [(index, dtype),] as the IndexError
supoort single argumens so that (index, dtype) works w/out [(), ]
full support of numpy.dtype
add in_dtype and out_dtype kwargs to wrapped functions which override defaults

"""

__all__ = [
    "dtypeDecorator",
    "dtypeDecoratorMaker",
    # built-in types
    "boolDecorator",
    "intDecorator",
    "floatDecorator",
    "strDecorator",
    # numpy types
    "ndarrayDecorator",
    "ndfloat64Decorator",
]


##############################################################################
# IMPORTS

# GENERAL

from typing import Any, Callable, Optional, Union, Iterable
from typing_extensions import Literal
import numpy as np

# PROJECT-SPECIFIC
from ..utils import functools


#############################################################################
# MAKING DECORATORS


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
        func: Optional[Callable] = None,
        in_dtype: Any = None,
        out_dtype: Any = None,
    ):
        """New dtypeDecorator."""
        self = super().__new__(cls)  # making instance of self

        # correcting if forgot to specify in_dtype and no function
        # in this case, *in_dtype* is stored in *func*
        # need to do func->None, inarags<-func, and out_dtype<-in_dtype
        if not isinstance(func, Callable):
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

    def __init__(self, in_dtype: Any = None, out_dtype: Any = None) -> None:
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

    def __call__(self, wrapped_func: Callable) -> Callable:
        """Make Decorator.

        Parameters
        ----------
        wrapped_func: Callable
            function to be wrapped

        """

        @functools.wraps(wrapped_func)
        def wrapper(*args: Any, **kw: Any) -> Any:
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


#############################################################################
# SINGLE-DECORATOR FACTORY


def dtypeDecoratorMaker(dtype: Any):
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
    # define class
    class dtypeDecorator:
        """Ensure arguments are type `dtype`.

        Parameters
        ----------
        func : function, optional
            function to decorate
        inargs : 'all' or iterable or slice or tuple, optional
            - None (default), does nothing
            - 'all': converts all arguments to dtype
            - iterable: convert arguments at index speficied in iterable
                ex: [0, 2] converts arguments 0 & 2
            - slice: convert all arguments specified by slicer
        outargs : 'all' or iterable or tuple or slice
            - None (default), does nothing
            - 'all': converts all arguments to dtype
            - iterable: convert arguments at index speficied in iterable
                ex: [0, 2] converts arguments 0 & 2
            - slice: convert all arguments specified by slicer

        these arguments, except func, should be specified by key word
        if inargs is forgotten and func is not a function, then func is
        assumed to be inargs.

        Examples
        --------
        >>> intDecorator = dtypeDecoratorMaker(int)
        >>> @intDecorator(inargs=[0, 1], outargs=2)
        ... def func(x, y, z):
        ...     return x, y, z, (x, y, z)
        ... # /def
        >>> x, y, z, orig = func(1.1, 2.2, 3.3)
        >>> print(x, y, z, orig)
        1 2 3 (1, 2, 3.3)

        """

        def __new__(
            cls,
            func: Callable = None,
            inargs: Union[Literal["all"], slice, Iterable] = None,
            outargs: Union[Literal["all"], slice, Iterable] = None,
        ):
            """__new__."""
            self = super().__new__(cls)  # making instance of self

            # correcting if forgot to specify inargs and did not provide a func
            # in this case, *inargs* is stored in *func*
            # need to do func->None, inarags<-func, and outargs<-inargs
            if not isinstance(func, Callable):
                # moving arguments 'forward'
                outargs = inargs
                inargs = func
                func = None

            # allowing for wrapping with calling the class
            if func is not None:
                self.__init__(inargs, outargs)
                return self(func)
            else:
                return self

        # /def

        def __init__(
            self,
            inargs: Union[Literal["all"], slice, Iterable] = None,
            outargs: Union[Literal["all"], slice, Iterable] = None,
        ) -> None:
            super().__init__()

            # data type
            self._dtype = dtype  # getting from outside
            if dtype is None:  # dtype is kept as-is
                self.dtype = lambda x: x

            # inargs
            if inargs == "all":
                self._inargs = slice(None)
            else:
                self._inargs = inargs

            # outargs
            if outargs == "all":
                self._outargs = slice(None)
            elif np.isscalar(outargs):
                self._outargs = [outargs]
            else:
                self._outargs = outargs

        # /def

        def __call__(self, wrapped_func: Callable) -> Callable:
            # print(self._inargs)

            @functools.wraps(wrapped_func)
            def wrapper(*args: Any, **kw: Any) -> Any:

                args = list(args)  # allowing modifications

                # PRE
                # making arguments self._dtype
                if self._inargs is None:  # no conversion needed
                    pass
                elif isinstance(self._inargs, slice):
                    # converting inargs to list of indices
                    inargs = list(range(len(args)))[self._inargs]
                    for i in inargs:
                        # converting to desired dtype
                        args[i] = self._dtype(args[i])
                else:
                    for i in self._inargs:
                        # converting to desired dtype
                        args[i] = self._dtype(args[i])
                # /PRE

                # CALLING
                return_ = wrapped_func(*args, **kw)
                # /CALLING

                # POST
                if self._outargs is None:  # no conversion needed
                    return return_
                else:
                    try:  # figure out whether return_ is a scalar or list
                        return_[0]
                    except IndexError:  # scalar output
                        inds = np.arange(len(args), dtype=self._dtype)[
                            self._outargs
                        ]
                        if inds == 0:
                            return self._dtype(return_)
                        else:  # inds doesn't match return_
                            raise ValueError
                    else:
                        return_ = list(return_)
                        inds = np.arange(len(args), dtype=self._dtype)[
                            self._outargs
                        ]
                        for i in inds:
                            return_[i] = self._dtype(return_[i])

                    return return_
                # /POST
                # /def

            return wrapper

        # /def

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
