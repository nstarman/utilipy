# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.utils`."""


__all__ = [
    "test_init_data_utils",
    "test_init_decorators",
    "test_init_imports",
    "test_init_ipython",
    "test_init_math",
    "test_init_plot",
    "test_init_scripts",
    "test_init_utils",
    "test_utils_top_level_imports",
]


##############################################################################
# IMPORTS

# BUILT-IN
import os

# PROJECT-SPECIFIC
from utilipy import (
    data_utils,
    decorators,
    imports,
    ipython,
    math,
    plot,
    scripts,
    utils,
)

##############################################################################
# TESTS
##############################################################################


def test_init_data_utils():
    """Test :mod:`~utilipy.data_utils` initialization."""
    # Expectations
    local = [
        # modules
        "crossmatch",
        "decorators",
        "select",
        "fitting",
        "utils",
        "xfm",
        # decorators
        "idxDecorator",
        # data transformation graph
        "data_graph",
        "TransformGraph",
        "DataTransform",
        # xmatch
        "indices_xmatch_fields",
        "xmatch_fields",
        "xmatch",
        "non_xmatched",
        # utils
        "get_path_to_file",
        "make_shuffler",
    ]
    local += data_utils.select.__all__

    # test __all__ conforms to module
    for name in data_utils.__all__:
        assert hasattr(data_utils, name)

    # test __all__ matches expectations
    for name in data_utils.__all__:
        assert name in local

    return


# /def


# --------------------------------------------------------------------------


def test_init_decorators():
    """Test :mod:`~utilipy.decorators` initialization."""
    # Expectations
    local = [
        # modules
        "baseclass",
        "docstring",
        "func_io",
        "code_dev",
        # defined here
        "store_function_input",
        "add_folder_backslash",
        # baseclass
        "DecoratorBaseClass",
        "classy_decorator",
        # data-type decorators
        "dtypeDecorator",
        "dtypeDecoratorMaker",
        "intDecorator",
        "floatDecorator",
        "strDecorator",
        "boolDecorator",
        "ndarrayDecorator",
        "ndfloat64Decorator",
        # convenience
        "functools",
        "inspect",
        "wraps",
    ]

    # test __all__ conforms to module
    for name in decorators.__all__:
        assert hasattr(decorators, name)

    # test __all__ matches expectations
    for name in decorators.__all__:
        assert name in local

    return


# /def


# --------------------------------------------------------------------------


def test_init_imports():
    """Test :mod:`~utilipy.imports` initialization."""
    # Expectations
    local = [
        "conf",
        "use_import_verbosity",
    ]

    # test __all__ conforms to module
    for name in imports.__all__:
        assert hasattr(imports, name)

    # test __all__ matches expectations
    for name in imports.__all__:
        assert name in local

    return


# /def


# --------------------------------------------------------------------------


def test_init_ipython():
    """Test :mod:`~utilipy.ipython` initialization."""
    # Expectations
    local = [
        "ipython_help",
        "get_ipython",
        "InteractiveShell",
        "set_trace",
        "display",
        "Latex",
        "Markdown",
        "HTML",
        "set_autoreload",
        "aimport",
        "run_imports",
        "import_from_file",
        "add_raw_code_toggle",
        "printMD",
        "printLTX",
    ]

    # test __all__ conforms to module
    for name in ipython.__all__:
        assert hasattr(ipython, name), name

    # test __all__ matches expectations
    for name in ipython.__all__:
        assert name in local

    return


# /def


# --------------------------------------------------------------------------


def test_init_math():
    """Test :mod:`~utilipy.math` initialization."""
    # Expectations
    local = []
    local += math.core.__all__

    # test __all__ conforms to module
    for name in math.__all__:
        assert hasattr(math, name)

    # test __all__ matches expectations
    for name in math.__all__:
        assert name in local

    return


# /def


# --------------------------------------------------------------------------


def test_init_plot():
    """Test :mod:`~utilipy.plot` initialization."""
    # Expectations
    local = []

    # test __all__ conforms to module
    for name in plot.__all__:
        assert hasattr(plot, name)

    # test __all__ matches expectations
    for name in plot.__all__:
        assert name in local

    return


# /def


# --------------------------------------------------------------------------


def test_init_scripts():
    """Test :mod:`~utilipy.scripts` initialization."""
    # Expectations
    local = []

    # test __all__ conforms to module
    for name in scripts.__all__:
        assert hasattr(scripts, name)

    # test __all__ matches expectations
    for name in scripts.__all__:
        assert name in local

    return


# /def


# --------------------------------------------------------------------------


def test_init_utils():
    """Test :mod:`~utilipy.utils` initialization."""
    # Expectations
    local = [
        # modules
        "collections",
        "logging",
        "exceptions",
        "functools",
        "inspect",
        "metaclasses",
        "misc",
        "pickle",
        "string",
        "typing",
        # classes and functions
        "LogPrint",
        "LogFile",
        "ObjDict",
        "WithDocstring",
        "WithMeta",
        "WithReference",
        "temporary_namespace",
        "make_help_function",
    ]

    # test __all__ conforms to module
    for name in utils.__all__:
        assert hasattr(utils, name)

    # test __all__ matches expectations
    for name in utils.__all__:
        assert name in local

    return


# /def


def test_utils_top_level_imports():
    """Test Top-Level Imports."""
    # First test they exist
    subpkg: str
    for subpkg in utils.__all_top_imports__:
        assert hasattr(utils, subpkg)

    # Next test that top-levels are all the possible top-levels
    drct: str = os.path.split(utils.__file__)[0]  # directory
    donottest = ("tests", "__pycache__")  # stuff not to test

    for file in os.listdir(drct):  # iterate through directory
        # test?
        if os.path.isdir(drct + "/" + file) and file not in donottest:
            assert file in utils.__all_top_imports__
        # else:  # nope, chuck testa.
        #     pass

    return


# /def


# --------------------------------------------------------------------------


##############################################################################
# END
