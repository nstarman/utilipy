# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : unit decorators
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Decorators for functions accepting Astropy Quantities."""

__author__ = "Nathaniel Starkman"
__credit__ = "astropy"


__all__ = ["quantity_output", "QuantityInputOutput", "quantity_io"]


##############################################################################
# IMPORTS

# BUILT-IN

import textwrap
from typing import Any, Union, Sequence, Callable


# THIRD-PARTY

from astropy.units import dimensionless_unscaled
from astropy.units.decorators import _validate_arg_value, _get_allowed_units
from astropy.units.core import Unit, add_enabled_equivalencies
from astropy.utils.misc import isiterable
from astropy.utils.decorators import format_doc


# PROJECT-SPECIFIC

from .core import quantity_return_, _doc_base_params, _doc_base_raises
from ..utils import functools, inspect


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


# ----------------------------------------


_doc_quantity_output_examples = """
`quantity_output` decorated function

    >>> from utilipy.units.decorators import quantity_output
    >>> @quantity_output(unit=u.m, to_value=True)
    ... def example_function(x):
    ...     return x
    >>> example_function(10 * u.km)
    10000.0
    >>> example_function(10)
    10
    >>> example_function(10 * u.km, to_value=False)  # doctest: +FLOAT_CMP
    <Quantity 10000. m>

"""

_doc_quantity_output_wrapped = """
Other Parameters
----------------
{parameters}

Raises
-------
{raises}

Examples
--------
{examples}
""".format(
    parameters=_doc_base_params,
    raises=_doc_base_raises,
    examples=_doc_quantity_output_examples,
)


# ----------------------------------------

# QuantityInputOutput parameters, combine base and assumed_units
_doc_qio_params = """
function: function
    the function to decorate
    (default None)
{parameters}
assumed_units: dict
    dictionary of default units
    (default dict())

    >>> from utilipy.units import QuantityInputOutput
    >>> dfu = dict(x=u.km)
    >>> x = 10
    >>> y = 20*u.km
    >>> @QuantityInputOutput.as_decorator(assumed_units=dfu)
    ... def add(x, y):
    ...     return x + y
    >>> add(x, y) # doctest: +SKIP
    <Quantity 30.0 km>

assume_annotation_units: bool, optional
    whether to interpret function annotations as default units
    (default False)
    function annotations have lower precedence than `assumed_units`

""".format(
    parameters=_doc_base_params,
)

_doc_qio_notes = """
Order of Precedence:

1. Function Arguments
2. Decorator Arguments
3. Function Annotation Arguments

Decorator Key-Word Arguments:

    Unit specifications can be provided as keyword arguments
    to the decorator, or by using function annotation syntax.
    Arguments to the decorator take precedence
    over any function annotations present.
    **note**
    decorator key-word arguments are NEVER interpreted as `assumed_units`

    >>> @QuantityInputOutput.as_decorator(x=u.m, y=u.s)
    ... def func(x, y):
    ...     pass

Function Annotation Arguments:

    Unit specifications can be provided as keyword arguments
    to the decorator, or by using function annotation syntax.
    Arguments to the function and decorator take precedence
    over any function annotations present.

    >>> def func(x: u.m, y: u.s) -> u.m / u.s:
    ...     pass

    if `assume_annotation_units` is True (default False)
    function annotations are interpreted as default units
    function annotations have lower precedence than `assumed_units`

"""

# TODO replace
_funcdec = """

Other Parameters
----------------
{parameters}

""".format(
    parameters=_doc_qio_params
)


###############################################################################
# CODE
###############################################################################


@format_doc(
    None,
    parameters=textwrap.indent(_doc_base_params, " " * 4),
    raises=textwrap.indent(_doc_base_raises, " " * 4),
    examples=textwrap.indent(_doc_quantity_output_examples, " " * 4),
    doc_quantity_output_wrapped=textwrap.indent(
        _doc_quantity_output_wrapped, " " * 12 + "| "
    ),
)
def quantity_output(
    function: Callable = None,
    *,
    unit: Unit = None,
    to_value: bool = False,
    equivalencies: Sequence = [],
    decompose: Union[bool, Sequence] = False,
):
    r"""Decorate functions for unit output.

    Any wrapped function accepts the additional key-word arguments:
        - `unit`
        - `to_value`
        - `equivalencies`
        - `decompose`

    Parameters
    ----------
    {parameters}

    Returns
    -------
    wrapper: Callable
        wrapped function
        with the unit operations performed by `quantity_return_`

        The following is added to the docstring

            {doc_quantity_output_wrapped}

    Raises
    ------
    {raises}

    Examples
    --------
    .. code-block:: python

        @quantity_output
        def func(x, y):
            return x + y

    is equivalent to

    .. code-block:: python

        def func(x, y, unit=None, to_value=False, equivalencies=[],
                 decompose=False):
            result = x + y
            return quantity_return_(result, unit, to_value, equivalencies,
                                    decompose)

    {examples}

    """
    # allowing for optional arguments
    if function is None:
        return functools.partial(
            quantity_output,
            unit=unit,
            to_value=to_value,
            equivalencies=equivalencies,
            decompose=decompose,
        )

    # making decorator
    @functools.wraps(function)
    @format_doc(
        None,
        parameters=textwrap.indent(_doc_base_params, " " * 8),
        raises=textwrap.indent(_doc_base_raises, " " * 8),
        examples=textwrap.indent(_doc_quantity_output_examples, " " * 8),
        # _doc_quantity_output_wrapped=textwrap.indent(
        #     _doc_quantity_output_wrapped, " " * 8
        # ),
    )
    def wrapper(
        *args: Any,
        unit: Unit = unit,
        to_value: bool = to_value,
        equivalencies: Sequence = equivalencies,
        decompose: Union[bool, Sequence] = decompose,
        **kwargs: Any,
    ):
        """Wrapper docstring.

        Other Parameters
        ----------------
        {parameters}

        Raises
        ------
        {raises}

        Examples
        --------
        {examples}

        """
        return quantity_return_(
            function(*args, **kwargs),  # evaluated function
            unit=unit,
            to_value=to_value,
            equivalencies=equivalencies,
            decompose=decompose,
        )

    # /def

    return wrapper


# /def


###############################################################################


class QuantityInputOutput:
    """Decorator for validating the units of arguments to functions."""

    @classmethod
    @format_doc(
        None,
        parameters=textwrap.indent(_doc_qio_params, " " * 8),
        notes=textwrap.indent(_doc_qio_notes, " " * 8),
    )
    def as_decorator(
        cls,
        function: Callable = None,
        unit: Unit = None,
        to_value: bool = False,
        equivalencies: Sequence = [],
        decompose: Union[bool, Sequence] = False,
        assumed_units: dict = {},
        assume_annotation_units: bool = False,
        **decorator_kwargs: Any,
    ):
        """Decorator for validating the units of arguments to functions.

        Parameters
        ----------
        {parameters}

        See Also
        --------
        :class:`~astropy.units.quantity_input`

        Notes
        -----
        {notes}

        """
        # making instance from base class
        self = super().__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = __doc__.format(
            **{k: _locals.get(k).__repr__() for k in set(_aioattrs)}
        )

        self.__init__(
            unit=unit,
            to_value=to_value,
            equivalencies=equivalencies,
            decompose=decompose,
            assumed_units=assumed_units,
            assume_annotation_units=assume_annotation_units,
            **decorator_kwargs,
        )

        if function is not None:
            return self(function)
        return self

    # /def

    # ------------------------------------------

    @format_doc(
        None,
        parameters=textwrap.indent(_doc_qio_params, " " * 4),
        notes=textwrap.indent(_doc_qio_notes, " " * 4),
    )
    def __init__(
        self,
        function: Callable = None,
        unit: Unit = None,
        to_value: bool = False,
        equivalencies: Sequence = [],
        decompose: Union[bool, Sequence] = False,
        assumed_units: dict = {},
        assume_annotation_units: bool = False,
        **decorator_kwargs: Any,
    ):
        """Decorator for validating the units of arguments to functions.

        Parameters
        ----------
        {parameters}

        See Also
        --------
        :class:`~astropy.units.quantity_input`

        Notes
        -----
        {notes}

        """
        super().__init__()

        self.unit = unit
        self.to_value = to_value
        self.equivalencies = equivalencies
        self.decompose = decompose

        self.assumed_units = assumed_units
        self.assume_annotation_units = assume_annotation_units

        self.decorator_kwargs = decorator_kwargs

    # /def

    # ------------------------------------------

    def __call__(self, wrapped_function: Callable):
        """Make decorator.

        Parameters
        ----------
        wrapped_function : Callable
            function to wrap

        Returns
        -------
        wrapped: Callable
            wrapped function

        """
        # Extract the function signature for the function we are wrapping.
        wrapped_signature = inspect.signature(wrapped_function)

        @functools.wraps(wrapped_function)
        def wrapped(
            *func_args: Any,
            unit: Unit = self.unit,
            to_value: bool = self.to_value,
            equivalencies: Sequence = self.equivalencies,
            decompose: Union[bool, Sequence] = self.decompose,
            assumed_units: dict = self.assumed_units,
            _skip_decorator: bool = False,
            **func_kwargs: Any,
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

            return quantity_return_(
                return_,
                unit=unit,
                to_value=to_value,
                equivalencies=equivalencies,
                decompose=decompose,
            )

        # /def

        # TODO dedent
        wrapped.__doc__ = inspect.cleandoc(wrapped.__doc__ or "") + _funcdec

        return wrapped

    # /def


quantity_io = QuantityInputOutput.as_decorator
# /class


###############################################################################


# del add_enabled_equivalencies


###############################################################################
# END
