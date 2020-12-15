#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test functions for galpy imports."""


__all__ = ["test_import_amuse"]

##############################################################################
# IMPORTS

# BUILT-IN
import warnings

# THIRD PARTY
import pytest

try:
    import galpy
except ImportError:
    HAS_GALPY = False
else:
    if isinstance(galpy.__version__, str):  # check not empty namespace
        HAS_GALPY = True
    else:
        HAS_GALPY = False


##############################################################################
# CODE
##############################################################################


@pytest.mark.skipif(~HAS_GALPY, reason="requires galpy")
def test_import_amuse():
    """Test AMUSE imports."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from utilipy.imports import amuse_imports as imports

    for obj in (
        "galpy",
        "potential",
        "MWPotential2014",
        "Orbit",
        "bovy_conversion",
        "bovy_coords",
    ):
        assert hasattr(imports, obj)


# /def


##############################################################################
# END
