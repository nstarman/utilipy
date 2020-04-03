# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Mixed MegaCam Gen1 PS1
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Mega-Cam gen1 and PanSTARRS1 Mixed Functions."""

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]

__all__ = ["iCFHT", "rPS", "CFHTtoPanstarrs_gmr"]

#############################################################################
# IMPORTS

# GENERAL

from astropy.table import Table


# PROJECT-SPECIFIC

from .. import quantity_io, MAG
from . import PS1_from_MegaCamGen1

# from . import MegaCamGen1_from_PS1


#############################################################################
# CODE
#############################################################################


@quantity_io()
def iCFHT(cfht: Table, ps: Table, **kw) -> MAG:
    """Mega-Cam gen1 i-band from CFHT R_MP9601 and I_MP9701.

    Parameters
    ----------
    cfht: Astropy Table
        needs r col
    ps: Astropy Table
        needs i col
    r: str
        r column
        used in cfht table
    i: str
        i column
        used in ps table

    Returns
    -------
    i_cfht : Quantity array_like
        CFHT i-band

    Notes
    -----
    .. math::

        i_{CFHT} = i_{PS} +.007 - 0.078 * (r_{CFHT}-i_{CFHT})

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html.

    """
    r = kw.get("r", "r")
    i = kw.get("i", "i")

    i_cfht = (ps[i] + 0.007 * MAG - 0.078 * cfht[r]) / (1 - 0.078)
    return i_cfht


# /def


@quantity_io()
def rPS(cfht: Table, ps: Table, **kw) -> MAG:
    """Pan-STARRS r band from CFHT r and Panstarrs i.

    rPS - rCFHT = -.001 + 0.023(rCFHT-iCFHT)
    calls iCFHT(cfht, ps)

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html

    Parameters
    ----------
    cfht: Astropy Table
        needs r col
    ps: Astropy Table
        needs i col
    r: str
        r column
        used in cfht table
    i: str
        i column
        used in ps table

    Returns
    -------
    r_ps : Quantity array_like
        Pan-STARRS1 r-band

    """
    r = kw.get("r", "r")
    i_cfht = iCFHT(cfht, ps, **kw)

    r_ps = cfht[r] - 0.001 * MAG + 0.023 * (cfht[r] - i_cfht)
    return r_ps


# /def


@quantity_io()
def CFHTtoPanstarrs_gmr(cfht: Table, ps: Table, **kw) -> MAG:
    """Pan-STARRS g-r color from CFHT g and Panstarrs r.

    Parameters
    ----------
    cfht: Astropy Table
        needs r col
    ps: Astropy Table
        needs i col
    g: str
        g column
        used in table
    r: str
        r column
        used in cfht table
    i: str
        i column
        used in ps table
    gmr: str
        g-r column

    Returns
    -------
    g-r_ps : Quantity array_like
        Pan-STARRS1 g-r color

    """
    # g filter
    g_ps = PS1_from_MegaCamGen1.G(cfht, **kw)
    # r filter
    r_ps = rPS(cfht, ps, **kw)
    return g_ps - r_ps


# /def


# @quantity_io()
# def PSfromCFHTg2gmrSpl(spline, ps, **kw) -> MAG:
#     """
#     g_ps -> g_cfht -> g-r_cfht (via spline), r_cfht -> g-r_ps
#     calculates g_cfht from PanSTARRS
#                gmr_cfht from the spline(g_cfht)
#     r_cfht = g_cfht - gmr_cfht

#     calculates gmr_ps from cfht information

#     Parameters
#     ----------
#     g: str
#         g column
#         used in _____ table
#     r: str
#         r column
#         used in cfht table
#     i: str
#         i column
#         used in ps table
#     gmr: str
#         g-r column
#     gmi: str
#         g-i column
#     """
#     g = kw.get('g', 'g')
#     r = kw.get('r', 'r')
#     gmr = kw.get('gmr', 'g-r')

#     # g in CFHT
#     g_cfht = MegaCamGen1_from_PS1.G_MP9401(ps, **kw)

#     # r in CFHT
#     gmr_cfht = spline(g_cfht) * MAG  # g-r from the spline
#     r_cfht = g_cfht - gmr_cfht  # r = g - (g-r)

#     # cfht table for CFHTtoPanstarrs_gmr
#     cfht = QTable([g_cfht, r_cfht, gmr_cfht], names=(g, r, gmr))

#     # g-r CFHTtoPanstarrs_gmr
#     gmr_ps = CFHTtoPanstarrs_gmr(cfht, ps, **kw)
#     return gmr_ps# /def
