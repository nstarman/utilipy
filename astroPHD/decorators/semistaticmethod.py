# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   :
# AUTHOR  : Nathaniel Starkman
# PROJECT :
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""SemiStaticMethod."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL
from typing import Any, Union, Callable, Optional

# PROJECT-SPECIFIC


##############################################################################
# SemiStaticMethod


class SemiStaticMethod(object):
    """Mixes a ``staticmethod`` and ``classmethod``.

    methods can be called either through the normal instance method
    or as a static method.

    based off of https://docs.python.org/3/howto/descriptor.html

    Examples
    --------
    >>> class A():
    ...     def __init__(self, name):
    ...         self.name = name
    ...
    ...     @SemiStaticMethod
    ...     def print_name(self, name=None):
    ...         name = name if name is not None else self.name
    ...         print(name)

    Calling as a ``staticmethod``, but without the required argument `name`:

    >>> A.print_name()  # BAD
    Error since no name parameter passed

    Calling as a static method with all arguments:

    >>> A.print_name('name')  # OK
    'name'

    Making an instance and calling the function:

    >>> a = A('name 2')
    >>> a.print_name()  # OK
    'name 2'
    >>> a.print_name(name='name 3')   # OK, but overriding
    'name 3'

    """

    def __init__(self, func: Callable) -> None:
        """Initialize with function."""
        self._func = func

    def __get__(self, obj: Any, klass: Optional[object] = None) -> Callable:
        """Make a semi-static method."""
        if klass is None:
            klass = type(obj)

        def newfunc(*args: Any, **kwargs: Any):
            return self._func(obj, *args, **kwargs)

        # /def
        return newfunc

    # /def


##############################################################################
# END
