# -*- coding: utf-8 -*-

"""IPython Imports.

Routine Listings
----------------
run_imports
    Import file, custom or provided, using ipython magic
import_from_file
    Run import(s) from a file(s)
aimport
    from `.autoreload` module
set_autoreload
    from `.autoreload` module

import_base
    ipython magic run `utilipy/imports/base.py`
import_extended
    ipython magic run `utilipy/imports/extended.py`
import_astropy
    ipython magic run `utilipy/imports/astropy.py`
import_matplotlib
    ipython magic run `utilipy/imports/matplotlib.py`
import_galpy
    ipython magic run `utilipy/imports/galpy.py`
import_amuse
    ipython magic run `utilipy/imports/amuse.py`

References
----------
IPython [#]_

.. [#] Fernando Pérez, Brian E. Granger, IPython: A System for Interactive
    Scientific Computing, Computing in Science and Engineering, vol. 9,
    no. 3, pp. 21-29, May/June 2007, doi:10.1109/MCSE.2007.53.
    URL: https://ipython.org

"""

__author__ = "Nathaniel Starkman"

__all__ = [
    "import_from_file",
    "run_imports",
    # specific importers
    "import_base",
    "import_extended",
    "import_astropy",
    "import_matplotlib",  # 'import_plotly',
    "import_galpy",
    "import_amuse",
]


##############################################################################
# IMPORTS

# GENERAL

import ast
import os.path
from pathlib import Path
from IPython import get_ipython
from typing import Optional, Dict


# PROJECT-SPECIFIC

from ..utils import functools
from ..config import use_import_verbosity
from ..utils.logging import LogFile

from .autoreload import aimport, set_autoreload


##############################################################################
# SETUP

_LOGFILE = LogFile(header=False, verbose=0)
_LOGGER_KW = {"print": False}


##############################################################################
# CODE


def import_from_file(
    *files: str,
    is_relative: bool = True,
    verbose_imports: Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose=None,
    logger_kw: Dict = _LOGGER_KW,
) -> None:
    """Run import(s) from a file(s).

    Parameters
    ----------
    *files: str(s)
        strings for files to import
        need to include file suffix
    is_relative: bool or list of bools
        whether the `*files` paths are relative or absolute
    verbose_imports: bool or None
        Verbose_imports or not, use default if None.

    """
    # Handle `relative`
    if isinstance(is_relative, bool):  # broadcasting to same length as files
        relatives = [is_relative] * len(files)
    else:  # already a list
        if len(is_relative) != len(files):  # checking correct length
            raise ValueError("len(relative) != len(files)")
        relatives = is_relative

    # handle verbose-imports
    with use_import_verbosity(verbose_imports):

        # Importing
        for file, relative in zip(files, relatives):
            if relative:
                file = str(Path(file).resolve())
            # get_ipython inbuilt to jupyter
            get_ipython().magic(f"run {file}")

            # logging
            # implemented separately b/c files often have own print statements
            logger.report(f"imported {file}", verbose=verbose, **logger_kw)

    return


# /def


# ----------------------------------------------------------------------------


def run_imports(
    *files: str,
    is_relative: bool = True,
    # standard import files
    base: bool = False,
    extended: bool = False,
    # extra standard files
    astropy: bool = False,
    matplotlib: bool = False,
    plotly: bool = False,
    # additional, requires extra installs
    galpy: bool = False,
    amuse: bool = False,
    # autoreload
    set_autoreload_to: Optional[int] = None,
    verbose_imports: Optional[bool] = None,
    # logging
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = 0,
    logger_kw: Dict = {},
) -> None:
    """Import file using IPython magic.

    if `astropy` and `matplotlib`, sets matplotlib style to astropy_mpl_style

    Parameters
    ----------
    files: str(s)
        strings for files to import
        need to include file suffix
    base: bool
        a broad set of basic imports
        import_base -> `utilipy/imports/base.py`
    astropy: bool
        import_astropy -> `utilipy/imports/astropy.py`
    matplotlib: bool
        import_matplotlib -> `utilipy/imports/matplotlib.py`
    plotly: bool
        import_plotly -> `utilipy/imports/plotly.py`
    extended: bool
        import_extended -> `utilipy/imports/extended.py`
    galpy: bool
        import_galpy -> `utilipy/imports/galpy.py`
    amuse: bool
        import_amuse -> `utilipy/imports/amuse.py`

    Other Parameters
    ----------------
    set_autoreload_to: int or None
        (default None)
        whether to change the autoreload state
    relative: bool or list of bools
        whether the `files` paths are relative or absolute
    verbose_imports: bool or None
        Verbose_imports or not, use ``.utilipyrc`` default if None.

    Examples
    --------
    ``run_imports(base=True, astropy=True)``
    imports from `utilipy/imports/base.py` and `utilipy/imports/astropy.py`,
    printing an import summary

    ``run_imports(base=True, verbose_imports=False)``
    imports from `utilipy/imports/base.py`, without an import summary

    ``utilipy.config.set_import_verbosity(False)``
    ``utilipy.ipython.imports.run_imports(base=True, verbose_imports=None)``
    imports from `utilipy/imports/base.py` with default import-verbosity state

    """
    kw = dict(verbose_imports=verbose_imports, logger=logger, verbose=verbose)
    # ---------------------------------------------
    # base

    if base:
        import_base(**kw)

    if extended:
        import_extended(**kw)

    # ---------------------------------------------
    # basic

    if astropy:
        import_astropy(**kw)

    if matplotlib:
        import_matplotlib(**kw)
    if plotly:
        import_plotly(**kw)

    # ---------------------------------------------
    # extras

    if galpy:
        import_galpy(**kw)

    if amuse:
        import_amuse(**kw)

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
        import_from_file(
            *files,
            is_relative=is_relative,
            verbose_imports=verbose_imports,
            logger=logger,
            verbose=verbose,
            logger_kw=logger_kw,
        )

    # ---------------------------------------------
    # autoreload

    set_autoreload(set_autoreload_to)

    return


# /def


# ----------------------------------------------------------------------------
# UTILITIES TODO BETTER


def _set_docstring_import_x(path: tuple) -> str:
    """Set docstring Returns section.

    takes a helper function for a module and adds the content of the modules'
    `Returns` section.

    Parameters
    ----------
    path: str
        path of import module

    """
    module = str(Path(__file__).parent.joinpath(os.path.join(*path)))

    # read docstring out of file
    with open(module, "r") as fd:
        module_doc = ast.get_docstring(ast.parse(fd.read()))

    # process docstring
    ind = module_doc.find("Returns")
    len_title = 2 * len("Returns")
    end_ind = ind + module_doc[ind + len_title :].find("---") + 2  # noqa

    doc = module_doc[ind:end_ind]  # get section (+ next header)

    # modify function with a basic decorator
    def decorator(func):
        @functools.wraps(func, docstring=func.__doc__ + "\n\n" + doc)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # /def
        return wrapper

    # /def
    return decorator


# /def


##############################################################################
# Specific Imports
# TODO make these with a function


@_set_docstring_import_x(("..", "imports", "base_imports.py"))
def import_base(
    verbose_imports: Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = None,
    logger_kw: Dict = _LOGGER_KW,
) -> None:
    """Import base packages."""
    import_from_file(
        ("..", "imports", "base_imports.py"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


@_set_docstring_import_x(("..", "imports", "extended_imports.py"))
def import_extended(
    verbose_imports: Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = None,
    logger_kw: Dict = _LOGGER_KW,
) -> None:
    """Import extended packages."""
    import_from_file(
        ("..", "imports", "extended_imports.py"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


@_set_docstring_import_x(("..", "imports", "astropy_imports.py"))
def import_astropy(
    verbose_imports: Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = None,
    logger_kw: Dict = _LOGGER_KW,
) -> None:
    """Import basic astropy packages."""
    import_from_file(
        ("..", "imports", "astropy_imports.py"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


# ----------------------------------------------------------------------------
# plotting


@_set_docstring_import_x(("..", "imports", "matplotlib_imports.py"))
def import_matplotlib(
    verbose_imports: Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = None,
    logger_kw: Dict = _LOGGER_KW,
) -> None:
    """Import basic Matplotlib packages."""
    import_from_file(
        ("..", "imports", "matplotlib_imports.py"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


@_set_docstring_import_x(("..", "imports", "plotly_imports.py"))
def import_plotly(
    verbose_imports: Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = None,
    logger_kw: Dict = _LOGGER_KW,
) -> None:
    """Import basic Matplotlib packages."""
    import_from_file(
        ("..", "imports", "plotly_imports.py"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


# ----------------------------------------------------------------------------
# extras


@_set_docstring_import_x(("..", "imports", "galpy_imports.py"))
def import_galpy(
    verbose_imports: Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = None,
    logger_kw: Dict = _LOGGER_KW,
) -> None:
    """Import basic galpy packages."""
    import_from_file(
        ("..", "imports", "galpy_imports.py"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


@_set_docstring_import_x(("..", "imports", "amuse_imports.py"))
def import_amuse(
    verbose_imports: Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = None,
    logger_kw: Dict = _LOGGER_KW,
) -> None:
    """Import basic amuse packages."""
    import_from_file(
        ("..", "imports", "amuse_imports.py"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


##############################################################################
# END
