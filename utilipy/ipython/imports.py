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
    "aimport",
    "set_autoreload",
    # specific importers
    "import_base",
    "import_extended",
    "import_astropy",
    "import_matplotlib",  # 'import_plotly',
    "import_galpy",
    "import_amuse",
    "import_astronat",
]


##############################################################################
# IMPORTS

# BUILT-IN
import typing as T
from pathlib import Path

# THIRD PARTY
from IPython import get_ipython

# PROJECT-SPECIFIC
from .autoreload import aimport, set_autoreload
from utilipy.data_utils import get_path_to_file
from utilipy.decorators.docstring import set_docstring_for_import_func
from utilipy.imports import use_import_verbosity
from utilipy.utils.logging import LogFile

##############################################################################
# SETUP

_LOGFILE = LogFile(header=False, verbose=0)
_LOGGER_KW = {"print": False}


##############################################################################
# CODE
##############################################################################


def import_from_file(
    *files: str,
    is_relative: bool = True,
    verbose_imports: T.Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose=None,
    logger_kw: T.Optional[T.Dict[str, T.Any]] = _LOGGER_KW,
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
        relative = [is_relative] * len(files)
    else:  # already a list
        if len(is_relative) != len(files):  # checking correct length
            raise ValueError("len(relative) != len(files)")
        relative = is_relative

    with use_import_verbosity(verbose_imports):  # handle verbose-imports

        for file, rltv in zip(files, relative):  # loop over imports
            if rltv:
                file = str(Path(file).resolve())

            # get_ipython inbuilt to jupyter
            get_ipython().magic(f"run {file}")

            # logging
            # implemented separately b/c files often have own print statements
            logger_kw = logger_kw or {}
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
    astronat: bool = False,
    # utils
    verbose_imports: T.Optional[bool] = None,
    # logging
    logger: LogFile = _LOGFILE,
    verbose: T.Optional[int] = 0,
    logger_kw: T.Optional[T.Dict[str, T.Any]] = None,
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
        import_base -> `utilipy/imports/base_imports.py`
    astropy: bool
        import_astropy -> `utilipy/imports/astropy_imports.py`
    matplotlib: bool
        import_matplotlib -> `utilipy/imports/matplotlib_imports.py`
    plotly: bool
        import_plotly -> `utilipy/imports/plotly_imports.py`
    extended: bool
        import_extended -> `utilipy/imports/extended_imports.py`
    galpy: bool
        import_galpy -> `utilipy/imports/galpy_imports.py`
    amuse: bool
        import_amuse -> `utilipy/imports/amuse_imports.py`
    astronat : bool
        import_astronat -> `utilipy/imports/astronat_imports.py`

    Other Parameters
    ----------------
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

    ``utilipy.imports.conf.verbose_imports = False``
    ``utilipy.ipython.imports.run_imports(base=True, verbose_imports=None)``
    imports from `utilipy/imports/base.py` with default import-verbosity state

    """
    # make kwargs that go into every standard import
    kw = dict(verbose_imports=verbose_imports, logger=logger, verbose=verbose)
    logger_kw = logger_kw or {}

    if verbose_imports:
        print("Importing:")

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

    if astronat:
        import_astronat(**kw)

    # ---------------------------------------------

    # when combined
    if astropy & matplotlib:
        from matplotlib import pyplot
        from astropy.visualization import astropy_mpl_style

        pyplot.style.use(astropy_mpl_style)

    # TODO, embed in galpy_imports using argparse
    if galpy & amuse:
        from galpy.potential import to_amuse  # noqa

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

    return


# /def


##############################################################################
# Specific Imports
# TODO make these with a function


@set_docstring_for_import_func(
    "base_imports.py", package="utilipy.imports", section="Returns"
)
def import_base(
    verbose_imports: T.Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: T.Optional[int] = None,
    logger_kw: T.Optional[T.Dict[str, T.Any]] = _LOGGER_KW,
) -> None:
    """Import base packages."""
    import_from_file(
        get_path_to_file("base_imports.py", package="utilipy.imports"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


@set_docstring_for_import_func(
    "extended_imports.py",
    package="utilipy.imports",
    section="Routine Listings",
)
def import_extended(
    verbose_imports: T.Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: T.Optional[int] = None,
    logger_kw: T.Optional[T.Dict[str, T.Any]] = _LOGGER_KW,
) -> None:
    """Import extended packages."""
    import_from_file(
        get_path_to_file("extended_imports.py", package="utilipy.imports"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


@set_docstring_for_import_func(
    "astropy_imports.py", package="utilipy.imports", section="Routine Listings"
)
def import_astropy(
    verbose_imports: T.Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: T.Optional[int] = None,
    logger_kw: T.Optional[T.Dict[str, T.Any]] = _LOGGER_KW,
) -> None:
    """Import basic astropy packages."""
    import_from_file(
        get_path_to_file("astropy_imports.py", package="utilipy.imports"),
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


@set_docstring_for_import_func(
    "matplotlib_imports.py",
    package="utilipy.imports",
    section="Routine Listings",
)
def import_matplotlib(
    verbose_imports: T.Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: T.Optional[int] = None,
    logger_kw: T.Optional[T.Dict[str, T.Any]] = _LOGGER_KW,
) -> None:
    """Import basic Matplotlib packages."""
    import_from_file(
        get_path_to_file("matplotlib_imports.py", package="utilipy.imports"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


@set_docstring_for_import_func(
    "plotly_imports.py", package="utilipy.imports", section="Routine Listings"
)
def import_plotly(
    verbose_imports: T.Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: T.Optional[int] = None,
    logger_kw: T.Optional[T.Dict[str, T.Any]] = _LOGGER_KW,
) -> None:
    """Import basic Matplotlib packages."""
    import_from_file(
        get_path_to_file("plotly_imports.py", package="utilipy.imports"),
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


@set_docstring_for_import_func(
    "galpy_imports.py", package="utilipy.imports", section="Routine Listings"
)
def import_galpy(
    verbose_imports: T.Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: T.Optional[int] = None,
    logger_kw: T.Optional[T.Dict[str, T.Any]] = _LOGGER_KW,
) -> None:
    """Import basic galpy packages."""
    import_from_file(
        get_path_to_file("galpy_imports.py", package="utilipy.imports"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


@set_docstring_for_import_func(
    "amuse_imports.py", package="utilipy.imports", section="Routine Listings"
)
def import_amuse(
    verbose_imports: T.Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: T.Optional[int] = None,
    logger_kw: T.Optional[T.Dict[str, T.Any]] = _LOGGER_KW,
) -> None:
    """Import basic amuse packages."""
    import_from_file(
        get_path_to_file("amuse_imports.py", package="utilipy.imports"),
        is_relative=False,
        verbose_imports=verbose_imports,
        logger=logger,
        verbose=verbose,
        logger_kw=logger_kw,
    )
    return


# /def


@set_docstring_for_import_func(
    "astronat_imports.py",
    package="utilipy.imports",
    section="Routine Listings",
)
def import_astronat(
    verbose_imports: T.Optional[bool] = None,
    logger: LogFile = _LOGFILE,
    verbose: T.Optional[int] = None,
    logger_kw: T.Optional[T.Dict[str, T.Any]] = _LOGGER_KW,
) -> None:
    """Import basic amuse packages."""
    import_from_file(
        get_path_to_file("astronat_imports.py", package="utilipy.imports"),
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
