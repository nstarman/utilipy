.. _utilipy-why:

===================
Benefits of utilipy
===================

    >>> import utilipy


Decorators
==========

``utilipy``-built decorators are better than normal decorators.

This decorator **does**:

* anything to the function input and output
* make a function that looks exactly like the input function for quality introspection.
* work when created with parenthesis 
* accept (kw)arguments on application
* add any extra (kw)arguments to control the `wrapper` also make the defaults be dynamically set on function creation.
* document what the wrapper is doing.


    >>> def template_decorator(function=None, *, kw1=None, kw2=None):
    ...     ''''Docstring for decorator.
    ...
    ...     Description of this decorator
    ...
    ...     Parameters
    ...     ----------
    ...     function : types.FunctionType or None, optional
    ...         the function to be decoratored
    ...         if None, then returns decorator to apply.
    ...     kw1, kw2 : any, optional
    ...         key-word only arguments
    ...         sets the wrappeer's default values.
    ...
    ...     Returns
    ...     -------
    ...     wrapper : types.FunctionType
    ...         wrapper for function
    ...         does a few things
    ...         includes the original function in a method `.__wrapped__`
    ...
    ...     '''
    ...     if function is None: # allowing for optional arguments
    ...         return functools.partial(template_decorator, kw1=k1, kw2=kw2)
    ...
    ...     @utilipy.wraps(function)
    ...     def wrapper(*args, kw1=kw1, kw2=kw2, kw3='not in decorator factory', **kw):
    ...         """wrapper docstring.
    ...
    ...         Decorator
    ...         ---------
    ...         prints information about function
    ...         kw1, kw2: defaults {kw1}, {kw2}
    ...
    ...         """
    ...         # do stuff here
    ...         return_ = function(*args, **kw)
    ...         # and here
    ...         return return_
    ...     # /def

    ...     return wrapper
    ... # /def
