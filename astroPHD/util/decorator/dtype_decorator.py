#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : decorators
# AUTHOR  : Nathaniel Starkman
# PROJECT : AST1500
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""decorators
"""

__author__ = "Nathaniel Starkman"
__all__ = [
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

        # inargs
        # TODO check inargs is list of lists
        self._inargs = inargs

        # outargs
        # TODO check outargs is list of lists
        self._outargs = outargs

        return
    # /def

    def __call__(self, wrapped_func):
        # print(self._inargs)

        @wraps(wrapped_func)
        def wrapper(*args, **kw):
            # PRE
            # making arguments self._dtype
            if self._inargs is None:  # no conversion needed
                pass
            else:
                args = list(args)  # allowing modifications
                for i, dtype in self._inargs:
                    args[i] = dtype(args[i])  # converting to desired dtype
            # /PRE

            # CALLING
            return_ = wrapped_func(*args, **kw)
            # /CALLING

            # POST
            if self._outargs is None:  # no conversion needed
                pass
            else:
                return_ = list(return_)  # allowing modifications
                for i, dtype in self._outargs:
                    return_[i] = dtype(return_[i])  # converting to desired dtype

                return return_
            # /POST
            # /def
        return wrapper
    # /def

#############################################################################
### SINGLE-DECORATOR MAKER

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
