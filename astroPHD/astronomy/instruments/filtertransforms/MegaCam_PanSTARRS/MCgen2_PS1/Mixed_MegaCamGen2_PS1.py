#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""

    Mega-Cam gen2 band and PanSTARRS 1 band Mixed Functions

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

# 3rd Party Imports
from astropy.table import Table, QTable
from .. import units

# Custom Imports
from . import PS1_from_MegaCamGen2
from . import MegaCamGen2_from_PS1

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
def iCFHT(cfht, ps, **kw) -> units.mag:
    """Mega-Cam gen1 i band from CFHT R_MP9601 and I_MP9701
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
    r = kw.get('r', 'r')
    i = kw.get('i', 'i')

    i_cfht = (ps[i] + .007 * units.mag - .078 * cfht[r]) / (1 - .078)
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
    g_ps = PS1_from_MegaCamGen2.G(cfht, **kw)
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
    g_cfht = MegaCamGen2_from_PS1.G_MP9401(ps, **kw)

    # r in CFHT
    gmr_cfht = spline(g_cfht) * units.mag  # g-r from the spline
    r_cfht = g_cfht - gmr_cfht  # r = g - (g-r)

    # cfht table for CFHTtoPanstarrs_gmr
    cfht = QTable([g_cfht, r_cfht, gmr_cfht], names=(g, r, gmr))

    # g-r CFHTtoPanstarrs_gmr
    gmr_ps = CFHTtoPanstarrs_gmr(cfht, ps, **kw)
    return gmr_ps
# /def
