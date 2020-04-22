# -*- coding: utf-8 -*-

"""Combining relevant functions.

Modules
-------
Mixed_MegaCamGen1_PS1
MegaCamGen1_from_PS1
PS1_from_MegaCamGen1

"""

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]


__all__ = [
    # Mixed_MegaCamGen2_PS1
    "mixed",
    # MegaCamGen2_from_PS1
    "I_MP9702",
    "i_MC",
]


#############################################################################
# IMPORTS

from . import Mixed_MegaCamGen2_PS1 as mixed

from .MegaCamGen2_from_PS1 import I_MP9702, I_MP9702 as i_MC


#############################################################################
# END
