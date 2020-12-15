# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.utils.collections`."""


__all__ = [
    "test_WithDocstring",
    "test_WithMeta",
    "test_WithReference",
    # -------
    "test_MetaDataBase",
    "test_ReferenceBase",
    # -------
    "test_ObjDict_creation",
    "test_ObjDict_getitem",
    "test_ObjDict__setitem__",
    "test_ObjDict__getattr__",
    "test_ObjDict__setattr__",
    "test_ObjDict__repr__",
    "test_ObjDict_values",
    "test_ObjDict_items",
    "test_ObjDict_fromkeys",
    "test_ObjDict_keyslist",
    "test_ObjDict__reduce__",
    "test_ObjDict__setstate__",
    "test_ObjDict_dump",
    "test_ObjDict_save",
    "test_ObjDict_load",
    "test_ObjDict_print",
]


###############################################################################
# IMPORTS

# BUILT-IN
import os.path
import tempfile
from collections import OrderedDict

# THIRD PARTY
import pytest

# PROJECT-SPECIFIC
from utilipy.utils import collections
from utilipy.utils.collections import ObjDict

###############################################################################
# PARAMETERS


###############################################################################
# CODE
###############################################################################

###############################################################################
# WithDdocstring


def test_WithDocstring():
    """Test :class:`~utilipy.utils.collections.WithDdocstring`."""
    doc = "this docstring has been added"

    # ------------------------------------------------------------------------
    # test integer

    x = collections.WithDocstring(2, doc=doc)

    assert x.__doc__ == doc  # test has docstring
    assert x.__wrapped__.__doc__ != doc  # test wrapped object does not

    # test operations do not carry through.
    y = x + 2
    assert y == 4
    assert y.__doc__ != doc

    # --------------------------------------------------
    # test something with docstring

    class Test(object):
        """Docstring for Test."""

        def __init__(self):
            super().__init__()

    # start with object
    test = Test()
    assert test.__doc__ == """Docstring for Test."""  # docstring matches

    # wrap & test
    wrapped = collections.WithDocstring(test, doc=doc)

    assert wrapped.__doc__ == doc  # test has docstring
    assert wrapped.__wrapped__.__doc__ == """Docstring for Test."""

    return


# /def


###############################################################################
# WithMeta


def test_WithMeta():
    """Test :class:`~utilipy.utils.collections.WithMeta`."""
    wm = collections.WithMeta(2, a="A", b="B")

    assert wm == 2

    # test meta
    assert hasattr(wm, "meta")
    assert isinstance(wm.meta, OrderedDict)
    assert wm.meta["a"] == "A"
    assert wm.meta["b"] == "B"

    with pytest.raises(KeyError):  # it shouldn't have this
        assert wm.meta["c"]

    # --------------------------------------------------
    # TODO test something with existing meta

    return


# /def


###############################################################################
# WithReference


def test_WithReference():
    """Test :class:`~utilipy.utils.collections.WithReference`."""
    doc = "this docstring has been added"
    ref = "Reference"

    wr = collections.WithReference(2, doc=doc, reference=ref, a="A", b="B")

    assert wr == 2

    # test docstring
    assert wr.__doc__ == doc

    wr.__doc__ = "changed"
    assert wr.__doc__ == "changed"

    # test reference
    assert wr.__reference__ == ref

    with pytest.raises(AttributeError):
        wr.__reference__ = "changed"

    # test meta
    assert isinstance(wr.meta, OrderedDict)
    assert wr.meta["a"] == "A"
    assert wr.meta["b"] == "B"

    assert wr.meta["reference"] == ref

    wr.meta["reference"] = "changed"
    assert wr.meta["reference"] == "changed"

    with pytest.raises(KeyError):  # it shouldn't have this
        assert wr.meta["c"]

    # --------------------------------------------------
    # TODO test something with existing meta

    return


# /def

###############################################################################
# MetaDataBase


def test_MetaDataBase_raises():
    """Test :class:`~utilipy.utils.collections.MetaDataBase` Exceptions."""
    with pytest.raises(TypeError):
        collections.MetaDataBase()  # MetaDataBase must be subclassed


# /def


def test_MetaDataBase():
    """Test :class:`~utilipy.utils.collections.MetaDataBase`."""
    # arguments into reference class
    meta = OrderedDict([("m1", "meta 1"), ("m2", "meta 2")])

    class ChildClass(collections.MetaDataBase):
        pass

    mdb = ChildClass(**meta)  # has reference in meta

    assert mdb._meta == meta
    assert mdb.meta == meta
    assert mdb.meta["m1"] == meta["m1"]


# /def


###############################################################################
# ReferenceBase


def test_ReferenceBase_raises():
    """Test :class:`~utilipy.utils.collections.ReferenceBase` Exceptions."""
    with pytest.raises(TypeError):
        collections.ReferenceBase()  # ReferenceBase must be subclassed


# /def


def test_ReferenceBase():
    """Test :class:`~utilipy.utils.collections.ReferenceBase`."""
    # arguments into reference class
    meta = OrderedDict([("m1", "meta 1"), ("m2", "meta 2")])
    reference = "the reference"

    class ChildClass(collections.ReferenceBase):
        pass

    mdb = ChildClass(reference=reference, **meta)  # has reference in meta

    # add reference into meta for comparisons
    meta["reference"] = reference

    assert mdb._meta == meta
    assert mdb.meta == meta
    assert mdb.meta["reference"] == meta["reference"] == reference
    assert mdb.meta["m1"] == meta["m1"]

    # test method
    assert mdb.__reference__ == reference


# /def


###############################################################################
# ObjDict


def test_ObjDict_creation():
    """Test creation of :class:`~utilipy.utils.collections.ObjDict`."""
    od = ObjDict(name="name", a=1, b=None, c=ObjDict("inner"))

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
    - as_generator
    - getitem method

    """
    od = ObjDict(name="name", a=1, b=None, c=ObjDict("inner"))

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

    # singular as_generator, should just be the object
    assert od.__getitem__("a", as_generator=True) == 1
    assert od.__getitem__("b", as_generator=True) is None
    assert od.__getitem__("c", as_generator=True).name == "inner"

    # plural as_generator
    iterable = od.__getitem__(("a", "b", "c"), as_generator=True)
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

    # singular as_generator, should just be the object
    assert od.getitem("a", as_generator=True) == 1
    assert od.getitem("b", as_generator=True) is None
    assert od.getitem("c", as_generator=True).name == "inner"

    # plural as_generator
    iterable = od.getitem(("a", "b", "c"), as_generator=True)
    assert iterable.__next__() == 1
    assert iterable.__next__() is None
    assert iterable.__next__().name == "inner"

    return


# /def


# -----------------------------------------------------------------------------


def test_ObjDict__setitem__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__setitem__`."""
    od = ObjDict(name="name", a=1, b=None, c=ObjDict("inner"))

    # setitem
    od["added"] = "added"
    assert od["added"] == "added"

    # __setitem__
    od.__setitem__("added2", "added2")
    assert od["added2"] == "added2"

    return


# /def


# -----------------------------------------------------------------------------


def test_ObjDict__getattr__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__getattr__`."""
    _c = ObjDict("inner", a="A")
    od = ObjDict(name="name", a=1, b=None, c=_c)

    assert od.__getattr__("a") == 1
    assert od.__getattr__("b") is None
    assert od.__getattr__("c").__getattr__("a") == "A"

    with pytest.raises(KeyError):
        assert od.__getattr__("name")  # only by __getattribute__

    return


# /def


# -----------------------------------------------------------------------------


def test_ObjDict__setattr__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__setattr__`."""
    # make ObjDict
    od = ObjDict()
    od.__setattr__("a", 1)

    # test
    assert od.__getattr__("a") == 1

    return


# /def

# -----------------------------------------------------------------------------


def test_ObjDict__repr__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__repr__`."""
    # --------------------------
    # without a name
    od = ObjDict(a=2)
    assert od.__repr__() == OrderedDict({"a": 2}).__repr__().replace(
        "OrderedDict", "ObjDict"
    )

    # --------------------------
    # with a name
    od = ObjDict("name", a=2)
    assert od.__repr__() == od.name + OrderedDict({"a": 2}).__repr__().replace(
        "OrderedDict", ""
    )
    return


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_values():
    """Test :func:`~utilipy.utils.collections.ObjDict.values`."""
    _c = ObjDict("inner", a="A")
    od = ObjDict(name="name", a=1, b=None, c=_c)

    # test standard (without keys)
    assert list(od.values()) == [1, None, _c]

    # test with keys
    assert list(od.values("a", "b")) == [1, None]

    return


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_items():
    """Test :func:`~utilipy.utils.collections.ObjDict.items`."""
    _c = ObjDict("inner", a="A")
    od = ObjDict(name="name", a=1, b=None, c=_c)

    # test standard (without keys)
    assert list(od.items()) == [
        ("a", 1),
        ("b", None),
        ("c", _c),
    ]

    # test when provide keys
    assert list(od.items("a", "b")) == [
        ("a", 1),
        ("b", None),
    ]

    return


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_fromkeys():
    """Test :func:`~utilipy.utils.collections.ObjDict.fromkeys`."""
    od = ObjDict(name="name", a=1, b=None, c="c")

    # test standard (without keys)
    assert od.fromkeys() == od

    # test standard, without keys, but name
    # shouldn't do anything
    assert od.fromkeys(name="new") == od

    # test with keys provided
    assert od.fromkeys(["a", "b"]) == ObjDict(name="name subset", a=1, b=None)
    assert od.fromkeys(["a", "b"], "Name") == ObjDict(name="Name", a=1, b=None)

    return


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_keyslist():
    """Test :func:`~utilipy.utils.collections.ObjDict.keyslist`."""
    od = ObjDict(name="name", a=1, b=None, c="c")

    assert set(od.keyslist()) == {"a", "b", "c"}


# /def


# -----------------------------------------------------------------------------


def test_ObjDict__reduce__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__reduce__`."""
    od = ObjDict(name="name", a=1, b=None, c="c")

    reduced = od.__reduce__()

    assert reduced[0] == od.__class__
    assert reduced[1] == (od.name,)
    assert reduced[2] == OrderedDict(od.items())


# /def


# -----------------------------------------------------------------------------


def test_ObjDict__setstate__():
    """Test :func:`~utilipy.utils.collections.ObjDict.__setstate__`."""
    od = ObjDict(name="name", a=1, b=None, c="c")

    new_od = ObjDict()
    new_od.__setstate__(od)

    assert new_od == od


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_dump():
    """Test :func:`~utilipy.utils.collections.ObjDict.dump`."""
    od = ObjDict(name="name", a=1, b=None, c="c")

    with tempfile.TemporaryDirectory() as tempdir:
        tempath = os.path.join(tempdir, "temp.pkl")
        od.dump(
            tempath,
            protocol=None,
            fopt="b",
            fix_imports=True,
        )

    # /with


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_save():
    """Test :func:`~utilipy.utils.collections.ObjDict.save`."""
    od = ObjDict(name="name", a=1, b=None, c="c")

    with tempfile.TemporaryDirectory() as tempdir:
        tempath = os.path.join(tempdir, "temp.pkl")
        od.save(
            tempath,
            protocol=None,
            fopt="b",
            fix_imports=True,
        )

    # /with


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_load():
    """Test :func:`~utilipy.utils.collections.ObjDict.load`."""
    od = ObjDict(name="name", a=1, b=None, c="c")

    with tempfile.TemporaryDirectory() as tempdir:
        tempath = os.path.join(tempdir, "temp.pkl")
        od.dump(
            tempath,
            protocol=None,
            fopt="b",
            fix_imports=True,
        )

        new_od = ObjDict.load(
            tempath,
            fopt="b",
            fix_imports=True,
            encoding="ASCII",
            errors="strict",
        )

    # /with

    # test equality between new and old
    assert new_od.name == od.name
    assert new_od.items() == od.items()


# /def


# -----------------------------------------------------------------------------


def test_ObjDict_print():  # TODO better test
    """Test :func:`~utilipy.utils.collections.ObjDict.print`.

    Right now, only testing that it doesn't error.

    """
    od = ObjDict(name="name", a=1, b=None, c="c")

    od.print()


# /def


##########################################################################


###############################################################################
# END
