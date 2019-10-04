#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : main initialization file
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""main initialization file
"""

##############################################################################
### IMPORTS

## Project-Specific
# import top level packages
from . import (
    data_utils,
    fitting,
    imports,
    ipython,
    math,
    plot,
    util
)

# import commonly used functions
from .util.logging import LogFile
from .util.collections import ObjDict


#############################################################################
### Info

__author__ = "Nathaniel Starkman, Shabaan Mohamed"
__copyright__ = "Copyright 2019, "
__credits__ = [""]
__license__ = "GPL3"
__version__ = "0.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"


#############################################################################
### END
