#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""

    PanSTARRS 2 bands from Mega-Cam gen1 bands

#############################################################################

Copyright (c) 2018 - Nathaniel Starkman
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  The name of the author may not be used to endorse or promote products
     derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

#############################################################################
Planned Features
"""

#############################################################################
# Imports

import warnings

# 3rd Party Imports
from astropy.table import Table, QTable
from .. import units

#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2018, "
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"

#############################################################################
# Code


@units.quantity_io()
def U_MP9301(ps, **kw) -> units.mag:
    """U_MP9301
    gmi = (gPS-iPS)
    uCFHT - gPS = .523 - .343 gmi + 2.44 gmi^2 - .998 gmi^3

    limited to .3 mag < gmi < 1.5 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. Top row, 1st plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    i: str
        i column
    gmi: str
        g-i column
    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (.3 * u.mag < gmi) & (gmi < 1.5 * u.mag)
    if not all(ind):
        warnings.warn('MCg1.U: not all .3 mag < (g-i)_ps < 1.5 mag')

    c0 = .523 * u.mag
    c1 = -.343
    c2 = 2.44 / u.mag
    c3 = -.998 / u.mag**2
    g_ps = ps[g]

    u_cfht = g_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return u_cfht
# /def


@units.quantity_io()
def G_MP9401(ps, **kw) -> units.mag:
    """G_MP9401
    gmi = (gPS-iPS)
    gCFHT - gPS = -.001 - .004 gmi - .0056 gmi^2 + .00292 gmi^3

    limited to -1 mag < gmi < 4 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. Top row, 2nd plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    i: str
        i column
    gmi: str
        g-i column
    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * u.mag < gmi) & (gmi < 4 * u.mag)
    if not all(ind):
        warnings.warn('MCg1.G: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = -.001 * u.mag
    c1 = -.004
    c2 = -.0056 / u.mag
    c3 = .00292 / u.mag**2
    g_ps = ps[g]

    g_cfht = g_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return g_cfht
# /def


@units.quantity_io()
def R_MP9601(ps, **kw) -> units.mag:
    """R_MP9601
    gmi = (gPS-iPS)
    rCFHT - rPS = .002 - .017 gmi + .00554 gmi^2 - .000692 gmi^3

    limited to -1 mag < gmi < 4 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. Top row, 3rd plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    r: str
        r column
    i: str
        i column
    gmi: str
        g-i column
    """
    g, r, i = kw.get('g', 'g'), kw.get('r', 'r'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * u.mag < gmi) & (gmi < 4 * u.mag)
    if not all(ind):
        warnings.warn('MCg1.R: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = .002 * u.mag
    c1 = -.017
    c2 = .00554 / u.mag
    c3 = -.000692 / u.mag**2
    r_ps = ps[r]

    r_cfht = r_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return r_cfht
# /def


@units.quantity_io()
def I_MP9701(ps, **kw) -> units.mag:
    """I_MP9701
    gmi = (gPS-iPS)
    iCFHT - iPS = .001 - .021 gmi + .00398 gmi^2 - .00369 gmi^3

    limited to -1 mag < gmi < 4 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. 2nd row, 1st plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    i: str
        i column
    gmi: str
        g-i column
    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * u.mag < gmi) & (gmi < 4 * u.mag)
    if not all(ind):
        warnings.warn('MCg1.I: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = .001 * u.mag
    c1 = -.021
    c2 = .00398 / u.mag
    c3 = -.00369 / u.mag**2
    i_ps = ps[i]

    i_cfht = i_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return i_cfht
# /def


@units.quantity_io()
def Z_MP9801(ps, **kw) -> units.mag:
    """Z_MP9801
    gmi = (gPS-iPS)
    zCFHT - zPS = -.009 - .029 gmi + .012 gmi^2 - .00367 gmi^3

    limited to -1 mag < gmi < 4 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. 2nd row, 2nd plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    i: str
        i column
    z: str
        z column
    gmi: str
        g-i column
    """
    g, i, z = kw.get('g', 'g'), kw.get('i', 'i'), kw.get('z', 'z')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * u.mag < gmi) & (gmi < 4 * u.mag)
    if not all(ind):
        warnings.warn('MCg1.Z: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = -.009 * u.mag
    c1 = -.029
    c2 = .012 / u.mag
    c3 = -.00367 / u.mag**2
    z_ps = ps[z]

    z_cfht = z_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return z_cfht
# /def


@units.quantity_io()
def I_MP9702(ps, **kw) -> units.mag:
    """I_MP9702
    gmi = (gPS-iPS)
    iCFHT - iPS = -.005 + .004 gmi + .0124 gmi^2 - .0048 gmi^3

    limited to -1 mag < gmi < 4 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. 2nd row, 3rd plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    i: str
        i column
    gmi: str
        g-i column
    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * u.mag < gmi) & (gmi < 4 * u.mag)
    if not all(ind):
        warnings.warn('MCg1.I: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = -.005 * u.mag
    c1 = -.004
    c2 = .0124 / u.mag
    c3 = -.0048 / u.mag**2
    i_ps = ps[i]

    z_cfht = i_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return z_cfht
# /def


@units.quantity_io()
def U_MP9302(ps, **kw) -> units.mag:
    """I_MP9702
    gmi = (gPS-iPS)
    uCFHT - gPS = .823 - 1.36 gmi + 4.18 gmi^2 - 1.64 gmi^3

    limited to .3 mag < gmi < 1.5 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. 3rd row, 1st plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    i: str
        i column
    gmi: str
        g-i column
    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (.3 * u.mag < gmi) & (gmi < 1.5 * u.mag)
    if not all(ind):
        warnings.warn('MCg1.U: not all .3 mag < (g-i)_ps < 1.5 mag')

    c0 = .823 * u.mag
    c1 = -1.36
    c2 = 4.18 / u.mag
    c3 = -1.64 / u.mag**2
    g_ps = ps[g]

    u_cfht = g_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return u_cfht
# /def


@units.quantity_io()
def G_MP9402(ps, **kw) -> units.mag:
    """G_MP9402
    gmi = (gPS-iPS)
    gCFHT - gPS = .014 - .059 gmi - .00313 gmi^2 - .00178 gmi^3

    limited to -1 mag < gmi < 4 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. 3rd row, 2nd plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    i: str
        i column
    gmi: str
        g-i column
    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * u.mag < gmi) & (gmi < 4 * u.mag)
    if not all(ind):
        warnings.warn('MCg1.G: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = .014 * u.mag
    c1 = .059
    c2 = -.00313 / u.mag
    c3 = -.00178 / u.mag**2
    g_ps = ps[g]

    g_cfht = g_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return g_cfht
# /def


@units.quantity_io()
def R_MP9602(ps, **kw) -> units.mag:
    """G_MP9402
    gmi = (gPS-iPS)
    rCFHT - rPS = .003 - .05 gmi - .0125 gmi^2 - .00699 gmi^3

    limited to -1 mag < gmi < 3 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. 3rd row, 2nd plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    r: str
        r column
    i: str
        i column
    gmi: str
        g-i column
    """
    g, r, i = kw.get('g', 'g'), kw.get('r', 'r'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * u.mag < gmi) & (gmi < 3. * u.mag)
    if not all(ind):
        warnings.warn('MCg1.R: not all -1 mag < (g-i)_ps < 3 mag')

    c0 = .003 * u.mag
    c1 = -.05
    c2 = .0125 / u.mag
    c3 = -.00699 / u.mag**2
    r_ps = ps[r]

    r_cfht = r_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return r_cfht
# /def


@units.quantity_io()
def I_MP9703(ps, **kw) -> units.mag:
    """I_MP9703
    gmi = (gPS-iPS)
    iCFHT - iPS = .006 - .024 gmi + .00627 gmi^2 - .00523 gmi^3

    limited to -1 mag < gmi < 3.6 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. 3rd row, 2nd plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    i: str
        i column
    gmi: str
        g-i column
    """
    g, i = kw.get('g', 'g'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * u.mag < gmi) & (gmi < 3.6 * u.mag)
    if not all(ind):
        warnings.warn('MCg1.I: not all -1 mag < (g-i)_ps < 3.6 mag')

    c0 = .006 * u.mag
    c1 = -.024
    c2 = .00627 / u.mag
    c3 = -.00523 / u.mag**2
    i_ps = ps[i]

    i_cfht = i_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return i_cfht
# /def


@units.quantity_io()
def Z_MP9901(ps, **kw) -> units.mag:
    """Z_MP9901
    gmi = (gPS-iPS)
    zCFHT - zPS = -.016 - .069 gmi + .0239 gmi^2 - .0056 gmi^3

    limited to -1 mag < gmi < 4 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. 3rd row, 2nd plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    i: str
        i column
    z: str
        z column
    gmi: str
        g-i column
    """
    g, i, z = kw.get('g', 'g'), kw.get('i', 'i'), kw.get('z', 'z')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * u.mag < gmi) & (gmi < 4. * u.mag)
    if not all(ind):
        warnings.warn('MCg1.Z: not all -1 mag < (g-i)_ps < 4 mag')

    c0 = -.016 * u.mag
    c1 = -.069
    c2 = .0239 / u.mag
    c3 = -.0056 / u.mag**2
    z_ps = ps[z]

    z_cfht = z_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return z_cfht
# /def


@units.quantity_io()
def G_MP9605(ps, **kw) -> units.mag:
    """G_MP9605
    gmi = (gPS-iPS)
    gCFHT - rPS = .005 + .244 gmi - .0692 gmi^2 - .0014 gmi^3

    limited to -1 mag < gmi < 1.2 mag

    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html
    Pan-STARRS to MegaCam plots. 3rd row, 2nd plot

    Arguments
    ----------
    ps: Astropy Table
        needs g, i cols
        optional: g-i col

    KeyWord Arguments
    -----------------
    g: str
        g column
    r: str
        r column
    i: str
        i column
    gmi: str
        g-i column
    """
    g, r, i = kw.get('g', 'g'), kw.get('r', 'r'), kw.get('i', 'i')
    gmi = kw.get('gmi', 'g-i')

    if gmi in ps.colnames:
        gmi = ps[gmi]
    else:
        gmi = ps[g] - ps[i]

    ind = (-1. * u.mag < gmi) & (gmi < 1.2 * u.mag)
    if not all(ind):
        warnings.warn('MCg1.G: not all -1 mag < (g-i)_ps < 1.2 mag')

    c0 = .005 * u.mag
    c1 = .244
    c2 = -.0692 / u.mag
    c3 = -.0014 / u.mag**2
    r_ps = ps[r]

    r_cfht = r_ps + c0 + (c1 * gmi) + (c2 * gmi**2) + (c3 * gmi**3)
    return r_cfht
# /def
