#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   :
# AUTHOR  : Nathaniel Starkman
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General

# Project-Specific


##############################################################################
# SemiStaticMethod

class SemiStaticMethod(object):
    """Mixes a Static and Classmethod.

    Info
    ----
    methods can be called either through the normal instance method
    or as a static method

    based off of https://docs.python.org/3/howto/descriptor.html

    Examples
    --------
    class A():
        def __init__(self, name):
            self.name = name

        @SemiStaticMethod
        def print_name(self, name=None):
            name = name if name is not None else self.name
            print(name)

    A.print_name()  # BAD
    > Error since no name parameter passed
    A.print_name('name')  # OK
    > 'name'
    a =  A('name 2')
    a.print_name()  # OK
    > 'name 2'
    a.print_name(name='name 3')   # OK, but overriding
    > 'name 3'

    """

    def __init__(self, func):
        """Initialize with function."""
        self._func = func

    def __get__(self, obj, klass=None):
        """Make a semi-static method."""
        if klass is None:
            klass = type(obj)

        def newfunc(*args, **kwargs):
            return self._func(obj, *args, **kwargs)
        return newfunc

##############################################################################
# END
