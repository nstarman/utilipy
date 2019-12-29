# -*- coding: utf-8 -*-

"""PanSTARRS1 bands from Mega-Cam gen2 bands."""

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]

__all__ = ["I_MP9702"]

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
def I_MP9702(ps: Table, **kw) -> MAG:
    r"""Convert Pan-STARRS1 bands to CFHT I-MP9702 band.

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
    I_MP9702 : Quantity array_like
        CFHT i-band

    Notes
    -----
    .. math::

        i_{CFHT} = i_{PS} -.005 + .004 gmi + .0124 gmi^2 - .0048 gmi^3

    where :math:`gmi \equiv g_{PS}-i_{PS}`
    in the range :math:`-1 \rm{mag} < g-i < 4 \rm{mag}`

    filter transformations from `Pan-STARRS to MegaCam plots. 2nd row, 3rd plot
    <http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html>`_.

    """
    g, i = kw.get("g", "g"), kw.get("i", "i")
    gmi = kw.get("gmi", "g-i")

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1.0 * MAG < gmi) & (gmi < 4 * MAG)
    if not all(ind):
        warnings.warn("MCg1.I: not all -1 mag < (g-i)_ps < 4 mag")

    c0 = -0.005 * MAG
    c1 = +0.004
    c2 = 0.0124 / MAG
    c3 = -0.0048 / MAG ** 2
    i_ps = ps[i]

    z_cfht = i_ps + c0 + (c1 * gmi) + (c2 * gmi ** 2) + (c3 * gmi ** 3)
    return z_cfht


# /def

#############################################################################
# END
