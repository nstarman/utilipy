#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   :
# AUTHOR  :
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
"""

__author__ = "Nathaniel Starkman"
# __copyright__ = "Copyright 2018, "
# __credits__ = [""]
# __license__ = "GPL3"
# __version__ = "0.0.0"
# __maintainer__ = "Nathaniel Starkman"
# __email__ = "n.starkman@mail.utoronto.ca"
# __status__ = "Production"


##############################################################################
### IMPORTS

# potential
from galpy import potential
from galpy.potential import MWPotential2014

# orbit
from galpy.orbit import Orbit

# util
from galpy.util import bovy_conversion, bovy_coords


##############################################################################
### INFORMATION

print("""Imported from galpy:
    potential, .MWPotential2014
    galpy.orbit.Orbit
    galpy.util: bovy_conversion, bovy_coords
"""
)


##############################################################################
### END