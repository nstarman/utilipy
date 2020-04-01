# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_amuse
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Test functions for data_utils/select."""

__author__ = "Nathaniel Starkman"


##############################################################################


def test_import_matplotlib():
    """Test import matplotlib."""
    from utilipy.imports import matplotlib_imports as imports

    imports.mpl
    imports.plt
    imports.cm, imports.colors
    # imports.Axes3D

    return


# /def


def test_import_matplotlib_has_ipython():
    """Test matplotlib imports when in IPython environment.

    combines with test_import_matplotlib to test all imports.

    """
    from utilipy.imports import matplotlib_imports as imports

    try:
        get_ipython()
        if get_ipython() is None:  # double checking
            raise NameError

    except NameError:
        pass

    else:

        imports.configure_matplotlib

    return


# /def

##############################################################################
# END
