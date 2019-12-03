# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : pickle
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""functions for making basic pickling easier.

Notes
-----
TODO:
    work save_pickles into here.
"""

__author__ = "Nathaniel Starkman"

#############################################################################
# IMPORTS

# GENERAL
from typing import Any, Union, Optional
import pickle

# import tempfile

# PROJECT-SPECIFIC
from ..decorators.docstring import format_doc
from . import LogPrint

#############################################################################
# PARAMETERS

_LOGFILE = LogPrint(header=False)


#############################################################################
# CODE


@format_doc(None, odoc="\n\t".join(pickle.dump.__doc__.split("\n")))
def dump(
    obj: Any,
    fname: str,
    protocol: Any = None,
    *,
    fopt: str = "b",
    fix_imports: bool = True,
    # logger
    logger: LogPrint = _LOGFILE,
    verbose: Optional[int] = None,
) -> None:
    """Wrap pickle.dump.

    *fname* replaces *file* and is a string for the filename
    this file is auto opened and closed

    pickle.dump docstring:

    ::

        {odoc}

    """
    logger.report(
        f"dumping obj at {fname}",
        (
            f"dumping obj at {fname} with fopt='{'w' + fopt}, "
            f"protocol=protocol, fix_imports={fix_imports}'"
        ),
        verbose=verbose,
    )

    with open(fname, "w" + fopt) as file:
        pickle.dump(obj, file, protocol=protocol, fix_imports=fix_imports)

    return


# /def


save = dump


# --------------------------------------------------------------------------


@format_doc(None, odoc="\n\t".join(pickle.load.__doc__.split("\n")))
def load(
    fname: str,
    *,
    fopt: str = "b",
    fix_imports: bool = True,
    encoding: str = "ASCII",
    errors: str = "strict",
    # logger
    logger: LogPrint = _LOGFILE,
    verbose: Optional[int] = None,
):
    """Wrap pickle.load.

    *fname* replaces *file* and is a string for the filename
    this file is auto opened and closed

    pickle.load docstring:

    ::

        {odoc}

    """
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
        res = pickle.load(
            file, fix_imports=fix_imports, encoding=encoding, errors=errors
        )
    return res


# /def

# --------------------------------------------------------------------------

# def save_pickles(savefilename, *args, **kwargs):
#     """
#     NAME:
#        save_pickles
#     PURPOSE:
#        relatively safely save things to a pickle
#     INPUT:
#        savefilename - name of the file to save to; actual save operation will be performed on a temporary file and then that file will be shell mv'ed to savefilename
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
