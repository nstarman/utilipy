# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_base
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""test functions for base imports."""

__author__ = "Nathaniel Starkman"


##############################################################################


def test_import_base():
    """Test base imports when not in ipython environment."""
    from utilipy.imports import base_imports as imports

    imports.os
    imports.sys
    imports.time
    imports.pdb
    imports.warnings

    imports.np
    imports.scipy

    imports.TQDM
    imports.tqdm, imports.tqdmn

    imports.ObjDict
    imports.LogFile

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

        imports.InteractiveShell
        imports.set_trace
        imports.display
        imports.Latex, imports.Markdown

        imports.printmd, imports.printMD
        imports.printltx, imports.printLaTeX
        imports.set_autoreload, imports.aimport
        imports.run_imports, imports.import_from_file
        imports.add_raw_code_toggle

    return


# /def


##############################################################################
# END
