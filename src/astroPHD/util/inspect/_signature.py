"""Added functionality to ``inspect.signature``.

Routine Listings
----------------
Signature

get_annotations_from_signature

get_defaults_from_signature

get_kwdefaults_from_signature

get_kwonlydefaults_from_signature

replace_parameter

insert_parameter

drop_parameter


TODO
----
have the `get_` methods use `Signature.method` if it is my custom signature object

"""

__author__ = "Nathaniel Starkman"

__all__ = [
    # Signature
    'Signature',
    # Signature / ArgSpec Interface
    'get_annotations_from_signature',
    'get_defaults_from_signature',
    'get_kwdefaults_from_signature',
    'get_kwonlydefaults_from_signature',
    # Signature Methods
    'replace_parameter',
    'insert_parameter',
    'drop_parameter',
]


##############################################################################
# IMPORTS

# General
import inspect
from inspect import Parameter

# Project-Specific
from ..metaclasses import InheritDocstrings


##############################################################################
# Parameters

_POSITIONAL_ONLY = Parameter.POSITIONAL_ONLY
_POSITIONAL_OR_KEYWORD = Parameter.POSITIONAL_OR_KEYWORD
_VAR_POSITIONAL = Parameter.VAR_POSITIONAL
_KEYWORD_ONLY = Parameter.KEYWORD_ONLY
_VAR_KEYWORD = Parameter.VAR_KEYWORD

_empty = inspect._empty


##############################################################################
# Signature / ArgSpec Interface

def get_annotations_from_signature(signature: inspect.Signature):
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
    annotations = {k: v.annotation for k, v in signature.parameters.items()
                   if v.annotation != _empty}
    annotations['return'] = signature.return_annotation
    return annotations
# /def


def get_defaults_from_signature(signature: inspect.Signature):
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
    return tuple([p.default for p in signature.parameters.values()
                  if ((p.kind == _POSITIONAL_OR_KEYWORD) &  # the kind
                      (p.default != _empty))])     # only defaulted
# /def


def get_kwdefaults_from_signature(signature: inspect.Signature):
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
    return {n: p.default for n, p in signature.parameters.items()
            if ((p.kind == _KEYWORD_ONLY) &
                (p.default != _empty))}
# /def


get_kwonlydefaults_from_signature = get_kwdefaults_from_signature


def get_kinds_from_signature(signature: inspect.Signature):
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

class Signature(inspect.Signature, metaclass=InheritDocstrings):
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
    def __signature__(self):
        """Return a classical Signature."""
        return inspect.Signature(parameters=list(self.parameters.values()),
                                 return_annotation=self._return_annotation,
                                 __validate_parameters__=False)
    # /def

    @property
    def signature(self):
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
        res = {k: v.annotation for k, v in self.parameters.items()
               if v.annotation != _empty}
        if self.return_annotation is not _empty:
            res['return'] = self.return_annotation
        return res
    # /def

    @property
    def annotations(self) -> dict:
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
    def __defaults__(self) -> tuple:
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
        out = tuple([p.default for p in self.parameters.values()
                     if ((p.kind == _POSITIONAL_OR_KEYWORD) &
                         (p.default != _empty))])
        if out == ():  # empty list
            return None
        else:
            return out
    # /def

    @property
    def defaults(self) -> tuple:
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
    def __kwdefaults__(self) -> dict:
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
        out = {n: p.default for n, p in self.parameters.items()
               if ((p.kind == _KEYWORD_ONLY) &
                   (p.default != _empty))}
        if out == {}:  # empty dict
            return None
        else:
            return out
    # /def

    @property
    def kwdefaults(self) -> dict:
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
    def kwonlydefaults(self) -> dict:
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
    def index_positional(self) -> (tuple, False):
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
    def index_var_positional(self) -> (int, False):
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
    def index_keyword_only(self) -> (tuple, False):
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
    def index_var_keyword(self) -> (int, False):
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

    def copy(self):
        """Copy of self."""
        return self.replace(parameters=list(self.parameters.values()))

    # ------------------------------------------

    def replace_parameter(self, param: str, name: str=None, kind=None,
                          default=None, annotation=None):
        """Replace a Parameter.

        Similar to `.replace,` but more convenient for modifying a single parameter
        Parameters are immutable, so will create a new `Signature` object

        Parameters
        ----------
        param: str
            the parameter name in `self.parameters`
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
        Signature:
            a new Signature object with the replaced parameter

        """
        # setup
        index = list(self.parameters.keys()).index(param)
        params = list(self.parameters.values())
        param = params[index]

        name = param.name if name is None else name
        kind = param.kind if kind is None else kind
        default = param.default if default is None else default
        annotation = param.annotation if annotation is None else annotation

        # adjust parameter list
        params[index] = param.replace(name=name, kind=kind, default=default,
                                      annotation=annotation)

        return self.replace(parameters=params)
    # /def

    def replace_with_parameter(self, name: (int, str), param: Parameter):
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
        Signature:
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
        Signature: Signature
            a new `Signature` object with the inserted `parameter`

        """
        params = list(self.parameters.values())
        params.insert(index, parameter)

        return self.replace(parameters=params)
    # /def

    def drop_parameter(self, param: str):
        """Drop a Parameter.

        Parameters
        ----------
        param: str
            the parameter name in self.parameters

        Returns
        -------
        Signature:
            a new Signature object with the replaced parameter

        """
        # setup
        index = list(self.parameters.keys()).index(param)
        params = list(self.parameters.values())

        # drop
        del params[index]

        return self.replace(parameters=params)
    # /def


# ----------------------------------------------------------------------------

def signature(obj, *, follow_wrapped: bool=True) -> Signature:
    """Get a signature object for the passed callable."""
    return Signature.from_callable(obj, follow_wrapped=follow_wrapped)


##############################################################################
# Signature Methods
# TODO replace as method versions from Signature, can use semi-static for this


def replace_parameter(signature: inspect.Signature, param: str, name: str=None,
                      kind=None, default=None, annotation=None,
                      return_annotation=None) -> Signature:
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
    param = params[index]

    # replace
    name = param.name if name is None else name
    kind = param.kind if kind is None else kind
    default = param.default if name is None else default
    annotation = param.annotation if name is None else annotation

    # adjust parameter list
    params[index] = param.replace(name=name, kind=kind, default=default,
                                  annotation=annotation,
                                  return_annotation=return_annotation)

    return signature.replace(parameters=params)
# /def


def insert_parameter(signature: inspect.Signature, index: int,
                     parameter: Parameter) -> Signature:
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


def drop_parameter(signature: Signature, param: str) -> Signature:
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


# def f1():
#     pass
# # inspect.signature(f1).kinds

# def f2(x, y):
#     pass
# # inspect.signature(f2).kinds

# def f3(x, y, a=10, b=11):
#     pass
# # inspect.signature(f3).kinds

# def f4(x, y, a=10, b=11, *args):
#     pass
# # inspect.signature(f4).kinds
# # inspect.signature(f4).var_pos_index

# def f5(x, y, a=10, b=11, *args, k='one', l='two'):
#     pass
# # inspect.signature(f5).kinds

# def f6(x, y, a=10, b=11, *args, k='one', **kw):
#     pass
# inspect.signature(f6).kinds
# inspect.signature(f6).index_positional
# inspect.signature(f6).index_var_positional
# inspect.signature(f6).index_keyword_only
# inspect.signature(f6).index_var_keyword

# np.array(inspect.signature(f6).kinds)[list(inspect.signature(f6).index_positional)]
