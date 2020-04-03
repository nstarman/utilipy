# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : pickle
#
# ----------------------------------------------------------------------------

"""Functions for making basic pickling easier.

Notes
-----
TODO:
    work save_pickles into here.
"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "dump",
    "dump_many",
    "load",
    "load_many",
]

#############################################################################
# IMPORTS

# GENERAL

import pickle as _pickle
import warnings
from typing import Optional, Tuple, Any

try:
    import dill
except ImportError:
    warnings.warn("can't import dill. Will only use pickle.")
    _HAS_DILL = False
else:
    _HAS_DILL = True


# PROJECT-SPECIFIC

from ..decorators.docstring import format_doc
from . import LogFile


#############################################################################
# PARAMETERS

_LOGFILE = LogFile(header=False)


#############################################################################
# CODE


@format_doc(None, odoc="\n\t".join(_pickle.dump.__doc__.split("\n")))
def dump(
    obj: Any,
    fname: str,
    protocol: Any = None,
    *,
    fopt: str = "b",
    fix_imports: bool = True,
    use_dill=False,
    # logger
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = None,
) -> None:
    """Wrap pickle.dump.

    `fname` replaces *file* and is a string for the filename
    this file is auto opened and closed

    pickle.dump docstring:

        {odoc}

    """
    if use_dill and not _HAS_DILL:
        raise ValueError("dill is not installed. cannot use dill.")

    logger.report(
        f"dumping obj at {fname}",
        (
            f"dumping obj at {fname} with fopt='{'w' + fopt}, "
            f"protocol=protocol, fix_imports={fix_imports}'"
        ),
        verbose=verbose,
    )

    with open(fname, "w" + fopt) as file:
        if use_dill:
            dill.dump(obj, file, protocol=protocol, fix_imports=fix_imports)
        else:
            _pickle.dump(obj, file, protocol=protocol, fix_imports=fix_imports)

    return


# /def


save = dump


# --------------------------------------------------------------------------


def dump_many(
    *objs: Tuple[Any, str],
    protocol: Any = None,
    fopt: str = "b",
    fix_imports: bool = True,
    use_dill=False,
    # logger
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = None,
) -> None:
    """Wrap pickle.dump.

    Parameters
    ----------
    *objs: Tuple[Any, str]
    protocol: Any
        (default None)
    fopt: str
        (default "b")
    fix_imports: bool
        (default True)
    logger: LogFile
    verbose: int or None, optional

    """
    for (obj, fname) in objs:
        dump(
            obj=obj,
            fname=fname,
            protocol=protocol,
            fopt=fopt,
            fix_imports=fix_imports,
            use_dill=use_dill,
            # logger
            logger=logger,
            verbose=verbose,
        )

    return


# /def


# --------------------------------------------------------------------------


@format_doc(None, odoc="\n\t".join(_pickle.load.__doc__.split("\n")))
def load(
    *fnames: str,
    fopt: str = "b",
    fix_imports: bool = True,
    encoding: str = "ASCII",
    errors: str = "strict",
    use_dill=False,
    # logger
    logger: LogFile = _LOGFILE,
    verbose: Optional[int] = None,
):
    """Wrap pickle.load.

    *fname* replaces *file* and is a string for the filename
    this file is auto opened and closed

    pickle.load docstring:

        {odoc}

    """
    if use_dill and not _HAS_DILL:
        raise ValueError("dill is not installed. cannot use dill.")

    res: list = [None] * len(fnames)  # preload results list
    for i, fname in enumerate(fnames):  # iterate through files

        logger.report(
            f"loading obj at {fname}",
            (
                f"loading obj at {fname} with fopt='{'r' + fopt}, "
                f"fix_imports={fix_imports}', encoding={encoding}, "
                f"errors={errors}"
            ),
            verbose=verbose,
        )

        with open(fname, "r" + fopt) as file:
            if use_dill:
                res[i] = dill.load(
                    file,
                    fix_imports=fix_imports,
                    encoding=encoding,
                    errors=errors,
                )
            else:
                res[i] = _pickle.load(
                    file,
                    fix_imports=fix_imports,
                    encoding=encoding,
                    errors=errors,
                )

    if len(fnames) == 1:
        return res[0]
    return res


# /def

load_many = load


# --------------------------------------------------------------------------

# def save_pickles(savefilename, *args, **kwargs):
#     """
#     NAME:
#        save_pickles
#     PURPOSE:
#        relatively safely save things to a pickle
#     INPUT:
#        savefilename - name of the file to save to; actual save operation
#                       will be performed on a temporary file and then that
#                       file will be shell mv'ed to savefilename
#        +things to pickle (as many as you want!)
#     OUTPUT:
#        none
#     HISTORY:
#        2010-? - Written - Bovy (NYU)
#        2011-08-23 - generalized and added to galpy.util - Bovy (NYU)

#     TODO work into this python

#     """
#     saving = True
#     interrupted = False
#     file, tmp_savefilename = tempfile.mkstemp()  # savefilename+'.tmp'
#     os.close(file)  # Easier this way
#     while saving:
#         try:
#             savefile = open(tmp_savefilename, 'wb')
#             file_open = True
#             if kwargs.get('testKeyboardInterrupt', False) and not interrupted:
#                 raise KeyboardInterrupt
#             for f in args:
#                 pickle.dump(f, savefile, pickle.HIGHEST_PROTOCOL)
#             savefile.close()
#             file_open = False
#             shutil.move(tmp_savefilename, savefilename)
#             saving = False
#             if interrupted:
#                 raise KeyboardInterrupt
#         except KeyboardInterrupt:
#             if not saving:
#                 raise
#             print("KeyboardInterrupt ignored while saving pickle ...")
#             interrupted = True
#         finally:
#             if file_open:
#                 savefile.close()
# # /def
