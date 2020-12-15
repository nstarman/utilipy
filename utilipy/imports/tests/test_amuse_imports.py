# -*- coding: utf-8 -*-

"""Test functions for AMUSE imports."""

__all__ = ["test_import_amuse"]


##############################################################################
# IMPORTS

# BUILT-IN
import warnings

# THIRD PARTY
import pytest

try:
    import amuse
except ImportError:
    HAS_AMUSE = False
else:
    if isinstance(amuse.__version__, str):  # check not empty namespace
        HAS_AMUSE = True
    else:
        HAS_AMUSE = False


##############################################################################


@pytest.mark.skipif(~HAS_AMUSE, reason="requires AMUSE")
def test_import_amuse():
    """Test AMUSE imports."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from utilipy.imports import amuse_imports as imports

    for obj in (
        "amuse",
        "lab",
        "units",
        "constants",
        "bridge",
    ):
        assert hasattr(imports, obj)


# /def


##############################################################################
# END
