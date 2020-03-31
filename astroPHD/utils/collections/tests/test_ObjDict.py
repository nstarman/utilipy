#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Docstring and Metadata
"""test functions for util/collections/_ObjDict."""

__author__ = "Nathaniel Starkman"


###############################################################################
# IMPORTS

# PROJECT-SPECIFIC

from .._ObjDict import ObjDict


###############################################################################
# PARAMETERS

od = ObjDict(name="name", a=1, b=None, c=ObjDict("inner"))


###############################################################################
# idxDecorator


def test_ObjDict_creation():
    """Test creation of ObjDict."""
    # test
    assert od.name == "name"
    assert od.a == 1
    assert od.b is None
    assert isinstance(od.c, ObjDict) & (od.c.name == "inner")

    return


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_getitem():
    """__getitem__ method.

    - `name` is special and can only be accessed by .name
    - single item access
    - multiple item access
    - _as_generator
    - .getitem method
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


def test_ObjDict__setitem__():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict__getattr__():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict__setattr__():
    """@TODO."""
    pass


# /def

# -----------------------------------------------------------------------------


def test_ObjDict__repr__():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_values():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_items():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_subset():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_keyslist():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict__reduce__():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict__setstate__():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_dump():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_save():
    """@TODO."""
    pass


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_load():
    """@TODO."""
    pass


# /def


###############################################################################
# END
