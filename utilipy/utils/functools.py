# -*- coding: utf-8 -*-

"""Added functionality to `functools`.

Routine Listings
----------------
`makeFunction`
    make a function from an existing code object.

`copy_function`
    Copy a function.

`update_wrapper`
    this overrides the default ``functools`` `update_wrapper`
    and adds signature and docstring overriding

`wraps`
    overrides the default ``functools`` `update_wrapper`
    and adds signature and docstring overriding

References
----------
Some functions modified from https://docs.python.org/3/library/functools.html

Notes
-----
.. todo::

    improve `makeFunction` call signature
    test `makeFunction`-made function speeds
    todo make partial respect signature

"""


__all__ = [
    "make_function",
    "copy_function",
    "update_wrapper",
    "wraps",
]


##############################################################################
# IMPORTS

# BUILT-IN
import typing as T
from functools import *  # noqa # so can be a drop-in for `functools`
from functools import partial
from types import CodeType, FunctionType

# PROJECT-SPECIFIC
from . import inspect as _nspct
from .inspect import FullerSignature as _FullerSig
from .string import FormatTemplate as _FormatTemplate
from utilipy.extern.doc_parse_tools import store as _store

# CLEAN MULTIPLE DEFINITIONS
del globals()["update_wrapper"]
del globals()["wraps"]


###############################################################################
# CODE
###############################################################################


def make_function(
    code: CodeType,
    globals_: T.Any,
    name: str,
    signature: _FullerSig,
    docstring: str = None,
    closure: T.Any = None,
    qualname: str = None,
    # options
    _add_signature: bool = False,
):
    r"""Make a function with a specified signature and docstring.

    This is pure python and may not make the fastest functions

    Parameters
    ----------
    code : code
        the .__code__ method of a function
    globals_ : Any
    name : str
    signature : Signature
        inspect.Signature converted to utilipy.Signature
    docstring : str
    closure : Any
    qualname : str

    Returns
    -------
    function: Callable
        the created function

    Other Parameters
    ----------------
    \_add_signature : bool
        Whether to add `signature` as ``__signature__``.

    .. todo::

        check how signature and closure relate
        __qualname__

    """
    if not isinstance(signature, _FullerSig):  # not my custom signature
        signature = _FullerSig(
            parameters=signature.parameters.values(),
            return_annotation=signature.return_annotation,
            # docstring=docstring  # not yet implemented
        )
    # else:
    #     pass

    # make function
    function = FunctionType(
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


def copy_function(func: T.Callable):
    """Copy an existing function.

    Notes
    -----
    copy's code, globals, name, signature, (kw)defaults, docstring, and dict
    custom methods / method overwriting may not be copied

    """
    function = make_function(
        func.__code__,
        func.__globals__,
        name=func.__name__,
        signature=_nspct.fuller_signature(func),
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


def __parse_sig_for_update_wrapper(
    signature: T.Union[_FullerSig, None, bool], wrapped: T.Callable
):
    """Parse signature for `~update_wrapper`.

    Parameters
    ----------
    signature : `~utilipy.utils.inspect.Signature` or None or bool

    Returns
    -------
    signature : `~utilipy.utils.inspect.Signature` or None or False
        If signature is True, returns `~utilipy.utils.inspect.Signature`

    """
    if signature is True:
        _update_sig = True
        signature = _FullerSig.from_callable(wrapped)
    elif signature in (None, False):
        pass
    else:  # convert to my signature object
        _update_sig = False
        # if not (type(signature) == _FullerSig):
        if not isinstance(signature, _FullerSig):
            signature = _FullerSig(
                parameters=signature.parameters.values(),
                return_annotation=signature.return_annotation,
                # docstring=docstring  # not yet implemented
            )
        elif isinstance(signature, _FullerSig):
            pass  # docstring considerations not yet implemented
        else:
            raise ValueError("signature must be a Signature object")
    # /if

    return signature, _update_sig


# /def


def __update_wrapper_update_sig(
    signature: T.Union[_FullerSig, None, bool],
    wrapper_sig: _FullerSig,
    _doc_fmt: T.Optional[dict],
) -> T.Callable:
    """Update signature for `~update_wrapper`."""
    # go through parameters in wrapper_sig, merging into signature
    for param in wrapper_sig.parameters.values():
        # skip _nspct.VAR_POSITIONAL and _nspct.VAR_KEYWORD
        if param.kind in {_nspct.VAR_POSITIONAL, _nspct.VAR_KEYWORD}:
            pass
        # already exists -> replace
        elif param.name in signature.parameters:
            # ensure kind matching
            if param.kind != signature.parameters[param.name].kind:
                raise TypeError(
                    f"{param.name} must match kind in function signature"
                )
            # can only merge keyword-only
            if param.kind == _nspct.KEYWORD_ONLY:
                signature = signature.modify_parameter(
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
            # can only merge keyword-only
            if param.kind == _nspct.KEYWORD_ONLY:
                signature = signature.insert_parameter(
                    signature.index_end_keyword_only, param
                )

                # track for docstring
                _doc_fmt[param.name] = param.default
    # /for

    return signature


# /def


def __update_wrapper_docstring(
    wrapped: T.Callable,
    docstring: T.Union[str, bool],
    wrapper_doc: str,
    _doc_style: T.Union[str, T.Callable, None],
):
    """Set docstring for `~update_wrapper`.

    Parameters
    ----------
    docstring : str or bool
    wrapper_doc : strr
    _doc_style : str or Callable or None

    Returns
    -------
    docstring : str

    """
    if isinstance(docstring, str):  # assign docstring
        docstring = _nspct.cleandoc(docstring)
    elif docstring is False:  # just inherit
        docstring = wrapped.__doc__
    else:  # merge wrapper docstring
        wrapped_doc = _nspct.getdoc(wrapped) or ""
        wrapper_doc = _nspct.cleandoc(wrapper_doc)

        if _doc_style is None:  # use original wrapper docstring
            docstring = wrapped_doc + "\n\n" + wrapper_doc

        else:  # TODO implement the full set of options
            docstring = _store[_doc_style](
                wrapped_doc,
                wrapper_doc,
                method="merge",
            )
    # /if

    return docstring


# /def


def update_wrapper(
    wrapper: T.Callable,
    wrapped: T.Callable,
    signature: T.Union[_FullerSig, None, bool] = True,  # not in functools
    docstring: T.Union[str, bool] = True,  # not in functools
    assigned: T.Sequence[str] = WRAPPER_ASSIGNMENTS,
    updated: T.Sequence[str] = WRAPPER_UPDATES,
    # docstring options
    _doc_fmt: T.Optional[dict] = None,  # not in functools
    _doc_style: T.Union[str, T.Callable, None] = None,
):
    """Update a wrapper function to look like the wrapped function.

    Parameters
    ----------
    wrapper : Callable
        the function to be updated
    wrapped : Callable
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
    _doc_style: str or Callable, optional
        the style of the docstring
        if None (default), appends `wrapper` docstring
        if str or Callable, merges the docstring

    Returns
    -------
    wrapper : Callable
        `wrapper` function updated by the `wrapped` function's attributes and
        also the provided `signature` and `docstring`.

    Raises
    ------
    ValueError
        if docstring is True

    """
    # ---------------------------------------
    # preamble

    signature, _update_sig = __parse_sig_for_update_wrapper(signature, wrapped)

    # need to get wrapper properties now
    wrapper_sig = _FullerSig.from_callable(wrapper)

    wrapper_doc = _nspct.getdoc(wrapper) or ""
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

        signature = __update_wrapper_update_sig(
            signature, wrapper_sig, _doc_fmt
        )

        for attr in SIGNATURE_ASSIGNMENTS:
            value = getattr(signature, attr)
            setattr(wrapper, attr, value)

        wrapper.__signature__ = signature.signature

    else:  # a signature object
        for attr in SIGNATURE_ASSIGNMENTS:
            _value = getattr(signature, attr)
            setattr(wrapper, attr, _value)

        # for docstring
        for param in wrapper_sig.parameters.values():
            # can only merge keyword-only
            if param.kind == _nspct.KEYWORD_ONLY:
                _doc_fmt[param.name] = param.default

        wrapper.__signature__ = signature.signature

    # ---------------------------------------
    # docstring

    if _doc_fmt:  # (not empty dict)
        wrapper_doc = _FormatTemplate(wrapper_doc).safe_substitute(**_doc_fmt)

    wrapper.__doc__ = __update_wrapper_docstring(
        wrapped,
        docstring=docstring,
        wrapper_doc=wrapper_doc,
        _doc_style=_doc_style,
    )

    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper


# /def


# -----------------------------------------------------------------------------


def wraps(
    wrapped: T.Callable,
    signature: T.Union[_FullerSig, None, bool] = True,
    docstring: T.Union[str, None, bool] = None,
    assigned: T.Sequence[str] = WRAPPER_ASSIGNMENTS,
    updated: T.Sequence[str] = WRAPPER_UPDATES,
    _doc_fmt: T.Optional[dict] = None,
    _doc_style: T.Union[str, T.Callable, None] = None,
):
    """:func:`~functools.wraps`, adding signature and docstring features.

    Decorator factory to apply ``update_wrapper()`` to a wrapper function.

    This is a convenience function to simplify applying ``partial()`` to
    ``update_wrapper()``.

    Parameters
    ----------
    wrapped: Callable
    signature: _FullerSig or bool or None, optional
        True (default)
    docstring: str or bool or None, optional
        None
    assigned: Sequence[str]
        WRAPPER_ASSIGNMENTS,
    updated: Sequence[str]
        WRAPPER_UPDATES,
    _doc_fmt: dict or None, optional
    _doc_style: Union[str, Callable, None], optional

    Returns
    -------
    partial
        a decorator that invokes ``update_wrapper()`` with the decorated
        function as the wrapper argument and the arguments to ``wraps()`` as
        the remaining arguments. Default arguments are as for
        ``update_wrapper()``.

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
