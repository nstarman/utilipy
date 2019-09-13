#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""

    Mega-Cam gen1 bands from PanSTARRS 1 bands

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
def G(cfht, **kw) -> units.mag:
    """Pan-STARRS g band from CFHT G_MP9401 and R_MP9601
    gPS - gCFHT = 0.004(gCFHT - rCFHT)
    limited to -1.5 mag < gmi < 2.5 mag
    filter transformations from
    http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html

    Arguments
    ----------
    cfht: Astropy Table
        need: g
        either: r, g-r col

    KeyWord Arguments
    -----------------
    g: str  (default 'g')
        G_MP9401 column name
    r: str  (default 'r')
        R_MP9601 column name
    gmr: str  (default 'g-r')
        G_MP9401-R_MP9601 column name
    """
    g, r = kw.get('g', 'g'), kw.get('r', 'r')
    gmr = kw.get('gmr', 'g-r')

    if gmr in cfht.colnames:
        gmr = cfht[gmr]
    else:
        gmr = cfht[g] - cfht[r]

    ind = (-1.5 * units.mag < gmr) & (gmr < 2.5 * units.mag)
    if not all(ind):
        warnings.warn('PS1.G: not all -1.5 mag < (g-r)_ps < 2.5 mag')

    c0 = 0. * units.mag
    c1 = .004
    g_cfht = cfht[g]

    g_ps = g_cfht + c0 + (c1 * gmr)
    return g_ps


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
        need: r col
        either: i, r-i col

    KeyWord Arguments
    -----------------
    r: str  (default 'r')
        R_MP9601 column name
    i: str  (default 'i')
        I_MP9701 column name
    rmi: str  (default 'r-i')
        G_MP9401-I_MP9701 column name
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

    c0 = -.001 * units.mag
    c1 = 0.023
    r_cfht = cfht[r]

    r_ps = r_cfht + c0 + (c1 * rmi)
    return r_ps


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
        need: i col
        either: r, r-i col

    KeyWord Arguments
    -----------------
    r: str  (default 'r')
        R_MP9601 column name
    i: str  (default 'i')
        I_MP9701 column name
    rmi: str  (default 'r-i')
        G_MP9401-I_MP9701 column name
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

    c0 = -.007 * units.mag
    c1 = .078
    i_cfht = cfht[i]

    i_ps = i_cfht + c0 + (c1 * rmi)
    return i_ps


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
        need: i, z cols
        either: i-z col

    KeyWord Arguments
    -----------------
    i: str  (default 'i')
        I_MP9701 column name
    z: str  (default 'z')
        Z_MP9801 column name
    imz: str  (default 'i-z')
        I_MP9701-Z_MP9801 column name
    """
    i, z = kw.get('i', 'i'), kw.get('z', 'z')
    imz = kw.get('imz', 'i-z')

    if imz in cfht.colnames:
        imz = cfht[imz]
    else:
        imz = cfht[i] - cfht[z]

    ind = (-.1 * units.mag < imz) & (imz < 2.5 * units.mag)
    if not all(ind):
        warnings.warn('PS1.Z not all -.1 mag < (g-i)_ps < 3 mag')

    c0 = 0. * units.mag
    c1 = .078
    c2 = .029 / units.mag
    z_cfht = cfht[z]

    z_ps = z_cfht + c0 + (c1 * imz) + (c2 * imz**2)
    return z_ps


@units.quantity_io()
def GmR(cfht, **kw) -> units.mag:
    return G(cfht, **kw) - R(cfht, **kw)


@units.quantity_io()
def GmI(cfht, **kw) -> units.mag:
    return G(cfht, **kw) - I(cfht, **kw)


@units.quantity_io()
def GmZ(cfht, **kw) -> units.mag:
    return G(cfht, **kw) - Z(cfht, **kw)


@units.quantity_io()
def RmI(cfht, **kw) -> units.mag:
    return R(cfht, **kw) - I(cfht, **kw)


@units.quantity_io()
def RmZ(cfht, **kw) -> units.mag:
    return R(cfht, **kw) - Z(cfht, **kw)


@units.quantity_io()
def ImZ(cfht, **kw) -> units.mag:
    return I(cfht, **kw) - Z(cfht, **kw)


###########################################################################
# CLEANUP
