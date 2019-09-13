#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""

#############################################################################

Copyright (c) 2018 - Nathaniel Starkman
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  The name of the author may not be used to endorse or promote products
     derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

#############################################################################
Planned Features
"""

#############################################################################
# Imports

import inspect
from warnings import warn

# 3rd Party Imports
from astropy.units import Unit, dimensionless_unscaled
from astropy.units.decorators import _validate_arg_value, _get_allowed_units
from astropy.units.core import add_enabled_equivalencies
from astropy.units.physical import _unit_physical_mapping

from astropy.utils.decorators import wraps
from astropy.utils.misc import isiterable

#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2018, "
__credits__ = [""]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"


###############################################################################
# Helper Functions

def unit_helper(res, unit=None, to_value=False,
                equivalencies=[], decompose=False):
    r"""helper function for return of Quantities
    ex: How to apply in a function directly
        def func(*args, **kw):
            result = do stuff
            return unit_helper(result,
                               unit=kw.get('unit', None),
                               to_value=kw.get('to_value', False),
                               equivalencies=kw.get('equivalencies', []),
                               decompose=kw.get('decompose', [])
                               )


    Arguments
    ----------
    res: Quantity
        the result
    unit: Astropy Unit
        sets the unit for the returned res
        if None, returns res unchanged, unless to_value is used
        if '', decomposes
    to_value: bool
        whether to return .to_value(unit)
        see Astropy.units.Quantity.to_value
    equivalencies: list
        equivalencies for .to() and .to_value()
        only used if `unit' to `to_value' are not None/False
    decompose: bool, list
        if bool:
            True, False for decomposing
        if list:
            bases for .decompose(bases=[])
            will first decompose, then apply unit, to_value, equivalencies
        Decomposing then converting wastes time, since .to(unit, equivalencies) internally does conversions
        the only use for combining decompose with other unit_helper params is with:
            unit=None, to_value=True, equivalencies=[], decompose=`bool or [user bases here]'
            since this will dcompose to desired bases then return the value in those bases
        ** experimental feature
            for things which are not (u.Unit, u.core.IrreducibleUnit), tries wrapping in Unit()
            this allows things such as:
                x = 5 * u.kpc * u.s
                bases = [2 * u.lyr, u.s]
                x.decompose(bases=basesConversionFunction(bases))
            this would normally return an error

    Returns
    -------
    res: function output
        function output, converted / decomposed / evaluated to desired units

    Exceptions
    ----------
    ValueError: if unit not astropy compatible
    UnitConversionError: if conversion not legit
    ...
    """

    # fast check to do nothing
    if (unit is None) & (to_value is False) & (equivalencies == []) & (decompose is False):
        return res

    # First decomposing
    if decompose is True:
        res = res.decompose()
    elif decompose:  # decompose is NOT empty list
        cls = (Unit, u.core.IrreducibleUnit)
        bases = [Unit(x) if not issubclass(x.__class__, cls) else x
                 for x in decompose]
        res = res.decompose(bases=bases)
    # else:  # decompose is False or empty list
    #    pass

    # Now Converting
    if (unit is None) and (to_value is False):  # nothing required
        return res
    elif to_value is True:  # return value
        return res.to_value(unit, equivalencies)
    else:  # return with unit
        return res.to(unit, equivalencies)


def _simple_unit_decorator(unit=None, to_value=False,
                           equivalencies=[], decompose=False):
    r"""Decorator for unit_helper
    Any wrapped function accepts the additional key-word arguments:
        unit, to_value, equivalencies, decompose
        see `Wrapped-Arguments' for details

     ex:
        @unit_decorator
        def func(*args, **kw):
            result = do stuff
            return result

        is equivalent to

        def func(*args, unit=None, to_value=False, equivalencies=[], decompose=False, **kw):
            result = do stuff w/ *args, and **kw
            return unit_helper(result, unit, to_value, equivalencies, decompose)

    Wrapped-Arguments
    -----------------
    If provided to the decorator (ex: @unit_decorator(unit=`unit')),
        then `unit' becomes the default value
    If provided when calling the function (ex: myfunc(*args, **kwargs, unit=`unit')),
        this unit is used in the conversion

    unit: Astropy Unit
        sets the unit for the returned res
        if None, returns res unchanged, unless to_value is used
        if '', decomposes
    to_value: bool
        whether to return .to_value(unit)
        see Astropy.units.Quantity.to_value
    equivalencies: list
        equivalencies for .to() and .to_value()
        only used if `unit' to `to_value' are not None/False
    decompose: bool, list
        if bool:
            True, False for decomposing
        if list:
            bases for .decompose(bases=[])
            will first decompose, then apply unit, to_value, equivalencies
        Decomposing then converting wastes time, since .to(unit, equivalencies) internally does conversions
        the only use for combining decompose with other unit_helper params is with:
            unit=None, to_value=True, equivalencies=[], decompose=`bool or [user bases here]'
            since this will dcompose to desired bases then return the value in those bases
        ** experimental feature
            for things which are not (u.Unit, u.core.IrreducibleUnit), tries wrapping in Unit()
            this allows things such as:
                x = 5 * u.kpc * u.s
                bases = [2 * u.lyr, u.s]
                x.decompose(bases=basesConversionFunction(bases))
            this would normally return an error

    Returns
    -------
    res: function result
        result of wrapped function, with the unit operations performed by unit_helper
    """

    def wrapper(func):
        @wraps(func)
        def wrapped(*args,
                    unit=unit, to_value=to_value,
                    equivalencies=equivalencies, decompose=decompose,
                    **kw):

            # evaluated function
            res = func(*args, **kw)

            return unit_helper(res, unit=unit, to_value=to_value,
                               equivalencies=equivalencies, decompose=decompose)

        return wrapped
    return wrapper


_aioattrs = ('unit', 'to_value', 'equivalencies', 'decompose',
             'default_units', 'annot2dfu')


class QuantityInputOutput(object):
    r"""A decorator for validating the units of arguments to functions.

    **function must allow kwargs**

    Order of Precedence:
    - Function Arguments
    - Decorator Arguments
    - Function Annotation Arguments

    Function Arguments
    ------------------
    See `decorator argument' section
    function arguments override decorator & function annotation arguments

    *func_args: function arguments
    unit
    to_value
    equivalencies
    decompose
    default_units
    **func_kwargs: function key-word argument

    Decorator Arguments
    -------------------
    arguments to the decorator take LOWER precedence
    than arguments to the function itself.

    func: function
        the function to decorate
        default: None
    unit: astropy Unit / Quantity or str  (default None)
        sets the unit for the function evaluation
        default: {unit}
        must be astropy-compatible unit specification
        equivalent to func(*args, **kw).to(unit)
        if None, skips unit conversion
    to_value: bool
        whether to return .to_value(unit)
        default: {to_value}
        see Astropy.units.Quantity.to_value
    equivalencies: list
        equivalencies for any units provided
        default: {equivalencies}
        used by .to() and .to_value()
    decompose: bool, list
        unit decomposition
        default: {decompose}
        if bool:
            True, False for decomposing
        if list:
            bases for .decompose(bases=[])
            will first decompose, then apply unit, to_value, equivalencies
        Decomposing then converting wastes time, since .to(unit, equivalencies) internally does conversions
        the only use for combining decompose with other unit_helper params is with:
            unit=None, to_value=True, equivalencies=[], decompose=`bool or [user bases here]'
            since this will dcompose to desired bases then return the value in those bases
        ** experimental feature
            for things which are not (u.Unit, u.core.IrreducibleUnit), tries wrapping in Unit()
            this allows things such as:
                x = 10 * u.km * u.s
                bases = [2 * u.km, u.s]
                x.decompose(bases=basesConversionFunction(bases))
                >> 5  2 km s
            (this would normally return an error)
    default_units: dict
        dictionary of default units
        default: {default_units}
        ex: dict(x=u.km)
            for func(x, y)
            if x has no units, it is assumed to be in u.km
    annot2dfu: bool (default False)
        whether to interpret function annotations as default units
        function annotations have lower precedence than *default_units*
        default: {annot2dfu}


    Decorator Key-Word Arguments
    ----------------------------
    Unit specifications can be provided as keyword arguments
    to the decorator, or by using function annotation syntax.
    Arguments to the decorator take precedence
    over any function annotations present.
    **note**
    decorator key-word arguments are NEVER interpreted as *default_units*

    ex:
        @quantity_io(x=u.m, y=u.s)
        def func(x, y):
            ...

    Function Annotation Arguments
    -----------------------------
    Unit specifications can be provided as keyword arguments
    to the decorator, or by using function annotation syntax.
    Arguments to the function and decorator take precedence
    over any function annotations present.

    ex:
        def func(x: u.m, y: u.s) -> u.m / u.s:
            ...

    if annot2dfu is True (default False)
        function annotations are interpreted as default units
        function annotations have lower precedence than *default_units*


    Examples
    --------
    # Simple Example
    @quantity_io()
    def func(x: 'km', **kw) -> 2 * u.m:
        return x

    passing the wrong/no units doesn't work
    >   func(2000 * u.s)
    >       >> UnitConversionError
    >   func(2000)
    >       >> AttributeError
    the distance is internally converted
    >   func(2000 * u.m)
    >       >> 1000.0 2 m
    function annotation is superceded by an argument
    >   func(2000 * u.m, unit=2 * u.km)
    >       >> 1.0 2 km
    >   func(2000 * u.m, unit=2 * u.km, to_value=True)
    >       >> 1.0


    # More Complex Example
    this function only accepts
        x arguments of type 'length'
        t arguments of type 'time'
    annotations are assumed to be also be default_units
    @quantity_io(x='length', annot2dfu=True,
                 default_units=dict(t=u.s))
    def func(x: 'km', t, **kw) -> 2 * u.m / u.s:
        return x * t

    arguments have implicit units
    >   func(2, 2)
    >       >> 500.0 2 m / s
    decorator & annotation supersceded by an argument
    >   func(2, 2 * u.ms, unit=2 * u.km / s)
    >       >> 500.0 2 km / s

    print(func(2, 2))
    print(func(2, 2, unit=2 * u.km / u.s))
    """

    __name__ = 'QuantityInputOutput'

    @classmethod
    def as_decorator(cls, func=None, unit=None, to_value=False,
                     equivalencies=[], decompose=False,
                     default_units={}, annot2dfu=False,
                     **decorator_kwargs):
        r"""
        A decorator for validating the units of arguments to functions.

        **function must allow kwargs**

        Order of Precedence:
        - Function Arguments
        - Decorator Arguments
        - Function Annotation Arguments

        Function Arguments
        ------------------
        See `decorator argument' section
        function arguments override decorator & function annotation arguments

        *func_args: function arguments
        unit
        to_value
        equivalencies
        decompose
        default_units
        **func_kwargs: function key-word argument

        Decorator Arguments
        -------------------
        arguments to the decorator take LOWER precedence
        than arguments to the function itself.

        func: function
            the function to decorate
        unit: astropy Unit / Quantity or str  (default None)
            sets the unit for the function evaluation
            must be astropy-compatible unit specification
            equivalent to func(*args, **kw).to(unit)
            if None, skips unit conversion
        to_value: bool  (default False)
            whether to return .to_value(unit)
            see Astropy.units.Quantity.to_value
        equivalencies: list  (default [])
            equivalencies for any units provided
            used by .to() and .to_value()
        decompose: bool, list  (default [])
            if bool:
                True, False for decomposing
            if list:
                bases for .decompose(bases=[])
                will first decompose, then apply unit, to_value, equivalencies
            Decomposing then converting wastes time, since .to(unit, equivalencies) internally does conversions
            the only use for combining decompose with other unit_helper params is with:
                unit=None, to_value=True, equivalencies=[], decompose=`bool or [user bases here]'
                since this will dcompose to desired bases then return the value in those bases
            ** experimental feature
                for things which are not (u.Unit, u.core.IrreducibleUnit), tries wrapping in Unit()
                this allows things such as:
                    x = 10 * u.km * u.s
                    bases = [2 * u.km, u.s]
                    x.decompose(bases=basesConversionFunction(bases))
                    >> 5  2 km s
                (this would normally return an error)
        default_units: dict  (default {})
            dictionary of default units
            ex: {x: u.km}
                for func(x, y)
                if x has no units, it is assumed to be in u.km
        annot2dfu: bool (default False)
            whether to interpret function annotations as default units
            function annotations have lower precedence than {default_units}


        Decorator Key-Word Arguments
        ----------------------------
        Unit specifications can be provided as keyword arguments
        to the decorator, or by using function annotation syntax.
        Arguments to the decorator take precedence
        over any function annotations present.
        **note**
        decorator key-word arguments are NEVER interpreted as {default_units}

        ex:
            @quantity_io(x=u.m, y=u.s)
            def func(x, y):
                ...

        Function Annotation Arguments
        -----------------------------
        Unit specifications can be provided as keyword arguments
        to the decorator, or by using function annotation syntax.
        Arguments to the function and decorator take precedence
        over any function annotations present.

        ex:
            def func(x: u.m, y: u.s) -> u.m / u.s:
                ...

        if annot2dfu is True (default False)
            function annotations are interpreted as default units
            function annotations have lower precedence than {default_units}


        Examples
        --------
        # Simple Example
        @quantity_io()
        def func(x: 'km', **kw) -> 2 * u.m:
            return x

        passing the wrong/no units doesn't work
        >   func(2000 * u.s)
        >       >> UnitConversionError
        >   func(2000)
        >       >> AttributeError
        the distance is internally converted
        >   func(2000 * u.m)
        >       >> 1000.0 2 m
        function annotation is superceded by an argument
        >   func(2000 * u.m, unit=2 * u.km)
        >       >> 1.0 2 km
        >   func(2000 * u.m, unit=2 * u.km, to_value=True)
        >       >> 1.0


        # More Complex Example
        this function only accepts
            x arguments of type 'length'
            t arguments of type 'time'
        annotations are assumed to be also be default_units
        @quantity_io(x='length', annot2dfu=True,
                     default_units={'t': u.s})
        def func(x: 'km', t, **kw) -> 2 * u.m / u.s:
            return x * t

        arguments have implicit units
        >   func(2, 2)
        >       >> 500.0 2 m / s
        decorator & annotation supersceded by an argument
        >   func(2, 2 * u.ms, unit=2 * u.km / s)
        >       >> 500.0 2 km / s

        print(func(2, 2))
        print(func(2, 2, unit=2 * u.km / u.s))
        """
        # making instance from base class
        self = super(QuantityInputOutput, cls).__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            # classname=func.__repr__() if func is not None else 'SideHists',
            **{k: _locals.get(k).__repr__() for k in set(_aioattrs)})

        self.__init__(unit=unit, to_value=to_value,
                      equivalencies=equivalencies, decompose=decompose,
                      default_units=default_units, annot2dfu=annot2dfu,
                      **decorator_kwargs
        )

        if func is not None:
            return self(func)
        else:
            return self

    def __init__(self, func=None, unit=None, to_value=False,
                 equivalencies=[], decompose=False,
                 default_units={}, annot2dfu=False,
                 **decorator_kwargs):

        super().__init__()

        self.unit = unit
        self.to_value = to_value
        self.equivalencies = equivalencies
        self.decompose = decompose

        self.default_units = default_units
        self.annot2dfu = annot2dfu

        self.decorator_kwargs = decorator_kwargs

    def __call__(self, wrapped_function):

        # Extract the function signature for the function we are wrapping.
        wrapped_signature = inspect.signature(wrapped_function)

        @wraps(wrapped_function)
        def wrapped(*func_args,
                    unit=self.unit, to_value=self.to_value,
                    equivalencies=self.equivalencies, decompose=self.decompose,
                    default_units=self.default_units,
                    **func_kwargs):

            # make func_args editable
            func_args = list(func_args)

            # Bind the arguments to our new function to the signature of the original.
            bound_args = wrapped_signature.bind(*func_args, **func_kwargs)

            # Iterate through the parameters of the original signature
            for i, param in enumerate(wrapped_signature.parameters.values()):
                # We do not support variable arguments (*args, **kwargs)
                if param.kind in (inspect.Parameter.VAR_KEYWORD,
                                  inspect.Parameter.VAR_POSITIONAL):
                    continue

                # Catch the (never triggered) case where bind relied on a default value.
                if param.name not in bound_args.arguments and param.default is not param.empty:
                    bound_args.arguments[param.name] = param.default

                # Get the value of this parameter (argument to new function)
                arg = bound_args.arguments[param.name]

                # +----------------------------------+
                # Get default unit or physical type, either from decorator kwargs
                #   or annotations
                if param.name in default_units:
                    dfunit = default_units[param.name]
                elif self.annot2dfu is True:
                    dfunit = param.annotation
                # elif not default_units:
                #     dfunit = param.annotation
                else:
                    dfunit = inspect.Parameter.empty

                adjargbydfunit = True

                # If the dfunit is empty, then no target units or physical
                #   types were specified so we can continue to the next arg
                if dfunit is inspect.Parameter.empty:
                    adjargbydfunit = False

                # If the argument value is None, and the default value is None,
                #   pass through the None even if there is a dfunit unit
                elif arg is None and param.default is None:
                    adjargbydfunit = False

                # Here, we check whether multiple dfunit unit/physical type's
                #   were specified in the decorator/annotation, or whether a
                #   single string (unit or physical type) or a Unit object was
                #   specified
                elif isinstance(dfunit, str):
                    dfunit = _get_allowed_units([dfunit])[0]
                elif not isiterable(dfunit):
                    pass
                else:
                    raise ValueError('target must be one Unit, not list')

                if (not hasattr(arg, 'unit')) & (adjargbydfunit is True):
                    if i < len(func_args):
                        # print(i, len(bound_args.args))
                        func_args[i] *= dfunit
                    else:
                        func_kwargs[param.name] *= dfunit
                    arg *= dfunit

                # +----------------------------------+
                # Get target unit or physical type, either from decorator kwargs
                #   or annotations
                if param.name in self.decorator_kwargs:
                    targets = self.decorator_kwargs[param.name]
                else:
                    targets = param.annotation

                # If the targets is empty, then no target units or physical
                #   types were specified so we can continue to the next arg
                if targets is inspect.Parameter.empty:
                    continue

                # If the argument value is None, and the default value is None,
                #   pass through the None even if there is a target unit
                if arg is None and param.default is None:
                    continue

                # Here, we check whether multiple target unit/physical type's
                #   were specified in the decorator/annotation, or whether a
                #   single string (unit or physical type) or a Unit object was
                #   specified
                if isinstance(targets, str) or not isiterable(targets):
                    valid_targets = [targets]

                # Check for None in the supplied list of allowed units and, if
                #   present and the passed value is also None, ignore.
                elif None in targets:
                    if arg is None:
                        continue
                    else:
                        valid_targets = [t for t in targets if t is not None]

                    if not hasattr(arg, 'unit'):
                        arg = arg * dimensionless_unscaled
                        valid_targets.append(dimensionless_unscaled)

                else:
                    valid_targets = targets

                # Now we loop over the allowed units/physical types and validate
                #   the value of the argument:
                _validate_arg_value(param.name, wrapped_function.__name__,
                                    arg, valid_targets, self.equivalencies)

            # # evaluated wrapped_function
            with add_enabled_equivalencies(equivalencies):
                return_ = wrapped_function(*func_args, **func_kwargs)
                # if func_kwargs:
                #     return_ = wrapped_function(*func_args, **func_kwargs)
                # else:
                #     return_ = wrapped_function(*func_args)

            if wrapped_signature.return_annotation not in (inspect.Signature.empty, None) and unit is None:
                unit = wrapped_signature.return_annotation

            return unit_helper(return_, unit=unit, to_value=to_value,
                               equivalencies=equivalencies,
                               decompose=decompose)

        # TODO dedent
        wrapped.__doc__ = (wrapped.__doc__ or '') + _funcdec

        # /def
        return wrapped
    # /def


###############################################################################

_funcdec = r"""\n\n\tDecorator Docstring\n\t-------------------
        A decorator for validating the units of arguments to functions.

        **function must allow kwargs**

        Decorator-Added Function Key-Word Arguments
        -------------------------------------------
        function arguments override decorator & function annotation arguments

        unit: astropy Unit / Quantity or str  (default None)
            sets the unit for the function evaluation
            must be astropy-compatible unit specification
            equivalent to func(*args, **kw).to(unit)
            if None, skips unit conversion
        to_value: bool  (default False)
            whether to return .to_value(unit)
            see Astropy.units.Quantity.to_value
        equivalencies: list  (default [])
            equivalencies for any units provided
            used by .to() and .to_value()
        decompose: bool, list  (default [])
            if bool:
                True, False for decomposing
            if list:
                bases for .decompose(bases=[])
                will first decompose, then apply unit, to_value, equivalencies
            Decomposing then converting wastes time, since .to(unit, equivalencies) internally does conversions
            the only use for combining decompose with other unit_helper params is with:
                unit=None, to_value=True, equivalencies=[], decompose=`bool or [user bases here]'
                since this will dcompose to desired bases then return the value in those bases
            ** experimental feature
                for things which are not (u.Unit, u.core.IrreducibleUnit), tries wrapping in Unit()
                this allows things such as:
                    x = 10 * u.km * u.s
                    bases = [2 * u.km, u.s]
                    x.decompose(bases=basesConversionFunction(bases))
                    >> 5  2 km s
                (this would normally return an error)
        default_units: dict  (default {})
            dictionary of default units
            ex: {x: u.km}
                for func(x, y)
                if x has no units, it is assumed to be in u.km
"""


###############################################################################

# unit_decorator = UnitDecorator.as_decorator
quantity_io = QuantityInputOutput.as_decorator


###############################################################################

if __name__ == '__main__':

    # @u.quantity_input(distance='length')
    # @quantity_io(unit=u.m**2, distance=('length', None))
    # @quantity_io(unit=u.m**2, default_units={'distance2': u.kpc})
    # def testfunc(distance: 'kpc', distance2: 'm', extra=None, **kw):

    #     return distance * distance2

    # print(testfunc(2 * u.pc, 2, test=4))
    # print(testfunc(2 * u.Hz))
    from astropy import units as u

    @quantity_io()
    def func(dist: 'km', **kw) -> 2 * u.m:
        return dist
    print(func(2 * u.km))
    # print(func(2000 * u.m))
    # # print(func(2000 * u.s))
    # print(func(2000 * u.m, unit=2 * u.km))


    @quantity_io(x='length', annot2dfu=True,
                default_units={'t': u.s})
    def func(x: 'km', t, **kw) -> 2 * u.m / u.s:
        r"""test
        """
        return x / t

    print(func(2, 2))
    print(func(2, 2 * u.ms, unit=2 * u.km / u.s))
    # print(func(2000 * u.m))
    # # print(func(2000 * u.s))
    # print(func(2000 * u.m, unit=2 * u.km))

    # +------------------------------+
    @quantity_io(annot2dfu=True)
    # @QuantityInputOutput()
    # @simple_unit_decorator()
    # @quantityIO()
    def returndistance(distance: 'km', **kw) -> 2 * u.m:
        return distance

    print(returndistance(2 * u.kpc))
    # print(returndistance(2, unit=u.m, to_value=True)
