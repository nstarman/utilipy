# -*- coding: utf-8 -*-

"""Added functionality to `functools`.

Routine Listings
----------------
makeFunction
    make a function from an existing code object.

copy_function
    Copy a function.

update_wrapper
    this overrides the default ``functools`` `update_wrapper`
    and adds signature and docstring overriding

wraps
    this overrides the default ``functools`` `update_wrapper`
    and adds signature and docstring overriding

References
----------
Some functions modified from https://docs.python.org/3/library/functools.html

TODO
----
improve `makeFunction` call signature
test `makeFunction`-made function speeds

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General
import types
from functools import *

from typing import Any, Union, Callable, Sequence, Optional

# Project-Specific
from .inspect import (
    signature as _get_signature,
    Signature as _Signature,
    cleandoc as _cleandoc,
    _VAR_POSITIONAL,
    _KEYWORD_ONLY,
    _VAR_KEYWORD,
    _void, _placehold
)


################################################################################
# CODE
################################################################################


def makeFunction(
    code: Any,
    globals_: Any,
    name: Optional[str] = None,
    signature: _Signature = None,
    docstring: str = None,
    closure: Any = None,
):
    """Make a function with a specified signature and docstring.

    This is pure python and may not make the fastest functions

    Parameters
    ----------
    code : code
        the .__code__ method of a function
    globals_ :
    name : str
    signature : Signature
        inspect.Signature converted to astroPHD.Signature
    docstring : str
    closure :

    Returns
    -------
    function: types.FunctionType
        the created function

    TODO
    ----
    check how signature and closure relate
    __qualname__

    """
    if not isinstance(signature, _Signature):  # not my custom signature
        signature = _Signature(
            parameters=signature.parameters.values(),
            return_annotation=signature.return_annotation,
            # docstring=docstring  # not yet implemented
        )
    else:
        pass  # docstring considerations not yet implemented

    # make function
    function = types.FunctionType(
        code, globals_, name=name, argdefs=signature.defaults, closure=closure
    )

    # assign properties not (properly) handled by FunctionType
    function.__kwdefaults__ = signature.__kwdefaults__
    function.__annotations__ = (
        signature.__annotations__
    )  # includes return_annote
    function.__signature__ = signature.__signature__  # classical signature
    function.__doc__ = docstring

    return function


# /def


# -----------------------------------------------------------------------------


def copy_function(func: Callable):
    """Copy an existing function."""
    function = makeFunction(
        func.__code__,
        func.__globals__,
        name=func.__name__,
        signature=_get_signature(func),
        docstring=func.__doc__,
        closure=func.__closure__,
    )

    # TODO necessary?
    function.__dict__.update(func.__dict__)

    return function


# /def


################################################################################
# update_wrapper() and wraps() decorator
################################################################################

WRAPPER_ASSIGNMENTS = (
    "__module__",
    "__name__",
    "__qualname__",
    "__doc__",
    "__annotations__",
)
SIGNATURE_ASSIGNMENTS = ("__kwdefaults__", "__annotations__")
WRAPPER_UPDATES = ("__dict__",)


def update_wrapper(
    wrapper: Callable,
    wrapped: Callable,
    signature: Union[_Signature, None, bool] = True,
    docstring: Union[str, None, bool] = None,
    assigned: Sequence[str] = WRAPPER_ASSIGNMENTS,
    updated: Sequence[str] = WRAPPER_UPDATES,
    _docstring_formatter: Optional[dict] = None,
):
    """Update a wrapper function to look like the wrapped function.

    Parameters
    ----------
    wrapper
        the function to be updated

    wrapped
       the original function

    signature : Signature or None or bool
        signature to impose on `wrapper`.
        None and False default to `wrapped`'s signature.
        True merges `wrapper` and `wrapped` kwdefaults & annotations

    docstring : str or None or bool
        docstring to impose on `wrapper`.
        False defaults to `wrapped` docstring.
        None defaults to `wrapped` docstring and appends `wrapper` docstring
        True (not yet implemented) parses the docstring (using the docstring configurator in .astroPHDrc) and merges the sections

    assigned : tuple
       tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       ``functools.WRAPPER_ASSIGNMENTS``)

    updated : tuple
       is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to ``functools.WRAPPER_UPDATES``)

    _docstring_formatter : dict
        dictionary to format wrapper docstring

    Returns
    -------
    wrapper : FunctionType
        `wrapper` function updated by the `wrapped` function's attributes and
        also the provided `signature` and `docstring`.

    Raises
    ------
    ValueError
        if docstring is True

    """
    # ---------------------------------------
    # preamble

    if signature is True:
        _update_sig = True
        signature = _Signature.from_callable(wrapped)
    elif signature in (None, False):
        pass
    else:  # convert to my signature object
        _update_sig = False
        if not (type(signature) == _Signature):  # not my custom signature
            signature = _Signature(
                parameters=signature.parameters.values(),
                return_annotation=signature.return_annotation,
                # docstring=docstring  # not yet implemented
            )
        elif isinstance(signature, _Signature):  #  checking a signature object
            pass  # docstring considerations not yet implemented
        else:
            raise ValueError("signature must be a Signature object")

    # need to get wrapper properties now
    wrapper_sig = _Signature.from_callable(wrapper)

    wrapper_doc = wrapper.__doc__ or ""
    wrapper_doc = "\n".join(wrapper_doc.split("\n")[1:])  # drop title

    if _docstring_formatter is None:
        _docstring_formatter = {}

    # ---------------------------------------
    # update wrapper (same as functools.update_wrapper)
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:  # update whole dictionary
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))

    # ---------------------------------------

    # deal with signature
    if signature in (None, False):
        pass

    elif _update_sig:  # merge wrapped and wrapper signature

        # go through parameters in wrapper_sig, merging into signature
        for param in wrapper_sig.parameters.values():
            # skip _VAR_POSITIONAL and _VAR_KEYWORD
            if param.kind in {_VAR_POSITIONAL, _VAR_KEYWORD}:
                pass
            # already exists -> replace
            elif param.name in signature.parameters:
                # ensure kind matching
                if param.kind != signature.parameters[param.name].kind:
                    raise TypeError(
                        f"{param.name} must match kind in function signature"
                    )
                # can only merge key-word only
                if param.kind == _KEYWORD_ONLY:
                    signature.modify_parameter(
                        param.name,
                        name=None,
                        kind=None,  # inherit b/c matching
                        default=param.default,
                        annotation=param.annotation,
                    )

                    # track for docstring
                    _docstring_formatter[param.name] = param.default

            # add to signature
            else:
                # can only merge key-word only
                if param.kind == _KEYWORD_ONLY:
                    signature = signature.insert_parameter(
                        signature.index_end_keyword_only, param
                    )

                    # track for docstring
                    _docstring_formatter[param.name] = param.default
        # /for

        for attr in SIGNATURE_ASSIGNMENTS:
            value = getattr(signature, attr)
            setattr(wrapper, attr, value)

        wrapper.__signature__ = signature.signature

    else:  # a signature object
        for attr in SIGNATURE_ASSIGNMENTS:
            value = getattr(signature, attr)
            setattr(wrapper, attr, value)

        # for docstring
        for param in wrapper_sig.parameters.values():
            # can only merge key-word only
            if param.kind == _KEYWORD_ONLY:
                _docstring_formatter[param.name] = param.default

        wrapper.__signature__ = signature.signature

    # ---------------------------------------
    # docstring

    if _docstring_formatter:  # (not empty dict)
        wrapper_doc = wrapper_doc.format(**_docstring_formatter)

    if docstring is False:  # just inherit
        wrapper.__doc__ = wrapped.__doc__
    elif docstring is None:  # append wrapper docstring
        wrapper_doc = "\n" + _cleandoc(wrapper_doc)
        wrapper.__doc__ = (wrapped.__doc__ or "") + wrapper_doc
    elif docstring is True:  # smart merge docstrings
        raise ValueError("NOT YET IMPLEMENTED")
    else:  # assign docstring
        wrapper.__doc__ = docstring

    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper


# /def


# -----------------------------------------------------------------------------


def wraps(
    wrapped: Callable,
    signature: Union[_Signature, None, bool] = True,
    docstring: Union[str, None, bool] = None,
    assigned: Sequence[str] = WRAPPER_ASSIGNMENTS,
    updated: Sequence[str] = WRAPPER_UPDATES,
    _docstring_formatter: Optional[dict] = None,
):
    """Decorator factory to apply ``update_wrapper()`` to a wrapper function.

    Returns a decorator that invokes ``update_wrapper()`` with the decorated
    function as the wrapper argument and the arguments to ``wraps()`` as the
    remaining arguments. Default arguments are as for ``update_wrapper()``.
    This is a convenience function to simplify applying ``partial()`` to
    ``update_wrapper()``.

    """
    return partial(
        update_wrapper,
        wrapped=wrapped,
        signature=signature,
        docstring=docstring,
        assigned=assigned,
        updated=updated,
        _docstring_formatter=_docstring_formatter,
    )


##############################################################################
# END
