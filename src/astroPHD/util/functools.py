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
from functools import *  # so can be a drop-in for `functools`
import functools

from typing import Any, Union, Callable, Sequence, Optional

# Project-Specific
from .string import FormatTemplate
from .inspect import (
    signature as _get_signature,
    FullerSignature as _FullerSignature,
    cleandoc as _cleandoc,
    _VAR_POSITIONAL,
    _KEYWORD_ONLY,
    _VAR_KEYWORD,
)
from .doc_parse_tools import store as _store


###############################################################################
# CODE
###############################################################################


def make_function(
    code: Any,
    globals_: Any,
    name: str,
    signature: _FullerSignature,
    docstring: str = None,
    closure: Any = None,
    qualname: str = None,
    # options
    _add_signature=False,
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
    if not isinstance(signature, _FullerSignature):  # not my custom signature
        signature = _FullerSignature(
            parameters=signature.parameters.values(),
            return_annotation=signature.return_annotation,
            # docstring=docstring  # not yet implemented
        )
    else:
        pass

    # make function
    function = types.FunctionType(
        code, globals_, name=name, argdefs=signature.defaults, closure=closure
    )

    # assign properties not (properly) handled by FunctionType
    function.__kwdefaults__ = signature.__kwdefaults__
    function.__annotations__ = signature.__annotations__
    function.__doc__ = docstring

    if qualname is not None:
        function.__qualname__ = qualname

    if _add_signature:
        function.__signature__ = signature.__signature__  # classical signature

    return function


# /def


# -----------------------------------------------------------------------------


def copy_function(func: Callable):
    """Copy an existing function.

    Note
    ----
    copy's code, globals, name, signature, (kw)defaults, docstring, and dict
    custom methods / method overwriting may not be copied

    """
    function = make_function(
        func.__code__,
        func.__globals__,
        name=func.__name__,
        signature=_get_signature(func),
        docstring=func.__doc__,
        closure=func.__closure__,
        qualname=func.__qualname__,
        # options
        _add_signature=hasattr(func, "__signature__"),
    )

    # TODO necessary?
    function.__dict__.update(func.__dict__)
    function.__defaults__ = func.__defaults__
    function.__kwdefaults__ = func.__kwdefaults__

    return function


# /def


###############################################################################
# update_wrapper() and wraps() decorator
###############################################################################

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
    signature: Union[_FullerSignature, None, bool] = True,  # not in functools
    docstring: Union[str, bool] = True,  # not in functools
    assigned: Sequence[str] = WRAPPER_ASSIGNMENTS,
    updated: Sequence[str] = WRAPPER_UPDATES,
    # docstring options
    _doc_fmt: Optional[dict] = None,  # not in functools
    _doc_style: Union[str, types.FunctionType, None] = None,
):
    """Update a wrapper function to look like the wrapped function.

    Parameters
    ----------
    wrapper
        the function to be updated
    wrapped
       the original function
    signature : Signature or None or bool, optional
        signature to impose on `wrapper`.
        None and False default to `wrapped`'s signature.
        True merges `wrapper` and `wrapped` kwdefaults & annotations
    docstring : str or bool, optional
        docstring to impose on `wrapper`.
        False ignores `wrapper`'s docstring, using only `wrapped`'s docstring.
        None (defualt) merges the `wrapper` and `wrapped` docstring
    assigned : tuple, optional
       tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       ``functools.WRAPPER_ASSIGNMENTS``)
    updated : tuple, optional
       is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to ``functools.WRAPPER_UPDATES``)
    _doc_fmt : dict, optional
        dictionary to format wrapper docstring
    _doc_style: str or FunctionType, optional
        the style of the docstring
        if None (default), appends `wrapper` docstring
        if str or FunctionType, merges the docstring

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
        signature = _FullerSignature.from_callable(wrapped)
    elif signature in (None, False):
        pass
    else:  # convert to my signature object
        _update_sig = False
        if not (type(signature) == _FullerSignature):
            signature = _FullerSignature(
                parameters=signature.parameters.values(),
                return_annotation=signature.return_annotation,
                # docstring=docstring  # not yet implemented
            )
        elif isinstance(signature, _FullerSignature):
            pass  # docstring considerations not yet implemented
        else:
            raise ValueError("signature must be a Signature object")

    # need to get wrapper properties now
    wrapper_sig = _FullerSignature.from_callable(wrapper)

    wrapper_doc = wrapper.__doc__ or ""
    wrapper_doc = "\n".join(wrapper_doc.split("\n")[1:])  # drop title

    if _doc_fmt is None:
        _doc_fmt = {}

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
                    _doc_fmt[param.name] = param.default

            # add to signature
            else:
                # can only merge key-word only
                if param.kind == _KEYWORD_ONLY:
                    signature = signature.insert_parameter(
                        signature.index_end_keyword_only, param
                    )

                    # track for docstring
                    _doc_fmt[param.name] = param.default
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
                _doc_fmt[param.name] = param.default

        wrapper.__signature__ = signature.signature

    # ---------------------------------------
    # docstring

    if _doc_fmt:  # (not empty dict)
        wrapper_doc = FormatTemplate(wrapper_doc).safe_substitute(**_doc_fmt)

    if isinstance(docstring, str):  # assign docstring
        wrapper.__doc__ = docstring
    elif docstring is False:  # just inherit
        wrapper.__doc__ = wrapped.__doc__
    else:  # merge wrapper docstring
        wrapper_doc = _cleandoc("\n" + wrapper_doc)

        if _doc_style is None:  # use original wrapper docstring
            wrapper.__doc__ = (wrapped.__doc__ or "") + wrapper_doc

        else:  # TODO implement the full set of options
            wrapper.__doc__ = _store[_doc_style](
                _cleandoc(wrapped.__doc__),
                _cleandoc(wrapper_doc),
                method="merge",
            )

    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper


# /def


# -----------------------------------------------------------------------------


def wraps(
    wrapped: Callable,
    signature: Union[_FullerSignature, None, bool] = True,  # not in functools
    docstring: Union[str, None, bool] = None,  # ibid
    assigned: Sequence[str] = WRAPPER_ASSIGNMENTS,
    updated: Sequence[str] = WRAPPER_UPDATES,
    # docstring options
    _doc_fmt: Optional[dict] = None,  # ibid
    _doc_style: Union[str, types.FunctionType, None] = None,  # ibid
):
    """Decorator factory to apply ``update_wrapper()`` to a wrapper function.

    This is a convenience function to simplify applying ``partial()`` to
    ``update_wrapper()``.

    Parameters
    ----------
    wrapped: Callable
    signature: _FullerSignature or bool or None, optional
        True (default)
    docstring: str or bool or None, optional
        None
    assigned: Sequence[str]
        WRAPPER_ASSIGNMENTS,
    updated: Sequence[str]
        WRAPPER_UPDATES,
    _doc_fmt: dict or None, optional
    _doc_style: Union[str, types.FunctionType, None], optional

    Returns
    -------
    partial
        a decorator that invokes ``update_wrapper()`` with the decorated
        function as the wrapper argument and the arguments to ``wraps()`` as
        the remaining arguments. Default arguments are as for
        ``update_wrapper()``.


    Examples
    --------
    Example Decorator:
    .. code-block:: python
        :linenos:

        def template_decorator(function=None, *, kw1=None):
            ''''Docstring for decorator.

            Description of this decorator

            Parameters
            ----------
            function : types.FunctionType or None, optional
                the function to be decoratored
                if None, then returns decorator to apply.
            kw1 : any, optional
                key-word only argument
                sets the wrapper's default values.

            Returns
            -------
            wrapper : types.FunctionType
                wrapper for function
                does a few things
                includes the original function in a method `.__wrapped__`

            '''
            if function is None: # allowing for optional arguments
                return functools.partial(template_decorator, kw1=kw1)

            @awraps(function)
            def wrapper(*args, kw1=kw1, kw2='added', **kw):
                ```wrapper docstring.

                Parameters
                ----------
                prints information about function
                kw1: defaults {kw1}
                kw2: default {kw2}

                ```
                # do stuff here
                return_ = function(*args, **kw)
                # and here
                return return_
            # /def

            return wrapper
        # /def

    """
    return partial(
        update_wrapper,
        wrapped=wrapped,
        signature=signature,
        docstring=docstring,
        assigned=assigned,
        updated=updated,
        _doc_fmt=_doc_fmt,
        _doc_style=_doc_style,
    )


# /def


##############################################################################
# END
