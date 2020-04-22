# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Test `utilipy.units.decorators`
# PROJECT : `utilipy`
#
# ----------------------------------------------------------------------------

"""Test `utilipy.units.decorators`.


Routine Listings
----------------
`test_quantity_return`

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "test_quantity_output_no_defaults",
    "test_quantity_output_with_unit_default",
    "test_quantity_output_with_value_default",
]


##############################################################################
# IMPORTS

# THIRD PARTY

import pytest

import astropy.units as u


# PROJECT-SPECIFIC

from .. import core
from ..decorators import (
    _aioattrs,
    _doc_quantity_output_examples,
    _doc_quantity_output_wrapped,
    _doc_qio_params,
    _doc_qio_notes,
    quantity_output,
    QuantityInputOutput,
)


##############################################################################
# CODE
##############################################################################


def test_ioattrs():
    """Test `_aioattrs`."""
    # type test
    assert isinstance(_aioattrs, tuple)
    assert all([isinstance(c, str) for c in _aioattrs])

    # test contents
    assert _aioattrs == (
        "unit",
        "to_value",
        "equivalencies",
        "decompose",
        "assumed_units",
        "assume_annotation_units",
    )

    return


# /def


# ------------------------------------------------------------------------


def test_doc_quantity_output_examples():

    assert isinstance(_doc_quantity_output_examples, str)

    return


# /def


# ------------------------------------------------------------------------


def test_doc_quantity_output_wrapped():

    # type test
    assert isinstance(_doc_quantity_output_wrapped, str)

    # test contents
    assert core._doc_base_params in _doc_quantity_output_wrapped
    assert core._doc_base_raises in _doc_quantity_output_wrapped
    assert _doc_quantity_output_examples in _doc_quantity_output_wrapped

    return


# /def


# ------------------------------------------------------------------------


def test_doc_qio_params():

    # type test
    assert isinstance(_doc_qio_params, str)

    # test contents
    assert core._doc_base_params in _doc_qio_params

    return


# /def


# ------------------------------------------------------------------------


def test_doc_qio_notes():

    # type test
    assert isinstance(_doc_qio_notes, str)

    return


# /def


##########################################################################


def test_quantity_output_no_defaults():
    """Test :func:`~utilipy.units.core.quantity_return_`, without defaults."""

    @quantity_output
    def basic_function(x):
        return x

    # /def

    # Basic Test

    assert basic_function(1 * u.km) == 1 * u.km
    assert basic_function(1) == 1

    # Convert Unit

    assert basic_function(1000 * u.m, unit=u.km) == 1 * u.km
    assert basic_function(1000 * u.m, unit=u.km).value == 1

    # To Value

    assert basic_function(1000 * u.m, to_value=True) == 1000

    # Equivalencies

    assert (
        basic_function(1 * u.arcsec, unit=u.parsec, equivalencies=u.parallax())
        == 1 * u.parsec
    )

    # Decompose

    assert basic_function(1 * u.km, decompose=True) == 1000 * u.m
    assert basic_function(1 * u.km, decompose=[u.mm]) == 1e6 * u.mm

    # Combined Calls

    assert basic_function(1 * u.km, unit=u.m, to_value=True) == 1000


# /def


# ------------------------------------------------------------------------


def test_quantity_output_with_unit_default():
    """Test :func:`~utilipy.units.core.quantity_return_`, unit default."""

    @quantity_output(unit=u.km)
    def func_with_unit(x):
        return x

    # /def

    # Basic Test

    assert func_with_unit(1000 * u.m) == 1 * u.km
    assert func_with_unit(1) == 1

    # Convert Unit

    assert func_with_unit(1000 * u.m, unit=u.mm) == 1e6 * u.mm

    # To Value (implicit unit call)

    assert func_with_unit(1000 * u.m, to_value=True) == 1

    # Equivalencies

    assert func_with_unit(1 * u.arcsec, equivalencies=u.parallax()) == (
        1 * u.parsec
    ).to(u.km)

    # Decompose

    assert func_with_unit(1 * u.km, decompose=True) == 1000 * u.m
    assert func_with_unit(1 * u.km, decompose=[u.mm]) == 1e6 * u.mm

    # Combined Calls

    assert func_with_unit(1 * u.km, unit=u.m, to_value=True) == 1000


# /def


# ------------------------------------------------------------------------


def test_quantity_output_with_value_default():
    """Test :func:`~utilipy.units.core.quantity_return_`, value default."""

    @quantity_output(to_value=True)
    def func_with_value(x):
        return x

    # /def

    # Basic Test (implicit `to_value` call)

    assert func_with_value(1000 * u.m) == 1000
    assert func_with_value(1) == 1

    # Convert Unit (implicit `to_value` call)

    assert func_with_value(1000 * u.m, unit=u.mm) == 1e6

    # To Value

    assert func_with_value(1000 * u.m, to_value=False) == 1000 * u.m

    # Equivalencies

    assert func_with_value(1 * u.arcsec, equivalencies=u.parallax()) == 1

    # Decompose

    assert func_with_value(1 * u.km, decompose=True) == 1000
    assert func_with_value(1 * u.km, decompose=[u.mm]) == 1e6

    # Combined Calls

    assert func_with_value(1 * u.km, unit=u.m, to_value=True) == 1000

    return


# /def


##########################################################################


def test_QuantityInputOutput_methods():
    """Test QuantityInputOutput methods."""
    methods = ("as_decorator", "__init__", "__call__")
    for method in methods:
        assert hasattr(QuantityInputOutput, method) is True

    return


# /def


# ------------------------------------------------------------------------


# default, actual, fail
@pytest.mark.parametrize("unit", [None, u.km])
@pytest.mark.parametrize("to_value", [False, True])
@pytest.mark.parametrize("equivalencies", [[], (u.parallax(),)])
@pytest.mark.parametrize("decompose", [False, (u.km, u.s)])
@pytest.mark.parametrize("assumed_units", [{}, {"a": u.km}])
@pytest.mark.parametrize("assume_annotation_units", [False, True])
def test_QuantityInputOutput_init(
    unit,
    to_value,
    equivalencies,
    decompose,
    assumed_units,
    assume_annotation_units,
):
    """Test :class:`utilipyQuantityInputOutput` initialization."""
    instance = QuantityInputOutput(
        function=None,  # nothing here
        unit=unit,
        to_value=to_value,
        equivalencies=equivalencies,
        decompose=decompose,
        assumed_units=assumed_units,
        assume_annotation_units=assume_annotation_units,
        **{},
    )

    # function not stored !?
    with pytest.raises(AttributeError):
        assert instance.function is None

    assert unit == instance.unit
    assert to_value == instance.to_value
    assert equivalencies == instance.equivalencies
    assert decompose == instance.decompose
    assert assumed_units == instance.assumed_units
    assert assume_annotation_units == instance.assume_annotation_units

    with pytest.raises(AssertionError):
        assert instance.decorator_kwargs is None

    return


# /def


# ------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_QuantityInputOutput_as_decorator():

    return


# /def


# ------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_QuantityInputOutput_call():

    return


# /def


##############################################################################
# END
