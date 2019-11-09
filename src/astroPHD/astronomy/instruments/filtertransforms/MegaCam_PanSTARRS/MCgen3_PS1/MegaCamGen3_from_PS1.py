# -*- coding: utf-8 -*-

"""PanSTARRS 1 bands from Mega-Cam gen1 bands."""

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]

__all__ = [
    'U_MP9302', 'G_MP9402', 'R_MP9602', 'I_MP9703', 'Z_MP9901', 'GRI_MP9605'
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
def U_MP9302(ps, **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT U-MP9302 band.

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
    U_MP9302 : Quantity array_like
        CFHT u-band

    Notes
    -----
    .. math::

        u_{CFHT} = g_{PS} +.823 - 1.36 gmi + 4.18 gmi^2 - 1.64 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`.3 \rm{mag} < g-i < 1.5 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots. 3rd row, 1st plot
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

    c0 = .823 * units.mag
    c1 = -1.360
    c2 = 4.18 / units.mag
    c3 = -1.64 / units.mag**2
    g_ps = ps[g]

    u_cfht = g_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return u_cfht
# /def


@units.quantity_io()
def G_MP9402(ps, **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT G-MP9402 band.

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
    G_MP9402 : Quantity array_like
        CFHT g-band

    Notes
    -----
    .. math::

        g_{CFHT} = g_{PS} +.014 - .059 gmi - .00313 gmi^2 - .00178 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`-1 \rm{mag} < g-i < 4 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots. 3rd row, 2nd plot
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

    c0 = .014 * units.mag
    c1 = .059
    c2 = -.00313 / units.mag
    c3 = -.00178 / units.mag**2
    g_ps = ps[g]

    g_cfht = g_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return g_cfht
# /def


@units.quantity_io()
def R_MP9602(ps, **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT R-MP9602 band.

    Parameters
    ----------
    ps: astropy Table
        need: r col
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
    R_MP9602 : Quantity array_like
        CFHT r-band

    Notes
    -----
    .. math::

        r_{CFHT} = r_{PS} + .003 - .05 gmi - .0125 gmi^2 - .00699 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`-1 \rm{mag} < g-i < 3 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots. 3rd row, 3rd plot
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    g, r, i = kw.get('g', 'g'), kw.get('r', 'r'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * units.mag < gmi) & (gmi < 3. * units.mag)
    if not all(ind):
        warnings.warn('MCg1.R: not all -1 mag < (g-i)_ps < 3 mag')

    c0 = .003 * units.mag
    c1 = -.050
    c2 = .0125 / units.mag
    c3 = -.00699 / units.mag**2
    r_ps = ps[r]

    r_cfht = r_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return r_cfht
# /def


@units.quantity_io()
def I_MP9703(ps, **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT I-MP9703 band.

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
    I_MP9703 : Quantity array_like
        CFHT i-band

    Notes
    -----
    .. math::

        i_{CFHT} = i_{PS} + .006 - .024 gmi + .00627 gmi^2 - .00523 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`-1 \rm{mag} < g-i < 3 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots. 4th row, 1st plot
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * units.mag < gmi) & (gmi < 3.6 * units.mag)
    if not all(ind):
        warnings.warn('MCg1.I: not all -1 mag < (g-i)_ps < 3.6 mag')

    c0 = .006 * units.mag
    c1 = -.024
    c2 = .00627 / units.mag
    c3 = -.00523 / units.mag**2
    i_ps = ps[i]

    i_cfht = i_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return i_cfht
# /def


@units.quantity_io()
def Z_MP9901(ps, g='g', i='i', z='z', gmi='g-i', **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT Z-MP9901 band.

    Parameters
    ----------
    ps: astropy Table
        need: z col
        either: (g & i), g-i col
    g: str
        (default 'g')
        i column name
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
    Z_MP9901 : Quantity array_like
        CFHT z-band

    Notes
    -----
    .. math::

        z_{CFHT} = z_{PS} - .016 - .069 gmi + .0239 gmi^2 - .0056 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`-1 \rm{mag} < g-i < 4 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots. 4th row, 2nd plot
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * units.mag < gmi) & (gmi < 4. * units.mag)
    if not all(ind):
        warnings.warn('MCg1.Z: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = -.016 * units.mag
    c1 = -.069
    c2 = .0239 / units.mag
    c3 = -.0056 / units.mag**2
    z_ps = ps[z]

    z_cfht = z_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return z_cfht
# /def


@units.quantity_io()
def GRI_MP9605(ps, **kw) -> units.mag:
    r"""Convert Pan-STARRS1 bands to CFHT R-MP9605 band.

    Parameters
    ----------
    ps: astropy Table
        need: r col
        either: (g & i), g-i col
    g: str, optional
        g column name
        (default 'g')
    r: str, optional
        r column name
        (default 'r')
    i: str, optional
        i column name
        (default 'i')
    gmi: str, optional
        g-i column name
        (default 'g-i')

    Returns
    -------
    R_MP9605 : Quantity array_like
        CFHT r-band

    Notes
    -----
    .. math::

        f_{CFHT} = rPS + .005 + .244 gmi - .0692 gmi^2 - .0014 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`-1 \rm{mag} < g-i < 1.2 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots: 4th row, 3rd plot
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_

    """
    g, r, i = kw.get('g', 'g'), kw.get('r', 'r'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * units.mag < gmi) & (gmi < 1.2 * units.mag)
    if not all(ind):
        warnings.warn('MCg1.G: not all -1 mag < (g-i)_ps < 1.2 mag')

    c0 = .005 * units.mag
    c1 = .244
    c2 = -.0692 / units.mag
    c3 = -.0014 / units.mag**2
    r_ps = ps[r]

    r_cfht = r_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)

    return r_cfht
# /def

#############################################################################
# END
