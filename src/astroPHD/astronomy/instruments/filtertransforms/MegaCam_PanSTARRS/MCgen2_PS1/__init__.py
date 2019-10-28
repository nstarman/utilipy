#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Combining relevant function

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

#############################################################################
# Imports

from . import Mixed_MegaCamGen2_PS1 as mixed

from .MegaCamGen2_from_PS1 import G_MP9401 as gCFHT, R_MP9601 as rCFHT

from .PS1_from_MegaCamGen2 import G as gPS, I as iPS, GmR as gmrPS

#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__credits__ = [
    "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/megapipe/docs/filt.html"
]
