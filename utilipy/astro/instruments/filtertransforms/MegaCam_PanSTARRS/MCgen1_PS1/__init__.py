# -*- coding: utf-8 -*-

"""MegaCam Generation 1 and panSTARRS generation 1.

    The conversions are sourced from [1]_

Modules
-------
Mixed_MegaCamGen1_PS1
MegaCamGen1_from_PS1:
PS1_from_MegaCamGen1:

References
----------
.. [1] http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html

"""

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]


__all__ = [
    # Mixed_MegaCamGen1_PS1
    "mixed",
    # MegaCamGen1_from_PS1
    "U_MP9301",
    "u_MC",
    "G_MP9401",
    "g_MC",
    "R_MP9601",
    "r_MC",
    "I_MP9701",
    "i_MC",
    "Z_MP9801",
    "z_MC",
    "umg_MC",
    "umr_MC",
    "umi_MC",
    "umz_MC",
    "gmr_MC",
    "gmi_MC",
    "gmz_MC",
    "rmi_MC",
    "rmz_MC",
    "imz_MC",
    # PS1_from_MegaCamGen1
    "g_PS",
    "r_PS",
    "i_PS",
    "z_PS",
    "gmr_PS",
    "gmi_PS",
    "gmz_PS",
    "rmi_PS",
    "rmz_PS",
    "imz_PS",
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
