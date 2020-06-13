# -*- coding: utf-8 -*-

"""Test functions for :mod:`~matplotlib` imports."""


##############################################################################


def test_import_matplotlib():
    """Test import matplotlib."""
    from utilipy.imports import matplotlib_imports as imports

    for obj in ("mpl", "plt", "cm", "colors"):
        assert hasattr(imports, obj)


# /def


# -------------------------------------------------------------------


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
