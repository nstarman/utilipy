# -*- coding: utf-8 -*-


"""test functions for base imports."""

__all__ = [
    "test_import_base",
    "test_import_base_has_ipython",
]


##############################################################################


def test_import_base():
    """Test base imports when not in ipython environment."""
    from utilipy.imports import base_imports as imports

    for obj in (
        "os",
        "sys",
        "time",
        "warnings",
        "np",
        "scipy",
        "TQDM",
        "tqdm",
        "tqdmn",
        "ObjDict",
        "LogFile",
    ):
        assert hasattr(imports, obj), f"{obj}"

    return


# /def


def test_import_base_has_ipython():
    """Test base imports when in ipython environment.

    combines with test_import_base to test all imports.

    """
    from utilipy.imports import base_imports as imports

    try:
        get_ipython()
        if get_ipython() is None:  # double checking
            raise NameError

    except NameError:
        pass

    else:
        for obj in (
            "InteractiveShell",
            "set_trace",
            "display",
            "Latex",
            "Markdown",
            "printmd",
            "printMD",
            "printltx",
            "printLaTeX",
            "set_autoreload",
            "aimport",
            "run_imports",
            "import_from_file",
            "add_raw_code_toggle",
        ):
            assert hasattr(imports, obj)

    return


# /def


##############################################################################
# END
