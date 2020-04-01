# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : _test_functools_util
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Functions for use in testing functools."""

__author__ = "Nathaniel Starkman"

__all__ = [
    # args
    "func_x",
    "func_xy",
    "func_xy_annotate",
    # defargs
    "func_a",
    "func_ab",
    "func_ab_annotate",
    # *args
    "func_args",
    "func_args_annotate",
    # kwargs
    "func_p",
    "func_pq",
    "func_pq_annotate",
    # **kwargs
    "func_kwargs",
    "func_kwargs_annotate",
    # args, defargs
    "func_x_a",
    "func_xy_ab",
    "func_xy_ab_annotate",
    # args, *args
    "func_x_args",
    "func_xy_args",
    "func_xy_args_annotate",
    # args, kwargs
    "func_x_p",
    "func_xy_pq",
    "func_xy_pq_annotate",
    # args, **kwargs
    "func_x_kwargs",
    "func_xy_kwargs",
    "func_xy_kwargs_annotate",
    # defargs, *args
    "func_a_args",
    "func_ab_args",
    "func_ab_args_annotate",
    # defargs, kwargs
    "func_a_p",
    "func_ab_pq",
    "func_ab_pq_annotate",
    # defargs, **kwargs
    "func_a_kwargs",
    "func_ab_kwargs",
    "func_ab_kwargs_annotate",
    # *args, kwargs
    "func_args_p",
    "func_args_pq",
    "func_args_pq_annotate",
    # *args, **kwargs
    "func_args_kwargs",
    "func_args_kwargs_annotate",
    # args, defargs, **args
    "func_x_a_args",
    "func_xy_ab_args",
    "func_xy_ab_args_annotate",
    # args, defargs, kwargs
    "func_x_a_p",
    "func_xy_ab_pq",
    "func_xy_ab_pq_annotate",
    # args, defargs, **kwargs
    "func_x_a_kwargs",
    "func_xy_ab_kwargs",
    "func_xy_ab_kwargs_annotate",
    # args, *args, kwargs
    "func_x_args_p",
    "func_xy_args_pq",
    "func_xy_args_pq_annotate",
    # args, *args, **kwargs
    "func_x_args_kwargs",
    "func_xy_args_kwargs",
    "func_xy_args_kwargs_annotate",
    # defargs, *args, kwargs
    "func_a_args_p",
    "func_ab_args_pq",
    "func_ab_args_pq_annotate",
    # defargs, *args, **kwargs
    "func_a_args_kwargs",
    "func_ab_args_kwargs",
    "func_ab_args_kwargs_annotate",
    # *args, kwargs, **kwargs
    "func_args_p_kwargs",
    "func_args_pq_kwargs",
    "func_args_pq_kwargs_annotate",
    # args, defargs, *args, kwargs
    "func_x_a_args_p",
    "func_xy_ab_args_pq",
    "func_xy_ab_args_pq_annotate",
    # args, defargs, *args, **kwargs
    "func_x_a_args_kwargs",
    "func_xy_ab_args_kwargs",
    "func_xy_ab_args_kwargs_annotate",
    # args, defargs, kwargs, **kwargs
    "func_x_a_p_kwargs",
    "func_xy_ab_pq_kwargs",
    "func_xy_ab_pq_kwargs_annotate",
    # args, *args, kwargs, **kwargs
    "func_x_args_p_kwargs",
    "func_xy_args_pq_kwargs",
    "func_xy_args_pq_kwargs_annotate",
    # defargs, *args, kwargs, **kwargs
    "func_a_args_p_kwargs",
    "func_ab_args_pq_kwargs",
    "func_ab_args_pq_kwargs_annotate",
    # args, defargs, *args, kwargs, **kwargs
    "func_x_a_args_p_kwargs",
    "func_xy_ab_args_pq_kwargs",
    "func_xy_ab_args_pq_kwargs_annotate",
]

##############################################################################
# IMPORTS

import typing


##############################################################################
# CODE
##############################################################################

# -----------------------------------------------------------------------------
# Make Function NameSpace

# ----------------------------------------------
# Function with args


def func_x(x):
    """func.

    Parameters
    ----------
    x: float

    Returns
    -------
    x: float
    None, None, None, None, None, None, None

    """
    return x, None, None, None, None, None, None, None


# /def


def func_xy(x, y):
    """func.

    Parameters
    ----------
    x, y: float

    Returns
    -------
    x, y: float
    None, None, None, None, None, None

    """
    return x, y, None, None, None, None, None, None


# /def


@typing.no_type_check
def func_xy_annotate(x: "0", y) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float

    Returns
    -------
    x, y: float
    None, None, None, None, None, None

    """
    return x, y, None, None, None, None, None, None


# /def


# ----------------------------------------------
# Function with defargs


def func_a(a=2):
    """func.

    Parameters
    ----------
    a: int, optional

    Returns
    -------
    None, None
    a: int
    None, None, None, None, None

    """
    return None, None, a, None, None, None, None, None


# /def


def func_ab(a=2, b=3):
    """func.

    Parameters
    ----------
    a, b: int, optional

    Returns
    -------
    None, None
    a, b: int
    None, None, None, None

    """
    return None, None, a, b, None, None, None, None


# /def


@typing.no_type_check
def func_ab_annotate(a: "1" = 2, b=3) -> typing.Tuple:
    """func.

    Parameters
    ----------
    a, b: int, optional

    Returns
    -------
    None, None
    a, b: int
    None, None, None, None

    """
    return None, None, a, b, None, None, None, None


# /def


# ----------------------------------------------
# Function with *args


def func_args(*args):
    """func.

    Parameters
    ----------
    *args

    Returns
    -------
    None, None, None, None
    args: tuple
    None, None, None

    """
    return None, None, None, None, args, None, None, None


# /def


@typing.no_type_check
def func_args_annotate(*args: "2") -> typing.Tuple:
    """func.

    Parameters
    ----------
    *args

    Returns
    -------
    None, None, None, None
    args: tuple
    None, None, None

    """
    return None, None, None, None, args, None, None, None


# /def


# ----------------------------------------------
# Function with kwargs


def func_p(*, p="p"):
    """func.

    Parameters
    ----------
    p: str, optional

    Returns
    -------
    p: str

    """
    return None, None, None, None, None, p, None, None


# /def


def func_pq(*, p="p", q="q"):
    """func.

    Parameters
    ----------
    p, q: str, optional

    Returns
    -------
    p, q: str

    """
    return None, None, None, None, None, p, q, None


# /def


@typing.no_type_check
def func_pq_annotate(*, p: "3" = "p", q="q") -> typing.Tuple:
    """func.

    Parameters
    ----------
    p, q: str, optional

    Returns
    -------
    p, q: str

    """
    return None, None, None, None, None, p, q, None


# /def


# ----------------------------------------------
# Function with **kwargs


def func_kwargs(**kwargs):
    """func.

    Parameters
    ----------
    **kwargs

    Returns
    -------
    kwargs: dict

    """
    return None, None, None, None, None, None, None, kwargs


# /def


@typing.no_type_check
def func_kwargs_annotate(**kwargs: "4") -> typing.Tuple:
    """func.

    Parameters
    ----------
    **kwargs

    Returns
    -------
    kwargs: dict

    """
    return None, None, None, None, None, None, None, kwargs


# /def


# -----------------------------------------------------------------------------
# Function with args, kwargs


def func_x_a(x, a=2):
    """func.

    Parameters
    ----------
    x: float
    a: int, optional

    Returns
    -------
    x: float
    a: int

    """
    return x, None, a, None, None, None, None, None


# /def


def func_xy_ab(x, y, a=2, b=3):
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int, optional

    Returns
    -------
    x, y: float
    a, b: int

    """
    return x, y, a, b, None, None, None, None


# /def


@typing.no_type_check
def func_xy_ab_annotate(x: "0", y, a: "1" = 2, b=3) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int, optional

    Returns
    -------
    x, y: float
    a, b: int

    """
    return x, y, a, b, None, None, None, None


# /def


# ----------------------------------------------
# Function with args, *args


def func_x_args(x, *args):
    """func.

    Parameters
    ----------
    x: float
    args: tuple

    Returns
    -------
    x: float
    args: tuple

    """
    return x, None, None, None, args, None, None, None


# /def


def func_xy_args(x, y, *args):
    """func.

    Parameters
    ----------
    x, y: float
    args: tuple

    Returns
    -------
    x, y: float
    args: tuple

    """
    return x, y, None, None, args, None, None, None


# /def


@typing.no_type_check
def func_xy_args_annotate(x: "0", y, *args: "2") -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    args: tuple

    Returns
    -------
    x, y: float
    args: tuple

    """
    return x, y, None, None, args, None, None, None


# /def


# ----------------------------------------------
# Function with args, kwargs


def func_x_p(x, *, p="p"):
    """func.

    Parameters
    ----------
    x: float
    p: str, optional

    Returns
    -------
    x: float
    p: str

    """
    return x, None, None, None, None, p, None, None


# /def


def func_xy_pq(x, y, *, p="p", q="q"):
    """func.

    Parameters
    ----------
    x, y: float
    p, q: str, optional

    Returns
    -------
    x, y: float
    p, q: str

    """
    return x, y, None, None, None, p, q, None


# /def


@typing.no_type_check
def func_xy_pq_annotate(x: "0", y, *, p: "3" = "p", q="q") -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    p, q: str, optional

    Returns
    -------
    x, y: float
    p, q: str

    """
    return x, y, None, None, None, p, q, None


# /def


# ----------------------------------------------
# Function with args, **kwargs


def func_x_kwargs(x, **kwargs):
    """func.

    Parameters
    ----------
    x: float
    kwargs: dict

    Returns
    -------
    x: float
    kwargs: dict

    """
    return x, None, None, None, None, None, None, kwargs


# /def


def func_xy_kwargs(x, y, **kwargs):
    """func.

    Parameters
    ----------
    x, y: float
    kwargs: dict

    Returns
    -------
    x, y: float
    kwargs: dict

    """
    return x, y, None, None, None, None, None, kwargs


# /def


@typing.no_type_check
def func_xy_kwargs_annotate(x: "0", y, **kwargs: "4") -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    kwargs: dict

    Returns
    -------
    x, y: float
    kwargs: dict

    """
    return x, y, None, None, None, None, None, kwargs


# /def


# ----------------------------------------------
# Function with defargs, *args


def func_a_args(a=2, *args):
    """func.

    Parameters
    ----------
    a: int
    args: tuple

    Returns
    -------
    a: int
    args: tuple

    """
    return None, None, a, None, args, None, None, None


# /def


def func_ab_args(a=2, b=3, *args):
    """func.

    Parameters
    ----------
    a, b: int
    args: tuple

    Returns
    -------
    a, b: int
    args: tuple

    """
    return None, None, a, b, args, None, None, None


# /def


@typing.no_type_check
def func_ab_args_annotate(a: "1" = 2, b=3, *args: "2") -> typing.Tuple:
    """func.

    Parameters
    ----------
    a, b: int
    args: tuple

    Returns
    -------
    a, b: int
    args: tuple

    """
    return None, None, a, b, args, None, None, None


# /def


# ----------------------------------------------
# Function with defargs, kwargs


def func_a_p(a=2, *, p="p"):
    """func.

    Parameters
    ----------
    a: int
    p: str, optional

    Returns
    -------
    a: int
    p: str

    """
    return None, None, a, None, p, None, None, None


# /def


def func_ab_pq(a=2, b=3, *, p="p", q="q"):
    """func.

    Parameters
    ----------
    a, b: int
    p, q: str, optional

    Returns
    -------
    a, b: int
    p, q: str

    """
    return None, None, a, b, None, p, q, None


# /def


@typing.no_type_check
def func_ab_pq_annotate(
    a: "1" = 2, b=3, *, p: "3" = "p", q="q"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    a, b: int
    p, q: str, optional

    Returns
    -------
    a, b: int
    p, q: str

    """
    return None, None, a, b, None, p, q, None


# /def


# ----------------------------------------------
# Function with defargs, **kwargs


def func_a_kwargs(a=2, **kwargs):
    """func.

    Parameters
    ----------
    a: int, optional
    kwargs: dict

    Returns
    -------
    a: int
    kwargs: dict

    """
    return None, None, a, None, None, None, None, kwargs


# /def


def func_ab_kwargs(a=2, b=3, **kwargs):
    """func.

    Parameters
    ----------
    a, b: int, optional
    kwargs: dict

    Returns
    -------
    a, b: int
    kwargs: dict

    """
    return None, None, a, b, None, None, None, kwargs


# /def


@typing.no_type_check
def func_ab_kwargs_annotate(a: "1" = 2, b=3, **kwargs: "4") -> typing.Tuple:
    """func.

    Parameters
    ----------
    a, b: int, optional
    kwargs: dict

    Returns
    -------
    a, b: int
    kwargs: dict

    """
    return None, None, a, b, None, None, None, kwargs


# /def


# ----------------------------------------------
# Function with *args, kwargs


def func_args_p(*args, p="p"):
    """func.

    Parameters
    ----------
    args: tuple
    p: str, optional

    Returns
    -------
    args: tuple
    p: str

    """
    return None, None, None, None, args, p, None, None


# /def


def func_args_pq(*args, p="p", q="q"):
    """func.

    Parameters
    ----------
    args: tuple
    p, q: str, optional

    Returns
    -------
    args: tuple
    p, q: str

    """
    return None, None, None, None, args, p, q, None


# /def


@typing.no_type_check
def func_args_pq_annotate(*args: "2", p: "3" = "p", q="q") -> typing.Tuple:
    """func.

    Parameters
    ----------
    args: tuple
    p, q: str, optional

    Returns
    -------
    args: tuple
    p, q: str

    """
    return None, None, None, None, args, p, q, None


# /def


# ----------------------------------------------
# Function with *args, **kwargs


def func_args_kwargs(*args, **kwargs):
    """func.

    Parameters
    ----------
    args: tuple
    kwargs: dict

    Returns
    -------
    args: tuple
    kwargs: dict

    """
    return None, None, None, None, args, None, None, kwargs


# /def


@typing.no_type_check
def func_args_kwargs_annotate(*args: "2", **kwargs: "4") -> typing.Tuple:
    """func.

    Parameters
    ----------
    args: tuple
    kwargs: dict

    Returns
    -------
    args: tuple
    kwargs: dict

    """
    return None, None, None, None, args, None, None, kwargs


# /def


# -----------------------------------------------------------------------------
# Function with args, defargs, *args


def func_x_a_args(x, a=2, *args):
    """func.

    Parameters
    ----------
    x: float
    a: int
    args: tuple

    Returns
    -------
    x: float
    a: int
    args: tuple

    """
    return x, None, a, None, args, None, None, None


# /def


def func_xy_ab_args(x, y, a=2, b=3, *args):
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    args: tuple

    Returns
    -------
    x, y: float
    a, b: int
    args: tuple

    """
    return x, y, a, b, args, None, None, None


# /def


@typing.no_type_check
def func_xy_ab_args_annotate(
    x: "0", y, a: "1" = 2, b=3, *args: "2"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    args: tuple

    Returns
    -------
    x, y: float
    a, b: int
    args: tuple

    """
    return x, y, a, b, args, None, None, None


# /def


# ----------------------------------------------
# Function with args, defargs, kwargs


def func_x_a_p(x, a=2, *, p="p"):
    """func.

    Parameters
    ----------
    x: float
    a: int
    p: str

    Returns
    -------
    x: float
    a: int
    p: str

    """
    return x, None, a, None, None, p, None, None


# /def


def func_xy_ab_pq(x, y, a=2, b=3, *, p="p", q="q"):
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    p, q: str

    Returns
    -------
    x, y: float
    a, b: int
    p, q: str

    """
    return x, y, a, b, None, p, q, None


# /def


@typing.no_type_check
def func_xy_ab_pq_annotate(
    x: "0", y, a: int = 2, b=3, *, p: "3" = "p", q="q"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    p, q: str

    Returns
    -------
    x, y: float
    a, b: int
    p, q: str

    """
    return x, y, a, b, None, p, q, None


# /def


# ----------------------------------------------
# Function with args, defargs, **kwargs


def func_x_a_kwargs(x, a=2, **kwargs):
    """func.

    Parameters
    ----------
    x: float
    a: int
    kwargs: dict

    Returns
    -------
    x: float
    a: int
    kwargs: dict

    """
    return x, None, a, None, None, None, None, kwargs


# /def


def func_xy_ab_kwargs(x, y, a=2, b=3, **kwargs):
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    kwargs: dict

    Returns
    -------
    x, y: float
    a, b: int
    kwargs: dict

    """
    return x, y, a, b, None, None, None, kwargs


# /def


@typing.no_type_check
def func_xy_ab_kwargs_annotate(
    x: "0", y, a: int = 2, b=3, **kwargs: "4"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    kwargs: dict

    Returns
    -------
    x, y: float
    a, b: int
    kwargs: dict

    """
    return x, y, a, b, None, None, None, kwargs


# /def


# ----------------------------------------------
# Function with args, *args, kwargs


def func_x_args_p(x, *args, p="p"):
    """func.

    Parameters
    ----------
    x: float
    args: tuple
    p: str

    Returns
    -------
    x: float
    args: tuple
    p: str

    """
    return x, None, None, None, args, p, None, None


# /def


def func_xy_args_pq(x, y, *args, p="p", q="q"):
    """func.

    Parameters
    ----------
    x, y: float
    args: tuple
    p, q: str

    Returns
    -------
    x, y: float
    args: tuple
    p, q: str

    """
    return x, y, None, None, args, p, q, None


# /def


@typing.no_type_check
def func_xy_args_pq_annotate(
    x: "0", y, *args: "2", p: "3" = "p", q="q"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    args: tuple
    p, q: str

    Returns
    -------
    x, y: float
    args: tuple
    p, q: str

    """
    return x, y, None, None, args, p, q, None


# /def


# ----------------------------------------------
# Function with args, *args, **kwargs


def func_x_args_kwargs(x, *args, **kwargs):
    """func.

    Parameters
    ----------
    x: float
    args: tuple
    kwargs: dict

    Returns
    -------
    x: float
    args: tuple
    kwargs: dict

    """
    return x, None, None, None, args, None, None, kwargs


# /def


def func_xy_args_kwargs(x, y, *args, **kwargs):
    """func.

    Parameters
    ----------
    x, y: float
    args: tuple
    kwargs: dict

    Returns
    -------
    x, y: float
    args: tuple
    kwargs: dict

    """
    return x, y, None, None, args, None, None, kwargs


# /def


@typing.no_type_check
def func_xy_args_kwargs_annotate(
    x: "0", y, *args: "2", **kwargs: "4"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    args: tuple
    kwargs: dict

    Returns
    -------
    x, y: float
    args: tuple
    kwargs: dict

    """
    return x, y, None, None, args, None, None, kwargs


# /def


# ----------------------------------------------
# Function with defargs, *args, kwargs


def func_a_args_p(a=2, *args, p="p"):
    """func.

    Parameters
    ----------
    a: int
    args: tuple
    p: str

    Returns
    -------
    a: int
    args: tuple
    p: str

    """
    return None, None, a, None, args, p, None, None


# /def


def func_ab_args_pq(a=2, b=3, *args, p="p", q="q"):
    """func.

    Parameters
    ----------
    a, b: int
    args: tuple
    p, q: str

    Returns
    -------
    a, b: int
    args: tuple
    p, q: str

    """
    return None, None, a, b, args, p, q, None


# /def


@typing.no_type_check
def func_ab_args_pq_annotate(
    a: "1" = 2, b=3, *args: "2", p: "3" = "p", q="q"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    a, b: int
    args: tuple
    p, q: str

    Returns
    -------
    a, b: int
    args: tuple
    p, q: str

    """
    return None, None, a, b, args, p, q, None


# /def


# ----------------------------------------------
# Function with defargs, *args, **kwargs


def func_a_args_kwargs(a=2, *args, **kwargs):
    """func.

    Parameters
    ----------
    a: int
    args: tuple
    kwargs: dict

    Returns
    -------
    a: int
    args: tuple
    kwargs: dict

    """
    return None, None, a, None, args, None, None, kwargs


# /def


def func_ab_args_kwargs(a=2, b=3, *args, **kwargs):
    """func.

    Parameters
    ----------
    a, b: int
    args: tuple
    kwargs: dict

    Returns
    -------
    a, b: int
    args: tuple
    kwargs: dict

    """
    return None, None, a, b, args, None, None, kwargs


# /def


@typing.no_type_check
def func_ab_args_kwargs_annotate(
    a: "1" = 2, b=3, *args: "2", **kwargs: "4"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    a, b: int
    args: tuple
    kwargs: dict

    Returns
    -------
    a, b: int
    args: tuple
    kwargs: dict

    """
    return None, None, a, b, args, None, None, kwargs


# /def


# ----------------------------------------------
# Function with *args, kwargs, **kwargs


def func_args_p_kwargs(*args, p="p", **kwargs):
    """func.

    Parameters
    ----------
    args: tuple
    p: str
    kwargs: dict

    Returns
    -------
    args: tuple
    p: str
    kwargs: dict

    """
    return None, None, None, None, args, p, None, kwargs


# /def


def func_args_pq_kwargs(*args, p="p", q="q", **kwargs):
    """func.

    Parameters
    ----------
    args: tuple
    p, q: str
    kwargs: dict

    Returns
    -------
    args: tuple
    p, q: str
    kwargs: dict

    """
    return None, None, None, None, args, p, q, kwargs


# /def


@typing.no_type_check
def func_args_pq_kwargs_annotate(
    *args: "2", p: "3" = "p", q="q", **kwargs: "4"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    args: tuple
    p, q: str
    kwargs: dict

    Returns
    -------
    args: tuple
    p, q: str
    kwargs: dict

    """
    return None, None, None, None, args, p, q, kwargs


# /def


# ----------------------------------------------
# Function with args, defargs, *args, kwargs


def func_x_a_args_p(x, a=2, *args, p="p"):
    """func.

    Parameters
    ----------
    x: float
    a: int
    args: tuple
    p: str

    Returns
    -------
    x: float
    a: int
    args: tuple
    p: str

    """
    return x, None, a, None, args, p, None, None


# /def


def func_xy_ab_args_pq(x, y, a=2, b=3, *args, p="p", q="q"):
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    args: tuple
    p, q: str

    Returns
    -------
    x, y: float
    a, b: int
    args: tuple
    p, q: str

    """
    return x, y, a, b, args, p, q, None


# /def


@typing.no_type_check
def func_xy_ab_args_pq_annotate(
    x: "0", y, a: "1" = 2, b=3, *args: "2", p: "3" = "p", q="q"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    args: tuple
    p, q: str

    Returns
    -------
    x, y: float
    a, b: int
    args: tuple
    p, q: str

    """
    return x, y, a, b, args, p, q, None


# /def


# ----------------------------------------------
# Function with args, defargs, *args, **kwargs


def func_x_a_args_kwargs(x, a=2, *args, **kwargs):
    """func.

    Parameters
    ----------
    x: float
    a: int
    args: tuple
    kwargs: dict

    Returns
    -------
    x: float
    a: int
    args: tuple
    kwargs: dict

    """
    return x, None, a, None, args, None, None, kwargs


# /def


def func_xy_ab_args_kwargs(x, y, a=2, b=3, *args, **kwargs):
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    args: tuple
    kwargs: dict

    Returns
    -------
    x, y: float
    a, b: int
    args: tuple
    kwargs: dict

    """
    return x, y, a, b, args, None, None, kwargs


# /def


@typing.no_type_check
def func_xy_ab_args_kwargs_annotate(
    x: "0", y, a: "1" = 2, b=3, *args: "2", **kwargs: "4"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    args: tuple
    kwargs: dict

    Returns
    -------
    x, y: float
    a, b: int
    args: tuple
    kwargs: dict

    """
    return x, y, a, b, args, None, None, kwargs


# /def


# ----------------------------------------------
# Function with args, defargs, kwargs, **kwargs


def func_x_a_p_kwargs(x, a=2, *, p="p", **kwargs):
    """func.

    Parameters
    ----------
    x: float
    a: int
    p: str
    kwargs: dict

    Returns
    -------
    x: float
    a: int
    p: str
    kwargs: dict

    """
    return x, None, a, None, None, p, None, kwargs


# /def


def func_xy_ab_pq_kwargs(x, y, a=2, b=3, *, p="p", q="q", **kwargs):
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    p, q: str
    kwargs: dict

    Returns
    -------
    x, y: float
    a, b: int
    p, q: str
    kwargs: dict

    """
    return x, y, a, b, None, p, q, kwargs


# /def


@typing.no_type_check
def func_xy_ab_pq_kwargs_annotate(
    x: "0", y, a: "1" = 2, b=3, *, p: "3" = "p", q="q", **kwargs: "4"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    p, q: str
    kwargs: dict

    Returns
    -------
    x, y: float
    a, b: int
    p, q: str
    kwargs: dict

    """
    return x, y, a, b, None, p, q, kwargs


# /def


# ----------------------------------------------
# Function with args, *args, kwargs, **kwargs


def func_x_args_p_kwargs(x, *args, p="p", **kwargs):
    """func.

    Parameters
    ----------
    x: float
    args: tuple
    p: str
    kwargs: dict

    Returns
    -------
    x: float
    args: tuple
    p: str
    kwargs: dict

    """
    return x, None, None, None, args, p, None, kwargs


# /def


def func_xy_args_pq_kwargs(x, y, *args, p="p", q="q", **kwargs):
    """func.

    Parameters
    ----------
    x, y: float
    args: tuple
    p, q: str
    kwargs: dict

    Returns
    -------
    x, y: float
    args: tuple
    p, q: str
    kwargs: dict

    """
    return x, y, None, None, args, p, q, kwargs


# /def


@typing.no_type_check
def func_xy_args_pq_kwargs_annotate(
    x: "0", y, *args, p: "3" = "p", q="q", **kwargs: "4"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    args: tuple
    p, q: str
    kwargs: dict

    Returns
    -------
    x, y: float
    args: tuple
    p, q: str
    kwargs: dict

    """
    return x, y, None, None, args, p, q, kwargs


# /def


# ----------------------------------------------
# Function with defargs, *args, kwargs, **kwargs


def func_a_args_p_kwargs(a=2, *args, p="p", **kwargs):
    """func.

    Parameters
    ----------
    a: int
    args: tuple
    p: str
    kwargs: dict

    Returns
    -------
    a: int
    args: tuple
    p: str
    kwargs: dict

    """
    return None, None, a, None, args, p, None, kwargs


# /def


def func_ab_args_pq_kwargs(a=2, b=3, *args, p="p", q="q", **kwargs):
    """func.

    Parameters
    ----------
    a, b: int
    args: tuple
    p, q: str
    kwargs: dict

    Returns
    -------
    a, b: int
    args: tuple
    p, q: str
    kwargs: dict

    """
    return None, None, a, b, args, p, q, kwargs


# /def


@typing.no_type_check
def func_ab_args_pq_kwargs_annotate(
    a: "1" = 2, b=3, *args: "2", p: "3" = "p", q="q", **kwargs: "4"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    a, b: int
    args: tuple
    p, q: str
    kwargs: dict

    Returns
    -------
    a, b: int
    args: tuple
    p, q: str
    kwargs: dict

    """
    return None, None, a, b, args, p, q, kwargs


# /def


# ----------------------------------------------
# Function with args, defargs, *args, kwargs, **kwargs


def func_x_a_args_p_kwargs(x, a=2, *args, p="p", **kwargs):
    """func.

    Parameters
    ----------
    x: float
    a: int
    args: tuple
    p: str
    kwargs: dict

    Returns
    -------
    x: float
    a: int
    args: tuple
    p: str
    kwargs: dict

    """
    return x, None, a, None, args, p, None, kwargs


# /def


def func_xy_ab_args_pq_kwargs(x, y, a=2, b=3, *args, p="p", q="q", **kwargs):
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    args: tuple
    p, q: str, optional
    kwargs: dict

    Returns
    -------
    x, y: float
    a, b: int
    args: tuple
    p, q: str
    kwargs: dict

    """
    return x, y, a, b, args, p, q, kwargs


# /def


@typing.no_type_check
def func_xy_ab_args_pq_kwargs_annotate(
    x, y, a: "1" = 2, b=3, *args: "2", p: "3" = "p", q="q", **kwargs: "4"
) -> typing.Tuple:
    """func.

    Parameters
    ----------
    x, y: float
    a, b: int
    args: tuple
    p, q: str, optional
    kwargs: dict

    Returns
    -------
    x, y: float
    a, b: int
    args: tuple
    p, q: str
    kwargs: dict

    """
    return x, y, a, b, args, p, q, kwargs


# /def


# ----------------------------------------------
