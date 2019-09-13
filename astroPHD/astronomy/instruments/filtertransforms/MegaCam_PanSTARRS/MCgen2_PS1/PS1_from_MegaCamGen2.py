#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""

    Mega-Cam gen2 bands from PanSTARRS 1 bands

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

from astropy.table import Table, QTable
from .. import units
import warnings

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
def G(cfht, **kw) -> units.mag:
    """Pan-STARRS g band from CFHT G_MP9401 and R_MP9601
    gPS - gCFHT = 0.004(gCFHT - rCFHT)
    limited to -1.5 mag < gmi < 2.5 mag
    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html

    Arguments
    ----------
    cfht: Astropy Table
        needs g, r cols
        optional: g-r col

    KeyWord Arguments
    -----------------
    g: str
        g column
    r: str
        r column
    gmr: str
        g-r column
    """
    g, r = kw.get('g', 'g'), kw.get('r', 'r')
    gmr = kw.get('gmr', 'g-r')

    if gmr in cfht.colnames:
        gmr = cfht[gmr]
    else:
        gmr = cfht[g] - cfht[r]

    ind = (-1.5 * units.mag < gmr) & (gmr < 2.5 * units.mag)
    if not all(ind):
        warnings.warn('PS1.G: not all -1.5 mag < (g-i)_ps < 2.5 mag')

    g_cfht = cfht[g]

    g_ps = g_cfht + 0.004 * gmr
    return g_ps
# /def


@units.quantity_io()
def R(cfht, **kw) -> units.mag:
    """Pan-STARRS g band from CFHT R_MP9601 and I_MP9701
    rPS - rCFHT = -.001 + 0.023(rCFHT-iCFHT)
    limited to -.9 mag < gmi < 3 mag
    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html

    Arguments
    ----------
    cfht: Astropy Table
        needs r, i cols
        optional: r-i col

    KeyWord Arguments
    -----------------
    r: str
        r column
    i: str
        i column
    rmi: str
        r-i column
    """
    r, i = kw.get('r', 'r'), kw.get('i', 'i')
    rmi = kw.get('rmi', 'r-i')

    if rmi in cfht.colnames:
        rmi = cfht[rmi]
    else:
        rmi = cfht[r] - cfht[i]

    ind = (-.9 * units.mag < rmi) & (rmi < 3 * units.mag)
    if not all(ind):
        warnings.warn('PS1.R: not all -.9 mag < (g-i)_ps < 3 mag')

    r_cfht = cfht[r]

    r_ps = r_cfht - .001 * units.mag + 0.023 * rmi
    return r_ps
# /def


@units.quantity_io()
def I(cfht, **kw) -> units.mag:
    """Pan-STARRS i band from CFHT R_MP9601 and I_MP9701
    iPS - iCFHT = -.007 + 0.078(rCFHT-iCFHT)
    limited to .1 mag < gmi < 3 mag
    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html

    Arguments
    ----------
    cfht: Astropy Table
        needs r, i cols
        optional: r-i col

    KeyWord Arguments
    -----------------
    r: str
        r column
    i: str
        i column
    rmi: str
        r-i column
    """
    r, i = kw.get('r', 'r'), kw.get('i', 'i')
    rmi = kw.get('rmi', 'r-i')

    if rmi in cfht.colnames:
        rmi = cfht[rmi]
    else:
        rmi = cfht[r] - cfht[i]

    ind = (.1 * units.mag < rmi) & (rmi < 3 * units.mag)
    if not all(ind):
        warnings.warn('PS1.I not all .1 mag < (g-i)_ps < 3 mag')

    i_cfht = cfht[i]

    i_ps = i_cfht - .007 * units.mag + 0.078 * rmi
    return i_ps
# /def


@units.quantity_io()
def Z(cfht, **kw) -> units.mag:
    """Pan-STARRS g band from CFHT I_MP9701, Z_MP9801
    zPS - zCFHT = 0.078(iCFHT-zCFHT) + 0.029(iCFHT-zCFHT)^2
    limited to -.1 mag < gmi
    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html

    Arguments
    ----------
    cfht: Astropy Table
        needs i, z cols
        optional: i-z col

    KeyWord Arguments
    -----------------
    i: str
        i column
    z: str
        z column
    imz: str
        i-z column
    """
    i, z = kw.get('i', 'i'), kw.get('z', 'z')
    imz = kw.get('imz', 'i-z')

    if imz in cfht.colnames:
        imz = cfht[imz]
    else:
        imz = cfht[i] - cfht[z]

    ind = (-.1 * units.mag < imz) & (imz < 2.5 * units.mag)
    if not all(ind):
        warnings.warn('PZ1.Z not all -.1 mag < (g-i)_ps < 3 mag')

    z_cfht = cfht[z]

    z_ps = z_cfht + 0.078 * imz + .029 * imz**2
    return z_ps
# /def


@units.quantity_io()
def GmR(cfht, **kw) -> units.mag:
    return G(cfht, **kw) - R(cfht, **kw)
# /def


@units.quantity_io()
def GmI(cfht, **kw) -> units.mag:
    return G(cfht, **kw) - I(cfht, **kw)
# /def


@units.quantity_io()
def GmZ(cfht, **kw) -> units.mag:
    return G(cfht, **kw) - Z(cfht, **kw)
# /def


@units.quantity_io()
def RmI(cfht, **kw) -> units.mag:
    return R(cfht, **kw) - I(cfht, **kw)
# /def


@units.quantity_io()
def RmZ(cfht, **kw) -> units.mag:
    return R(cfht, **kw) - Z(cfht, **kw)
# /def


@units.quantity_io()
def ImZ(cfht, **kw) -> units.mag:
    return I(cfht, **kw) - Z(cfht, **kw)
# /def
