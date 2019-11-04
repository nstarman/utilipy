"""Mega-Cam gen3 band and PanSTARRS 1 band Mixed Functions
"""

#############################################################################
# Imports

# 3rd Party Imports
from astropy.table import Table, QTable
from .. import units

# Custom Imports
from . import PS1_from_MegaCamGen3
from . import MegaCamGen3_from_PS1

#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]


#############################################################################
# Code

@units.quantity_io()
def iCFHT(cfht, ps, **kw) -> units.mag:
    """Mega-Cam gen3 i band from CFHT R_MP9601 and I_MP9701
    iCFHT = iPS +.007 - 0.078(rCFHT-iCFHT)

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html

    Arguments
    ----------
    cfht: Astropy Table
        needs r col
    ps: Astropy Table
        needs i col

    KeyWord Arguments
    -----------------
    r: str
        r column
        used in cfht table
    i: str
        i column
        used in ps table
    """
    r, i = kw.get('r', 'r'), kw.get('i', 'i')

    i_cfht = (ps[i] + .002 * units.mag - .087 * cfht[r]) / (1 - .087)
    return i_cfht
# /def


@units.quantity_io()
def rPS(cfht, ps, **kw) -> units.mag:
    """Pan-STARRS r band from CFHT r and Panstarrs i
    rPS - rCFHT = -.001 + 0.023(rCFHT-iCFHT)
    calls iCFHT(cfht, ps)

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html

    Arguments
    ----------
    cfht: Astropy Table
        needs r col
    ps: Astropy Table
        needs i col

    KeyWord Arguments
    -----------------
    r: str
        r column
        used in cfht table
    i: str
        i column
        used in ps table
    """
    r = kw.get('r', 'r')
    i_cfht = iCFHT(cfht, ps, **kw)

    r_ps = cfht[r] - 0.001 * units.mag + 0.023 * (cfht[r] - i_cfht)
    return r_ps
# /def


@units.quantity_io()
def CFHTtoPanstarrs_gmr(cfht, ps, **kw) -> units.mag:
    """
    Arguments
    ----------
    cfht: Astropy Table
        needs r col
    ps: Astropy Table
        needs i col

    KeyWord Arguments
    -----------------
    g: str
        g column
        used in _____ table
    r: str
        r column
        used in cfht table
    i: str
        i column
        used in ps table
    gmr: str
        g-r column
    """
    # g filter
    g_ps = PS1_from_MegaCamGen3.G(cfht, **kw)
    # r filter
    r_ps = rPS(cfht, ps, **kw)
    return g_ps - r_ps
# /def


@units.quantity_io()
def PSfromCFHTg2gmrSpl(spline, ps, **kw) -> units.mag:
    """
    g_ps -> g_cfht -> g-r_cfht (via spline), r_cfht -> g-r_ps
    calculates g_cfht from PanSTARRS
               gmr_cfht from the spline(g_cfht)
    r_cfht = g_cfht - gmr_cfht

    calculates gmr_ps from cfht information

    KeyWord Arguments
    -----------------
    g: str
        g column
        used in _____ table
    r: str
        r column
        used in cfht table
    i: str
        i column
        used in ps table
    gmr: str
        g-r column
    gmi: str
        g-i column
    """
    g = kw.get('g', 'g')
    r = kw.get('r', 'r')
    gmr = kw.get('gmr', 'g-r')

    # g in CFHT
    g_cfht = MegaCamGen3_from_PS1.G_MP9401(ps, **kw)

    # r in CFHT
    gmr_cfht = spline(g_cfht) * units.mag  # g-r from the spline
    r_cfht = g_cfht - gmr_cfht  # r = g - (g-r)

    # cfht table for CFHTtoPanstarrs_gmr
    cfht = QTable([g_cfht, r_cfht, gmr_cfht], names=(g, r, gmr))

    # g-r CFHTtoPanstarrs_gmr
    gmr_ps = CFHTtoPanstarrs_gmr(cfht, ps, **kw)
    return gmr_ps
# /def
