"""signature.

Notes
-----
? have the get_ methods use Signature.___ if it is my custom signature object

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

# Project-Specific
from ..metaclasses import InheritDocstrings


##############################################################################
# Parameters

POSITIONAL_OR_KEYWORD = inspect.Parameter.POSITIONAL_OR_KEYWORD
KEYWORD_ONLY = inspect.Parameter.KEYWORD_ONLY


##############################################################################
# Signature / ArgSpec Interface

def get_annotations_from_signature(signature):
    """Get annotations from Signature object.

    ex: def f(x: 'x annotation') -> 'return annotation':
            pass
    -> {'x': 'x annotation', 'return': 'return annotation'}

    Parameters
    ----------
    signature: Signature
        the object's signature

    Returns
    -------
    annotations: dict
        argument {name: annotation} values
        return annotations under key 'return'

    """
    annotations = {k: v.annotation for k, v in signature.parameters.items()
                   if v.annotation != inspect._empty}
    annotations['return'] = signature.return_annotation
    return annotations
# /def


def get_defaults_from_signature(signature):
    """Get defaults from Signature object.

    ex: def f(x=2):
            pass
    -> (2,)

    Parameters
    ----------
    signature: Signature
        the object's signature

    Returns
    -------
    defaults: tuple
        n-tuple for n defaulted positional parameters

    """
    return tuple([p.default for p in signature.parameters.values()
                  if ((p.kind == POSITIONAL_OR_KEYWORD) &  # the type
                      (p.default != inspect._empty))])     # only defaulted
    # TODO replace p.default != inspect._empty with
    #              p.kind != POSITIONAL_ONLY
# /def


def get_kwdefaults_from_signature(signature):
    """Get key-word only defaults from Signature object.

    ex: def f(x=2):
            pass
    -> (2,)

    Parameters
    ----------
    signature: Signature
        the object's signature

    Returns
    -------
    defaults: dict
        argument {name: default}

    """
    return {n: p.default for n, p in signature.parameters.items()
            if ((p.kind == KEYWORD_ONLY) &
                (p.default != inspect._empty))}
# /def


get_kwonlydefaults_from_signature = get_kwdefaults_from_signature


##############################################################################
# Signature

class Signature(inspect.Signature, metaclass=InheritDocstrings):
    """Signature with better ArgSpec bridges.

    Though Signature is the new object, python still largely
    uses the outputs  as  defined by getfullargspec
    This serves as a bridge, providing methods that return
    the same output as getfullargspec

    New Methods
    -----------
    annotations
    defaults
    kwdefaults / kwonlydefaults
    replace_parameter
    insert_parameter

    Modified Methods
    ----------------
    __init__
    from_callable

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
    def signature(self):
        """TODO Return a classical Signature."""
        return self
    # /def

    @property
    def annotations(self):
        """Get annotations from Signature object.

        ex: def f(x: 'x annotation') -> 'return annotation':
                pass
        -> {'x': 'x annotation', 'return': 'return annotation'}

        Returns
        -------
        annotations: dict
            argument {name: annotation} values
            return annotations under key 'return'

        """
        res = {k: v.annotation for k, v in self.parameters.items()
               if v.annotation != inspect._empty}
        res['return'] = self.return_annotation
        return res
    # /def

    @property
    def defaults(self):
        """Get defaults.

        ex: def f(x=2):
                pass
        -> (2,)

        Returns
        -------
        defaults: tuple
            n-tuple for n defaulted positional parameters

        """
        return tuple([p.default for p in self.parameters.values()
                      if ((p.kind == POSITIONAL_OR_KEYWORD) &
                          (p.default != inspect._empty))])
        # TODO replace p.default != inspect._empty with
    #                  p.kind != POSITIONAL_ONLY
    # /def

    @property
    def kwdefaults(self):
        """Get key-word only defaults.

        ex: def f(x=2):
                pass
        -> (2,)

        Returns
        -------
        defaults: dict
            argument {name: default}

        """
        return {n: p.default for n, p in self.parameters.items()
                if ((p.kind == KEYWORD_ONLY) &
                    (p.default != inspect._empty))}
    # /def

    @property
    def kwonlydefaults(self):
        """Get key-word only defaults.

        ex: def f(x=2):
                pass
        -> (2,)

        Returns
        -------
        defaults: dict
            argument {name: default}

        """
        return self.kwdefaults()
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

    def replace_parameter(self, param, name=None, kind=None, default=None,
                          annotation=None):
        """Replace a Parameter.

        Similar to .replace, but more convenient for modifying a single parameter
        Parameters are immutable, so will create a new Signature object

        Parameters
        ----------
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
        index = list(self.parameters.keys()).index(param)
        params = list(self.parameters.values())
        param = params[index]

        name = param.name if name is None else name
        kind = param.kind if kind is None else kind
        default = param.default if name is None else default
        annotation = param.annotation if name is None else annotation

        # adjust parameter list
        params[index] = param.replace(name=name, kind=kind, default=default,
                                      annotation=annotation)

        return self.replace(parameters=params)
    # /def

    def insert_parameter(self, index: int, parameter: inspect.Parameter):
        """Insert a new Parameter.

        Similar to .replace, but more convenient for adding a single parameter
        Parameters are immutable, so will create a new Signature object

        Parameters
        ----------
        index: int
            index into Signature.parameters at which to insert new parameter
        parameter: inspect.Parameter
            parameter to insert at index

        Returns
        -------
        Signature:
            a new Signature object with the inserted parameter

        """
        params = list(self.parameters.values())
        params.insert(index, parameter)

        return self.replace(parameters=params)
    # /def

    def drop_parameter(self, param):
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


##############################################################################
# Signature Methods
# TODO replace as method versions from Signature, can use semi-static for this


def replace_parameter(signature, param, name=None, kind=None,
                      default=None, annotation=None, return_annotation=None):
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


def insert_parameter(signature, index: int, parameter: inspect.Parameter):
    """Insert a new Parameter.

    Similar to .replace, but more convenient for adding a single parameter
    Parameters are immutable, so will create a new Signature object

    Parameters
    ----------
    index: int
        index into Signature.parameters at which to insert new parameter
    parameter: inspect.Parameter
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


def drop_parameter(signature, param):
    """Drop a Parameter.

    Parameters
    ----------
    signature:  Signature
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
