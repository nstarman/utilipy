# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : initialization file
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""initialization file for fitting module."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# General
# try:
#     import lmfit
# except ImportError:
#     print('cannot import lmfit')

# Project-Specific
from .lmfit_decorator import scipy_residual_to_lmfit


##############################################################################
# END
