# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.utils.collections`."""


__all__ = [
    "od",
    "test_ObjDict_creation",
    "test_ObjDict_getitem",
    "test_ObjDict__setitem__",
    "test_ObjDict__getattr__",
    "test_ObjDict__setattr__",
    "test_ObjDict__repr__",
    "test_ObjDict_values",
    "test_ObjDict_items",
    "test_ObjDict_subset",
    "test_ObjDict_keyslist",
    "test_ObjDict__reduce__",
    "test_ObjDict__setstate__",
    "test_ObjDict_dump",
    "test_ObjDict_save",
    "test_ObjDict_load",
    "test_ObjDict_print",
    "test_ReadOnlyDictionaryWrapper",
]


###############################################################################
# IMPORTS

# THIRD PARTY

import pytest


# PROJECT-SPECIFIC

from .. import collections
from ..collections import ObjDict


###############################################################################
# PARAMETERS

od = ObjDict(name="name", a=1, b=None, c=ObjDict("inner"))


###############################################################################
# idxDecorator


def test_ObjDict_creation():
    """Test creation of :class:`~utilipy.utils.collections.ObjDict`."""
    # test
    assert od.name == "name"
    assert od.a == 1
    assert od.b is None
    assert isinstance(od.c, ObjDict) & (od.c.name == "inner")

    return


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_getitem():
    """Test :func:`~utilipy.utils.collections.ObjDict.__getitem__`.

    - `name` is special and can only be accessed by .name
    - single item access
    - multiple item access
    - _as_generator
    - getitem method

    """
    # name
    assert od.name == "name"

    # ------------------------------------------------------------------------
    # [] syntax

    # singular
    assert od["a"] == 1
    assert od["b"] is None
    assert isinstance(od["c"], ObjDict) & (od["c"].name == "inner")

    # plural
    assert od["a", "b"] == [1, None]
    assert od["c",] == [  # noqa
        ObjDict("inner"),
    ]

    # ------------------------------------------------------------------------
    # __getitem__

    assert od.__getitem__("a") == 1
    assert od.__getitem__("b") is None
    assert od.__getitem__("c").name == "inner"

    # plural
    assert od.__getitem__(["a", "b"]) == [1, None]
    assert od.__getitem__(["c",]) == [  # noqa
        ObjDict("inner"),
    ]

    # singular _as_generator, should just be the object
    assert od.__getitem__("a", _as_generator=True) == 1
    assert od.__getitem__("b", _as_generator=True) is None
    assert od.__getitem__("c", _as_generator=True).name == "inner"

    # plural _as_generator
    iterable = od.__getitem__(("a", "b", "c"), _as_generator=True)
    assert iterable.__next__() == 1
    assert iterable.__next__() is None
    assert iterable.__next__().name == "inner"

    # ------------------------------------------------------------------------
    # getitem

    assert od.getitem("a") == 1
    assert od.getitem("b") is None
    assert od.getitem("c").name == "inner"

    # plural
    assert od.getitem(["a", "b"]) == [1, None]
    assert od.getitem(["c",]) == [  # noqa
        ObjDict("inner"),
    ]

    # singular _as_generator, should just be the object
    assert od.getitem("a", _as_generator=True) == 1
    assert od.getitem("b", _as_generator=True) is None
    assert od.getitem("c", _as_generator=True).name == "inner"

    # plural _as_generator
    iterable = od.getitem(("a", "b", "c"), _as_generator=True)
    assert iterable.__next__() == 1
    assert iterable.__next__() is None
    assert iterable.__next__().name == "inner"

    return


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict__setitem__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__setitem__`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict__getattr__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__getattr__`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict__setattr__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__setattr__`."""
    pass


# /def

# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict__repr__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__repr__`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict_values():
    """Test :func:`~utilipy.utils.collections.ObjDict.values`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict_items():
    """Test :func:`~utilipy.utils.collections.ObjDict.items`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict_subset():
    """Test :func:`~utilipy.utils.collections.ObjDict.subset`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict_keyslist():
    """Test :func:`~utilipy.utils.collections.ObjDict.keyslist`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict__reduce__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__reduce__`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict__setstate__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__setstate__`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict_dump():
    """Test :func:`~utilipy.utils.collections.ObjDict.dump`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict_save():
    """Test :func:`~utilipy.utils.collections.ObjDict.save`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict_load():
    """Test :func:`~utilipy.utils.collections.ObjDict.load`."""
    pass


# /def


# -----------------------------------------------------------------------------


@pytest.mark.skip(reason="TODO")
def test_ObjDict_print():
    """Test :func:`~utilipy.utils.collections.ObjDict.print`."""
    pass


# /def


##########################################################################


@pytest.mark.skip(reason="TODO")
def test_ReadOnlyDictionaryWrapper():
    """Test :class:`~utilipy.utils.collections.ReadOnlyDictionaryWrapper`."""
    pass


# /def


# -----------------------------------------------------------------------------


###############################################################################
# END
