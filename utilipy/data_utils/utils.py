# -*- coding: utf-8 -*-

"""Utilities for :mod:`~utilipy.data_utils`."""


__all__ = [
    "intermix_arrays",
    "make_shuffler",
    "get_path_to_file",
]


##############################################################################
# IMPORTS

# BUILT-IN
import pathlib
import typing as T

# THIRD PARTY
import numpy as np
from astropy.utils.data import get_pkg_data_filenames

##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


# TODO stride option for block sizes
def intermix_arrays(*arrs: T.Sequence, axis=-1):
    """Intermix arrays.

    Parameters
    ----------
    *arrs : Sequence
    axis : int, optional

    Return
    ------
    arr : Sequence

    Examples
    --------
    Mix single scalar array (does nothing)

        >>> x = np.arange(5)
        >>> intermix_arrays(x)
        array([0, 1, 2, 3, 4])

    Mix two scalar arrays

        >>> y = np.arange(5, 10)
        >>> intermix_arrays(x, y)
        array([0, 5, 1, 6, 2, 7, 3, 8, 4, 9])

    Mix multiple scalar arrays

        >>> z = np.arange(10, 15)
        >>> intermix_arrays(x, y, z)
        array([ 0,  5, 10,  1,  6, 11,  2,  7, 12,  3,  8, 13,  4,  9, 14])

    Mix single ND array

        >>> xx = np.c_[x, y]
        >>> intermix_arrays(xx)
        array([[0, 1, 2, 3, 4],
               [5, 6, 7, 8, 9]])

    Mix two ND arrays

        >>> yy = np.c_[z, np.arange(15, 20)]
        >>> intermix_arrays(xx, yy)
        array([[ 0, 10,  1, 11,  2, 12,  3, 13,  4, 14],
               [ 5, 15,  6, 16,  7, 17,  8, 18,  9, 19]])

    """
    shape = list(np.asanyarray(arrs[0]).shape[::-1])
    shape[axis] *= len(arrs)

    return np.array(arrs).T.flatten().reshape(shape)


# /def


# -------------------------------------------------------------------


def make_shuffler(
    length: int, rng=None
) -> T.Tuple[T.Sequence[int], T.Sequence[int]]:
    """
    Shuffle and Unshuffle arrays.

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
    The package directory must exist.

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
