#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Extending the Standard Import File
# AUTHOR  : Nathaniel Starkman
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""extending the standard import file.
imports:

NUMPY
-----
.linalg.norm

SCIPY
-----
.stats.binned_statistic -> binned_stats

"""

__author__ = "Nathaniel Starkman"


##############################################################################
### Imports

## numpy
from numpy.linalg import norm

## scipy
from scipy.stats import binned_statistic as binned_stats

## astropy

##############################################################################
### Priting Information

print("""Imported:
numpy: linalg.norm
scipy stats.binned_statistic->binned_stats
""")
