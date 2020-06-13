# -*- coding: utf-8 -*-

"""Data Utilities."""

__author__ = "Nathaniel Starkman"


__all__ = [
    # modules
    "crossmatch",
    "decorators",
    "select",
    "fitting",
    "xfm",
    # functions
    "idxDecorator",
    # data transformation graph
    "data_graph",
    "TransformGraph",
    "DataTransform",
    # xmatch
    "indices_xmatch_fields",
    "xmatch_fields",
    "xmatch",
    "non_xmatched",
    # local
    "get_path_to_file",
]


##############################################################################
# IMPORTS

# BUILT-IN

import pathlib


# THIRD PARTY

from astropy.utils.data import get_pkg_data_filenames


# PACKAGE-SPECIFIC

from .crossmatch import (
    indices_xmatch_fields,
    xmatch_fields,
    xmatch,
    non_xmatched,
)
from .decorators import idxDecorator
from .xfm import data_graph, TransformGraph, DataTransform
from .select import *  # noqa

# modules
from . import decorators, select, fitting, xfm, crossmatch


# -------------------------------------------------------------------
# __ALL__

__all__ += select.__all__


##############################################################################
# CODE
##############################################################################


def get_path_to_file(*data_name: str, package=None):
    """Get path to file.

    Similar to :func:`~astropy.utils.data.get_pkg_data_filename`, but only
    gets the path to the file, does not check if the file exists.

    Parameters
    ----------
    *data_name : tuple of str
        the path, without folder delimiters (which are platform specific)
        relative to `package`.

        One of the following:

        * The name of a directory included in the source
          distribution.  The path is relative to the module
          calling this function.  For example, if calling from
          ``astropy.pkname``, use ``'data'`` to get the
          files in ``astropy/pkgname/data``.
        * Remote URLs are not currently supported.

    package : str, optional
        If specified, look for a file relative to the given package, rather
        than the default of looking relative to the calling module's package.

    Returns
    -------
    filename : str
        A file path on the local file system corresponding to the data
        requested in ``data_name``.

    """
    # TODO more robust system
    fps = list(get_pkg_data_filenames(".", package=package))
    filename = pathlib.Path(fps[0]).parent.joinpath(*data_name)

    return str(filename)


# /def


# ------------------------------------------------------------------------


##############################################################################
# DONE
