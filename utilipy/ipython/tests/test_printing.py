# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.ipython.printing`."""


__all__ = ["test_printMD"]


##############################################################################
# printing

# PROJECT-SPECIFIC
from utilipy.ipython import printing

##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


def test_printMD():  # TODO actual test
    """Test :class:`~utilipy.ipython.printing.printMD`."""
    # all major options
    printing.printMD(
        "test",
        color="green",
        size=32,
        fontweight=15,
        fontstyle="italic",
        highlight=True,
    )

    # all minor options
    printing.printMD(
        "test",
        bold=True,
        italic=True,
    )


# /def


# -------------------------------------------------------------------


def test_printLTX():  # TODO actual test
    """Test :class:`~utilipy.ipython.printing.printMD`."""
    # major options
    printing.printLTX("test", label="", math="$$")

    # minor options
    printing.printLTX("test", math=True)

    printing.printLTX("i=0", equation=True, label="i_eq_0")

    printing.printLTX("i=1", equation=None, label="i_eq_1")

    printing.printLTX("i=2", matrix="b", label="i_eq_2")

    printing.printLTX("i=2", matrix=True, label="i_eq_2")


# /def


##############################################################################
# END
