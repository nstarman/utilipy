# -*- coding: utf-8 -*-

"""Test Code in __init__."""

__all__ = [
    "test_get_path_to_file",
]


##############################################################################
# IMPORTS

# BUILT-IN
import os.path

# PROJECT-SPECIFIC
from utilipy.data_utils.utils import get_path_to_file

##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


def test_get_path_to_file():
    path = get_path_to_file("__init__.py", package="utilipy.data_utils")

    assert isinstance(path, str)

    assert os.path.join("utilipy", "data_utils", "__init__.py") in path


# /def


# -------------------------------------------------------------------


##############################################################################
# END
