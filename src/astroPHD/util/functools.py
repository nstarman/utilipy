#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""functools

TODO
----
improve makeFunction call signature
test makeFunction-made function speeds
"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General
from functools import *

# Project-Specific
from .metaclasses import InheritDocstrings
from .inspect import (Signature,
                      get_annotations_from_signature,
                      get_defaults_from_signature,
                      get_kwdefaults_from_signature,
                      get_kwonlydefaults_from_signature)


################################################################################
# Signature / ArgSpec Interface
################################################################################

def makeFunction(code, globals_, name=None, signature=None, docstring=None,
                 closure=None):
    """Make a function with a specified signature and docstring.

    This is pure python and may not make the fastest functions

    Parameters
    ----------
    code:
    globals_:
    name:
    signature:
    docstring:
    closure:

    Returns
    -------
    function:

    TODO
    ----
    check how signature and closure relate
    __qualname__

    """
    if not isinstance(signature, Signature):  # not my custom signature
        signature = Signature(parameters=signature.parameters,
                              return_annotation=signature.return_annotation,
                              # docstring=docstring  # not yet implemented
                              )
    else:
        pass  # docstring considerations not yet implemented

    function = types.FunctionType(code, globals_, name=name,
                                  argdefs=signature.defaults,
                                  closure=closure)

    function.__kwdefaults__ = signature.kwdefaults
    function.__annotations__ = signature.annotations  # includes return_annote
    function.__signature__ = signature.signature  # classical signature
    function.__doc__ = docstring

    return function
# /def


# -----------------------------------------------------------------------------

def copy_function(func):
    """Copy a function."""
    function = makeFunction(func.__code__, func.__globals__,
                            name=func.__name__,
                            signature=inspect.signature(func),
                            docstring=func.__doc__,
                            closure=func.__closure__)

    # TODO necessary?
    function.__dict__.update(func.__dict__)

    return function
# /def


################################################################################
# update_wrapper() and wraps() decorator
################################################################################

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__')
SIGNATURE_ASSIGNMENTS = ('defaults', 'kwdefaults', 'annotations')
WRAPPER_UPDATES = ('__dict__',)


def update_wrapper(wrapper, wrapped,
                   signature: (Signature, None)=None,
                   docstring: (str, None)=None,
                   assigned=WRAPPER_ASSIGNMENTS,
                   updated=WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function.

    Info
    ----
       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)

    """
    if signature is None:  # get function signature if None
        signature = Signature.from_callable(wrapped)
    else:  # convert to my signature object
        if not isinstance(signature, Signature):  # not my custom signature
            signature = Signature(parameters=signature.parameters,
                                  return_annotation=signature.return_annotation,
                                  # docstring=docstring  # not yet implemented
                                  )
        else:
            pass  # docstring considerations not yet implemented

    # build parameters
    # defaults = get_defaults_from_signature(signature)
    # kwdefaults = get_kwdefaults_from_signature(signature)
    # annotations = get_annotations_from_signature(signature)

    # same as functools.update_wrapper (sans __doc__)
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))

    # set from signature and doc
    for attr in SIGNATURE_ASSIGNMENTS:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, f'__{attr}__', value)
    wrapper.__signature__ = signature.signature
    wrapper.__doc__ = wrapped.__doc__ if docstring is None else docstring

    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper
# /def


# -----------------------------------------------------------------------------

def wraps(wrapped,
          signature: (Signature, None)=None,
          docstring: (str, None)=None,
          assigned=WRAPPER_ASSIGNMENTS,
          updated=WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function
       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=wrapped,
                   signature=signature, docstring=docstring,
                   assigned=assigned, updated=updated)


##############################################################################
# END
