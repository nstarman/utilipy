# -*- coding: utf-8 -*-

"""Docstring decorators."""


__all__ = [
    # "format_doc",
    "set_docstring_for_import_func",
]


##############################################################################
# IMPORTS

# BUILT-IN
import ast
import typing as T

# PROJECT-SPECIFIC
from utilipy.data_utils import get_path_to_file
from utilipy.utils import functools

##############################################################################
# CODE
##############################################################################


def set_docstring_for_import_func(
    *path: str, package: T.Optional[str] = None, section: str = "Returns"
) -> str:
    """Set docstring for IPython import function, from import file's docstring.

    Takes a helper function for a module and adds the content of the modules'
    `section`. This currently only works on numpy-doc style docstrings.

    Parameters
    ----------
    *path: str
        path of import module
    package : str, optional, keyword only
        package for :func:`~utilipy.data_utils.get_path_to_file`
    section: str, optiona, keyword only
        numpy-doc style section name

    Notes
    -----
    This function might be moved

    """
    module = get_path_to_file(*path, package=package)

    # read docstring out of file
    with open(module, "r") as fd:
        module_doc = ast.get_docstring(ast.parse(fd.read()))

    # process docstring
    len_title = 2 * len(section) + 1  # section & underline
    ind_section = module_doc.find(section)
    if ind_section == -1:
        raise IndexError(f"Section {section} does not exist.")

    ind = ind_section + len_title
    end_ind = ind + module_doc[ind:].find("---")  # noqa

    sub_doc = module_doc[ind:end_ind]  # get section (+ next header)

    # drop next header
    sec = "\n".join(sub_doc.split("\n")[:-2])

    # modify function with a basic decorator
    def decorator(func):
        @functools.wraps(func, docstring=(func.__doc__ or "") + "\n" + sec)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    # /def

    return decorator


# /def


##############################################################################
# END
