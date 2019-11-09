# -*- coding: utf-8 -*-

"""Combining relevant functions.

Functions
---------
Mixed_MegaCamGen1_PS1:
- iCFHT
- rPS
- CFHTtoPanstarrs_gmr
- PSfromCFHTg2gmrSpl

MegaCamGen1_from_PS1:
- gCFHT
- rCFHT

PS1_from_MegaCamGen1:
- gPS
- gmrPS

"""

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]


#############################################################################
# IMPORTS

from . import Mixed_MegaCamGen2_PS1 as mixed

from .MegaCamGen2_from_PS1 import I_MP9702, I_MP9702 as i_MC

# from .PS1_from_MegaCamGen2 import

#############################################################################
# END
