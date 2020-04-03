# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : initialize MCgen1_PS1
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata

"""MegaCam Generation 1 and panSTARRS generation 1.

    The conversions are sourced from [1]_

Modules
-------
Mixed_MegaCamGen1_PS1:
    iCFHT
    rPS
    CFHTtoPanstarrs_gm
    PSfromCFHTg2gmrSpl
MegaCamGen1_from_PS1:
    gCFHT
    rCFHT
PS1_from_MegaCamGen1:
    gPS
    gmrPS


References
----------
.. [1] http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html

"""

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]


#############################################################################
# IMPORTS

# PROJECT-SPECIFIC
from . import Mixed_MegaCamGen1_PS1 as mixed

from .MegaCamGen1_from_PS1 import (
    U_MP9301,
    U_MP9301 as u_MC,
    G_MP9401,
    G_MP9401 as g_MC,
    R_MP9601,
    R_MP9601 as r_MC,
    I_MP9701,
    I_MP9701 as i_MC,
    Z_MP9801,
    Z_MP9801 as z_MC,
    UmG as umg_MC,
    UmR as umr_MC,
    UmI as umi_MC,
    UmZ as umz_MC,
    GmR as gmr_MC,
    GmI as gmi_MC,
    GmZ as gmz_MC,
    RmI as rmi_MC,
    RmZ as rmz_MC,
    ImZ as imz_MC,
)

from .PS1_from_MegaCamGen1 import (
    G as g_PS,
    R as r_PS,
    I as i_PS,
    Z as z_PS,
    GmR as gmr_PS,
    GmI as gmi_PS,
    GmZ as gmz_PS,
    RmI as rmi_PS,
    RmZ as rmz_PS,
    ImZ as imz_PS,
)


#############################################################################
# END
