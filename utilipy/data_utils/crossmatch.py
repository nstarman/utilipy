# -*- coding: utf-8 -*-

"""Catalog x-matching on data fields.

Built from the extensive x-matching program in Jo Bovy's ``gaia_tools``,
but reconfigured to use the Astropy framework as much as possible.

"""

__author__ = "Nathaniel Starkman"
__credits__ = ["Jo Bovy", "Henry Leung"]


__all__ = [
    "indices_xmatch_fields",
    "xmatch_fields",
    "xmatch",
    "non_xmatched",
]


##############################################################################
# IMPORTS

# BUILT-IN
import functools
import itertools
import typing as T

# THIRD PARTY
import numpy as np

# PROJECT-SPECIFIC
from .decorators import idxDecorator

# from .xfm import data_graph as old_data_graph, DataTransform


##############################################################################
# PARAMETERS

_TBL_TYPE = np.recarray
_FIELDS_TYPE = T.List[str]
_IDX_TYPE = np.array
_IDXS_TYPE = T.List[_IDX_TYPE]
_INFO_TYPE = T.Dict[str, T.Sequence]


##############################################################################
# CODE
##############################################################################


@idxDecorator(as_ind=False)
def _indices_equality_match_on_catalog(
    catalog: _TBL_TYPE, other: _TBL_TYPE, fields: _FIELDS_TYPE
) -> _IDX_TYPE:
    """Indices of catalog data field(s) to match against a source catalog.

    This function is for discrete-valued data, such as tags.
    Note that this only matches `other` against `catalog`, meaning
    `catalog` can still have values which do not appear in `other`
    For coordinates, see `~indices_xmatch_coords`.

    This match is done on all the fields simultaneously, so in terms or
    a 2D array, two rows are considered a match only if all the values
    in the columns `fields` match.

    Parameters
    ----------
    catalog : recarray
        the source catalog against which the `other` catalog is matched.
    other : recarray
        match this against `catalog`
    fields : list
        List of fields on which to match.
        ex, ["color", "location"] where both `catalog` and `other` have
        those columns, hopefully with some matching values.

    Returns
    -------
    idx : ndarray
        indices into `other` such that only has values in `fields` that
        are in `catalog`.

    Notes
    -----
    .. todo::

        try more axes tricks to avoid loops.

    """
    # uniques for each field
    uns: T.Tuple[np.array]
    uns = (np.unique(np.array(catalog[n])) for n in fields)

    # indices into cat1
    # loop over fields  TODO vectorize ?
    idxs = (other[n] == un[:, None] for n, un in zip(fields, uns))
    # get combined index
    idx: _IDX_TYPE
    idx = np.sum(functools.reduce(np.logical_and, idxs), axis=0, dtype=bool)

    return idx


# /def


def indices_xmatch_fields(
    catalog: _TBL_TYPE, *others: _TBL_TYPE, fields: _FIELDS_TYPE
) -> T.Tuple[_IDXS_TYPE, _INFO_TYPE]:
    """Indices of xmatch of catalogs' data field(s) against a source catalog.

    This function is for discrete-valued data, such as tags.
    For coordinates, see `~indices_xmatch_coords`.

    This match is done on all the fields simultaneously, so in terms or
    a 2D array, two rows are considered a match only if all the values
    in the columns `fields` match.

    Parameters
    ----------
    catalog : Table or recarray
        The source catalog against which the `others` catalogs are matched.
    *others : Table or recarray
        match these against `catalog`
    fields : list
        List of fields on which to match.
        ex, ["color", "location"] where both `catalog` and `other` have
        those columns, hopefully with some matching values.

    Returns
    -------
    idxs : list of ndarrays
        each element of list is the x-match indices into the ith catalog,
        starting with `catalog`. So the i=0 index list is for `catalog` and
        the i=1 index list is the x-match indices for the first table
        in `others`.
    info : dict
        Useful information. Nothing yet.

    Notes
    -----
    .. todo::

        try more axes tricks to avoid loops.

    """
    idxs: _IDXS_TYPE = [
        _indices_equality_match_on_catalog(catalog, c, fields=fields)
        for c in others
    ]  # TODO with numpy
    # and need to do once in reverse on the source catalog
    catalog_idx: _IDX_TYPE = _indices_equality_match_on_catalog(
        others[1][idxs[0]], catalog, fields
    )
    idxs.insert(0, catalog_idx)

    info: _INFO_TYPE = {}

    return idxs, info


# /def


def xmatch_fields(
    catalog: _TBL_TYPE, *others: _TBL_TYPE, fields: _FIELDS_TYPE
) -> T.Tuple[T.List[T.Any], _INFO_TYPE]:
    """Cross-match catalogs' data field(s) against a source catalog.

    This function is for discrete-valued data, such as tags.
    For coordinates, see `~indices_xmatch_coords`.

    This match is done on all the fields simultaneously, so in terms or
    a 2D array, two rows are considered a match only if all the values
    in the columns `fields` match.

    Parameters
    ----------
    catalog : Table or recarray
        The source catalog against which the `others` catalogs are matched.
        fields for which there are no matches are also filtered.
    *others : Table or recarray
        match these against `catalog`
    fields : list
        List of fields on which to match.
        ex, ["color", "location"] where both `catalog` and `other` have
        those columns, hopefully with some matching values.

    Returns
    -------
    idxs : list of ndarrays
        each element of list is the x-match indices into the ith catalog,
        starting with `catalog`. So the i=0 index list is for `catalog` and
        the i=1 index list is the x-match indices for the first table
        in `others`,


    Notes
    -----
    .. todo::

        try more axes tricks to avoid loops.

    """
    if not isinstance(fields, list):  # TODO less draconian
        raise TypeError("must be a list")
    if len(others) == 0:
        raise ValueError(
            "Must have at least one catalog against-which to xmatch."
        )

    # iterate through all catalogs, making sure has the field name
    # iterators are the catalog number and field names
    # these are itered together to generate all list combinations.
    for i, field in itertools.product(range(len(others) + 1), fields):
        try:
            if i == 0:
                catalog[field]
            else:
                others[i][field]
        except Exception as e:  # TODO better error message
            print(f"need to have {field} in catalog {i}")
            raise e

    # ------------------------------

    idxs: _IDXS_TYPE
    info: _INFO_TYPE
    idxs, info = indices_xmatch_fields(catalog, *others, fields=fields)

    cat_matches = [catalog[idxs[0]]] + [
        c[idx] for c, idx in zip(others, idxs[1:])
    ]

    info.update({"idxs": idxs})

    return cat_matches, info


xmatch_tags = xmatch_fields  # just another name

# /def


##############################################################################
# General Cross-Match

# @data_graph.decorate(cat1=np.recarray, cat2=np.recarray)
def xmatch(
    *catalogs,
    match_fields: T.Sequence,
) -> T.Tuple[T.List[T.Any], _INFO_TYPE]:
    """Cross-match two catalogs.

    .. todo::

        - find duplicates before matching ?
        - allow more catalogs to be xmatched

    Parameters
    ----------
    cat1, cat2: Any
        the two catalogs to crossmatch
        must be convertible to recarray
    match_fields : str, optional
        data tag on which to additionally cross-match, default None.
        this also works for any discrete-valued data column.

    References
    ----------
    https://github.com/jobovy/gaia_tools/

    """
    cat_matches, info = xmatch_fields(*catalogs, fields=match_fields)

    return cat_matches, info


# /def

# -------------------------------------------------------------------


def non_xmatched(
    catalog1: T.Sequence,
    catalog2: T.Sequence,
    indices1: T.Sequence,
    indices2: T.Sequence,
):
    """Find non cross-matched catalog components.

    Parameters
    ----------
    catalog1, catalog2 : Sequence
        the catalogs
    indices1, indices2 : Sequence
        indices into catalogs for the x-match.
        :func:`~starkman_thesis.utils.data.xmatch.xmatch_indices_coords` output
        or in :func:`~starkman_thesis.utils.data.xmatch.xmatch_coords` info

    Returns
    -------
    catalog1_matches, catalog2_matches : catalog input types
        the x-matched catalogs
    info : dict
        Useful information.

            - nindices1 : indices into `catalog1` not x-matched.
            - nindices1 : indices into `catalog2` not x-matched.

    """
    # index arrays of length catalog, for getting non-matches
    c1idx = np.arange(len(catalog1))  # catalog1 array
    c2idx = np.arange(len(catalog2))  # catalog2 array
    # bool array of non-matches
    nindices1 = np.where(~np.in1d(c1idx, indices1))[0]
    nindices2 = np.where(~np.in1d(c2idx, indices2))[0]

    ninfo = {
        "nindices1": nindices1,
        "nindices2": nindices2,
    }  # non-match info dict

    return (catalog1[nindices1], catalog2[nindices2]), ninfo


# /def


##############################################################################
# END
