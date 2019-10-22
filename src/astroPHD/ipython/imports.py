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
# IMPORTS

# General
from IPython import get_ipython

# Project-Specific
from ..util.logging import LogFile
from ..util.paths import (
    get_absolute_path as _gap,
    parent_file_directory as _pfd
)

from .autoreload import aimport

##############################################################################
# SETUP

_LOGFILE = LogFile(header=False, verbose=0)
# _LOGGER_KW = {'print': False}


##############################################################################
# CODE

def import_from_file(*files, relative: bool=True,
                     logger=_LOGFILE, verbose=None, logger_kw={'print': False}
                     ) -> None:
    """run import(s) from a file(s)

    Parameters
    ----------
    *files: str(s)
        strings for files to import
        need to include file suffix
    relative: bool, list of bools
        whether the `*files` paths are relative or absolute
    """

    # broadcasting relative to same length as files
    if isinstance(relative, bool):
        relatives = [relative] * len(files)
    else:  # already a list
        if len(relative) != len(files):  # checking correct length
            raise ValueError("len(relative) != len(files)")
        relatives = relative

    # importing
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
                base: bool=False, astropy: bool=False, matplotlib: bool=False,
                extended: bool=False, galpy: bool=False, amuse: bool=False,
                logger=_LOGFILE, verbose=0, logger_kw={}) -> None:
    """runs .imports file using ipython magic

    Info
    ----
    if `astropy` & `matplotlib`, sets matplotlib style to astropy_mpl_style

    Parameters
    ----------
    *files: str(s)
        strings for files to import
        need to include file suffix
    relative: bool, list of bools
        whether the `*files` paths are relative or absolute

    base: bool
        import_base -> `astroPHD/ipython/imports/base_imports.py'
    astropy: bool
        import_astropy -> `astroPHD/imports/astropy_imports.py'
    matplotlib: bool
        import_matplotlib -> `astroPHD/imports/matplotlib_imports.py'
    extended: bool
        import_extended -> `astroPHD/imports/extended_imports.py'
    galpy: bool
        import_galpy -> `astroPHD/imports/galpy_imports.py'
    amuse: bool
        import_amuse -> `astroPHD/imports/amuse_imports.py'
    """

    # running imports file
    if base:
        import_base(logger=logger, verbose=verbose)

    if astropy:
        import_astropy(logger=logger, verbose=verbose)

    if matplotlib:
        import_matplotlib(logger=logger, verbose=verbose)

    if extended:
        import_extended(logger=logger, verbose=verbose)

    if galpy:
        import_galpy(logger=logger, verbose=verbose)

    if amuse:
        import_amuse(logger=logger, verbose=verbose)

    # when combined
    if astropy & matplotlib:
        from matplotlib import pyplot
        from astropy.visualization import astropy_mpl_style
        pyplot.style.use(astropy_mpl_style)

    # if galpy & amuse:  # TODO, embed in galpy_imports using argparse
    #     from galpy.potential import to_amuse

    # other import filess
    if files:  # True if not empty
        import_from_file(*files, relative=relative,
                         logger=logger, verbose=verbose,
                         logger_kw=logger_kw)

    return
# /def


def _join_pfd(path):
    # TODO better way to get this file directory & join path file
    return _pfd(__file__).joinpath(path)
# /def


def run_standard_imports() -> None:
    """
    """
    raise DeprecationWarning("use run_imports() with options instead,"
                             "or './import_files/full_standard_imports.py'")

    import_from_file(_join_pfd('import_files/full_standard_imports.py'),
                     relative=False)

    return
# /def


##############################################################################
# Specific Imports

def import_base(logger=_LOGFILE, verbose=None, logger_kw={'print': False}
                ) -> None:
    """Import base packages.

    Base: os, sys, time, pdb, warnings,
          numpy -> np, scipy,
          tqdm -> TQDM, .tqdm, .tqdm_notebook ->. tqdmn
    Logging: .LogFile
    Misc: ObjDict
    IPython: display, Latex, Markdown, set_trace,
             printmd, printMD, printltx, printLaTeX,
             set_autoreload, aimport,
             run_imports, import_from_file,
             add_raw_code_toggle
    """
    import_from_file(_join_pfd('import_files/base_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)

    return
# /def


# ----------------------------------------------------------------------------

def import_extended(logger=_LOGFILE, verbose=None, logger_kw={'print': False}
                    ) -> None:
    """Import extended packages.

    numpy: linalg.norm
    scipy stats.binned_statistic->binned_stats
    """
    import_from_file(_join_pfd('import_files/extended_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)

    return
# /def


# ----------------------------------------------------------------------------

def import_astropy(logger=_LOGFILE, verbose=None, logger_kw={'print': False}
                   ) -> None:
    """
    """
    import_from_file(_join_pfd('import_files/astropy_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)

    return
# /def


# ----------------------------------------------------------------------------

def import_matplotlib(logger=_LOGFILE, verbose=None, logger_kw={'print': False}
                      ) -> None:
    """
    """
    import_from_file(_join_pfd('import_files/matplotlib_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)

    return
# /def


# ----------------------------------------------------------------------------

def import_galpy(logger=_LOGFILE, verbose=None, logger_kw={'print': False}
                 ) -> None:
    """
    """
    import_from_file(_join_pfd('import_files/galpy_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)

    return
# /def


# ----------------------------------------------------------------------------

def import_amuse(logger=_LOGFILE, verbose=None, logger_kw={'print': False}
                 ) -> None:
    """
    """
    import_from_file(_join_pfd('import_files/amuse_imports.py'),
                     relative=False,
                     logger=logger, verbose=verbose, logger_kw=logger_kw)

    return
# /def


##############################################################################
# END
