# -*- coding: utf-8 -*-

"""Test functions for astropy imports."""


__all__ = ["test_import_astropy"]


##############################################################################


def test_import_astropy():
    """Test _inRange."""
    from utilipy.imports import astropy_imports as imports

    for obj in (
        "astropy",
        "u",
        "coord",
        "SkyCoord",
        "Table",
        "QTable",
        "quantity_support",
        "astropy_mpl_style",
    ):
        assert hasattr(imports, obj)

    return


# /def


##############################################################################
# END
