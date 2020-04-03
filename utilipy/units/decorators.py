# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : unit decorators
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Decorators for functions acceptingAstropy Quantities."""

__author__ = "Nathaniel Starkman"
__credit__ = "astropy"


__all__ = ["unit_output_decorator", "QuantityInputOutput", "quantity_io"]


##############################################################################
# IMPORTS

# GENERAL
from typing import Any, Union, Sequence, Callable
import inspect

# from warnings import warn

from astropy.units import dimensionless_unscaled
from astropy.units.decorators import _validate_arg_value, _get_allowed_units
from astropy.units.core import Unit, add_enabled_equivalencies
from astropy.utils.misc import isiterable

# PROJECT-SPECIFIC
from .util import unit_output
from ..decorators.docstring import format_doc
from ..utils.functools import wraps

###############################################################################
# PARAMETERS

_aioattrs = (
    "unit",
    "to_value",
    "equivalencies",
    "decompose",
    "assumed_units",
    "assume_annotation_units",
)


###############################################################################
# CODE


def unit_output_decorator(
    unit: Unit = None,
    to_value: bool = False,
    equivalencies: Sequence = [],
    decompose: Union[bool, Sequence] = False,
):
    r"""Decorate functions for unit output.

    Any wrapped function accepts the additional key-word arguments:
        ``unit``, ``to_value``, ``equivalencies``, ``decompose``

    If provided to the decorator (ex: ``@unit_decorator(unit=unit)``),
        then `unit` becomes the default value
    If provided when calling the function (ex: ``myfunc(*args, **kwargs, unit=unit)``),
        this unit is used in the conversion

    Parameters
    ----------
    unit: Unit, optional
        sets the unit for the returned `res`
        if None, returns `res` unchanged, unless `to_value` is used
        if '', decomposes
    to_value: bool, optional
        whether to return ``.to_value(unit)``
        see Astropy.units.Quantity.to_value
    equivalencies: list, optional
        equivalencies for ``.to()`` and ``.to_value()``
        only used if `unit' to `to_value` are not None/False
    decompose: bool or list, optional
        unit decomposition
        default, False

        * bool: True, False for decomposing.
        * list: bases for ``.decompose(bases=[])``

            will first decompose, then apply ``unit``, ``to_value``, ``equivalencies``

        Decomposing then converting wastes time, since
        ``.to(unit, equivalencies)`` internally does conversions.
        The only use for combining decompose with other `unit_output`
        parameters is with::

            unit=None, to_value=True, equivalencies=[], decompose=`bool or [user bases here]'
            since this will decompose to desired bases then return the value in those bases

        .. note::

            **experimental feature:**
            for things which are not (astropy.unit.Unit, astropy.unit.core.IrreducibleUnit),
            tries wrapping in ``Unit()``. This would normally return an error, but now
            allows for conversions such as:

            >>> x = 10 * u.km * u.s
            >>> bases = [u.Unit(2 * u.km), u.s]
            >>> x.decompose(bases=bases) # doctest: +SKIP
            <Quantity 5.0 2 km s>

    Returns
    -------
    res: function result
        result of wrapped function, with the unit operations performed by unit_output

    Examples
    --------
    .. code-block:: python

        @unit_decorator
        def func(x, y, **kw):
            return x + y

    is equivalent to

    .. code-block:: python

        def func(x, y, unit=None, to_value=False, equivalencies=[],
                 decompose=False, **kw):
            result = x + y
            return unit_output(result, unit, to_value, equivalencies,
                               decompose)

    """

    def wrapper(func: Callable):
        @wraps(func)
        def wrapped(
            *args: Any,
            unit: Unit = unit,
            to_value: bool = to_value,
            equivalencies: Sequence = equivalencies,
            decompose: Union[bool, Sequence] = decompose,
            **kw: Any
        ):

            # evaluated function
            res = func(*args, **kw)

            return unit_output(
                res,
                unit=unit,
                to_value=to_value,
                equivalencies=equivalencies,
                decompose=decompose,
            )

        return wrapped

    return wrapper


# /def


###############################################################################


class QuantityInputOutput(object):
    r"""A decorator for validating the units of arguments to functions.

    Parameters
    ----------
    func: function
        the function to decorate
        (default None)
    unit: astropy Unit or Quantity or str
        sets the unit for the function evaluation
        (default {unit})
        must be astropy-compatible unit specification
        equivalent to ``func(*args, **kw).to(unit)``
        if None, skips unit conversion
    to_value: bool
        whether to return .to_value(unit)
        (default {to_value})
        see Astropy.units.Quantity.to_value
    equivalencies: list
        equivalencies for any units provided
        (default {equivalencies})
        used by `.to()` and `.to_value()`
    decompose: bool or list, optional
        unit decomposition
        (default {decompose})

        * bool: True, False for decomposing.
        * list: bases for ``.decompose(bases=[])``

            will first decompose, then apply `unit`, `to_value`, `equivalencies`

        Decomposing then converting wastes time, since
        ``.to(unit, equivalencies)`` internally does conversions.
        The only use for combining decompose with other `unit_output`
        parameters is with::

            unit=None, to_value=True, equivalencies=[], decompose=`bool or [user bases here]'
            since this will decompose to desired bases then return the value in those bases

        .. note::

            **experimental feature:**
            for things which are not (astropy.unit.Unit, astropy.unit.core.IrreducibleUnit),
            tries wrapping in ``Unit()``.
            allows for conversions such as:

            >>> x = 10 * u.km * u.s
            >>> bases = [u.Unit(2 * u.km), u.s]
            >>> x.decompose(bases=bases) # doctest: +SKIP
            <Quantity 5. 2 km s>

    assumed_units: dict, optional
        dictionary of default units
        (default {assumed_units})

        ex) if x has no units, it is assumed to be in u.km

    assume_annotation_units: bool, optional
        whether to interpret function annotations as default units
        (default {assume_annotation_units})
        function annotations have lower precedence than *assumed_units*

    Notes
    -----
    **function must allow kwargs**

    Order of Precedence:

    - Function Arguments
    - Decorator Arguments
    - Function Annotation Arguments

    arguments to the decorator take LOWER precedence
    than arguments to the function itself.

    See decorator argument section
    function arguments override decorator & function annotation arguments

    func_args: function arguments
    unit
    to_value
    equivalencies
    decompose
    assumed_units
    func_kwargs: function key-word argument

    Decorator Key-Word Arguments:
        Unit specifications can be provided as keyword arguments
        to the decorator, or by using function annotation syntax.
        Arguments to the decorator take precedence
        over any function annotations present.
        **note**
        decorator key-word arguments are NEVER interpreted as `assumed_units`

        >>> @quantity_io(x=u.m, y=u.s)
        ... def func(x, y):
        ...     pass

    Function Annotation Arguments:

        Unit specifications can be provided as keyword arguments
        to the decorator, or by using function annotation syntax.
        Arguments to the function and decorator take precedence
        over any function annotations present.

        >>> def func(x: u.m, y: u.s) -> u.m / u.s:
        ...     pass

        if assume_annotation_units is True (default False)
        function annotations are interpreted as default units
        function annotations have lower precedence than *assumed_units*

    """

    @classmethod
    @format_doc(None, doc=__doc__)
    def as_decorator(
        cls,
        func: Callable = None,
        unit: Unit = None,
        to_value: bool = False,
        equivalencies: Sequence = [],
        decompose: Union[bool, Sequence] = False,
        assumed_units: dict = {},
        assume_annotation_units: bool = False,
        **decorator_kwargs: Any
    ):
        """{doc}."""
        # making instance from base class
        self = super().__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            # classname=func.__repr__() if func is not None else 'SideHists',
            **{k: _locals.get(k).__repr__() for k in set(_aioattrs)}
        )

        self.__init__(
            unit=unit,
            to_value=to_value,
            equivalencies=equivalencies,
            decompose=decompose,
            assumed_units=assumed_units,
            assume_annotation_units=assume_annotation_units,
            **decorator_kwargs
        )

        if func is not None:
            return self(func)
        return self

    # /def

    def __init__(
        self,
        func: Callable = None,
        unit: Unit = None,
        to_value: bool = False,
        equivalencies: Sequence = [],
        decompose: Union[bool, Sequence] = False,
        assumed_units: dict = {},
        assume_annotation_units: bool = False,
        **decorator_kwargs: Any
    ):
        """Initialize decorator class."""
        super().__init__()

        self.unit = unit
        self.to_value = to_value
        self.equivalencies = equivalencies
        self.decompose = decompose

        self.assumed_units = assumed_units
        self.assume_annotation_units = assume_annotation_units

        self.decorator_kwargs = decorator_kwargs

    # /def

    def __call__(self, wrapped_function: Callable):
        """Make decorator."""
        # Extract the function signature for the function we are wrapping.
        wrapped_signature = inspect.signature(wrapped_function)

        @wraps(wrapped_function)
        def wrapped(
            *func_args: Any,
            unit: Unit = self.unit,
            to_value: bool = self.to_value,
            equivalencies: Sequence = self.equivalencies,
            decompose: Union[bool, Sequence] = self.decompose,
            assumed_units: dict = self.assumed_units,
            _skip_decorator: bool = False,
            **func_kwargs: Any
        ):

            # skip the decorator
            if _skip_decorator:
                return wrapped_function(*func_args, **func_kwargs)

            # make func_args editable
            _func_args: list = list(func_args)

            # Bind the arguments to our new function to the signature of the original.
            bound_args = wrapped_signature.bind(*_func_args, **func_kwargs)

            # Iterate through the parameters of the original signature
            for i, param in enumerate(wrapped_signature.parameters.values()):
                # We do not support variable arguments (*args, **kwargs)
                if param.kind in {
                    inspect.Parameter.VAR_KEYWORD,
                    inspect.Parameter.VAR_POSITIONAL,
                }:
                    continue

                # Catch the (never triggered) case where bind relied on a default value.
                if (
                    param.name not in bound_args.arguments
                    and param.default is not param.empty
                ):
                    bound_args.arguments[param.name] = param.default

                # Get the value of this parameter (argument to new function)
                arg = bound_args.arguments[param.name]

                # +----------------------------------+
                # Get default unit or physical type, either from decorator kwargs
                #   or annotations
                if param.name in assumed_units:
                    dfunit = assumed_units[param.name]
                elif self.assume_annotation_units is True:
                    dfunit = param.annotation
                # elif not assumed_units:
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
                    raise ValueError("target must be one Unit, not list")

                if (not hasattr(arg, "unit")) & (adjargbydfunit is True):
                    if i < len(_func_args):
                        # print(i, len(bound_args.args))
                        _func_args[i] *= dfunit
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

                    if not hasattr(arg, "unit"):
                        arg = arg * dimensionless_unscaled
                        valid_targets.append(dimensionless_unscaled)

                else:
                    valid_targets = targets

                # Now we loop over the allowed units/physical types and validate
                #   the value of the argument:
                _validate_arg_value(
                    param.name,
                    wrapped_function.__name__,
                    arg,
                    valid_targets,
                    self.equivalencies,
                )

            # # evaluated wrapped_function
            with add_enabled_equivalencies(equivalencies):
                return_ = wrapped_function(*_func_args, **func_kwargs)
                # if func_kwargs:
                #     return_ = wrapped_function(*_func_args, **func_kwargs)
                # else:
                #     return_ = wrapped_function(*_func_args)

            if (
                wrapped_signature.return_annotation
                not in (inspect.Signature.empty, None)
                and unit is None
            ):
                unit = wrapped_signature.return_annotation

            return unit_output(
                return_,
                unit=unit,
                to_value=to_value,
                equivalencies=equivalencies,
                decompose=decompose,
            )

        # /def

        # TODO dedent
        wrapped.__doc__ = inspect.cleandoc(wrapped.__doc__ or "") + _funcdec

        # /def
        return wrapped

    # /def


###############################################################################

_funcdec = """

Other Parameters
----------------
unit : astropy Unit or Quantity or str
    sets the unit for the function evaluation.
    (default None)
    must be astropy-compatible unit specification.
    equivalent to ``func(*args, **kw).to(unit)``
    if None, skips unit conversion.
    function arguments override decorator and function annotation arguments
to_value : bool
    whether to return ``.to_value(unit)``
    (default False)
    see ``astropy.units.Quantity.to_value``
    function arguments override decorator and function annotation arguments
equivalencies : list
    equivalencies for any units provided
    (default [])
    used by ``.to()`` and ``.to_value()``
    function arguments override decorator and function annotation arguments
decompose : bool or list
    Decompose the unit into base units, can provide base as list.
    (default [])
    function arguments override decorator and function annotation arguments
    if bool, then do/don't decompose
    if list, bases for ``.decompose(bases=[])``
    will first decompose, then apply unit, to_value, equivalencies

    Decomposing then converting wastes time, since `.to(unit, equivalencies)`
    internally does conversions. The only use for combining decompose with
    other params is with::

        unit=None, to_value=True, equivalencies=[], decompose=[bases]

    since this will decompose to desired bases then return the value

    .. note::

        for things which are not (u.Unit, u.core.IrreducibleUnit),
        tries wrapping in Unit()
        this allows things such as::

            >>> x = 10 * u.km * u.s
            >>> bases = [u.Unit(2 * u.km), u.s]
            >>> x.decompose(bases=bases) # doctest: +SKIP
            <Quantity 5. 2 km s>

        (this would normally return an error)

assumed_units: dict
    dictionary of default units
    (default {})

    >>> from utilipy.units.decorators import QuantityInputOutput
    >>> dfu = {'x': u.km}
    >>> x = 10
    >>> y = 20*u.km
    >>> @QuantityInputOutput.as_decorator(assumed_units=dfu)
    ... def add(x, y):
    ...     return x + y
    >>> add(x, y) # doctest: +SKIP
    <Quantity 30.0 km>
"""


###############################################################################


quantity_io = QuantityInputOutput.as_decorator


###############################################################################
# END
