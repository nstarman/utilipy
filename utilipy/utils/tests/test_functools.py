# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : functools
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring
"""functools.

Routine Listings
----------------
test_WRAPPER_ASSIGNMENTS
test_SIGNATURE_ASSIGNMENTS
test_WRAPPER_UPDATES


"""

__author__ = "Nathaniel  Starkman"

# __all__ = [
#     ""
# ]


###############################################################################
# IMPORTS

# GENERAL

# import inspect
# import types


# PROJECT-SPECIFIC

from .. import functools

# from . import _test_functools_util


###############################################################################
# PARAMETERS


def test_WRAPPER_ASSIGNMENTS():
    """Test WRAPPER_ASSIGNMENTS."""
    assert functools.WRAPPER_ASSIGNMENTS == (
        "__module__",
        "__name__",
        "__qualname__",
        "__doc__",
        "__annotations__",
    )


# /def


def test_SIGNATURE_ASSIGNMENTS():
    """Test SIGNATURE_ASSIGNMENTS."""
    assert functools.SIGNATURE_ASSIGNMENTS == (
        "__kwdefaults__",
        "__annotations__",
    )


# /def


def test_WRAPPER_UPDATES():
    """Test WRAPPER_UPDATES."""
    assert functools.WRAPPER_UPDATES == ("__dict__",)

    # /def

    ###############################################################################
    # CODE
    ###############################################################################

    ###############################################################################
    # makeFunction

    # def test_makeFunction():
    #     """test makeFunction."""

    #     def function_code_block():

    #     pass

    # # /def

    # --------------------------------------------------------------------------

    ###############################################################################
    # copy_function

    # def test_copy_function():
    #     def test_func(
    #         x: "args",
    #         y,
    #         a: "default args" = 2,
    #         b=3,
    #         *args: "var args",
    #         p: "keyword args" = "L",
    #         q="M",
    #         **kwargs: "var kwargs"
    #     ):
    #         return x, y, a, b, args, p, q, kwargs

    #     tfc = functools.copy_function(test_func)

    #     # ------------------------------------
    #     # test properties

    #     for attr in dir(test_func):
    #         if attr not in (
    #             "__call__",
    #             "__delattr__",
    #             "__dir__",
    #             "__eq__",
    #             "__format__",
    #             "__ge__",
    #             "__get__",
    #             "__getattribute__",
    #             "__gt__",
    #             "__hash__",
    #             "__init__",
    #             "__le__",
    #             "__lt__",
    #             "__ne__",
    #             "__reduce__",
    #             "__reduce_ex__",
    #             "__repr__",
    #             "__setattr__",
    #             "__sizeof__",
    #             "__str__",
    #         ):
    #             assert getattr(tfc, attr) == getattr(test_func, attr)

    #     # __call__
    #     ba = inspect.signature(test_func).bind(
    #         0,
    #         [1, 1.5],
    #         2.1,
    #         3.1,
    #         4.0,
    #         4.33,
    #         4.66,
    #         p=5,
    #         q=[6, 6.5],
    #         r=7,
    #         s=[8, 8.5],
    #     )
    #     assert tfc.__call__(*ba.args, **ba.kwargs) == test_func.__call__(
    #         *ba.args, **ba.kwargs
    #     )

    #     # __delattr__
    #     assert hasattr(tfc, "attr_to_del") == hasattr(test_func, "attr_to_del")
    #     tfc.attr_to_del = "delete me"
    #     test_func.attr_to_del = "delete me"
    #     assert hasattr(tfc, "attr_to_del") == hasattr(test_func, "attr_to_del")
    #     assert tfc.attr_to_del == test_func.attr_to_del  # test equality
    #     tfc.__delattr__("attr_to_del")
    #     test_func.__delattr__("attr_to_del")
    #     assert hasattr(tfc, "attr_to_del") == hasattr(test_func, "attr_to_del")

    #     # __setattr__
    #     assert hasattr(tfc, "attr_to_del") == hasattr(test_func, "attr_to_del")
    #     tfc.__setattr__("attr_to_del", "delete me")
    #     test_func.__setattr__("attr_to_del", "delete me")
    #     assert hasattr(tfc, "attr_to_del") == hasattr(test_func, "attr_to_del")
    #     assert tfc.attr_to_del == test_func.attr_to_del  # and be equal
    #     del tfc.attr_to_del, test_func.attr_to_del
    #     assert hasattr(tfc, "attr_to_del") == hasattr(test_func, "attr_to_del")

    #     # __dir__
    #     assert set(tfc.__dir__()) == set(test_func.__dir__())

    #     # __getattribute__
    #     assert set(tfc.__getattribute__("__dir__")()) == set(
    #         test_func.__getattribute__("__dir__")()
    #     )

    #     # __eq__, __ge__, __gt__, '__le__', '__lt__', '__ne__'
    #     for attr in ("__eq__", "__ge__", "__gt__", "__le__", "__lt__", "__ne__"):
    #         assert tfc.__getattribute__(attr)(tfc) == test_func.__getattribute__(
    #             attr
    #         )(test_func)
    #         assert tfc.__getattribute__(attr)(
    #             test_func
    #         ) == test_func.__getattribute__(attr)(tfc)

    #     # __format__
    #     # TODO

    #     # __get__
    #     # TODO

    #     # __hash__
    #     # TODO

    #     # __init__
    #     # TODO

    #     # __reduce__, __reduce_ex__ TypeError: can't pickle function objects

    #     # __repr__
    #     # TODO, right now they are the same. Problem?

    #     # __sizeof__
    #     assert tfc.__sizeof__() == test_func.__sizeof__()

    #     # __str__
    #     assert tfc.__str__() != test_func.__str__()
    #     assert tfc.__str__().split(" ")[:-1] == test_func.__str__().split(" ")[:-1]

    #     # ------------------------------------
    #     # test calling

    #     # TODO

    #     return

    # # /def

    ###############################################################################
    # update_wrapper

    # def test_update_wrapper_defaults():

    #     # ----------------------------------------------
    #     # basic decorator

    #     def decorator(function):
    #         def wrapper(*args, **kwargs):
    #             return function(*args, **kwargs)

    #         return wrapper

    #     # /def

    #     for name in _test_functools_util.__all__:
    #         func = getattr(_test_functools_util, name)
    #         f_sig = inspect.signature(func)

    #         dec_func = functools.update_wrapper(decorator(func), func)
    #         df_sig = inspect.signature(dec_func)

    #         # assigned
    #         uwsig = inspect.signature(functools.update_wrapper)
    #         assigned = uwsig.parameters["assigned"].default
    #         for attr in assigned:
    #             assert getattr(dec_func, attr) == getattr(func, attr)

    #         # # updated  # doesn't work b/c stuff added to __dict__ after
    #         # updated = uwsig.parameters["updated"].default
    #         # for attr in updated:
    #         #     assert getattr(dec_func, attr) == getattr(func, attr)

    #         assert not hasattr(func, "__signature__")
    #         assert hasattr(dec_func, "__signature__")
    #         assert dec_func.__signature__ == df_sig

    #         # signature
    #         for attr in functools.SIGNATURE_ASSIGNMENTS:
    #             assert getattr(dec_func, attr) == getattr(func, attr)

    #         assert df_sig == f_sig

    #         # wrapped
    #         assert hasattr(dec_func, "__wrapped__")
    #         assert dec_func.__wrapped__ == func

    #         # TODO more tests

    #     # /for

    #     # ----------------------------------------------
    #     # decorator with kwargs

    #     def decorator(function):
    #         def wrapper(*args, kw1="test", **kwargs):
    #             return function(*args, **kwargs)

    #         return wrapper

    #     # /def


#     for name in _test_functools_util.__all__:
#         func = getattr(_test_functools_util, name)


#         f_sig = inspect.signature(func)

#         dec_func = functools.update_wrapper(decorator(func), func)
#         df_sig = inspect.signature(dec_func)

#         # assigned
#         uwsig = inspect.signature(functools.update_wrapper)
#         assigned = uwsig.parameters["assigned"].default
#         for attr in assigned:
#             assert getattr(dec_func, attr) == getattr(func, attr)

#         # # updated  # doesn't work b/c stuff added to __dict__ after
#         # updated = uwsig.parameters["updated"].default
#         # for attr in updated:
#         #     assert getattr(dec_func, attr) == getattr(func, attr)

#         assert not hasattr(func, "__signature__")
#         assert hasattr(dec_func, "__signature__")
#         assert dec_func.__signature__ == df_sig

#         # signature
#         for attr in functools.SIGNATURE_ASSIGNMENTS:
#             dfa = {
#                 k: v for k, v in getattr(dec_func, attr).items() if k != "kw1"
#             }
#             assert dfa == (getattr(func, attr) or {})

#         # same signature, except for 'kw1'
#         indx = list(df_sig.parameters.keys()).index("kw1")
#         sig = list(df_sig.parameters.values())
#         del sig[indx]
#         assert sig == list(f_sig.parameters.values())

#         # signature adds 'kw1' after *args
#         indx = list(df_sig.parameters.keys()).index("kw1")
#         list(df_sig.parameters.values())[
#             indx - 1
#         ].kind == inspect._VAR_POSITIONAL

#         # wrapped
#         assert hasattr(dec_func, "__wrapped__")
#         assert dec_func.__wrapped__ == func

#         # TODO more tests

#     # /for

#     # ----------------------------------------------
#     # decorator with args

#     def decorator(function):
#         def wrapper(x, *args, **kwargs):
#             return function(*args, **kwargs)

#         return wrapper

#     # /def

#     # TODO

#     # ----------------------------------------------

#     return


# # /def


# -----------------------------------------------------------------------------


def test_update_wrapper_signature_true():
    """Test the case when `signature`=True."""

    return


def test_update_wrapper_signature_false():
    """Test the case when `signature`=False."""

    return


def test_update_wrapper_signature_None():
    """Test the case when `signature`=None."""

    return


def test_update_wrapper_signature_Signature():
    """Test the case when `signature`is an inspect.Signature object."""
    return


def test_update_wrapper_signature_FullerSignature():
    """Test the case when `signature`is an FullerSignature object."""

    return


def test_update_wrapper_signature_notSignature():
    """Test the case when `signature`is not a Signature object.

    This should raise an error.

    """

    return


###############################################################################
# wraps


###############################################################################
# END
