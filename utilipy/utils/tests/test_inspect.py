# -*- coding: utf-8 -*-

"""Tests for :mod:`~utilipy.utils.inspect`."""


__all__ = [
    "test_parameters",
    "test__is_empty",
    "test__is_void",
    "test__is_placehold",
    "test__is_placeholder",
    "test_getfullerargspec",
    "test_get_annotations_from_signature",
    "test_get_defaults_from_signature",
    "test_get_kwdefaults_from_signature",
    "test_get_kwonlydefaults_from_signature",
    "test_get_kinds_from_signature",
    "test_modify_parameter",
    "test_replace_with_parameter",
    "test_insert_parameter",
    "test_prepend_parameter",
    "test_append_parameter",
    "test_drop_parameter",
    # test FullerSignature
    "test_FullerSignature_creation",
    "test_FullerSignature_bind",
    "test_FullerSignature_signature",
    "test_FullerSignature_annotations",
    "test_FullerSignature_defaults",
    "test_FullerSignature_kwdefaults",
    "test_FullerSignature_kinds",
    "test_FullerSignature_names",
    "test_FullerSignature_index_positional",
    "test_FullerSignature_index_positional_only",
    "test_FullerSignature_defaulted",
    "test_FullerSignature_index_var_positional",
    "test_FullerSignature_index_keyword_only",
    "test_FullerSignature_index_end_keyword_only",
    "test_FullerSignature_index_var_keyword",
    "test_FullerSignature_copy",
    "test_FullerSignature_modify_parameter",
    "test_FullerSignature_replace_with_parameter",
    "test_FullerSignature_insert_parameter",
    "test_FullerSignature_prepend_parameter",
    "test_FullerSignature_append_parameter",
    "test_FullerSignature_drop_parameter",
    "test_FullerSignature_add_var_positional_parameter",
    "test_FullerSignature_add_var_keyword_parameter",
    # "test_FullerSignature_hidden_methods",
    # fuller_signature
    "test_fuller_signature",
    "test_signature_from_method",
    "test_fuller_signature_from_method",
]


##############################################################################
# IMPORTS

# BUILT-IN
import inspect as nspct
from collections import OrderedDict
from types import MappingProxyType

# THIRD PARTY
import pytest

# PROJECT-SPECIFIC
from utilipy.utils import inspect

##############################################################################
# PARAMETERS


class NS:
    """Name Space. Testing without messing up pytest."""

    @staticmethod
    def test_func(
        x: int, y, a: int = 1, b=2, *args: str, j: str = "a", k="b", **kw: dict
    ) -> bool:
        """Function with all possible arguments."""
        x, y, a, b, args, j, k, kw  # pragma: no cover
        return True

    # /def

    @staticmethod
    def appendable_func(x, y):
        """Fumction with only positional-or-keyword arguments."""

    # /def

    @staticmethod
    def no_arg_func():
        """Function with no arguments."""

    # /def

    class ExceptEquality(object):
        """Throw an Exception on any equality test."""

        def __eq__(self, other):
            """No Equality."""
            raise Exception(f"forbidden equality tests with {other}")

        # /def

    # /class

    def method(
        self,
        x: int,
        y,
        a: int = 1,
        b=2,
        *args: str,
        j: str = "a",
        k="b",
        **kw: dict,
    ):
        pass

    # /def

    @classmethod
    def classmethod(
        cls,
        x: int,
        y,
        a: int = 1,
        b=2,
        *args: str,
        j: str = "a",
        k="b",
        **kw: dict,
    ):
        pass

    # /def


# /class

NS.NEQ = NS.ExceptEquality()
NS.normsig = nspct.Signature.from_callable(NS.test_func)
NS.fullsig = inspect.FullerSignature.from_callable(NS.test_func)
NS.noargsig = inspect.FullerSignature.from_callable(NS.no_arg_func)
NS.appsig = inspect.FullerSignature.from_callable(NS.appendable_func)


##############################################################################
# Tests
##############################################################################


def test_parameters():
    """Test array_like.

    TODO

    """
    # types
    assert inspect.POSITIONAL_ONLY == nspct.Parameter.POSITIONAL_ONLY
    assert (
        inspect.POSITIONAL_OR_KEYWORD == nspct.Parameter.POSITIONAL_OR_KEYWORD
    )
    assert inspect.VAR_POSITIONAL == nspct.Parameter.VAR_POSITIONAL
    assert inspect.KEYWORD_ONLY == nspct.Parameter.KEYWORD_ONLY
    assert inspect.VAR_KEYWORD == nspct.Parameter.VAR_KEYWORD

    # placeholders
    assert inspect._empty == nspct.Parameter.empty
    assert inspect._void == nspct._void

    assert type(inspect._placehold()) == inspect._placehold

    assert issubclass(inspect.FullerArgSpec, tuple)  # TODO full type check
    FAS = inspect.FullerArgSpec(1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert all(
        (
            FAS.args == 1,
            FAS.defaultargs == 2,
            FAS.argdefaults == 3,
            FAS.varargs == 4,
            FAS.kwonlyargs == 5,
            FAS.kwonlydefaults == 6,
            FAS.varkw == 7,
            FAS.annotations == 8,
            FAS.docstring == 9,
        )
    )


# /def


##########################################################################
# safe placeholder comparison


def test__is_empty():
    """Test _is_empty."""
    # True
    assert inspect._is_empty(inspect._empty)  # my inspect module
    assert inspect._is_empty(nspct.Parameter.empty)  # built-in

    # False
    assert not inspect._is_empty(1)

    # Exception
    assert not inspect._is_empty(NS.NEQ)


# /def


def test__is_void():
    """Test _is_void."""

    # True
    assert inspect._is_void(inspect._void)  # my inspect module
    assert inspect._is_void(nspct._void)  # built-in

    # False
    assert not inspect._is_void(1)

    # Exception
    assert not inspect._is_void(NS.NEQ)


# /def


def test__is_placehold():
    """Test _is_placehold."""

    # True
    assert inspect._is_placehold(inspect._placehold)  # my inspect module

    # False
    assert not inspect._is_placehold(1)

    # Exception
    assert not inspect._is_placehold(NS.NEQ)


# /def


def test__is_placeholder():
    """Test _is_placeholder."""
    # True
    assert all(
        (
            inspect._is_placeholder(inspect._empty),
            inspect._is_placeholder(inspect._void),
            inspect._is_placeholder(inspect._placehold),
        )
    )

    # False
    assert not inspect._is_placeholder(1)

    # Exception
    assert not inspect._is_placeholder(NS.NEQ)


# /def


###########################################################################
# getfullerargspec


def test_getfullerargspec():
    """Test :func:`~utilipy.utils.inspect.getfullerargspec`"""
    fullargspec = nspct.getfullargspec(NS.test_func)
    fullerargspec = inspect.getfullerargspec(NS.test_func)

    # arguments
    assert fullerargspec.args == ["x", "y"] == fullargspec.args[:-2]

    # default arguments
    assert fullerargspec.defaultargs == ["a", "b"] == fullargspec.args[-2:]
    assert fullerargspec.argdefaults == {"a": 1, "b": 2}
    assert tuple(fullerargspec.argdefaults.values()) == fullargspec.defaults

    # varargs
    assert fullerargspec.varargs == fullargspec.varargs

    # kwonlyargs
    assert fullerargspec.kwonlyargs == fullargspec.kwonlyargs
    assert fullerargspec.kwonlydefaults == fullargspec.kwonlydefaults

    # varkw
    assert fullerargspec.varkw == fullargspec.varkw

    # annotations
    assert fullerargspec.annotations == fullargspec.annotations

    assert fullerargspec.docstring == NS.test_func.__doc__

    return


# /def


###########################################################################
# Signature / ArgSpec Interface


def test_get_annotations_from_signature():
    """Test get_annotations_from_signature."""
    signature = inspect.signature(NS.test_func)
    annotations = inspect.get_annotations_from_signature(signature)

    assert annotations == {
        "x": int,
        "a": int,
        "args": str,
        "j": str,
        "kw": dict,
        "return": bool,
    }

    return


# /def


def test_get_defaults_from_signature():
    """Test get_annotations_from_signature."""
    signature = inspect.signature(NS.test_func)
    defaults = inspect.get_defaults_from_signature(signature)

    assert defaults == (1, 2)

    return


# /def


def test_get_kwdefaults_from_signature():
    """Test get_annotations_from_signature."""
    signature = inspect.signature(NS.test_func)
    kwdefaults = inspect.get_kwdefaults_from_signature(signature)

    assert kwdefaults == {"j": "a", "k": "b"}

    return


# /def


def test_get_kwonlydefaults_from_signature():
    """Test get_annotations_from_signature."""
    signature = inspect.signature(NS.test_func)
    kwdefaults = inspect.get_kwonlydefaults_from_signature(signature)

    assert kwdefaults == {"j": "a", "k": "b"}

    return


# /def


def test_get_kinds_from_signature():
    """Test get_annotations_from_signature."""
    signature = inspect.signature(NS.test_func)
    kinds = inspect.get_kinds_from_signature(signature)

    assert kinds == (
        inspect.POSITIONAL_OR_KEYWORD,
        inspect.POSITIONAL_OR_KEYWORD,
        inspect.POSITIONAL_OR_KEYWORD,
        inspect.POSITIONAL_OR_KEYWORD,
        inspect.VAR_POSITIONAL,
        inspect.KEYWORD_ONLY,
        inspect.KEYWORD_ONLY,
        inspect.VAR_KEYWORD,
    )


###########################################################################
# Signature Methods


def test_modify_parameter():
    """Test modify_parameter."""
    signature = inspect.signature(NS.test_func)

    # ----------------------------------------------------
    # doing piecemeal for full code coverage
    # and so can cycle through index / versus name as `param` arg
    sig = inspect.modify_parameter(signature, "x", name="xx")
    sig = inspect.modify_parameter(sig, "xx", kind=inspect.POSITIONAL_ONLY)
    sig = inspect.modify_parameter(sig, "y", default="Y")
    sig = inspect.modify_parameter(sig, 1, annotation="YY")

    parameters = list(sig.parameters.values())

    # changed
    assert parameters[0].name == "xx"
    assert parameters[0].kind == inspect.POSITIONAL_ONLY
    assert parameters[1].default == "Y"
    assert parameters[1].annotation == "YY"

    # not changed
    assert parameters[0].annotation == int
    assert parameters[1].name == "y"

    return


# /def


def test_replace_with_parameter():
    """Test replace_with_parameter."""
    signature = inspect.signature(NS.test_func)

    sig = inspect.modify_parameter(signature, 0, name="xx")
    sig = inspect.modify_parameter(sig, 1, name="yy")
    new_param0 = list(sig.parameters.values())[0]
    new_param1 = list(sig.parameters.values())[1]

    signature = inspect.replace_with_parameter(signature, "x", new_param0)
    signature = inspect.replace_with_parameter(signature, 1, new_param1)

    parameters = list(sig.parameters.values())

    assert parameters[0].name == "xx"
    assert parameters[1].name == "yy"

    return


# /def


def test_insert_parameter():
    """Test insert_parameter."""
    signature = inspect.signature(NS.test_func)

    sig = inspect.modify_parameter(signature, 0, name="xx")
    new_param = list(sig.parameters.values())[0]

    signature = inspect.insert_parameter(signature, 1, new_param)

    assert list(signature.parameters.values())[1].name == "xx"

    return


# /def


def test_prepend_parameter():
    """Test prepend_parameter."""
    signature = inspect.signature(NS.test_func)

    sig = inspect.modify_parameter(signature, 0, name="xx")
    new_param = list(sig.parameters.values())[0]

    signature = inspect.prepend_parameter(signature, new_param)

    assert list(signature.parameters.values())[0].name == "xx"

    return


# /def


def test_append_parameter():
    """Test append_parameter."""
    signature = inspect.signature(NS.appendable_func)

    sig = inspect.modify_parameter(signature, 0, name="xx")
    new_param = list(sig.parameters.values())[0]

    signature = inspect.append_parameter(signature, new_param)

    assert list(signature.parameters.values())[2].name == "xx"

    return


# /def


def test_drop_parameter():
    """Test drop_parameter."""
    signature = inspect.signature(NS.test_func)

    # don't drop anything
    newsignature = inspect.drop_parameter(signature, None)
    assert newsignature == signature

    # drop x, by name
    signature = inspect.drop_parameter(signature, "x")
    assert list(signature.parameters.values())[0].name == "y"

    # drop y, by index
    signature = inspect.drop_parameter(signature, 0)
    assert list(signature.parameters.values())[0].name == "a"

    # drop a, by parameter
    signature = inspect.drop_parameter(
        signature, list(signature.parameters.values())[0]
    )
    assert list(signature.parameters.values())[0].name == "b"

    # exception
    with pytest.raises(TypeError):  # can't drop a set
        inspect.drop_parameter(signature, set())

    return


# /def


###########################################################################
# Signature


def test_FullerSignature_creation():
    """Test `~utilipy.utils.inspect.FullerSignature` class creation."""
    # ------------------
    # __init__

    blanksig = inspect.FullerSignature()

    assert blanksig.parameters == MappingProxyType(OrderedDict())
    assert blanksig.return_annotation == inspect._empty
    assert blanksig.obj is None

    # manual construction
    parameters = {
        "x": inspect.Parameter("x", inspect.POSITIONAL_OR_KEYWORD, default=0),
        "y": inspect.Parameter("y", inspect.POSITIONAL_OR_KEYWORD, default=1),
    }

    madesig = inspect.FullerSignature(
        parameters=parameters.values(), return_annotation="return_"
    )

    assert madesig.parameters == parameters
    assert madesig.return_annotation == "return_"
    assert madesig.obj is None

    # ------------------
    # from_callable

    normsig = nspct.Signature.from_callable(NS.test_func)
    fromcallsig = inspect.FullerSignature.from_callable(NS.test_func)

    assert fromcallsig.parameters == normsig.parameters
    assert fromcallsig.return_annotation == normsig.return_annotation
    assert fromcallsig.obj == NS.test_func

    # ------------------
    # from_signature

    fromsigsig = inspect.FullerSignature.from_signature(
        fromcallsig, obj=NS.test_func
    )

    assert fromsigsig.parameters == fromcallsig.parameters
    assert fromsigsig.return_annotation == fromcallsig.return_annotation
    assert fromsigsig.obj == NS.test_func


# /def


def test_FullerSignature_bind():
    """Test `~utilipy.utils.inspect.FullerSignature` argument binding.

    The ``bind`` and ``bind_partial`` methods are tested by base python.
    Here we test the ``bind_with_defaults`` and ``bind_partial_with_defaults``

    """
    # ------------------
    # bind_with_defaults

    sig = NS.fullsig

    ba = sig.bind_with_defaults(-1, -2, 1.1, 2.2, 4, 5, l="cc")

    assert ba.args == (-1, -2, 1.1, 2.2, 4, 5)
    assert ba.kwargs == dict(j="a", k="b", l="cc")  # defaults in here

    # ------------------
    # bind_partial_with_defaults

    ba = sig.bind_partial_with_defaults(-1, l="cc")

    assert ba.args == (-1,)  # no y
    assert ba.arguments["a"] == 1
    assert ba.arguments["b"] == 2
    assert ba.kwargs == dict(
        a=1, b=2, args=(), j="a", k="b", l="cc"
    )  # defaults in here


# /def


def test_FullerSignature_signature():
    """Test `~utilipy.utils.inspect.FullerSignature` signature."""
    normsig = NS.normsig
    fullsig = NS.fullsig

    assert fullsig.signature == fullsig.__signature__ == normsig


# /def


def test_FullerSignature_annotations():
    normsig = NS.normsig
    fullsig = NS.fullsig

    assert (
        fullsig.annotations
        == fullsig.__annotations__
        == inspect.get_annotations_from_signature(normsig)
    )


# /def


def test_FullerSignature_defaults():
    normsig = NS.normsig
    fullsig = NS.fullsig

    assert (
        fullsig.defaults
        == fullsig.__defaults__
        == inspect.get_defaults_from_signature(normsig)
    )


# /def


def test_FullerSignature_kwdefaults():
    normsig = NS.normsig
    fullsig = NS.fullsig

    assert (
        fullsig.kwdefaults
        == fullsig.__kwdefaults__
        == fullsig.kwonlydefaults
        == inspect.get_kwdefaults_from_signature(normsig)
    )


# /def


def test_FullerSignature_kinds():
    normsig = NS.normsig
    fullsig = NS.fullsig

    assert fullsig.kinds == inspect.get_kinds_from_signature(normsig)


# /def


def test_FullerSignature_names():

    assert NS.fullsig.names == ("x", "y", "a", "b", "args", "j", "k", "kw")


# /def


def test_FullerSignature_index_positional():
    noargsig = NS.noargsig
    fullsig = NS.fullsig

    assert fullsig.index_positional == (0, 1, 2, 3)
    assert noargsig.index_positional is False


# /def


def test_FullerSignature_index_positional_only():
    fullsig = NS.fullsig

    assert fullsig.index_positional_only is False
    # need to make such a signature
    sig = fullsig.modify_parameter("x", kind=inspect.POSITIONAL_ONLY)
    assert sig.index_positional_only == (0,)


# /def


def test_FullerSignature_defaulted():
    fullsig = NS.fullsig
    noargsig = NS.noargsig

    assert fullsig.index_positional_defaulted == (0, 1, 2, 3)  # FIXME
    assert noargsig.index_positional_defaulted is False


# /def


def test_FullerSignature_index_var_positional():
    fullsig = NS.fullsig
    noargsig = NS.noargsig

    assert fullsig.index_var_positional == 4
    assert noargsig.index_var_positional is False


# /def


def test_FullerSignature_index_keyword_only():
    fullsig = NS.fullsig
    noargsig = NS.noargsig

    assert fullsig.index_keyword_only == (5, 6)
    assert noargsig.index_keyword_only is False


# /def


def test_FullerSignature_index_end_keyword_only():
    fullsig = NS.fullsig
    noargsig = NS.noargsig

    assert fullsig.index_end_keyword_only == (6 + 1)
    assert noargsig.index_end_keyword_only == (0 + 1)


# /def


def test_FullerSignature_index_var_keyword():
    fullsig = NS.fullsig
    noargsig = NS.noargsig

    assert fullsig.index_var_keyword == 7
    assert noargsig.index_var_keyword is False


# /def


def test_FullerSignature_copy():
    fullsig = NS.fullsig
    noargsig = NS.noargsig

    assert fullsig == fullsig.copy()
    assert noargsig == noargsig.copy()


# /def


def test_FullerSignature_modify_parameter():
    fullsig = NS.fullsig

    # doing piecemeal for full code coverage
    # and so can cycle through index / versus name as `param` arg
    sig = fullsig.modify_parameter("x", name="xx")
    sig = sig.modify_parameter("xx", kind=inspect.POSITIONAL_ONLY)
    sig = sig.modify_parameter("y", default="Y")
    sig = sig.modify_parameter(1, annotation="YY")

    assert isinstance(sig, inspect.FullerSignature)

    parameters = list(sig.parameters.values())

    # changed
    assert parameters[0].name == "xx"
    assert parameters[0].kind == inspect.POSITIONAL_ONLY
    assert parameters[1].default == "Y"
    assert parameters[1].annotation == "YY"

    # not changed
    assert parameters[0].annotation == int
    assert parameters[1].name == "y"


# /def


def test_FullerSignature_replace_with_parameter():
    fullsig = NS.fullsig

    sig = fullsig.modify_parameter(0, name="xx")
    sig = sig.modify_parameter(1, name="yy")
    new_param0 = list(sig.parameters.values())[0]
    new_param1 = list(sig.parameters.values())[1]

    sig = fullsig.replace_with_parameter("x", new_param0)
    sig = sig.replace_with_parameter(1, new_param1)

    assert isinstance(sig, inspect.FullerSignature)

    parameters = list(sig.parameters.values())

    assert parameters[0].name == "xx"
    assert parameters[1].name == "yy"


# /def


def test_FullerSignature_insert_parameter():
    fullsig = NS.fullsig

    sig = fullsig.modify_parameter(0, name="xx")
    new_param = list(sig.parameters.values())[0]

    sig = fullsig.insert_parameter(1, new_param)

    assert isinstance(sig, inspect.FullerSignature)

    assert list(sig.parameters.values())[1].name == "xx"


# /def


def test_FullerSignature_prepend_parameter():
    fullsig = NS.fullsig

    sig = fullsig.modify_parameter(0, name="xx")
    new_param = list(sig.parameters.values())[0]

    sig = fullsig.prepend_parameter(new_param)

    assert isinstance(sig, inspect.FullerSignature)

    assert list(sig.parameters.values())[0].name == "xx"


# /def


def test_FullerSignature_append_parameter():
    appsig = NS.appsig

    sig = appsig.modify_parameter(0, name="xx")
    new_param = list(sig.parameters.values())[0]

    sig = appsig.append_parameter(new_param)

    assert isinstance(sig, inspect.FullerSignature)

    assert list(sig.parameters.values())[2].name == "xx"


# /def


def test_FullerSignature_drop_parameter():
    fullsig = NS.fullsig

    # drop x, by name
    sig = fullsig.drop_parameter("x")
    assert list(sig.parameters.values())[0].name == "y"

    # drop y, by index
    sig = sig.drop_parameter(0)
    assert list(sig.parameters.values())[0].name == "a"

    # drop a, by parameter
    sig = sig.drop_parameter(list(sig.parameters.values())[0])
    assert list(sig.parameters.values())[0].name == "b"


# /def


def test_FullerSignature_add_var_positional_parameter():
    fullsig = NS.fullsig
    noargsig = NS.noargsig

    sig1 = fullsig.add_var_positional_parameter()
    sig2 = fullsig.add_var_positional_parameter(name="nargs")  # not changed
    sig3 = noargsig.add_var_positional_parameter(name="nargs")

    assert list(sig1.parameters.values())[4].name == "args"
    assert list(sig2.parameters.values())[4].name == "args"
    assert list(sig3.parameters.values())[0].name == "nargs"

    # if index in self.index_positional_defaulted
    dropsig = fullsig.drop_parameter("args")
    sig4 = dropsig.add_var_positional_parameter(name="args", index=3)
    assert list(sig4.parameters.values())[3].name == "args"

    # index < self.index_positional_defaulted[0]
    sig5 = dropsig.add_var_positional_parameter(name="args", index=2)
    assert list(sig5.parameters.values())[2].name == "args"

    # adding what already exists
    sig6 = dropsig.add_var_positional_parameter()
    assert list(sig6.parameters.values())[4].name == "args"


# /def


def test_FullerSignature_add_var_keyword_parameter():
    fullsig = NS.fullsig
    noargsig = NS.noargsig

    sig1 = fullsig.add_var_keyword_parameter()
    sig2 = fullsig.add_var_keyword_parameter(name="nargs")  # not changed
    sig3 = noargsig.add_var_keyword_parameter(name="kw")

    assert list(sig1.parameters.values())[-1].name == "kw"
    assert list(sig2.parameters.values())[-1].name == "kw"
    assert list(sig3.parameters.values())[-1].name == "kw"

    return


# /def


# def test_FullerSignature_hidden_methods():
#     fullsig = NS.fullsig

#     sig = fullsig._default_pos_to_kwonly_from(index=3)

#     assert False, list(sig.parameters.values())[2].kind


# # /def

# ------------------------------------------------------------------------


def test_fuller_signature():
    """Test `~utilipy.utils.inspect.fuller_signature`."""
    test_FullerSignature_creation()


# /def


def test_signature_from_method():
    """Test `~utilipy.utils.inspect.signature_from_method`."""
    # instance method
    sig = inspect.signature_from_method(NS.method)

    assert tuple(sig.parameters.values()) == tuple(
        NS.fullsig.signature.parameters.values()
    )

    # class method

    sig = inspect.signature_from_method(NS.classmethod)

    assert tuple(sig.parameters.values()) == tuple(
        NS.fullsig.signature.parameters.values()
    )


# /def


def test_fuller_signature_from_method():
    """Test `~utilipy.utils.inspect.fuller_signature_from_method`."""
    # instance method
    sig = inspect.fuller_signature_from_method(NS.method)

    assert tuple(sig.parameters.values()) == tuple(
        NS.fullsig.parameters.values()
    )

    # class method

    sig = inspect.fuller_signature_from_method(NS.classmethod)

    assert tuple(sig.parameters.values()) == tuple(
        NS.fullsig.parameters.values()
    )


# /def


##############################################################################
# END
