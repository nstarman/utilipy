# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE  : test util/inspect
#
# ----------------------------------------------------------------------------

"""tests for util/inspect.py."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

import inspect as nspct


# PROJECT-SPECIFIC

from .. import inspect


##############################################################################
# PARAMETERS


class NameSpace:
    """Store things for use in testing without messing up pytest."""

    @staticmethod
    def test_func(
        x: int, y, a: int = 1, b=2, *args: str, j: str = "a", k="b", **kw: dict
    ) -> bool:
        """Docstring."""
        x, y, a, b, args, j, k, kw  # pragma: no cover
        return True

    # /def

    def appendable_func(x, y):
        """Docstring."""
        pass

    # /def

    def no_arg_func():
        """Docstring."""
        pass

    # /def

    class ExceptEquality(object):
        """Docstring for ExceptEquality."""

        def __eq__(self, other):
            """No Equality."""
            other
            raise Exception

        # /def

    # /class


# /class

NameSpace.NEQ = NameSpace.ExceptEquality()


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
    FAS = inspect.FullerArgSpec(1, 2, 3, 4, 5, 6, 7, 8, 9,)
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

    return


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
    assert not inspect._is_empty(NameSpace.NEQ)

    return


# /def


def test__is_void():
    """Test _is_void."""

    # True
    assert inspect._is_void(inspect._void)  # my inspect module
    assert inspect._is_void(nspct._void)  # built-in

    # False
    assert not inspect._is_void(1)

    # Exception
    assert not inspect._is_void(NameSpace.NEQ)

    return


# /def


def test__is_placehold():
    """Test _is_placehold."""

    # True
    assert inspect._is_placehold(inspect._placehold)  # my inspect module

    # False
    assert not inspect._is_placehold(1)

    # Exception
    assert not inspect._is_placehold(NameSpace.NEQ)

    return


# /def


def test__is_placeholder():
    """Test _is_placeholder."""
    test__is_empty()
    test__is_void()
    test__is_placehold()


# /def


###########################################################################
# getfullerargspec


def test_getfullerargspec():

    fullargspec = nspct.getfullargspec(NameSpace.test_func)
    fullerargspec = inspect.getfullerargspec(NameSpace.test_func)

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

    assert fullerargspec.docstring == NameSpace.test_func.__doc__

    return


# /def

###########################################################################
# Signature / ArgSpec Interface


def test_get_annotations_from_signature():
    """Test get_annotations_from_signature."""
    signature = inspect.signature(NameSpace.test_func)
    annotations = inspect.get_annotations_from_signature(signature)

    assert annotations == {
        "x": int,
        "a": int,
        "args": str,
        "j": str,
        "kw": dict,
        "return": bool,
    }


def test_get_defaults_from_signature():
    """Test get_annotations_from_signature."""
    signature = inspect.signature(NameSpace.test_func)
    defaults = inspect.get_defaults_from_signature(signature)

    assert defaults == (1, 2)


def test_get_kwdefaults_from_signature():
    """Test get_annotations_from_signature."""
    signature = inspect.signature(NameSpace.test_func)
    kwdefaults = inspect.get_kwdefaults_from_signature(signature)

    assert kwdefaults == {"j": "a", "k": "b"}


def test_get_kwonlydefaults_from_signature():
    """Test get_annotations_from_signature."""
    signature = inspect.signature(NameSpace.test_func)
    kwdefaults = inspect.get_kwonlydefaults_from_signature(signature)

    assert kwdefaults == {"j": "a", "k": "b"}


def test_get_kinds_from_signature():
    """Test get_annotations_from_signature."""
    signature = inspect.signature(NameSpace.test_func)
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
    signature = inspect.signature(NameSpace.test_func)

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
    signature = inspect.signature(NameSpace.test_func)

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
    signature = inspect.signature(NameSpace.test_func)

    sig = inspect.modify_parameter(signature, 0, name="xx")
    new_param = list(sig.parameters.values())[0]

    signature = inspect.insert_parameter(signature, 1, new_param)

    assert list(signature.parameters.values())[1].name == "xx"

    return


# /def


def test_prepend_parameter():
    """Test prepend_parameter."""
    signature = inspect.signature(NameSpace.test_func)

    sig = inspect.modify_parameter(signature, 0, name="xx")
    new_param = list(sig.parameters.values())[0]

    signature = inspect.prepend_parameter(signature, new_param)

    assert list(signature.parameters.values())[0].name == "xx"

    return


# /def


def test_append_parameter():
    """Test append_parameter."""
    signature = inspect.signature(NameSpace.appendable_func)

    sig = inspect.modify_parameter(signature, 0, name="xx")
    new_param = list(sig.parameters.values())[0]

    signature = inspect.append_parameter(signature, new_param)

    assert list(signature.parameters.values())[2].name == "xx"

    return


# /def


def test_drop_parameter():
    """Test drop_parameter."""
    signature = inspect.signature(NameSpace.test_func)

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

    return


# /def


###########################################################################
# Signature


def test_FullerSignature():
    """TODO."""
    normsig = nspct.Signature.from_callable(NameSpace.test_func)
    fullsig = inspect.FullerSignature.from_callable(NameSpace.test_func)
    noargsig = inspect.FullerSignature.from_callable(NameSpace.no_arg_func)
    appsig = inspect.FullerSignature.from_callable(NameSpace.appendable_func)

    # ------------------
    # basic test
    assert fullsig.parameters == normsig.parameters
    assert fullsig.return_annotation == normsig.return_annotation

    # ------------------
    # signature
    assert fullsig.signature == fullsig.__signature__ == normsig

    # ------------------
    # annotations
    assert (
        fullsig.annotations
        == fullsig.__annotations__
        == inspect.get_annotations_from_signature(normsig)
    )

    # ------------------
    # defaults
    assert (
        fullsig.defaults
        == fullsig.__defaults__
        == inspect.get_defaults_from_signature(normsig)
    )

    # ------------------
    # kwdefaults
    assert (
        fullsig.kwdefaults
        == fullsig.__kwdefaults__
        == fullsig.kwonlydefaults
        == inspect.get_kwdefaults_from_signature(normsig)
    )

    # ------------------
    # kinds
    assert fullsig.kinds == inspect.get_kinds_from_signature(normsig)

    # ------------------
    # names
    assert fullsig.names == ("x", "y", "a", "b", "args", "j", "k", "kw")

    # ------------------
    # index_positional
    assert fullsig.index_positional == (0, 1, 2, 3)
    assert noargsig.index_positional is False

    # ------------------
    # index_positional_only
    # for parameters with kind = POSITIONAL_ONLY

    assert fullsig.index_positional_only is False
    # need to make such a signature
    sig = fullsig.modify_parameter("x", kind=inspect.POSITIONAL_ONLY)
    assert sig.index_positional_only == (0,)

    # ------------------
    # index_positional_defaulted
    assert fullsig.index_positional_defaulted == (0, 1, 2, 3)  # FIXME
    assert noargsig.index_positional_defaulted is False

    # ------------------
    # index_var_positional
    assert fullsig.index_var_positional == 4
    assert noargsig.index_var_positional is False

    # ------------------
    # index_keyword_only
    assert fullsig.index_keyword_only == (5, 6)
    assert noargsig.index_keyword_only is False

    # ------------------
    # index_end_keyword_only
    assert fullsig.index_end_keyword_only == (6 + 1)
    assert noargsig.index_end_keyword_only == (0 + 1)

    # ------------------
    # index_var_keyword
    assert fullsig.index_var_keyword == 7
    assert noargsig.index_var_keyword is False

    # ------------------
    # copy
    assert fullsig == fullsig.copy()

    # ------------------
    # modify_parameter

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

    # ------------------
    # replace_with_parameter

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

    # ------------------
    # insert_parameter

    sig = fullsig.modify_parameter(0, name="xx")
    new_param = list(sig.parameters.values())[0]

    sig = fullsig.insert_parameter(1, new_param)

    assert isinstance(sig, inspect.FullerSignature)

    assert list(sig.parameters.values())[1].name == "xx"

    # ------------------
    # prepend_parameter

    sig = fullsig.modify_parameter(0, name="xx")
    new_param = list(sig.parameters.values())[0]

    sig = fullsig.prepend_parameter(new_param)

    assert isinstance(sig, inspect.FullerSignature)

    assert list(sig.parameters.values())[0].name == "xx"

    # ------------------
    # append_parameter

    sig = appsig.modify_parameter(0, name="xx")
    new_param = list(sig.parameters.values())[0]

    sig = appsig.append_parameter(new_param)

    assert isinstance(sig, inspect.FullerSignature)

    assert list(sig.parameters.values())[2].name == "xx"

    # ------------------
    # drop_parameter

    # drop x, by name
    sig = fullsig.drop_parameter("x")
    assert list(sig.parameters.values())[0].name == "y"

    # drop y, by index
    sig = sig.drop_parameter(0)
    assert list(sig.parameters.values())[0].name == "a"

    # drop a, by parameter
    sig = sig.drop_parameter(list(sig.parameters.values())[0])
    assert list(sig.parameters.values())[0].name == "b"

    # ------------------
    # _default_pos_to_kwonly_from

    # sig = fullsig._default_pos_to_kwonly_from(index=3)

    # assert False, list(sig.parameters.values())[2].kind

    # ------------------
    # add_var_positional_parameter

    sig1 = fullsig.add_var_positional_parameter()
    sig2 = fullsig.add_var_positional_parameter(name="nargs")  # not changed
    sig3 = noargsig.add_var_positional_parameter(name="nargs")

    assert list(sig1.parameters.values())[4].name == "args"
    assert list(sig2.parameters.values())[4].name == "args"
    assert list(sig3.parameters.values())[0].name == "nargs"

    # ------------------
    # add_var_keyword_parameter

    sig1 = fullsig.add_var_keyword_parameter()
    sig2 = fullsig.add_var_keyword_parameter(name="nargs")  # not changed
    sig3 = noargsig.add_var_keyword_parameter(name="kw")

    assert list(sig1.parameters.values())[-1].name == "kw"
    assert list(sig2.parameters.values())[-1].name == "kw"
    assert list(sig3.parameters.values())[-1].name == "kw"


# ------------------------------------------------------------------------


def test_fuller_signature():
    """Test fuller_signature."""
    test_FullerSignature()


# /def


##############################################################################
# END
