# -*- coding: utf-8 -*-

"""Custom `inspect` module."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# BUILT-IN
import inspect
import typing as T
from collections import namedtuple
from inspect import *  # noqa  # so can be a drop-in for `inspect`
from inspect import FullArgSpec, Parameter
from inspect import Signature as Signature
from inspect import _void, getfullargspec

# THIRD PARTY
from astropy.utils.decorators import format_doc
from typing_extensions import Literal

##############################################################################
# PARAMETERS

__all__ = [
    "POSITIONAL_ONLY",
    "POSITIONAL_OR_KEYWORD",
    "VAR_POSITIONAL",
    "KEYWORD_ONLY",
    "VAR_KEYWORD",
    # "_void",  # TODO: add to RTD
    # "_empty",  # TODO: add to RTD
    "_placehold",
    "_is_empty",
    "_is_void",
    "_is_placehold",
    "_is_placeholder",
    "FullerArgSpec",
    "getfullerargspec",
    "get_annotations_from_signature",
    "get_defaults_from_signature",
    "get_kwdefaults_from_signature",
    "get_kwonlydefaults_from_signature",
    "get_kinds_from_signature",
    "modify_parameter",
    "replace_with_parameter",
    "insert_parameter",
    "prepend_parameter",
    "append_parameter",
    "drop_parameter",
    "FullerSignature",
    "fuller_signature",
]

POSITIONAL_ONLY = Parameter.POSITIONAL_ONLY
POSITIONAL_OR_KEYWORD = Parameter.POSITIONAL_OR_KEYWORD
VAR_POSITIONAL = Parameter.VAR_POSITIONAL
KEYWORD_ONLY = Parameter.KEYWORD_ONLY
VAR_KEYWORD = Parameter.VAR_KEYWORD

# placeholders
_empty = Parameter.empty  # TODO: add to RTD
_void = _void  # TODO: add to RTD


# class _void:  # FIX import _void from `inspect`
#     """Void."""

#     pass


# /class


class _placehold:
    """Placehold."""


# /class


# types

# EmptyType = T.Type[_empty]
_typing_tuple_false = T.Union[tuple, Literal[False]]


FullerArgSpec: namedtuple = namedtuple(
    "FullerArgSpec",
    [
        "args",
        "defaultargs",
        "argdefaults",
        "varargs",
        "kwonlyargs",
        "kwonlydefaults",
        "varkw",
        "annotations",
        "docstring",
    ],
)


##############################################################################
# CODE
##############################################################################


##########################################################################
# safe placeholder comparison
# some 3rd party packages have quantities which cannot be directly compared to
# via ``==`` or ``!=`` and will throw an exception. These methods implement
# safe testing against ``_empty``, ``_void``, ``_placehold``
# and the combination.


def _is_empty(value):
    """Test whether `value`==`_empty`."""
    try:
        value == _empty
    except Exception:
        # if it throws an exception, it clearly isn't `_empty`
        return False
    else:
        return value == _empty


# /def


def _is_void(value):
    """Test whether `value`==`_void`."""
    try:
        value == _void
    except Exception:
        # if it throws an exception, it clearly isn't `_void`
        return False
    else:
        return value == _void


# /def


def _is_placehold(value):
    """Test whether `value`==`_placehold`."""
    try:
        value == _placehold
    except Exception:
        # if it throws an exception, it clearly isn't `_placehold`
        return False
    else:
        return value == _placehold


# /def


def _is_placeholder(value):
    """Test whether `value`==`_placeholder`."""
    try:
        value == _empty
    except Exception:
        # if it throws an exception, it clearly isn't `_placeholder`
        return False
    else:
        return (value == _empty) | (value == _void) | (value == _placehold)


# /def


###########################################################################
# getfullerargspec


def getfullerargspec(func: T.Callable) -> FullerArgSpec:
    """Separated version of FullerArgSpec.

    fullargspec with separation of mandatory and optional arguments
    adds *defargs* which corresponds *defaults*

    Parameters
    ----------
    func : function
        the function to inspect

    Returns
    -------
    FullerArgSpec : namedtuple
        args             : the mandatory arguments
        defargs          : arguments with defaults
        defaults         : dictionary of defaults to `defargs`
        varargs          : variable arguments (args)
        kwonlyargs       : keyword-only arguments
        kwonlydefaults   : keyword-only argument defaults
        varkw            : variable key-word arguments (kwargs)
        annotations      : function annotations
        docstring        : function docstring

    """
    spec: FullArgSpec = getfullargspec(func)  # get argspec

    if spec.defaults is not None:  # separate out argument types

        args: T.Optional[T.List[str]] = spec.args[: -len(spec.defaults)]
        defargs: T.Optional[T.List[str, T.Any]] = spec.args[
            -len(spec.defaults) :
        ]
        defaults = {k: v for k, v in zip(defargs, spec.defaults)}

    else:  # nothing to separate
        args = spec.args
        defargs = None
        defaults = None

    # build FullerArgSpec
    return FullerArgSpec(
        args=args,
        defaultargs=defargs,
        argdefaults=defaults,
        varargs=spec.varargs,
        kwonlyargs=spec.kwonlyargs,
        kwonlydefaults=spec.kwonlydefaults,
        varkw=spec.varkw,
        annotations=spec.annotations,
        docstring=func.__doc__,
    )


# /def


###########################################################################
# Signature / ArgSpec Interface


def get_annotations_from_signature(signature: Signature) -> T.Dict[str, T.Any]:
    """Get annotations from Signature object.

    Parameters
    ----------
    signature: Signature
        the object's signature

    Returns
    -------
    annotations: dict
        argument {name: annotation} values
        return annotations under key 'return'

    Examples
    --------
    >>> def func(x: 'x annotation') -> 'return annotation':
    ...   pass
    >>> sig = Signature.from_callable(func)
    >>> get_annotations_from_signature(sig)
    {'x': 'x annotation', 'return': 'return annotation'}

    """
    annotations: T.Dict[str, T.Any] = {
        k: v.annotation
        for k, v in signature.parameters.items()
        if not _is_empty(v.annotation)
    }
    if not _is_empty(signature.return_annotation):
        annotations["return"] = signature.return_annotation

    return annotations


# /def


def get_defaults_from_signature(signature: Signature) -> tuple:
    """Get defaults from Signature object.

    Parameters
    ----------
    signature: Signature
        the object's signature

    Returns
    -------
    defaults: tuple
        n-tuple for n defaulted positional parameters

    Examples
    --------
    >>> def func(x=2,):
    ...     pass
    >>> FullerSignature.from_callable(func).defaults
    (2,)

    this does not get the keyword only defaults

    >>> def func(x=2,*,k=3):
    ...     pass
    >>> FullerSignature.from_callable(func).defaults
    (2,)

    """
    return tuple(
        [
            p.default
            for p in signature.parameters.values()
            if (
                (p.kind == POSITIONAL_OR_KEYWORD) & ~_is_empty(p.default)
            )  # the kind
        ]
    )  # only defaulted


# /def


def get_kwdefaults_from_signature(signature: Signature) -> dict:
    """Get keyword-only defaults from Signature object.

    Parameters
    ----------
    signature: Signature
        the object's signature

    Returns
    -------
    defaults: dict
        argument {name: default}

    Examples
    --------
    >>> def func(x=2,*,k=3):
    ...     pass
    >>> FullerSignature.from_callable(func).kwdefaults
    {'k': 3}

    """
    return {
        n: p.default
        for n, p in signature.parameters.items()
        if ((p.kind == KEYWORD_ONLY) and not _is_empty(p.default))
    }


# /def


get_kwonlydefaults_from_signature = get_kwdefaults_from_signature


def get_kinds_from_signature(signature: Signature) -> tuple:
    """Get parameter kinds from Signature object.

    Parameters
    ----------
    signature: Signature
        the object's signature

    Returns
    -------
    kinds: tuple
        POSITIONAL_OR_KEYWORD, VAR_POSITIONAL, KEYWORD_ONLY, VAR_KEYWORD

    Examples
    --------
    >>> def func(x, *args, k=3, **kw):
    ...     pass
    >>> kinds = FullerSignature.from_callable(func).kinds
    >>> kinds[0]
    <_ParameterKind.POSITIONAL_OR_KEYWORD: 1>
    >>> kinds[1]
    <_ParameterKind.VAR_POSITIONAL: 2>
    >>> kinds[2]
    <_ParameterKind.KEYWORD_ONLY: 3>
    >>> kinds[3]
    <_ParameterKind.VAR_KEYWORD: 4>

    """
    return tuple([p.kind for p in signature.parameters.values()])


# /def


###########################################################################
# Signature Methods


def modify_parameter(
    sig: Signature,
    param: T.Union[str, int],
    name: T.Union[str, _empty] = _empty,
    kind: T.Any = _empty,
    default: T.Any = _empty,
    annotation: T.Any = _empty,
) -> Signature:
    """Modify a Parameter.

    Similar to `.replace,` but more convenient for modifying a single parameter
    Parameters are immutable, so will create a new `Signature` object

    Parameters
    ----------
    sig:  Signature
        Signature object
    param: int or str
        the parameter index (or name) in `self.parameters`
    name: str
        new parameter name, defaults to old parameter name
        **default: None**
    kind: type
        new parameter kind, defaults to old parameter kind
        **default: None**
    default: any
        new parameter default, defaults to old parameter default
        **default: None**
    annotation: any
        new parameter annotation, defaults to old parameter annotation
        **default: None**

    Returns
    -------
    Signature
        a new Signature object with the replaced parameter

    """
    # identify parameter to modify
    if isinstance(param, int):
        index = param
    else:
        index = list(sig.parameters.keys()).index(param)
    # get the parameters, and the specific param
    params = list(sig.parameters.values())
    _param = params[index]

    # replacements
    name = _param.name if name is _empty else name
    kind = _param.kind if kind is _empty else kind
    default = _param.default if default is _empty else default
    annotation = _param.annotation if annotation is _empty else annotation

    # adjust parameter list
    params[index] = _param.replace(
        name=name, kind=kind, default=default, annotation=annotation
    )

    return sig.replace(parameters=params)


# /def


def replace_with_parameter(
    sig: Signature, name: T.Union[int, str], param: Parameter
) -> Signature:
    """Replace a Parameter with another Parameter.

    Similar to `.replace,` but more convenient for modifying a single parameter
    Parameters are immutable, so will create a new `Signature` object

    Parameters
    ----------
    sig:  Signature
        Signature object
    name: int or str
        parameter to replace
    param: Parameter
        new parameter kind, defaults to old parameter kind
        **default: None**

    Returns
    -------
    Signature
        a new Signature object with the replaced parameter

    """
    # identify parameter to replace
    if isinstance(name, int):  # convert index to name
        index = name
        name = list(sig.parameters.keys())[name]
    else:
        index = list(sig.parameters.keys()).index(name)

    sig = drop_parameter(sig, name)
    sig = insert_parameter(sig, index, param)

    return sig


# /def


def insert_parameter(
    sig: Signature, index: int, param: Parameter
) -> Signature:
    """Insert a new Parameter.

    Similar to .replace, but more convenient for adding a single parameter
    Parameters are immutable, so will create a new Signature object

    Parameters
    ----------
    sig:  Signature
        Signature object
    index: int
        index into Signature.parameters at which to insert new parameter
    param: Parameter
        param to insert at index

    Returns
    -------
    Signature:
        a new Signature object with the inserted parameter

    """
    parameters = list(sig.parameters.values())
    parameters.insert(index, param)

    return sig.replace(parameters=parameters)


# /def


def prepend_parameter(sig: Signature, param: Parameter) -> Signature:
    """Insert a new Parameter at the start.

    Similar to .replace, but more convenient for adding a single parameter
    Parameters are immutable, so will create a new Signature object

    Parameters
    ----------
    sig:  Signature
        Signature object
    index: int
        index into Signature.parameters at which to insert new parameter
    param: Parameter
        param to insert at `index`

    Returns
    -------
    Signature: Signature
        a new `Signature` object with the inserted `param`

    .. todo::

        have a `skip_self` option to skip self/cls in class methods.

    """
    return insert_parameter(sig, 0, param)


# /def


def append_parameter(sig: Signature, param: Parameter) -> Signature:
    """Insert a new Parameter at the end.

    Similar to .replace, but more convenient for adding a single parameter
    Parameters are immutable, so will create a new Signature object

    Parameters
    ----------
    sig:  Signature
        Signature object
    index: int
        index into Signature.parameters at which to insert new parameter
    param: Parameter
        param to insert at `index`

    Returns
    -------
    Signature: Signature
        a new `Signature` object with the inserted `param`

    """
    kinds = get_kinds_from_signature(sig)
    return insert_parameter(sig, len(kinds) + 1, param)


# /def


def drop_parameter(
    sig: Signature, param: T.Union[str, int, Parameter, None]
) -> Signature:
    """Drop a Parameter.

    Parameters
    ----------
    sig : Signature
        Signature object
    param: str, int, Parameter
        the parameter to drop in self.parameters
        identified by either the name (str) or index (int)
        (Parameter type calls name)
        If None, does not drop anything

    Returns
    -------
    Signature:
        a new Signature object with the replaced parameter

    """
    if param is None:
        return sig
    elif isinstance(param, int):  # convert index to name
        index = param
    elif isinstance(param, str):
        index = list(sig.parameters.keys()).index(param)
    elif isinstance(param, Parameter):
        index = list(sig.parameters.keys()).index(param.name)
    else:
        raise TypeError
    # setup
    parameters = list(sig.parameters.values())

    # drop
    del parameters[index]

    return sig.replace(parameters=parameters)


# /def


###########################################################################
# Signature


class FullerSignature(Signature):
    """Signature with better ArgSpec compatibility.

    Constructs FullerSignature from the given list of Parameter
    objects and 'return_annotation'.  All arguments are optional.

    Though `Signature` is the new object, python still largely
    uses the outputs  as  defined by ``getfullargspec``
    This serves as a bridge, providing methods that return
    the same output as ``getfullargspec``

    Parameters
    ----------
    parameters : Sequence, optional
        list of Parameter objects
    return_annotation : Any
        return annotation of `obj`
    obj : Any
        the object for which this is the signature

    """

    def __init__(
        self,
        parameters=None,
        *,
        return_annotation=_empty,
        obj=None,
        __validate_parameters__=True
    ):
        super().__init__(
            parameters=parameters,
            return_annotation=return_annotation,
            __validate_parameters__=__validate_parameters__,
        )

        self.obj = obj

    # /def

    @classmethod
    def from_callable(cls, obj, *, follow_wrapped=True):
        """From callable.

        Parameters
        ----------
        obj : Callable
        follow_wrapped : bool

        Returns
        -------
        FullerSignature

        """
        sig = super().from_callable(obj, follow_wrapped=follow_wrapped)
        sig = FullerSignature(
            parameters=sig.parameters.values(),
            return_annotation=sig.return_annotation,
            obj=obj,
        )
        return sig

    # /def

    @classmethod
    def from_signature(cls, signature: Signature, *, obj=None):
        """Create :class:`FullerSignature` from :class:`~inspect.Signature`.

        Parameters
        ----------
        signature : Signature

        Returns
        -------
        FullerSignature instance

        """
        sig = cls(
            parameters=signature.parameters.values(),
            return_annotation=signature.return_annotation,
            obj=obj,
        )

        # TODO check on obj, that has matching sig as signature

        return sig

    # /def

    @format_doc(None, original_doc=Signature.bind.__doc__)
    def bind_with_defaults(self, *args, **kwargs):
        """Bind arguments to parameters.

        {original_doc}

        Applies defaults to the BoundArgument using ``apply_defaults``.

        """
        ba = self.bind(*args, **kwargs)
        ba.apply_defaults()
        return ba

    # /def

    @format_doc(None, original_doc=Signature.bind_partial.__doc__)
    def bind_partial_with_defaults(self, *args, **kwargs):
        """Bind (allowing omissions) arguments to parameters.

        {original_doc}

        Applies defaults to the BoundArgument using ``apply_defaults``.

        """
        ba = self.bind_partial(*args, **kwargs)
        ba.apply_defaults()
        return ba

    # /def

    # ------------------------------------------

    @property
    def __signature__(self) -> Signature:
        """Return a classical Signature."""
        return Signature(
            parameters=list(self.parameters.values()),
            return_annotation=self.return_annotation,
            # __validate_parameters__=False,
        )

    # /def

    @property
    def signature(self) -> Signature:
        """Return a classical Signature."""
        return self.__signature__

    # /def

    @property
    def __annotations__(self) -> dict:
        """Get annotations from Signature object.

        Returns
        -------
        annotations: dict
            argument {name: annotation} values
            return annotations under key 'return'

        Examples
        --------
        >>> def func(x: 'x annotation') -> 'return annotation':
        ...   pass
        >>> FullerSignature.from_callable(func).annotations
        {'x': 'x annotation', 'return': 'return annotation'}

        """
        annotations: T.Dict[str, T.Any] = get_annotations_from_signature(
            self.signature
        )

        return annotations

    # /def

    @property
    def annotations(self) -> T.Any:
        """Get annotations from Signature object.

        Returns
        -------
        annotations: dict
            argument {name: annotation} values
            return annotations under key 'return'

        Examples
        --------
        >>> def func(x: 'x annotation') -> 'return annotation':
        ...   pass
        >>> FullerSignature.from_callable(func).annotations
        {'x': 'x annotation', 'return': 'return annotation'}

        """
        return self.__annotations__

    # /def

    @property
    def __defaults__(self) -> T.Optional[tuple]:
        """Get defaults.

        Returns
        -------
        tuple
            n-tuple for n defaulted positional parameters

        Examples
        --------
        >>> def func(x=2,):
        ...     pass
        >>> FullerSignature.from_callable(func).defaults
        (2,)

        """
        return get_defaults_from_signature(self.signature)

    # /def

    @property
    def defaults(self) -> T.Optional[tuple]:
        """Get defaults.

        Returns
        -------
        tuple
            n-tuple for n defaulted positional parameters

        Examples
        --------
        >>> def func(x=2,):
        ...     pass
        >>> FullerSignature.from_callable(func).defaults
        (2,)

        """
        return self.__defaults__

    # /def

    @property
    def __kwdefaults__(self) -> T.Optional[dict]:
        """Get keyword-only defaults.

        Returns
        -------
        defaults: dict
            argument {name: default value}

        Examples
        --------
        >>> def func(x=2,*,k=3):
        ...     pass
        >>> FullerSignature.from_callable(func).kwdefaults
        {'k': 3}

        """
        return get_kwdefaults_from_signature(self.signature)

    # /def

    @property
    def kwdefaults(self) -> T.Optional[dict]:
        """Get keyword-only defaults.

        Returns
        -------
        defaults: dict
            argument {name: default}

        Examples
        --------
        >>> def func(x=2,*,k=3):
        ...     pass
        >>> FullerSignature.from_callable(func).kwdefaults
        {'k': 3}

        """
        return self.__kwdefaults__

    # /def

    @property
    def kwonlydefaults(self) -> T.Optional[dict]:
        """Get keyword-only defaults.

        Returns
        -------
        defaults: dict
            argument {name: default}

        Examples
        --------
        >>> def func(x=2,*,k=3):
        ...     pass
        >>> FullerSignature.from_callable(func).kwdefaults
        {'k': 3}

        """
        return self.__kwdefaults__

    # /def

    @property
    def kinds(self) -> tuple:
        """Get parameter kinds.

        Returns
        -------
        kinds: tuple
            POSITIONAL_OR_KEYWORD, VAR_POSITIONAL, KEYWORD_ONLY, VAR_KEYWORD

        Examples
        --------
        >>> def func(x, *args, k=3, **kw):
        ...     pass
        >>> kinds = FullerSignature.from_callable(func).kinds
        >>> kinds[0]
        <_ParameterKind.POSITIONAL_OR_KEYWORD: 1>
        >>> kinds[1]
        <_ParameterKind.VAR_POSITIONAL: 2>
        >>> kinds[2]
        <_ParameterKind.KEYWORD_ONLY: 3>
        >>> kinds[3]
        <_ParameterKind.VAR_KEYWORD: 4>

        """
        return get_kinds_from_signature(self.signature)

    @property
    def names(self) -> tuple:
        """Get parameter kinds.

        Returns
        -------
        names: tuple of str

        Examples
        --------
        >>> def func(x, *args, k=3, **kw):
        ...     pass
        >>> FullerSignature.from_callable(func).names
        ('x', 'args', 'k', 'kw')

        """
        return tuple(self.parameters.keys())

    # /def

    #     (args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations).
    #     'args' is a list of the parameter names.
    #     'varargs' and 'varkw' are the names of the * and ** parameters or None.
    #     'defaults' is an n-tuple of the default values of the last n parameters.
    #     'kwonlyargs' is a list of keyword-only parameter names.
    #     'kwonlydefaults' is a dictionary mapping names from kwonlyargs to defaults.
    #     'annotations' is a dictionary mapping parameter names to annotations.

    #     def fullargspec(self):
    #         return

    # ------------------------------------------

    @property
    def index_positional(self) -> _typing_tuple_false:
        """Index(ices) of positional arguments.

        This includes defaulted positional arguments.

        Returns
        -------
        tuple or False
            False if no positional arguments, tuple of indices otherwise

        """
        kinds: tuple = self.kinds
        try:
            kinds.index(1)  # POSITIONAL_OR_KEYWORD = 1
        except ValueError:
            return False
        else:
            return tuple(
                [i for i, k in enumerate(kinds) if ((k == 0) | (k == 1))]
            )

    # /def

    @property
    def index_positional_only(self) -> _typing_tuple_false:
        """Index(ices) of positional-only arguments.

        Returns
        -------
        tuple or False
            False if no positional arguments, tuple of indices otherwise

        """
        kinds: tuple = self.kinds
        try:
            kinds.index(0)  # POSITIONAL_ONLY = 0
        except ValueError:
            return False
        else:
            return tuple([i for i, k in enumerate(kinds) if (k == 0)])

    # /def

    @property
    def index_positional_defaulted(self) -> _typing_tuple_false:
        """Index(ices) of positional arguments with default values.

        FIXME, wrong b/c returns indices of POSITIONAL_OR_KEYWORD arguments
        that do not have defaults

        Returns
        -------
        tuple or False
            False if no positional arguments, tuple of indices otherwise

        """
        kinds: tuple = self.kinds
        try:
            kinds.index(1)  # POSITIONAL_OR_KEYWORD = 1
        except ValueError:
            return False
        else:
            pos_only: list = self.index_positional_only or []

            return tuple(
                [
                    i
                    for i, k in enumerate(kinds)
                    if ((k == 1) & (i not in pos_only))
                ]
            )

    # /def

    @property
    def index_var_positional(self) -> T.Union[int, Literal[False]]:
        """Index of `*args`.

        Returns
        -------
        int or False
            False if no variable positional argument, index int otherwise

        """
        kinds = self.kinds
        try:
            kinds.index(2)  # VAR_POSITIONAL = 2
        except ValueError:
            return False
        else:
            return kinds.index(2)

    # /def

    @property
    def index_keyword_only(self) -> _typing_tuple_false:
        """Index of `*args`.

        Returns
        -------
        tuple or False
            False if no keyword-only arguments, tuple of indices otherwise

        """
        kinds = self.kinds
        try:
            kinds.index(3)  # KEYWORD_ONLY = 3
        except ValueError:
            return False
        else:
            return tuple([i for i, k in enumerate(kinds) if (k == 3)])

    # /def

    @property
    def index_end_keyword_only(self) -> int:
        """Index to place new keyword-only parameters.

        Returns
        -------
        int
            var_keyword index if var_keyword exists, last index otherwise

        """
        index = self.index_var_keyword
        if index is False:  # no variable kwargs
            index = len(self.kinds) + 1
        return index

    # /def

    @property
    def index_var_keyword(self) -> T.Union[int, Literal[False]]:
        """Index of `**kwargs`.

        Returns
        -------
        int or False
            False if no variable keyword argument, index int otherwise

        """
        kinds = self.kinds
        try:
            kinds.index(4)  # VAR_KEYWORD = 4
        except ValueError:
            return False
        else:
            return kinds.index(4)

    # /def

    # ------------------------------------------

    def copy(self):
        """Copy of self."""
        return self.replace(parameters=list(self.parameters.values()))

    # ------------------------------------------

    def modify_parameter(
        self,
        param: T.Union[str, int],
        name: T.Union[str, _empty] = _empty,
        kind: T.Any = _empty,
        default: T.Any = _empty,
        annotation: T.Any = _empty,
    ):
        """Modify a Parameter.

        Similar to `.replace,` but more convenient for modifying a single parameter
        Parameters are immutable, so will create a new `Signature` object

        Parameters
        ----------
        param: int or str
            the parameter index (or name) in `self.parameters`
        name: str
            new parameter name, defaults to old parameter name
            **default: None**
        kind: type
            new parameter kind, defaults to old parameter kind
            **default: None**
        default: T.Any
            new parameter default, defaults to old parameter default
            **default: None**
        annotation: T.Any
            new parameter annotation, defaults to old parameter annotation
            **default: None**

        Returns
        -------
        FullerSignature
            a new Signature object with the replaced parameter

        """
        return modify_parameter(
            self,
            param=param,
            name=name,
            kind=kind,
            default=default,
            annotation=annotation,
        )

    # /def

    def replace_with_parameter(
        self, name: T.Union[int, str], param: Parameter
    ):
        """Replace a Parameter with another Parameter.

        Similar to `.replace,` but more convenient for modifying a single parameter
        Parameters are immutable, so will create a new `Signature` object

        Parameters
        ----------
        name: int or str
            parameter to replace
        param: Parameter
            new parameter kind, defaults to old parameter kind
            **default: None**

        Returns
        -------
        FullerSignature
            a new Signature object with the replaced parameter

        """
        return replace_with_parameter(self, name, param)

    # /def

    def insert_parameter(self, index: int, parameter: Parameter):
        """Insert a new Parameter.

        Similar to .replace, but more convenient for adding a single parameter
        Parameters are immutable, so will create a new Signature object

        Parameters
        ----------
        index: int
            index into Signature.parameters at which to insert new parameter
        parameter: Parameter
            parameter to insert at `index`

        Returns
        -------
        FullerSignature
            a new `Signature` object with the inserted `parameter`

        """
        return insert_parameter(self, index, parameter)

    # /def

    def prepend_parameter(self, param: Parameter):
        """Insert a new Parameter at the start.

        Similar to .replace, but more convenient for adding a single parameter
        Parameters are immutable, so will create a new Signature object

        Parameters
        ----------
        index: int
            index into Signature.parameters at which to insert new parameter
        param: Parameter
            param to insert at `index`

        Returns
        -------
        FullerSignature
            a new `Signature` object with the inserted `param`

        .. todo::

            have a `skip_self` option to skip self/cls in class methods.

        """
        return prepend_parameter(self, param)

    # /def

    def append_parameter(self, param: Parameter):
        """Insert a new Parameter at the end.

        Similar to .replace, but more convenient for adding a single parameter
        Parameters are immutable, so will create a new Signature object

        Parameters
        ----------
        index: int
            index into Signature.parameters at which to insert new parameter
        param: Parameter
            param to insert at `index`

        Returns
        -------
        FullerSignature
            a new `Signature` object with the inserted `param`

        """
        return append_parameter(self, param)

    # /def

    def drop_parameter(self, param: str):
        """Drop a Parameter.

        Parameters
        ----------
        param: str
            the parameter name in self.parameters

        Returns
        -------
        FullerSignature
            a new FullerSignature object with the replaced parameter

        """
        return drop_parameter(self, param)

    # /def

    def _default_pos_to_kwonly_from(self, index: int = 0):
        """Promote default positional to keyword only arguments.

        Parameter
        ---------
        index: int, optional
            default positional arguments after `index`
            will be changed to keyword only arguments
            ``None`` changes all available arguments

            example, (x, y=2, z=3) with index 1 means only z is changed
            because the defaults are (2, 3)

        Returns
        -------
        Signature
            a new Signature object with the promoted parameters

        TODO
        ----
        return list/info of parameters promoted

        """
        signature: FullerSignature = self

        if signature.defaults is None:  # no defaults
            return signature

        # promote parameters
        i: int
        for i in signature.index_positional_defaulted[index:][::-1]:
            signature = signature.modify_parameter(i, kind=KEYWORD_ONLY)

        return signature

    # /def

    def add_var_positional_parameter(
        self, name: str = "args", index: T.Optional[int] = None
    ):
        """Add var positional parameter.

        Does not add if one already exists.

        Parameters
        ----------
        name: str
            the var_positional argument name
            (default 'args')
        index: int, optional
            the index at which to place the var_positional_parameter
            default positional arguments after the var_positional parameter
            will be changed to keyword only arguments

        Returns
        -------
        Signature
            a new Signature object with the new var_positional parameter
            and also promoted parameters if `promote_default_pos`=True

        """
        signature: FullerSignature = self

        if self.index_var_positional is not False:  # already exists
            pass

        else:  # doesn't have ``*``

            if index is not None:
                # promote default-valued positional arguments to kwargs
                if index in self.index_positional_defaulted:
                    pos_index = self.index_positional_defaulted.index(index)
                elif index < self.index_positional_defaulted[0]:
                    pos_index = None
                else:
                    pos_index = self.index_positional_defaulted[-1] + 1

                signature = self._default_pos_to_kwonly_from(index=pos_index)

            else:  # has no defaulted positionals
                if not self.index_positional:  # no positional
                    index = 0
                else:
                    index = self.index_positional[-1] + 1

            signature = signature.insert_parameter(
                index,
                Parameter(name, VAR_POSITIONAL),
            )

        return signature

    # /def

    def add_var_keyword_parameter(self, name: str = "kwargs"):
        """Add var keyword parameter.

        Does not add if one already exists.

        Parameters
        ----------
        name: str
            the var_keyword argument name
            (default 'kwargs')

        Returns
        -------
        FullerSignature
            a new Signature object with the new var_positional parameter
            and also promoted parameters if `promote_default_pos`=True

        """
        signature: FullerSignature

        if self.index_keyword_only is not False:  # already exists
            signature = self

        else:
            signature = self.append_parameter(
                Parameter(name, VAR_KEYWORD),
            )

        return signature

    # /def


# ------------------------------------------------------------------------


def fuller_signature(obj: T.Callable, *, follow_wrapped: bool = True):
    """Get a signature object for the passed callable."""
    return FullerSignature.from_callable(obj, follow_wrapped=follow_wrapped)


# /def


###########################################################################
# Signature Convenience Methods


def fuller_signature_from_method(method: T.Callable):
    sig = fuller_signature(method)

    if tuple(sig.parameters.keys())[0] == "self":
        sig = sig.drop_parameter("self")
    elif tuple(sig.parameters.keys())[0] == "cls":
        sig = sig.drop_parameter("cls")

    return sig


# /def


def signature_from_method(method: T.Callable):
    sig = inspect.signature(method)

    if tuple(sig.parameters.keys())[0] == "self":
        sig = drop_parameter(sig, "self")
    elif tuple(sig.parameters.keys())[0] == "cls":
        sig = sig.drop_parameter("cls")

    return sig


# /def


##############################################################################
# END
