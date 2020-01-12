# -*- coding: utf-8 -*-

"""initialization file for `inspect`."""

__author__ = "Nathaniel Starkman"

# __all__ = [
#     # Signature
#     'Signature',
#     # Signature / ArgSpec Interface
#     'get_annotations_from_signature',
#     'get_defaults_from_signature',
#     'get_kwdefaults_from_signature',
#     'get_kwonlydefaults_from_signature',
#     # Signature Methods
#     'replace_parameter',
#     'insert_parameter',
#     'drop_parameter',
#     # FullerArgSpec,
#     ''
# ]

##############################################################################
# IMPORTS

# GENERAL
from inspect import *
import inspect as _inspect
from inspect import (
    getfullargspec,
    FullArgSpec,
    Parameter,
    Signature as _Signature,
)

from typing import (
    Callable as _Callable,
    Union as _Union,
    Any as _Any,
    Optional as _Optional,
)
from typing_extensions import Literal as _Literal
from collections import namedtuple as _namedtuple

# PROJECT-SPECIFIC
from .metaclasses import InheritDocstrings as _InheritDocstrings

##############################################################################
# Parameters

_POSITIONAL_ONLY = Parameter.POSITIONAL_ONLY
_POSITIONAL_OR_KEYWORD = Parameter.POSITIONAL_OR_KEYWORD
_VAR_POSITIONAL = Parameter.VAR_POSITIONAL
_KEYWORD_ONLY = Parameter.KEYWORD_ONLY
_VAR_KEYWORD = Parameter.VAR_KEYWORD

_empty = Parameter.empty


##############################################################################
# Types

FullerArgSpec: _namedtuple = _namedtuple(
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
# getfullerargspec


def getfullerargspec(func: _Callable) -> FullerArgSpec:
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
        kwonlyargs       : key-word only arguments
        kwonlydefaults   : key-word only argument defaults
        varkw            : variable key-word arguments (kwargs)
        annotations      : function annotations
        docstring        : function docstring

    """
    spec: FullArgSpec = getfullargspec(func)  # get argspec

    if spec.defaults is not None:  # separate out argument types

        args = spec.args[: -len(spec.defaults)]
        defargs = spec.args[-len(spec.defaults) :]
        defaults = {k: v for k, v in zip(defargs, spec.defaults)}

    else:  # nothing to separate
        args = spec.args
        defargs = None
        defaults = None

    # build FullerArgSpec
    return FullerArgSpec(
        args,
        defargs,
        defaults,
        spec.varargs,
        spec.kwonlyargs,
        spec.kwonlydefaults,
        spec.varkw,
        spec.annotations,
        func.__doc__,
    )


# /def


##############################################################################
# Signature / ArgSpec Interface


def get_annotations_from_signature(signature: _Signature) -> dict:
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
    >>> Signature(func).annotations
    {'x': 'x annotation', 'return': 'return annotation'}

    """
    annotations = {
        k: v.annotation
        for k, v in signature.parameters.items()
        if v.annotation != _empty
    }
    annotations["return"] = signature.return_annotation
    return annotations


# /def


def get_defaults_from_signature(signature: _Signature) -> tuple:
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
    >>> Signature(func).defaults
    (2,)

    this does not get the keyword only defaults

    >>> def func(x=2,*,k=3):
    ...     pass
    >>> Signature(func).defaults
    (2,)

    """
    return tuple(
        [
            p.default
            for p in signature.parameters.values()
            if (
                (p.kind == _POSITIONAL_OR_KEYWORD) & (p.default != _empty)
            )  # the kind
        ]
    )  # only defaulted


# /def


def get_kwdefaults_from_signature(signature: _Signature) -> dict:
    """Get key-word only defaults from Signature object.

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
    >>> def func(*, k=3):
    ...     pass
    >>> Signature(func).kwdefaults
    (3,)

    this does not get the positional arguments with defaults

    >>> def func(x=2,*,k=3):
    ...     pass
    >>> Signature(func).kwdefaults
    (3,)

    """
    return {
        n: p.default
        for n, p in signature.parameters.items()
        if ((p.kind == _KEYWORD_ONLY) & (p.default != _empty))
    }


# /def


get_kwonlydefaults_from_signature = get_kwdefaults_from_signature


def get_kinds_from_signature(signature: _Signature) -> tuple:
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
    >>> Signature(func).kinds
    [POSITIONAL_OR_KEYWORD, VAR_POSITIONAL, KEYWORD_ONLY]

    """
    return tuple([p.kind for p in signature.parameters.values()])


# /def


##############################################################################
# Signature


class Signature(_Signature, metaclass=_InheritDocstrings):
    """Signature with better ArgSpec compatibility.

    Though `Signature` is the new object, python still largely
    uses the outputs  as  defined by ``getfullargspec``
    This serves as a bridge, providing methods that return
    the same output as ``getfullargspec``

    Methods
    -------
    signature
    annotations
    defaults
    kwdefaults
    kwonlydefaults
    replace_parameter
    insert_parameter
    drop_parameter

    """

    # ------------------------------------------

    # def __init__(self, parameters=None, *, return_annotation,
    #              # docstring=None,
    #              __validate_parameters__=True):
    #     super().__init__(parameters=parameters,
    #                      return_annotation=return_annotation,
    #                      __validate_parameters__=__validate_parameters__)
    #     # self.docstring = docstring
    #     return
    # # /def

    # @classmethod
    # def from_callable(cls, obj, *, follow_wrapped=True):
    #     sig = super().from_callable(obj, follow_wrapped=follow_wrapped)
    #     # sig.docstring = obj.__doc__
    #     return sig
    # # /def

    # ------------------------------------------

    @property
    def __signature__(self) -> _Signature:
        """Return a classical Signature."""
        return _Signature(
            parameters=list(self.parameters.values()),
            return_annotation=self._return_annotation,
            __validate_parameters__=False,
        )

    # /def

    @property
    def signature(self) -> _Signature:
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
        >>> Signature(func).annotations
        {'x': 'x annotation', 'return': 'return annotation'}

        """
        res = {
            k: v.annotation
            for k, v in self.parameters.items()
            if v.annotation != _empty
        }
        if self.return_annotation is not _empty:
            res["return"] = self.return_annotation
        return res

    # /def

    @property
    def annotations(self) -> _Any:
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
        >>> Signature(func).annotations
        {'x': 'x annotation', 'return': 'return annotation'}

        """
        return self.__annotations__

    # /def

    @property
    def __defaults__(self) -> _Optional[tuple]:
        """Get defaults.

        Returns
        -------
        tuple
            n-tuple for n defaulted positional parameters

        Examples
        --------
        >>> def func(x=2,):
        ...     pass
        >>> Signature(func).defaults
        (2,)

        """
        out = tuple(
            [
                p.default
                for p in self.parameters.values()
                if ((p.kind == _POSITIONAL_OR_KEYWORD) & (p.default != _empty))
            ]
        )
        if out == ():  # empty list
            return None
        else:
            return out

    # /def

    @property
    def defaults(self) -> _Optional[tuple]:
        """Get defaults.

        Returns
        -------
        tuple
            n-tuple for n defaulted positional parameters

        Examples
        --------
        >>> def func(x=2,):
        ...     pass
        >>> Signature(func).defaults
        (2,)

        """
        return self.__defaults__

    # /def

    @property
    def __kwdefaults__(self) -> _Optional[dict]:
        """Get key-word only defaults.

        Returns
        -------
        defaults: dict
            argument {name: default}

        Examples
        --------
        >>> def func(*, x=2):
        ...     pass
        >>> Signature(func).kwdefaults
        (2,)

        this does not get the positional arguments with defaults

        >>> def func(x=2,*,k=3):
        ...     pass
        >>> Signature(func).kwdefaults
        (3,)

        """
        out = {
            n: p.default
            for n, p in self.parameters.items()
            if ((p.kind == _KEYWORD_ONLY) & (p.default != _empty))
        }
        if out == {}:  # empty dict
            return None
        else:
            return out

    # /def

    @property
    def kwdefaults(self) -> _Optional[dict]:
        """Get key-word only defaults.

        Returns
        -------
        defaults: dict
            argument {name: default}

        Examples
        --------
        >>> def func(*, x=2):
        ...     pass
        >>> Signature(func).kwdefaults
        (2,)

        this does not get the positional arguments with defaults

        >>> def func(x=2,*,k=3):
        ...     pass
        >>> Signature(func).kwdefaults
        (3,)

        """
        return self.__kwdefaults__

    # /def

    @property
    def kwonlydefaults(self) -> _Optional[dict]:
        """Get key-word only defaults.

        Returns
        -------
        defaults: dict
            argument {name: default}

        Examples
        --------
        >>> def func(*, x=3):
        ...     pass
        >>> Signature(func).kwdefaults
        (3,)

        this does not get the positional arguments with defaults

        >>> def func(x=2,*,k=3):
        ...     pass
        >>> Signature(func).kwdefaults
        (3,)

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
        >>> Signature(func).kinds
        [POSITIONAL_OR_KEYWORD, VAR_POSITIONAL, KEYWORD_ONLY]

        """
        return tuple([p.kind for p in self.parameters.values()])

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
    def index_positional(self) -> _Union[tuple, _Literal[False]]:
        """Index(ices) of positional arguments.

        This includes defaulted positional arguments.

        Returns
        -------
        tuple or False
            False if no positional arguments, tuple of indices otherwise

        """
        kinds = self.kinds
        try:
            kinds.index(1)  # _POSITIONAL_OR_KEYWORD = 1
        except ValueError:
            return False
        else:
            return tuple([i for i, k in enumerate(kinds) if (k == 1)])

    # /def

    @property
    def index_var_positional(self) -> _Union[int, _Literal[False]]:
        """Index of `*args`.

        Returns
        -------
        int or False
            False if no variable positional argument, index int otherwise

        """
        kinds = self.kinds
        try:
            kinds.index(2)  # _VAR_POSITIONAL = 2
        except ValueError:
            return False
        else:
            return kinds.index(2)

    # /def

    @property
    def index_keyword_only(self) -> _Union[tuple, _Literal[False]]:
        """Index of `*args`.

        Returns
        -------
        tuple or False
            False if no keyword-only arguments, tuple of indices otherwise

        """
        kinds = self.kinds
        try:
            kinds.index(3)  # _KEYWORD_ONLY = 3
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
    def index_var_keyword(self) -> _Union[int, _Literal[False]]:
        """Index of `**kwargs`.

        Returns
        -------
        int or False
            False if no variable keyword argument, index int otherwise

        """
        kinds = self.kinds
        try:
            kinds.index(4)  # _VAR_KEYWORD = 4
        except ValueError:
            return False
        else:
            return kinds.index(4)

    # /def

    # ------------------------------------------

    def copy(self) -> _Signature:
        """Copy of self."""
        return self.replace(parameters=list(self.parameters.values()))

    # ------------------------------------------

    def replace_parameter(
        self,
        param: _Union[str, int],
        name: _Optional[str] = None,
        kind: _Any = None,
        default: _Any = None,
        annotation: _Any = None,
    ) -> _Signature:
        """Replace a Parameter.

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
        # setup
        if isinstance(param, int):
            index = param
        else:
            index = list(self.parameters.keys()).index(param)
        params = list(self.parameters.values())
        _param = params[index]

        name = _param.name if name is None else name
        kind = _param.kind if kind is None else kind
        default = _param.default if default is None else default
        annotation = _param.annotation if annotation is None else annotation

        # adjust parameter list
        params[index] = _param.replace(
            name=name, kind=kind, default=default, annotation=annotation
        )

        return self.replace(parameters=params)

    # /def

    def replace_with_parameter(
        self, name: _Union[int, str], param: Parameter
    ) -> _Any:
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
        Signature
            a new Signature object with the replaced parameter

        """
        # setup
        if isinstance(name, int):  # convert index to name
            index = name
            name = list(self.parameters.keys())[name]
        else:
            index = list(self.parameters.keys()).index(name)

        signature = self.drop_parameter(name)
        signature = signature.insert_parameter(index, param)

        return signature

    # /def

    def insert_parameter(self, index: int, parameter: Parameter) -> _Signature:
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
        Signature: Signature
            a new `Signature` object with the inserted `parameter`

        """
        params = list(self.parameters.values())
        params.insert(index, parameter)

        return self.replace(parameters=params)

    # /def

    def prepend_parameter(self, parameter: Parameter) -> _Signature:
        """Insert a new Parameter at the start.

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
        Signature: Signature
            a new `Signature` object with the inserted `parameter`

        TODO
        ----
        have a `skip_self` option to skip self/cls in class methods.

        """
        return self.insert_parameter(0, parameter)

    # /def

    def append_parameter(self, parameter: Parameter) -> _Signature:
        """Insert a new Parameter at the end.

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
        Signature: Signature
            a new `Signature` object with the inserted `parameter`

        """
        return self.insert_parameter(len(self.kinds) + 1, parameter)

    # /def

    def drop_parameter(self, param: str) -> _Signature:
        """Drop a Parameter.

        Parameters
        ----------
        param: str
            the parameter name in self.parameters

        Returns
        -------
        Signature
            a new Signature object with the replaced parameter

        """
        # setup
        index = list(self.parameters.keys()).index(param)
        params = list(self.parameters.values())

        # drop
        del params[index]

        return self.replace(parameters=params)

    # /def

    def promote_default_pos_to_kwonly(self):
        """Promote default positional to keyword only arguments.

        Returns
        -------
        Signature
            a new Signature object with the promoted parameters

        Raises
        ------
        ValueError: no positional arguments

        TODO
        ----
        return list/info of parameters promoted

        """
        # if self.index_var_positional is False:
        #     raise AttributeError("there is no existing var_positional (*arg)")
        if self.index_positional is False:
            raise ValueError("no positional arguments")

        signature: Signature = self

        if signature.defaults is None:  # no defaults
            return signature

        num_defaults: int = len(signature.defaults)
        index: int = signature.index_positional[-num_defaults]
        # promote parameters
        i: int
        for i in range(num_defaults):
            signature = signature.replace_parameter(
                index + num_defaults - i - 1, kind=_KEYWORD_ONLY
            )

        return signature

    # /def

    def add_var_positional_parameter(
        self, name: str='args', promote_default_pos: bool = False
    ):
        """Add var positional parameter.

        Does not add if one already exists. Can still promote.

        Parameters
        ----------
        name: str
            the var_positional argument name
            (default 'args')
        promote_default_pos: bool
            whether to promote default positional to keyword only arguments

        Returns
        -------
        Signature
            a new Signature object with the new var_positional parameter
            and also promoted parameters if `promote_default_pos`=True

        """
        if self.index_var_positional is not False:  # already exists
            if promote_default_pos:
                self.promote_default_pos_to_kwonly()
            else:
                pass

        else:  # doesn't have ``*``
            signature: Signature = self

            if promote_default_pos:
                # promote default-valued positional arguments to kwargs
                if self.defaults is not None:  # has defaulted positionals
                    index = self.index_positional[-len(self.defaults)]
                    signature = self.promote_default_pos_to_kwonly()
                else:  # has no defaulted positionals
                    index = len(self.index_positional) + 1
            else:
                index = len(self.index_positional) + 1

            signature = signature.insert_parameter(
                index, Parameter(name, _VAR_POSITIONAL),
            )

        return signature

    # /def

    def add_var_keyword_parameter(self, name: str='kwargs'):
        """Add var keyword parameter.

        Does not add if one already exists.

        Parameters
        ----------
        name: str
            the var_keyword argument name
            (default 'kwargs')

        Returns
        -------
        Signature
            a new Signature object with the new var_positional parameter
            and also promoted parameters if `promote_default_pos`=True

        """
        if self.index_keyword_only is not False:  # already exists
            signature = self

        else:
            signature = self.append_parameter(
                Parameter(name, _VAR_KEYWORD),
            )

        return signature

    # /def


# ----------------------------------------------------------------------------


def signature(obj: _Any, *, follow_wrapped: bool = True) -> _Any:
    """Get a signature object for the passed callable."""
    return Signature.from_callable(obj, follow_wrapped=follow_wrapped)


##############################################################################
# Signature Methods
# TODO replace as method versions from Signature, can use semi-static for this


def replace_parameter(
    signature: _Signature,
    param: str,
    name: str = None,
    kind=None,
    default=None,
    annotation=None,
    return_annotation=None,
) -> Signature:
    """Replace a Parameter.

    Similar to .replace, but more convenient for modifying a single parameter
    Parameters are immutable, so will create a new Signature object

    Parameters
    ----------
    signature:  Signature
        Signature object
    param: str
        the parameter name in self.parameters
    name: str  (default None)
        new parameter name, defaults to old parameter name
    kind: type  (default None)
        new parameter kind, defaults to old parameter kind
    default: any  (default None)
        new parameter default, defaults to old parameter default
    annotation: any  (default None)
        new parameter annotation, defaults to old parameter annotation

    Returns
    -------
    Signature:
        a new Signature object with the replaced parameter

    """
    # setup
    index = list(signature.parameters.keys()).index(param)
    params = list(signature.parameters.values())
    _param = params[index]

    # replace
    name = _param.name if name is None else name
    kind = _param.kind if kind is None else kind
    default = _param.default if name is None else default
    annotation = _param.annotation if name is None else annotation

    # adjust parameter list
    params[index] = _param.replace(
        name=name,
        kind=kind,
        default=default,
        annotation=annotation,
        return_annotation=return_annotation,
    )

    return signature.replace(parameters=params)


# /def


def insert_parameter(
    signature: _Signature, index: int, parameter: Parameter
) -> _Any:
    """Insert a new Parameter.

    Similar to .replace, but more convenient for adding a single parameter
    Parameters are immutable, so will create a new Signature object

    Parameters
    ----------
    index: int
        index into Signature.parameters at which to insert new parameter
    parameter: Parameter
        parameter to insert at index

    Returns
    -------
    Signature:
        a new Signature object with the inserted parameter

    """
    params = list(signature.parameters.values())
    params.insert(index, parameter)

    return signature.replace(parameters=params)


# /def


def drop_parameter(signature: Signature, param: str) -> _Any:
    """Drop a Parameter.

    Parameters
    ----------
    signature : Signature
        Signature object
    param: str
        the parameter name in self.parameters

    Returns
    -------
    Signature:
        a new Signature object with the replaced parameter

    """
    # setup
    index = list(signature.parameters.keys()).index(param)
    params = list(signature.parameters.values())

    # drop
    del params[index]

    return signature.replace(parameters=params)


# /def


##############################################################################
# END
