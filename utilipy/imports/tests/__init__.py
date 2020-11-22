# -*- coding: utf-8 -*-
# see LICENSE.rst

"""Test for :mod:`~utilipy.imports`."""


__all__ = [
    "test_amuse_imports",
    "test_astropy_imports",
    "test_base_imports",
    "test_extended_imports",
    "test_galpy_imports",
    "test_matplotlib_imports",
]


##############################################################################
# IMPORTS

# PROJECT-SPECIFIC
from . import (
    test_amuse_imports,
    test_astropy_imports,
    test_base_imports,
    test_extended_imports,
    test_galpy_imports,
)

##############################################################################
# END
