# -*- coding: utf-8 -*-

# Docstring and Metadata
"""Mega-Cam gen1 bands from PanSTARRS 1 bands."""

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]

__all__ = ["G", "R", "I", "Z", "GmR", "GmI", "GmZ", "RmI", "RmZ", "ImZ"]

#############################################################################
# IMPORTS

# GENERAL
import warnings
from astropy.table import Table

# PROJECT-SPECIFIC
from .. import quantity_io, MAG


#############################################################################
# CODE
#############################################################################


@quantity_io()
def G(cfht: Table, **kw) -> MAG:
    r"""Pan-STARRS g band from CFHT G_MP9401 and R_MP9601.

    Parameters
    ----------
    cfht: Astropy Table
        need: g
        either: r, g-r col
    g: str  (default 'g')
        G_MP9401 column name
    r: str  (default 'r')
        R_MP9601 column name
    gmr: str  (default 'g-r')
        G_MP9401-R_MP9601 column name

    Returns
    -------
    g_ps : Quantity array_like
        Pan-STARRS1 g-band

    Notes
    -----
    .. math::

        g_{PS} = g_{CFHT} = 0.004 * (g_{CFHT} - r_{CFHT})

    limited to :math:`-1.5 \rm{mag} < g-i < 2.5 \rm{mag}`

    filter transformations from
    `<http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_

    """
    g, r = kw.get("g", "g"), kw.get("r", "r")
    gmr = kw.get("gmr", "g-r")

    if gmr in cfht.colnames:
        gmr = cfht[gmr]
    else:
        gmr = cfht[g] - cfht[r]

    ind = (-1.5 * MAG < gmr) & (gmr < 2.5 * MAG)
    if not all(ind):
        warnings.warn("PS1.G: not all -1.5 mag < (g-r)_ps < 2.5 mag")

    c0 = 0.0 * MAG
    c1 = 0.004
    g_cfht = cfht[g]

    g_ps = g_cfht + c0 + (c1 * gmr)
    return g_ps


@quantity_io()
def R(cfht: Table, **kw) -> MAG:
    r"""Pan-STARRS g band from CFHT R_MP9601 and I_MP9701.

    Parameters
    ----------
    cfht: Astropy Table
        need: r col
        either: i, r-i col
    r: str  (default 'r')
        R_MP9601 column name
    i: str  (default 'i')
        I_MP9701 column name
    rmi: str  (default 'r-i')
        G_MP9401-I_MP9701 column name

    Returns
    -------
    r_ps : Quantity array_like

    Notes
    -----
    .. math::

        r_{PS} = r_{CFHT} -.001 + 0.023*(r_{CFHT}-i_{CFHT})

    limited to :math:`-.9 \rm{mag} < (g-i)_{CFHT} < 3 \rm{mag}`

    filter transformations from
    `<http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_

    """
    r, i = kw.get("r", "r"), kw.get("i", "i")
    rmi = kw.get("rmi", "r-i")

    if rmi in cfht.colnames:
        rmi = cfht[rmi]
    else:
        rmi = cfht[r] - cfht[i]

    ind = (-0.9 * MAG < rmi) & (rmi < 3 * MAG)
    if not all(ind):
        warnings.warn("PS1.R: not all -.9 mag < (g-i)_ps < 3 mag")

    c0 = -0.001 * MAG
    c1 = 0.023
    r_cfht = cfht[r]

    r_ps = r_cfht + c0 + (c1 * rmi)
    return r_ps


@quantity_io()
def I(cfht: Table, **kw) -> MAG:
    r"""Pan-STARRS i band from CFHT R_MP9601 and I_MP9701.

    Parameters
    ----------
    cfht: Astropy Table
        need: i col
        either: r, r-i col
    r: str  (default 'r')
        R_MP9601 column name
    i: str  (default 'i')
        I_MP9701 column name
    rmi: str  (default 'r-i')
        G_MP9401-I_MP9701 column name

    Returns
    -------
    i_ps : Quantity array_like

    Notes
    -----
    .. math::

        i_{PS} = i_{CFHT} -.007 + 0.078 * (r_{CFHT}-i_{CFHT})

    limited to :math:`.1 \rm{mag} < (g-i)_{CFHT} < 3 \rm{mag}`

    filter transformations from
    `<http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_

    """
    r, i = kw.get("r", "r"), kw.get("i", "i")
    rmi = kw.get("rmi", "r-i")

    if rmi in cfht.colnames:
        rmi = cfht[rmi]
    else:
        rmi = cfht[r] - cfht[i]

    ind = (0.1 * MAG < rmi) & (rmi < 3 * MAG)
    if not all(ind):
        warnings.warn("PS1.I not all .1 mag < (g-i)_ps < 3 mag")

    c0 = -0.007 * MAG
    c1 = 0.078
    i_cfht = cfht[i]

    i_ps = i_cfht + c0 + (c1 * rmi)
    return i_ps


@quantity_io()
def Z(cfht: Table, **kw) -> MAG:
    r"""Pan-STARRS g band from CFHT I_MP9701, Z_MP9801.

    Parameters
    ----------
    cfht: Astropy Table
        need: i, z cols
        either: i-z col
    i: str  (default 'i')
        I_MP9701 column name
    z: str  (default 'z')
        Z_MP9801 column name
    imz: str  (default 'i-z')
        I_MP9701-Z_MP9801 column name

    Returns
    -------
    z_ps : Quantity array_like

    Notes
    -----
    .. math::

        z_{PS}-z_{CFHT} = 0.078(i_{CFHT}-z_{CFHT}) + 0.029(i_{CFHT}-z_{CFHT})^2

    limited to :math:`-.1 \rm{mag} < (g-i)_{CFHT}`

    filter transformations from
    `<http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_

    """
    i, z = kw.get("i", "i"), kw.get("z", "z")
    imz = kw.get("imz", "i-z")

    if imz in cfht.colnames:
        imz = cfht[imz]
    else:
        imz = cfht[i] - cfht[z]

    ind = (-0.1 * MAG < imz) & (imz < 2.5 * MAG)
    if not all(ind):
        warnings.warn("PS1.Z not all -.1 mag < (g-i)_ps < 3 mag")

    c0 = 0.0 * MAG
    c1 = 0.078
    c2 = 0.029 / MAG
    z_cfht = cfht[z]

    z_ps = z_cfht + c0 + (c1 * imz) + (c2 * imz ** 2)
    return z_ps


#############################################################################
# Colors


@quantity_io()
def GmR(cfht: Table, **kw) -> MAG:
    """G-R CFHT.

    Parameters
    ----------
    cfht: astropy Table

    Returns
    -------
    G-R : Quantity array_like

    Notes
    -----
    filter transformations from
    `MegaCam to Pan-STARRS
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    return G(cfht, **kw) - R(cfht, **kw)


@quantity_io()
def GmI(cfht: Table, **kw) -> MAG:
    """G-R CFHT.

    Parameters
    ----------
    cfht: astropy Table

    Returns
    -------
    G-I : Quantity array_like

    Notes
    -----
    filter transformations from
    `MegaCam to Pan-STARRS
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    return G(cfht, **kw) - I(cfht, **kw)


@quantity_io()
def GmZ(cfht: Table, **kw) -> MAG:
    """G-R CFHT.

    Parameters
    ----------
    cfht: astropy Table

    Returns
    -------
    G-I : Quantity array_like

    Notes
    -----
    filter transformations from
    `MegaCam to Pan-STARRS
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    return G(cfht, **kw) - Z(cfht, **kw)


@quantity_io()
def RmI(cfht: Table, **kw) -> MAG:
    """G-R CFHT.

    Parameters
    ----------
    cfht: astropy Table

    Returns
    -------
    G-I : Quantity array_like

    Notes
    -----
    filter transformations from
    `MegaCam to Pan-STARRS
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    return R(cfht, **kw) - I(cfht, **kw)


@quantity_io()
def RmZ(cfht: Table, **kw) -> MAG:
    """G-R CFHT.

    Parameters
    ----------
    cfht: astropy Table

    Returns
    -------
    G-I : Quantity array_like

    Notes
    -----
    filter transformations from
    `MegaCam to Pan-STARRS
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    return R(cfht, **kw) - Z(cfht, **kw)


@quantity_io()
def ImZ(cfht: Table, **kw) -> MAG:
    """G-R CFHT.

    Parameters
    ----------
    cfht: astropy Table

    Returns
    -------
    G-I : Quantity array_like

    Notes
    -----
    filter transformations from
    `MegaCam to Pan-STARRS
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    return I(cfht, **kw) - Z(cfht, **kw)


###########################################################################
# END
