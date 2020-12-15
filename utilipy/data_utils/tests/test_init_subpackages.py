# -*- coding: utf-8 -*-

"""Test subpackages for :mod:`~utilipy.data_utils`."""


__all__ = [
    "test_init_fitting",
    "test_init_xfm",
]


##############################################################################
# IMPORTS


# PROJECT-SPECIFIC
from utilipy.data_utils import fitting, xfm

##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


def test_init_fitting():
    """Test module initialization."""
    # Expectations
    local = [
        # modules
        "lmfit_utils",
        # functions
        "scipy_residual_to_lmfit",
    ]

    # test __all__ conforms to module
    for name in fitting.__all__:
        assert hasattr(fitting, name)

    # test __all__ matches expectations
    for name in fitting.__all__:
        assert name in local

    return


# /def

# -------------------------------------------------------------------


def test_init_xfm():
    """Test module initialization."""
    # Expectations
    local = [
        # modules
        "graph",
        "transformations",
        # functions
        "TransformGraph",
        # transformations
        "DataTransform",
        "CompositeTransform",
        # Parameters
        "data_graph",
    ]

    # test __all__ conforms to module
    for name in xfm.__all__:
        assert hasattr(xfm, name)

    # test __all__ matches expectations
    for name in xfm.__all__:
        assert name in local

    return


# /def


# def test_fitting_top_level_imports():
#     """Test top-level imports of :mod:`~utilipy.data_utils.fitting`."""
#     # First test they exist
#     subpkg: str
#     for subpkg in fitting.__all_top_imports__:
#         assert hasattr(fitting, subpkg)

#     # Next test that top-levels are all the possible top-levels
#     drct: str = os.path.split(fitting.__file__)[0]  # directory
#     donottest = ("__pycache__", "data", "tests")  # stuff not to test

#     for file in os.listdir(drct):  # iterate through directory
#         # test?
#         if os.path.isdir(drct + "/" + file) and file not in donottest:
#             assert file in fitting.__all_top_imports__
#         else:  # nope, chuck testa.
#             pass

#     return


# # /def


# -------------------------------------------------------------------


##############################################################################
# END
