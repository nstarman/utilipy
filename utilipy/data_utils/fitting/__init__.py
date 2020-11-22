# -*- coding: utf-8 -*-

"""Fitting utilities."""

__all__ = [
    # modules
    "lmfit_utils",
    # functions
    "scipy_residual_to_lmfit",
]


##############################################################################
# IMPORTS

# PROJECT-SPECIFIC
from . import lmfit_utils
from .lmfit_utils import scipy_residual_to_lmfit

# from .astropy_decorator import scipy_function_to_astropy_model


##############################################################################
# END
