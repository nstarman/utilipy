# -*- coding: utf-8 -*-

"""Miscellaneous Utility Functions."""

__all__ = [
    # functions
    "temporary_namespace",
    "make_help_function",
]


##############################################################################
# IMPORTS

# BUILT-IN
import typing as T
from contextlib import contextmanager
from types import ModuleType

# THIRD PARTY
from astropy.utils.data import find_current_module

##############################################################################
# CODE
##############################################################################


@contextmanager
def temporary_namespace(locals_ref, keep: T.List[str] = []):
    """Temporary Namespace within ``with`` statement.

    1. copies current namespace from `locals_ref`
    2. Enters ``with`` statement
    3. restores original namespace except those specified in `keep`

    Parameters
    ----------
    module : module
        ``sys.modules[__name__]`` of module calling from.

        .. todo::

            not need to pass any module information. infer.

    keep : list, optional
        list of (str) variable names to keep.

    Yields
    ------
    locals_ref : locals
        for accessing namespace

    Warnings
    --------
    Does NOT work within functions.

    """
    original_namespace = locals_ref.copy()

    try:
        yield locals_ref
    finally:
        # difference of current and old namespace
        # without the keep keys
        drop_keys = (
            set(locals_ref.keys())
            .difference(original_namespace.keys())
            .difference(keep)
        )
        # kept values
        keep_dict = {k: locals_ref[k] for k in keep}

        # print("drop_keys", drop_keys, "keep_dict", keep_dict)

        # Restoring Namespace
        original_namespace.update(keep_dict)  # add keep values to original
        locals_ref.update(original_namespace)  # restore original (+kept)
        for key in drop_keys:  # drop unkept context-specific values
            locals_ref.pop(key)

    # /try


# -------------------------------------------------------------------


def make_help_function(
    name: str,
    module: T.Union[None, ModuleType, str] = None,
    look_for: T.Optional[str] = None,  # "Routine Listings",
    doctitle: T.Optional[str] = None,
) -> T.Callable:
    """Set docstring from module Returns section.

    Takes a helper function for a module and adds the content of the modules'
    `look_for` section. Currently only works on numpy-style docstring.

    Parameters
    ----------
    name: str
        name of function. Add "_help".
    module:
        Module
    look_for : str, optional
        The section to look for (default None)
        The section name "Routine Listings" is replaced by "Returns"
    doctitle : str, optional

    Returns
    -------
    decorator : Callable
        decorator function to change the wrapped function's docstring.

    Raises
    ------
    TypeError
        if `look_for` is not None or str

    Notes
    -----
    .. todo::

        separate the imports help function from the general helps function.
        the general help function should be similar to the find_api_page
        in astropy and the help function in the utilipy init.

    """
    if module is None:
        module = find_current_module(2)
        mod_name = module.__name__
        module_doc = module.__doc__
    elif isinstance(module, ModuleType):
        module_doc = module.__doc__
        mod_name = module.__name__
    elif isinstance(module, str):
        module_doc = module
        mod_name = find_current_module(2).__name__

    if look_for is None:
        doc = module_doc

    elif isinstance(look_for, str):
        ind = module_doc.find(look_for) + 2 * len(look_for) + 2
        end_ind = ind + module_doc[ind:].find("---")  # finding next section

        doc = module_doc[ind:end_ind]  # get section (+ next header)
        doc = "\n".join(doc.split("\n")[:-2])  # strip next header

        if look_for == "Routine Listings":  # skip 'Routine Listings' & line
            # Name = name.capitalize()
            doc = f"\nReturns\n{'-'*(len(name) + 1)}-------\n" + doc

    else:
        raise TypeError

    # TODO with FunctionType in types
    def help_function():
        print(doc)

    # help_function._doc = doc
    help_function.__name__ = f"{name}_help"
    help_function.__module__ = mod_name
    help_function.__doc__ = f"Help for {doctitle or name}.\n\n" + (doc or "")
    # /def

    return help_function


# /def


##############################################################################
# END
