# -*- coding: utf-8 -*-

"""Utilities for :mod:`~utilipy.data_utils`."""


__all__ = [
    "shuffle",
    "get_path_to_file",
]


##############################################################################
# IMPORTS

# BUILT-IN

import pathlib
import typing as T


# THIRD PARTY

from astropy.utils.data import get_pkg_data_filenames

import numpy as np

# PROJECT-SPECIFIC


##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


def shuffle(
    length: int, rng=None
) -> T.Tuple[T.Sequence[int], T.Sequence[int]]:
    """Shuffle and Unshuffle arrays.

    Parameters
    ----------
    length : int
        Array length for which to construct (un)shuffle arrays.
    rng : :class:`~numpy.random.Generator` instance, optional
        random number generator.

    Returns
    -------
    shuffler : `~numpy.ndarray`
        index array that shuffles any array of size `length` along
        a specified axis
    undo : `~numpy.ndarray`
        index array that undoes above, if applied identically.

    """
    if rng is None:
        try:
            rng = np.random.default_rng()
        except AttributeError:
            rng = np.random

    # start with index array
    shuffler = np.arange(length)
    # now shuffle array (in-place)
    rng.shuffle(shuffler)

    # and construct the unshuffler
    undo = shuffler.argsort()

    return shuffler, undo


# /def


# -------------------------------------------------------------------


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


##############################################################################
# END
