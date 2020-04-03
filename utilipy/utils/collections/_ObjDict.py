# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ObjDict
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""initialization file for util."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL

from collections import OrderedDict
from typing import Any, Union, Sequence, Tuple, Callable, Optional


# PROJECT-SPECIFIC

from ..pickle import dump as _dump, load as _load
from ...decorators.docstring import format_doc


##############################################################################
# PARAMETERS

odict_values = type(OrderedDict().values())
odict_items = type(OrderedDict().items())


##############################################################################
# CODE


class ObjDict(OrderedDict):
    """Dictionary-like object intended to store information.

    instantiated with a name (str)
    supports __getattr__ as a redirect to __getitem__.

    Parameters
    ----------
    name: str
        the name of the object
    **kw
        items for ObjDict

    Examples
    --------
    >>> obj = ObjDict('NAME', a=1, b=2)
    >>> print(obj.name, obj.a, obj['b'])
    NAME 1 2

    """

    def __init__(self, name: str = "", **kw: Any) -> None:
        """Initialize ObjDict."""
        super().__init__()

        object.__setattr__(self, "name", name)

        # TODO better fix for inspect._is_wrapper
        object.__setattr__(self, "__wrapped__", None)

        for key, value in kw.items():
            self[key] = value

        return

    # /def

    # ----------------------------------
    # item get / set

    def __getitem__(
        self, keys: Union[str, Sequence[str]], _as_generator: bool = False
    ) -> Any:
        """Override __getitem__.

        Parameters
        ----------
        keys: str, list of str
            the keys into ObjDict
            if str: just the value from key-value pair
            if list: list of values
        _as_generator: bool  (default False)
            whether to return as a generator
            only if keys is a list

        Returns
        -------
        value(s): anything
            if str, just the value from key-value pair
            if list, list of values
            if _as_generator, generator for list

        Examples
        --------
        obj = ObjDict('NAME', a=1, b=2)
        print(obj['a'])
        >> 1, [NAME, 2]
        print(obj['name', 'b'])
        >> [NAME, 2]

        """
        # single key
        if isinstance(keys, str):
            return super().__getitem__(keys)
        # multiple keys
        if _as_generator:  # return generator
            return (OrderedDict.__getitem__(self, k) for k in keys)
        return [OrderedDict.__getitem__(self, k) for k in keys]

    # /def

    @format_doc(__getitem__.__doc__)
    def getitem(
        self, keys: Union[str, Sequence[str]], _as_generator: bool = False
    ) -> Any:
        """Docstring from __getitem__."""
        return self.__getitem__(keys, _as_generator=_as_generator)

    # /def

    # ----------------------------------
    # attribute get / set
    # redirects to item get / set

    def __setattr__(self, key: Any, value: Any) -> None:
        """Setattr -> setitem."""
        self[key] = value

    # /def

    def __getattr__(self, key: Any) -> Any:
        """Getattr -> getitem."""
        return self[key]

    # /def

    # ----------------------------------
    # Printing

    def __repr__(self) -> str:
        """__repr__."""
        if self.name == "":
            return super().__repr__()
        else:
            return self.name + super().__repr__().replace("ObjDict", "")

    # /def

    # ----------------------------------

    def values(self, *keys: Any) -> Union[odict_values, tuple]:
        """Values.

        Parameters
        ----------
        *keys: keys for values subset, default is all keys

        Returns
        -------
        values: list
            list of values for `*keys`

        """
        if not keys:  # if no specific keys provided
            return super().values()
        return tuple([self[k] for k in keys])

    # /def

    def items(self, *keys: Any) -> Union[odict_items, dict]:
        """Items.

        Parameters
        ----------
        *keys: keys for items subset, default is all keys

        Returns
        -------
        items: dictionary
            items for `*keys`

        """
        if not keys:
            return super().items()
        return self.subset(*keys).items()

    # /def

    def subset(self, *keys: Any) -> Any:
        """Subset.

        Parameters
        ----------
        *keys: keys for subset dictionary, default is all keys

        Returns
        -------
        subset: list
            items for `*keys`

        """
        if not keys:
            return self
        return {k: self[k] for k in keys}

    # /def

    def keyslist(self) -> list:
        """Keys in list form.

        Parameters
        ----------
        *keys: keys for subset dictionary, default is all keys

        Returns
        -------
        subset: list
            items for `*keys`

        """
        return list(self.keys())

    # /def

    # ----------------------------------
    # Serialize (I/O)

    def __reduce__(self) -> Tuple[Callable, str, odict_items]:
        """Reduction method for serialization.

        structured as:
        1. the class
        2. (ObjDict name, )
        3. items

        """
        return (self.__class__, (self.name,), OrderedDict(self.items()))

    def __setstate__(self, state: dict) -> None:
        """Set-state method for loading from pickle.

        sets by key, value pairs

        """
        for key, value in state.items():
            self[key] = value

    # /def

    def dump(
        self,
        fname: str,
        protocol: Optional[int] = None,
        *,
        fopt: str = "b",
        fix_imports: bool = True
    ):
        """Dump to pickle file.

        uses .utils.pickle.dump

        """
        _dump(
            self, fname, protocol=protocol, fopt=fopt, fix_imports=fix_imports
        )

    # /def

    @format_doc(dump.__doc__)
    def save(
        self,
        fname: str,
        protocol: Optional[int] = None,
        *,
        fopt: str = "b",
        fix_imports: bool = True
    ):
        """.Dump alias."""
        self.dump(fname, protocol=protocol, fopt=fopt, fix_imports=fix_imports)

    # /def

    @staticmethod
    def load(
        fname: str,
        *,
        fopt: str = "b",
        fix_imports: bool = True,
        encoding: str = "ASCII",
        errors: str = "strict"
    ):
        """Load from pickle file.

        uses .utils.pickle.load

        """
        self = _load(
            fname,
            fopt=fopt,
            fix_imports=fix_imports,
            encoding=encoding,
            errors=errors,
        )
        return self

    # /def

    # ----------------------------------

    def print(self):
        """Print."""
        print(self.__repr__())


# /class


##############################################################################
# END
