# -*- coding: utf-8 -*-

"""PanSTARRS 1 bands from Mega-Cam gen1 bands."""

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]

__all__ = [
    'U_MP9301', 'G_MP9401', 'R_MP9601', 'I_MP9701', 'Z_MP9801',
    'UmG', 'UmR', 'UmI', 'UmZ', 'GmR', 'GmI', 'GmZ', 'RmI', 'RmZ', 'ImZ'
]

#############################################################################
# IMPORTS

# GENERAL
import warnings

# PROJECT-SPECIFIC
from astropy.table import Table, QTable
from .. import units


#############################################################################
# CODE
#############################################################################

@units.quantity_io()
def U_MP9301(ps, **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT U-MP9301 band.

    Parameters
    ----------
    ps: astropy Table
        need: g col
        either: i, g-i col
    g: str
        g column name
        (default 'g')
    i: str
        i column name
        (default 'i')
    gmi: str
        g-i column name
        (default 'g-i')

    Returns
    -------
    U_MP9301 : Quantity array_like
        CFHT u-band

    Notes
    -----
    The conversion is::

        u_CFHT = g_PS + .523 - .343 gmi + 2.44 gmi^2 - .998 gmi^3

    where `gmi = g_PS - i_PS`
    in the range `0.3 < gmi < 1.5 [mag]`.

    filter transformations from `Pan-STARRS to MegaCam plots. Top row, 1st plot
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (.3 * units.mag < gmi) & (gmi < 1.5 * units.mag)
    if not all(ind):
        warnings.warn('MCg1.U: not all .3 mag < (g-i)_ps < 1.5 mag')

    c0 = .523 * units.mag
    c1 = -.343
    c2 = 2.44 / units.mag
    c3 = -.998 / units.mag**2
    g_ps = ps[g]

    u_cfht = g_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)

    return u_cfht
# /def


@units.quantity_io()
def G_MP9401(ps, **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT G-MP9401 band.

    Parameters
    ----------
    ps: astropy Table
        need: g col
        either: i, g-i col
    g: str
        (default 'g')
        g column name
    i: str
        (default 'i')
        i column name
    gmi: str
        (default 'g-i')
        g-i column name

    Returns
    -------
    G_MP9401 : Quantity array_like
        CFHT g-band

    Notes
    -----
    .. math::

        g_{CFHT} = g_{PS} -.001 - .004 gmi - .0056 gmi^2 + .00292 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`-1 \rm{mag} < g-i < 4 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots. Top row, 2nd plot
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * units.mag < gmi) & (gmi < 4 * units.mag)
    if not all(ind):
        warnings.warn('MCg1.G: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = -.001 * units.mag
    c1 = -.004
    c2 = -.0056 / units.mag
    c3 = .00292 / units.mag**2
    g_ps = ps[g]

    g_cfht = g_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return g_cfht
# /def


@units.quantity_io()
def R_MP9601(ps, **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT R-MP9601 band.

    Parameters
    ----------
    ps: astropy Table
        need: r, col
        either: (g & i), g-i col
    g: str
        (default 'g')
        g column name
    r: str
        (default 'r')
        r column name
    i: str
        (default 'i')
        i column name
    gmi: str
        (default 'g-i')
        g-i column name

    Returns
    -------
    R_MP9601 : Quantity array_like
        CFHT r-band

    Notes
    -----

    .. math::

        r_{CFHT} = r_{PS} + .002 - .017 gmi + .00554 gmi^2 - .000692 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`-1 \rm{mag} < g-i < 4 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots. Top row, 3rd plot
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    g, r, i = kw.get('g', 'g'), kw.get('r', 'r'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * units.mag < gmi) & (gmi < 4 * units.mag)
    if not all(ind):
        warnings.warn('MCg1.R: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = .002 * units.mag
    c1 = -.017
    c2 = .00554 / units.mag
    c3 = -.000692 / units.mag**2
    r_ps = ps[r]

    r_cfht = r_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return r_cfht
# /def


@units.quantity_io()
def I_MP9701(ps, **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT I-MP9701 band.

    Parameters
    ----------
    ps: astropy Table
        need: i col
        either: g, g-i col
    g: str
        (default 'g')
        g column name
    i: str
        (default 'i')
        i column name
    gmi: str
        (default 'g-i')
        g-i column name

    Returns
    -------
    I_MP9701 : Quantity array_like
        CFHT i-band

    Notes
    -----
    .. math::

        i_{CFHT} = i_{PS} + .001 - .021 gmi + .00398 gmi^2 - .00369 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`-1 \rm{mag} < g-i < 4 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots. 2nd row, 1st plot
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * units.mag < gmi) & (gmi < 4 * units.mag)
    if not all(ind):
        warnings.warn('MCg1.I: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = .001 * units.mag
    c1 = -.021
    c2 = .00398 / units.mag
    c3 = -.00369 / units.mag**2
    i_ps = ps[i]

    i_cfht = i_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return i_cfht
# /def


@units.quantity_io()
def Z_MP9801(ps, **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT Z-MP9801 band.

    Parameters
    ----------
    ps: astropy Table
        need: z col
        either: (g & i), g-i col
    g: str
        (default 'g')
        g column name
    i: str
        (default 'i')
        i column name
    z: str
        (default 'z')
        z column name
    gmi: str
        (default 'g-i')
        g-i column name

    Returns
    -------
    Z_MP9801 : Quantity array_like
        CFHT z-band

    Notes
    -----
    .. math::

        z_{CFHT} = z_{PS} -.009 - .029 gmi + .012 gmi^2 - .00367 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`-1 \rm{mag} < g-i < 4 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots. 2nd row, 2nd plot
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    g, i, z = kw.get('g', 'g'), kw.get('i', 'i'), kw.get('z', 'z')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * units.mag < gmi) & (gmi < 4 * units.mag)
    if not all(ind):
        warnings.warn('MCg1.Z: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = -.009 * units.mag
    c1 = -.029
    c2 = .012 / units.mag
    c3 = -.00367 / units.mag**2
    z_ps = ps[z]

    z_cfht = z_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return z_cfht
# /def


#############################################################################
# Colors

@units.quantity_io()
def UmG(ps, **kw) -> units.mag:
    """U-G color.

    Parameters
    ----------
    ps : astropy.table.Table
        need arguments for u(g)-band functions

    kwargs
        passes to U & G-band functions

    Returns
    -------
    U-G color : Quantity array_like

    """
    return U_MP9301(ps, **kw) - G_MP9401(ps, **kw)
# /def


@units.quantity_io()
def UmR(ps, **kw) -> units.mag:
    """U-R color.

    Parameters
    ----------
    ps : astropy.table.Table
        need arguments for u(r)-band functions

    kwargs
        passes to U & R-band functions

    Returns
    -------
    U-G color : Quantity array_like

    """
    return U_MP9301(ps, **kw) - R_MP9601(ps, **kw)
# /def


@units.quantity_io()
def UmI(ps, **kw) -> units.mag:
    """U-I color.

    Parameters
    ----------
    ps : astropy.table.Table
        need arguments for u(i)-band functions

    kwargs
        passes to U & I-band functions

    Returns
    -------
    U-I color : Quantity array_like

    """
    return U_MP9301(ps, **kw) - I_MP9701(ps, **kw)
# /def


@units.quantity_io()
def UmZ(ps, **kw) -> units.mag:
    """U-Z color.

    Parameters
    ----------
    ps : astropy.table.Table
        need arguments for u(z)-band functions

    kwargs
        passes to U & Z-band functions

    Returns
    -------
    U-Z color : Quantity array_like

    """
    return U_MP9301(ps, **kw) - Z_MP9801(ps, **kw)
# /def


@units.quantity_io()
def GmR(ps, **kw) -> units.mag:
    """G-R color.

    Parameters
    ----------
    ps : astropy.table.Table
        need arguments for g(r)-band functions

    kwargs
        passes to G & R-band functions

    Returns
    -------
    G-R color : Quantity array_like

    """
    return G_MP9401(ps, **kw) - R_MP9601(ps, **kw)
# /def


@units.quantity_io()
def GmI(ps, **kw) -> units.mag:
    """G-I color.

    Parameters
    ----------
    ps : astropy.table.Table
        need arguments for g(i)-band functions

    kwargs
        passes to G & I-band functions

    Returns
    -------
    G-I color : Quantity array_like

    """
    return G_MP9401(ps, **kw) - I_MP9701(ps, **kw)
# /def


@units.quantity_io()
def GmZ(ps, **kw) -> units.mag:
    """G-Z color.

    Parameters
    ----------
    ps : astropy.table.Table
        need arguments for g(z)-band functions

    kwargs
        passes to G & Z-band functions

    Returns
    -------
    G-Z color : Quantity array_like

    """
    return G_MP9401(ps, **kw) - Z_MP9801(ps, **kw)
# /def


@units.quantity_io()
def RmI(ps, **kw) -> units.mag:
    """R-I color.

    Parameters
    ----------
    ps : astropy.table.Table
        need arguments for r(i)-band functions

    kwargs
        passes to R & I-band functions

    Returns
    -------
    R-I color : Quantity array_like

    """
    return R_MP9601(ps, **kw) - I_MP9701(ps, **kw)
# /def


@units.quantity_io()
def RmZ(ps, **kw) -> units.mag:
    """R-Z color.

    Parameters
    ----------
    ps : astropy.table.Table
        need arguments for r(z)-band functions

    kwargs
        passes to R & Z-band functions

    Returns
    -------
    R-Z color : Quantity array_like

    """
    return R_MP9601(ps, **kw) - Z_MP9801(ps, **kw)
# /def


@units.quantity_io()
def ImZ(ps, **kw) -> units.mag:
    """I-Z color.

    Parameters
    ----------
    ps : astropy.table.Table
        need arguments for i(z)-band functions

    kwargs
        passes to I & Z-band functions

    Returns
    -------
    I-Z color : Quantity array_like

    """
    return I_MP9701(ps, **kw) - Z_MP9801(ps, **kw)
# /def

#############################################################################
# END
