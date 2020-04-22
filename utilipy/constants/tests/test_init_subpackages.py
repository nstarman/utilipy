# -*- coding: utf-8 -*-

"""Test subpackages for :mod:`~utilipy.data_utils`."""


__all__ = [
    "test_init_data",
]


##############################################################################
# IMPORTS

# PROJECT-SPECIFIC

from .. import data


##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


def test_init_data():
    """Test module initialization."""
    # Expectations
    local = [
        "read_constants",
        "__all_constants__",
    ]

    # test __all__ conforms to module
    for name in data.__all__:
        assert hasattr(data, name)

    # test __all__ matches expectations
    for name in data.__all__:
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
