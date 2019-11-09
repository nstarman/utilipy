# -*- coding: utf-8 -*-

"""IPython Imports.
"""

__author__ = "Nathaniel Starkman"

__all__ = [
    'import_from_file', 'run_imports',
    # specific importers
    'import_base', 'import_extended',
    'import_astropy', 'import_matplotlib',  # 'import_plotly',
    'import_galpy', 'import_amuse'
]

##############################################################################
# IMPORTS

# General
# import os
import ast
import functools
from IPython import get_ipython

# Project-Specific
from ..util.logging import LogFile
from ..util.paths import (
    get_absolute_path as _gap,
    parent_file_directory as _pfd
)

from .autoreload import aimport, set_autoreload

##############################################################################
# SETUP

_LOGFILE = LogFile(header=False, verbose=0)
_LOGGER_KW = {'print': False}


##############################################################################
# CODE

def import_from_file(*files, relative: bool=True,
                     logger=_LOGFILE, verbose=None, logger_kw=_LOGGER_KW
                     ) -> None:
    """Run import(s) from a file(s).

    Parameters
    ----------
    *files: str(s)
        strings for files to import
        need to include file suffix
    relative: bool, list of bools
        whether the `*files` paths are relative or absolute

    """
    # Handle `relative`
    if isinstance(relative, bool):  # broadcasting to same length as files
        relatives = [relative] * len(files)
    else:  # already a list
        if len(relative) != len(files):  # checking correct length
            raise ValueError("len(relative) != len(files)")
        relatives = relative

    # Importing
    for file, relative in zip(files, relatives):
        if relative:
            file = _gap(file)
        get_ipython().magic(f"run {file}")  # get_ipython inbuilt to jupyter

        # logging
        # implemented separately b/c files often have own print statements
        logger.report(f'imported {file}', verbose=verbose, **logger_kw)

    return
# /def


# ----------------------------------------------------------------------------

def run_imports(*files, relative: bool=True,
                # standard import files
                base: bool=False, extended: bool=False,
                # extra standard files
                astropy: bool=False,
                matplotlib: bool=False,
                # plotly: bool=False,
                # additional, requires extra installs
                galpy: bool=False, amuse: bool=False,
                # autoreload
                set_autoreload_to=None,
                # logging
                logger=_LOGFILE, verbose=0, logger_kw={}) -> None:
    """Run .imports file using ipython magic.

    if `astropy` & `matplotlib`, sets matplotlib style to astropy_mpl_style

    Parameters
    ----------
    files: str(s)
        strings for files to import
        need to include file suffix
    relative: bool, bool list
        whether the `files` paths are relative or absolute
    base: bool
        import_base -> `astroPHD/ipython/imports/base_imports.py`
    astropy: bool
        import_astropy -> `astroPHD/imports/astropy_imports.py`
    matplotlib: bool
        import_matplotlib -> `astroPHD/imports/matplotlib_imports.py`
    extended: bool
        import_extended -> `astroPHD/imports/extended_imports.py`
    galpy: bool
        import_galpy -> `astroPHD/imports/galpy_imports.py`
    amuse: bool
        import_amuse -> `astroPHD/imports/amuse_imports.py`

    Other Parameters
    ----------------
    set_autoreload_to: int or None  (default None)
        whether to change the autoreload state
    """
    # ---------------------------------------------
    # base

    if base:
        import_base(logger=logger, verbose=verbose)

    if extended:
        import_extended(logger=logger, verbose=verbose)

    # ---------------------------------------------
    # basic

    if astropy:
        import_astropy(logger=logger, verbose=verbose)

    if matplotlib:
        import_matplotlib(logger=logger, verbose=verbose)
    # if plotly:
    #     import_plotly(logger=logger, verbose=verbose)

    # ---------------------------------------------
    # extras

    if galpy:
        import_galpy(logger=logger, verbose=verbose)

    if amuse:
        import_amuse(logger=logger, verbose=verbose)

    # ---------------------------------------------

    # when combined
    if astropy & matplotlib:
        from matplotlib import pyplot
        from astropy.visualization import astropy_mpl_style
        pyplot.style.use(astropy_mpl_style)

    if galpy & amuse:  # TODO, embed in galpy_imports using argparse
        from galpy.potential import to_amuse

    # other import filess
    if files:  # True if not empty
        import_from_file(*files, relative=relative,
                         logger=logger, verbose=verbose,
                         logger_kw=logger_kw)

    # ---------------------------------------------
    # autoreload

    set_autoreload(set_autoreload_to)

    return
# /def


# ----------------------------------------------------------------------------
# UTILITIES TODO BETTER

def _join_pfd(path):
    # TODO better way to get this file directory & join path file
    return _pfd(__file__).joinpath(path)
# /def


def _set_docstring_import_x(module: str):
    """Set docstring Returns section.

    takes a helper function for a module and adds the content of the modules'
    `Returns` section.

    Parameters
    ----------
    module_doc: str
        docstring of import module

    """
    # read docstring out of file
    # fname = os.path.abspath(module)
    with open(module) as fd:
        module_doc = ast.get_docstring(ast.parse(fd.read()))

    # process docstring
    ind = module_doc.find('Returns')
    len_title = 2 * len('Returns')
    end_ind = ind + module_doc[ind + len_title:].find('---') + 2

    doc = module_doc[ind:end_ind]  # get section (+ next header)

    # modify function with a basic decorator
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        # /def
        wrapper.__doc__ = func.__doc__ + '\n\n' + doc
        return wrapper
    # /def
    return decorator
# /def


##############################################################################
# Specific Imports
# TODO make these with a function

@_set_docstring_import_x(_join_pfd('../imports/base_imports.py'))
def import_base(logger=_LOGFILE, verbose=None, logger_kw=_LOGGER_KW
                ) -> None:
    """Import base packages."""
    import_from_file(_join_pfd('../imports/base_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)
    return
# /def


@_set_docstring_import_x(_join_pfd('../imports/extended_imports.py'))
def import_extended(logger=_LOGFILE, verbose=None, logger_kw=_LOGGER_KW
                    ) -> None:
    """Import extended packages."""
    import_from_file(_join_pfd('../imports/extended_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)
    return
# /def


@_set_docstring_import_x(_join_pfd('../imports/astropy_imports.py'))
def import_astropy(logger=_LOGFILE, verbose=None, logger_kw=_LOGGER_KW
                   ) -> None:
    """Import basic astropy packages."""
    import_from_file(_join_pfd('../imports/astropy_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)
    return
# /def


# ----------------------------------------------------------------------------
# plotting

@_set_docstring_import_x(_join_pfd('../imports/matplotlib_imports.py'))
def import_matplotlib(logger=_LOGFILE, verbose=None, logger_kw=_LOGGER_KW
                      ) -> None:
    """Import basic Matplotlib packages."""
    import_from_file(_join_pfd('../imports/matplotlib_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)
    return
# /def


# @_set_docstring_import_x(_join_pfd('../imports/plotly_imports.py'))
# def import_plotly(logger=_LOGFILE, verbose=None, logger_kw=_LOGGER_KW
#                   ) -> None:
#     """Import basic plotly packages."""
#     import_from_file(_join_pfd('../imports/plotly_imports.py'),
#                      relative=False,
#                      logger=logger, verbose=verbose, logger_kw=logger_kw)
#     return
# # /def


# ----------------------------------------------------------------------------
# extras

@_set_docstring_import_x(_join_pfd('../imports/galpy_imports.py'))
def import_galpy(logger=_LOGFILE, verbose=None, logger_kw={'print': False}
                 ) -> None:
    """Import basic galpy packages."""
    import_from_file(_join_pfd('../imports/galpy_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)
    return
# /def


@_set_docstring_import_x(_join_pfd('../imports/amuse_imports.py'))
def import_amuse(logger=_LOGFILE, verbose=None, logger_kw={'print': False}
                 ) -> None:
    """Import basic amuse packages."""
    import_from_file(_join_pfd('../imports/amuse_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)
    return
# /def


##############################################################################
# END
