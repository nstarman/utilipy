#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ipython imports file
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

from ..util.logging import LogPrint
from ..util.paths import (
    get_absolute_path as _gap,
    parent_file_directory as _pfd
)


##############################################################################
### SETUP

_LOGFILE = LogPrint(header=False, verbose=0)


##############################################################################
### CODE

def import_from_file(*files, relative:bool=True) -> None:
    """run import(s) from a file(s)

    Parameters
    ----------
    *files: str(s)
        strings for files to import
        need to include file suffix
    """

    for file in files:
        print(file)
        if relative:
            file = _gap(file)
        get_ipython().magic(f"run {file}")

        _LOGFILE.write(f'imported {file}')

    return
# /def


# ----------------------------------------------------------------------------

def run_imports(*files, relative:bool=True,
                base:bool=False, astropy:bool=False, matplotlib:bool=False,
                extended:bool=False) -> None:
    """runs .imports file using ipython magic

    Info
    ----
    if `astropy` & `matplotlib`, sets matplotlib style to astropy_mpl_style

    Parameters
    ----------
    *files: str(s)
        strings for files to import
        need to include file suffix
    relative: bool
        whether the `*files` paths are relative or absolute
    base: bool
        run_base_imports() -> `astroPHD/ipython/import_files/base_imports.py'
    astropy: bool
        run_astropy_imports() -> `astroPHD/ipython/import_files/astropy_imports.py'
    matplotlib: bool
        run_matplotlib_imports() -> `astroPHD/ipython/import_files/matplotlib_imports.py'
    extended: bool
        run_extended_imports() -> `astroPHD/ipython/import_files/extended_imports.py'
    """

    # running imports file
    if base:
        run_base_imports()

    if astropy:
        run_astropy_imports()

    if matplotlib:
        run_matplotlib_imports()

    if extended:
        run_extended_imports()

    # when combined
    if astropy & matplotlib:
        from matplotlib import pyplot
        from astropy.visualization import astropy_mpl_style
        pyplot.style.use(astropy_mpl_style)

    # other import filess
    if files:  # True if not empty
        import_from_file(*files, relative=relative)

    return
# /def


# ----------------------------------------------------------------------------

def _join_pfd(path):
    # TODO better way to get this file directory & join path file
    return _pfd(__file__).joinpath(path)
# /def


def run_standard_imports() -> None:
    """
    """

    import_from_file(_join_pfd('import_files/full_standard_imports.py'),
                     relative=False)

    return
# /def


##############################################################################
### Specific Imports

def run_base_imports() -> None:
    """
    """

    import_from_file(_join_pfd('import_files/base_imports.py'),
                     relative=False)

    return
# /def


# ----------------------------------------------------------------------------

def run_extended_imports() -> None:
    """
    """

    import_from_file(_join_pfd('import_files/extended_imports.py'),
                     relative=False)

    return
# /def


# ----------------------------------------------------------------------------

def run_astropy_imports() -> None:
    """
    """

    import_from_file(_join_pfd('import_files/astropy_imports.py'),
                     relative=False)

    return
# /def


# ----------------------------------------------------------------------------

def run_matplotlib_imports() -> None:
    """
    """

    import_from_file(_join_pfd('import_files/matplotlib_imports.py'),
                     relative=False)

    return
# /def


##############################################################################
### END
