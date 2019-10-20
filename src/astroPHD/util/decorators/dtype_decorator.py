#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : decorators
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""decorators

TODO for dtypeDecorator
-----------------------
support argument 'all' in [(index, dtype),] as the IndexError
supoort single argumens so that (index, dtype) works w/out [(), ]
full support of numpy.dtype
add in_dtype and out_dtype kwargs to wrapped functions which override
    defaults
"""

__all__ = [
    'dtypeDecorator',
    'dtypeDecoratorMaker',
    # built-in types
    'boolDecorator',
    'intDecorator', 'floatDecorator',
    'strDecorator',
    # numpy types
    'ndarrayDecorator',
    'ndfloat64Decorator',
]


##############################################################################
### IMPORTS

## General
import numpy as np
import types

try:
    from astropy.utils.decorators import wraps
except ImportError as e:
    print("could not import wraps from astropy. using functools' instead")
    from functools import wraps


#############################################################################
# MAKING DECORATORS

class dtypeDecorator():
    """ensure arguments are type *dtype*

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

    Examples
    --------
    intDecorator = dtypeDecoratorMaker(int)
    @intDecorator(inargs=[(0, int), (1, float)], outargs=[(2, int),])
    def func(x, y, z):
        print(x, y, z)
        return x, y, z
    # /def

    x, y, z = func(1.1, 2.2, 3.3)
    >>> 1, 2.2, 3.3  # x -> int, y, z remain float within the function
    print(z, y, z)  # z->int before returned
    >>> 1, 2.2, 3
    """

    def __new__(cls, func=None, in_dtype=None, out_dtype=None):
        """"""
        self = super().__new__(cls)  # making instance of self

        # correcting if forgot to specify in_dtype= and did not provide a function
        # in this case, *in_dtype* is stored in *func*
        # need to do func->None, inarags<-func, and out_dtype<-in_dtype
        if not isinstance(func, types.FunctionType):
            # moving arguments 'forward'
            out_dtype = in_dtype
            in_dtype = func
            func = None

        # allowing for wrapping with calling the class
        if func is not None:
            self.__init__(in_dtype, out_dtype)
            return self(func)
        else:
            return self
    # /def

    def __init__(self, in_dtype=None, out_dtype=None):
        super().__init__()

        # in_dtype
        # TODO check in_dtype is list of lists
        self._in_dtype = in_dtype

        # out_dtype
        # TODO check out_dtype is list of lists
        self._out_dtype = out_dtype

        return
    # /def

    def __call__(self, wrapped_func):
        # print(self._in_dtype)

        @wraps(wrapped_func)
        def wrapper(*args, **kw):
            # making arguments self._dtype
            if self._in_dtype is None:  # no conversion needed
                return_ = wrapped_func(*args, **kw)
            elif len(args) == 0:
                return_ = wrapped_func(**kw)
            elif len(args) == 1:
                if len(self._in_dtype) != 1 or self._in_dtype[0][0] != 0:  # TODO better
                    raise IndexError('too many indices')
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
                        return_[i] = dtype(return_[i])  # converting to desired dtype
                else:
                    if len(self._out_dtype) != 1:  # TODO do this check?
                        raise ValueError('out_dtype has too many indices')
                    return_ = self._out_dtype[0][1](return_)

            return return_
            # /POST
            # /def
        return wrapper
    # /def


#############################################################################
### SINGLE-DECORATOR FACTORY

def dtypeDecoratorMaker(dtype):
    """function to make a dtype decorator

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
    intDecorator = dtypeDecoratorMaker(int)
    @intDecorator(inargs=[0, 1], outargs=[2,])
    def func(x, y, z):
        print(x, y, z)
        return x, y, z
    # /def

    x, y, z = func(1.1, 2.2, 3.3)
    >>> 1, 2, 3.3  # x,y -> int, z remains float within the function
    print(z, y, z)  # z->int before returned
    >>> 1, 2, 3
    """

    class dtypeDecorator():
        """ensure arguments are type *dtype*

        Parameters
        ----------
        func : function, optional
            function to decorate
        inargs : 'all', iterable, or slice, optional
            - None (default), does nothing
            - 'all': converts all arguments to dtype
            - iterable: convert arguments at index speficied in iterable
                ex: [0, 2] converts arguments 0 & 2
            - slice: convert all arguments specified by slicer

        outargs : 'all', iterable, or slice
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
        intDecorator = dtypeDecoratorMaker(int)
        @intDecorator(inargs=[0, 1], outargs=[2,])
        def func(x, y, z):
            print(x, y, z)
            return x, y, z
        # /def

        x, y, z = func(1.1, 2.2, 3.3)
        >>> 1, 2, 3.3  # x,y -> int, z remains float within the function
        print(z, y, z)  # z->int before returned
        >>> 1, 2, 3
        """

        def __new__(cls, func=None, inargs=None, outargs=None):
            """"""
            self = super().__new__(cls)  # making instance of self

            # correcting if forgot to specify inargs= and did not provide a function
            # in this case, *inargs* is stored in *func*
            # need to do func->None, inarags<-func, and outargs<-inargs
            if not isinstance(func, types.FunctionType):
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

        def __init__(self, inargs=None, outargs=None):
            super().__init__()

            # data type
            self._dtype = dtype  # getting from outside
            if dtype is None:  # dtype is kept as-is
                self.dtype = lambda x: x

            # inargs
            self._inargs = inargs
            if inargs == 'all':
                self._inargs = slice(None)

            # outargs
            self._outargs = outargs
            if outargs == 'all':
                self._outargs = slice(None)
            if np.isscalar(self._outargs):
                self._outargs = [self._outargs, ]
        # /def

        def __call__(self, wrapped_func):
            # print(self._inargs)

            @wraps(wrapped_func)
            def wrapper(*args, **kw):

                args = list(args)  # allowing modifications

                # PRE
                # making arguments self._dtype
                if self._inargs is None:  # no conversion needed
                    pass
                elif isinstance(self._inargs, slice):
                    # converting inargs to list of indices
                    inargs = list(range(len(args)))[self._inargs]
                    for i in inargs:
                        args[i] = self._dtype(args[i])  # converting to desired dtype
                else:
                    for i in self._inargs:
                        args[i] = self._dtype(args[i])  # converting to desired dtype
                # /PRE

                # CALLING
                return_ = wrapped_func(*args, **kw)
                # /CALLING

                # POST
                if self._outargs is None:  # no conversion needed
                    return return_
                else:
                    try:  # need to figure out whether return_ is a scalar or a list
                        return_[0]
                    except IndexError:  # scalar output
                        inds = np.arange(len(args), dtype=self._dtype)[self._outargs]
                        if inds == 0:
                            return self._dtype(return_)
                        else:  # inds doesn't match return_
                            raise ValueError
                    else:
                        return_ = list(return_)
                        inds = np.arange(len(args), dtype=self._dtype)[self._outargs]
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
