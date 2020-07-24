# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst


"""Decorators for code in active development.

See Also
--------
deprecation decorators in :function:`~astropy.util.exceptions.deprecated`,
upon which this code is based.

"""

__author__ = "Nathaniel Starkman"

__all__ = [
    "indev",
    "indev_attribute",
]


##############################################################################
# IMPORTS

# GENERAL

import functools
import inspect
import textwrap
import types
import warnings
import typing as T


# PROJECT-SPECIFIC

from ..utils.exceptions import utilipyWarning


##############################################################################
# CODE
##############################################################################


class DevelopmentWarning(utilipyWarning):
    """Warning class to indicate a feature as being actively developed.

    Expect the feature to change in input, output and implementation.

    """


# /class


class BetaDevelopmentWarning(DevelopmentWarning):
    """Warning class to indicate an upcoming feature that is nearly ready."""


# /class


##############################################################################


def indev(
    message="",
    name="",
    alternative="",
    todo="",
    beta=False,
    obj_type=None,
    warning_type=DevelopmentWarning,
):
    """Used to mark a function or class as in the development phase.

    Expect the feature to change in input, output and implementation.

    To mark an attribute as upcoming / in development, use `indev_attribute`.

    Parameters
    ----------
    message : str, optional
        Override the default in-dev message.  The format
        specifier ``func`` may be used for the name of the function,
        and ``alternative`` may be used in the in-dev message
        to insert the name of an alternative to the in-dev
        function. ``obj_type`` may be used to insert a friendly name
        for the type of object being in-dev.

    name : str, optional
        The name of the in-dev function or class; if not provided
        the name is automatically determined from the passed in
        function or class, though this is useful in the case of
        renamed functions, where the new function is just assigned to
        the name of the in-dev function.  For example::

            def new_function():
                ...
            oldFunction = new_function

    alternative : str, optional
        An alternative function or class name that the user may use in
        place of the in-dev object.  The in-dev warning will
        tell the user about this alternative if provided.

    todo : str, optional
        A todo about intended features and functionality. The in-dev warning
        will tell the user about this alternative if provided.

    beta : bool, optional
        If True, uses a BetaDevelopmentWarning instead of a
        ``warning_type``.

    obj_type : str, optional
        The type of this object, if the automatically determined one
        needs to be overridden.

    warning_type : warning
        Warning to be issued.
        Default is `~DevelopmentWarning`.


    See Also
    --------
    deprecation decorators in :func:`~astropy.util.exceptions.deprecated`

    """
    method_types = (classmethod, staticmethod, types.MethodType)

    # -----------------------------------------------------

    def indev_doc(old_doc: T.Union[str, None], message: str):
        """Returns a given docstring with an in-dev message prepended.

        .. todo::

            process docstring better

        Parameters
        ----------
        old_doc: str
        message : str

        Returns
        -------
        new_doc : str

        """
        if not old_doc:  # empty str or None
            old_doc = ""

        old_doc = textwrap.dedent(old_doc).strip("\n")

        note_indev = (
            "\n    .. versionchanged:: indev\n"
            "\n        {message}\n".format(**{"message": message.strip()})
        )

        # TODO, process docstring better
        _sections = [
            "\n    Parameters\n    ----------",
            "\n    Returns\n    -------",
        ]
        if _sections[0] in old_doc:  # check if has Parameters
            descr, rest = old_doc.split(_sections[0])
            descr += note_indev
            new_doc = descr + _sections[0] + rest

        elif _sections[1] in old_doc:  # maybe starts with Returns
            descr, rest = old_doc.split(_sections[1])
            descr += note_indev
            new_doc = descr + _sections[1] + rest

        else:  # just a regular doc
            new_doc = old_doc + "\n" + note_indev + "\n"

        return new_doc

    # /def

    # -----------------------------------------------------

    def get_function(func):
        """Get function object given function."""
        if isinstance(func, method_types):
            func = func.__func__
        return func

    # /def

    def indev_function(func, message, warning_type=warning_type):
        """Returns a wrapped function that displays ``warning_type`` when called."""
        if isinstance(func, method_types):
            func_wrapper = type(func)
        else:
            func_wrapper = lambda f: f  # noqa

        func = get_function(func)

        def upcoming_func(*args, **kwargs):
            if beta:
                category = BetaDevelopmentWarning
            else:
                category = warning_type

            warnings.warn(message, category, stacklevel=2)

            return func(*args, **kwargs)

        # If this is an extension function, we can't call
        # functools.wraps on it, but we normally don't care.
        # This crazy way to get the type of a wrapper descriptor is
        # straight out of the Python 3.3 inspect module docs.
        if type(func) is not type(str.__dict__["__add__"]):  # noqa
            upcoming_func = functools.wraps(func)(upcoming_func)

        upcoming_func.__doc__ = indev_doc(upcoming_func.__doc__, message)

        return func_wrapper(upcoming_func)

    # /def

    # -----------------------------------------------------

    def indev_class(cls, message, warning_type=warning_type):
        """Class in-dev.

        Update the docstring and wrap the ``__init__`` in-place (or ``__new__``
        if the class or any of the bases overrides ``__new__``) so it will give
        an in-dev warning when an instance is created.

        This won't work for extension classes because these can't be modified
        in-place and the alternatives don't work in the general case:

        - Using a new class that looks and behaves like the original doesn't
          work because the __new__ method of extension types usually makes sure
          that it's the same class or a subclass.
        - Subclassing the class and return the subclass can lead to problems
          with pickle and will look weird in the Sphinx docs.

        Returns
        -------
        cls : ClassType

        """
        cls.__doc__ = indev_doc(cls.__doc__, message)
        if cls.__new__ is object.__new__:
            cls.__init__ = indev_function(
                get_function(cls.__init__), message, warning_type
            )
        else:
            cls.__new__ = indev_function(
                get_function(cls.__new__), message, warning_type
            )
        return cls

    # /def

    # -----------------------------------------------------

    def make_indev(
        obj,
        message=message,
        name=name,
        alternative=alternative,
        beta=beta,
        warning_type=warning_type,
    ):
        """Mark object as in-development.

        Parameters
        ----------
        obj : object
        message : str
        name : str
        alternative : str
        beta : bool
        warning_type : ClassType

        Returns
        -------
        Callable

        """
        if obj_type is None:
            if isinstance(obj, type):
                obj_type_name = "class"
            elif inspect.isfunction(obj):
                obj_type_name = "function"
            elif inspect.ismethod(obj) or isinstance(obj, method_types):
                obj_type_name = "method"
            else:
                obj_type_name = "object"
        else:
            obj_type_name = obj_type

        if not name:
            name = get_function(obj).__name__

        altmessage = ""
        todomessage = ""
        if not message or type(message) is type(make_indev):
            if beta:
                message = (
                    "The {func} {obj_type} will be added in a "
                    "future version."
                )
            else:
                message = (
                    "The {func} {obj_type} is in development and may "
                    "be added in a future version."
                )
            if alternative:
                altmessage = f"\n        Use {alternative} instead."
            if todomessage:
                todomessage = f"\n        {todo}"

        message = (
            (
                message.format(
                    **{
                        "func": name,
                        "name": name,
                        "alternative": alternative,
                        "todo": todo,
                        "obj_type": obj_type_name,
                    }
                )
            )
            + altmessage
            + todomessage
        )

        if isinstance(obj, type):
            return indev_class(obj, message, warning_type)
        else:
            return indev_function(obj, message, warning_type)

    # /def

    if type(message) is type(make_indev):
        return make_indev(message)

    return make_indev


# /def


# ------------------------------------------------------------------------


def indev_attribute(
    name,
    message=None,
    alternative=None,
    todo=None,
    beta=False,
    warning_type=DevelopmentWarning,
):
    """Mark a public attribute as in development.

    This creates a property that will warn when the given attribute name
    is accessed. To prevent the warning (i.e. for internal code),
    use the private name for the attribute by prepending an underscore
    (i.e. ``self._name``).

    Parameters
    ----------
    name : str
        The name of the in-dev attribute.

    message : str, optional
        Override the default in-dev message.  The format
        specifier ``name`` may be used for the name of the attribute,
        and ``alternative`` may be used in the in-dev message
        to insert the name of an alternative to the in-dev
        function.

    alternative : str, optional
        An alternative attribute that the user may use in place of the
        in-dev attribute.  The in-dev warning will tell the
        user about this alternative if provided.

    todo : str, optional
        A todo about intended functionality. The in-dev warning
        will tell the user about this alternative if provided.

    beta : bool, optional
        If True, uses a BetaDevelopmentWarning instead of
        ``warning_type``.

    warning_type : warning
        Warning to be issued.
        Default is `~DevelopmentWarning`.

    Examples
    --------
    ::

        class MyClass:
            # Mark the new_attr as in development
            new_attr = misc.indev_attribute('new_attr')

            def method(self):
                self._new_attr = 42

    Returns
    -------
    property

    """
    private_name = "_" + name

    @indev(
        name=name,
        obj_type="attribute",
        warning_type=warning_type,
        alternative=alternative,  # TODO, implement for attribute
        todo=todo,  # TODO, implement for attribute
    )
    def get(self):
        return getattr(self, private_name)

    @indev(
        name=name,
        obj_type="attribute",
        warning_type=warning_type,
        alternative=alternative,  # TODO, implement for attribute
        todo=todo,  # TODO, implement for attribute
    )
    def set(self, val):
        setattr(self, private_name, val)

    @indev(
        name=name,
        obj_type="attribute",
        warning_type=warning_type,
        alternative=alternative,  # TODO, implement for attribute
        todo=todo,  # TODO, implement for attribute
    )
    def delete(self):
        delattr(self, private_name)

    return property(get, set, delete)


# /def


##############################################################################
# END
