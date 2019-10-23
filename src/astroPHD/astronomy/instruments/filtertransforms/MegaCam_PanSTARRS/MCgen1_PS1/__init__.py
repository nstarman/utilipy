#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""Combining relevant function

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

#############################################################################
Planned Features
"""

#############################################################################
# Imports

from . import Mixed_MegaCamGen1_PS1 as mixed

from .MegaCamGen1_from_PS1 import G_MP9401 as gMC, R_MP9601 as rMC

from .PS1_from_MegaCamGen1 import G as gPS, I as iPS, GmR as gmrPS


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
