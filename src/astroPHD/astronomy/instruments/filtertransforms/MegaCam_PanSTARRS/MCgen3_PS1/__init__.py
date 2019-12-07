# -*- coding: utf-8 -*-

"""Combining relevant functions."""

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]


#############################################################################
# IMPORTS

# PROJECT-SPECIFIC
from . import Mixed_MegaCamGen3_PS1 as mixed

from .MegaCamGen3_from_PS1 import (
    U_MP9302,
    U_MP9302 as u_MC,
    G_MP9402,
    G_MP9402 as g_MC,
    R_MP9602,
    R_MP9602 as r_MC,
    I_MP9703,
    I_MP9703 as i_MC,
    Z_MP9901,
    Z_MP9901 as z_MC,
    GRI_MP9605,
    GRI_MP9605 as gri_MC,
)

# from .PS1_from_MegaCamGen3 import


#############################################################################
# END
