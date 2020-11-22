# -*- coding: utf-8 -*-

"""Collections."""

__author__ = "Nathaniel Starkman"


__all__ = [
    # -------
    "WithDocstring",
    "WithMeta",
    "WithReference",
    # -------
    "MetaDataBase",
    "ReferenceBase",
    # -------
    "ObjDict",
]


##############################################################################
# IMPORTS

# BUILT-IN
import typing as T
from collections import OrderedDict

# THIRD PARTY
import wrapt
from astropy.utils.decorators import format_doc
from astropy.utils.metadata import MetaData

# PROJECT-SPECIFIC
from .pickle import dump as _dump  # nosec
from .pickle import load as _load  # nosec

##############################################################################
# PARAMETERS

odict_values = type(OrderedDict().values())
odict_items = type(OrderedDict().items())


##############################################################################
# CODE
##############################################################################

##########################################################################
# Wrapper Classes


class WithDocstring(wrapt.ObjectProxy):
    """Wrap object to add docstring.

    This is a :class:`~wrapt.ObjectProxy`.

    - Thin: All operations are carried to the wrapt value,
        except for ``__doc__``, which accesses the docstring attribute.
    - Light: operations do not carry the docstring

        >>> x = WithDocstring(2, doc="description")
        >>> y = x + 2

    Attributes
    ----------
    __doc__ : str
        description.

    """

    __doc__ = None

    def __init__(self, wrapped: T.Any, doc: str = None):
        """Object wrapt to include metadata.

        Parameters
        ----------
        wrapped : T.Any
            `WithMeta` wraps anything, just adding metadata.
        kw : Dict[T.Any, T.Any]
            the key, value pairs for the metadata

        """
        super().__init__(wrapped)
        self.__doc__ = doc

        return

    # /def


# /class


# ---------------------------------------------------------------------------


class WithMeta(wrapt.ObjectProxy):
    """Objects wrapt to include metadata.

    This is an :class:`~wrapt.ObjectProxy` for thin and light wrappers.

    - Thin: All operations are carried to the wrapt value,
            except for ``self.meta``, which accesses the meta attribute.
    - Light: operations do not carry the metadata

        >>> x = WithMeta(2)
        >>> y = x + 2
        >>> y.meta  # doctest: +SKIP
        AttributeError: 'int' object has no attribute 'meta'

    Attributes
    ----------
    meta : `~astropy.utils.metadata.MetaData`
        metadata OrderedDict managed by the Astropy metadata module.

        .. todo::

            implement with actual MetaData descriptor, not OrderedDict


    Notes
    -----
    see :mod:`~astropy.utils.metadata` for usage of the metadata module.

    """

    # meta = MetaData(copy=False)
    _meta: T.Optional[T.Dict] = None

    def __init__(self, wrapped: T.Any, **kw):
        """Object wrapt to include metadata.

        Parameters
        ----------
        wrapped : T.Any
            `WithMeta` wraps anything, just adding metadata.
        kw : Dict[T.Any, T.Any]
            the key, value pairs for the metadata

        """
        super().__init__(wrapped)
        # self.meta = MetaData(copy=False)
        self._meta = OrderedDict()

        for k, v in kw.items():
            self._meta[k] = v

    # /def

    @property
    def meta(self):
        """Metadata."""
        return self._meta

    # /def


# /class


# ---------------------------------------------------------------------------


class WithReference(WithMeta, WithDocstring):
    """Objects wrapt to include reference(s) and other metadata.

    Attributes
    ----------
    meta : `~astropy.utils.metadata.MetaData`
        metadata OrderedDict managed by the Astropy metadata module.
        Always has a "reference" item; None if not set.

    Notes
    -----
    see :mod:`~astropy.utils.metadata` for usage of the metadata module.

    """

    def __init__(
        self,
        wrapped: T.Any,
        *,
        doc: str = None,
        reference: T.Optional[T.Any] = None,
        **kw,
    ):
        """Object wrapt to include a reference, and any other metadata.

        Parameters
        ----------
        wrapped : Any
            `WithMeta` wraps anything, just adding metadata.
        reference: Any, optional
            The attribution for the object, such as a paper link.
        kw : Dict[Any, Any], any
            the key, value pairs for the metadata

        """
        # instantiate, with metadata
        # need to do this first to make the wrapt object
        super().__init__(wrapped, reference=reference, **kw)
        # then manually do WithDocstring
        self.__doc__ = doc

        return

    # /def

    @property
    def __reference__(self):
        """References Meta Information."""
        return self.meta["reference"]

    # /def


# /class


##########################################################################
# Base Classes


class MetaDataBase:
    r"""Superclass for object with MetaData.

    Child classes accept the class argument ``meta_copy``.

    Attributes
    ----------
    meta : `~astropy.utils.metadata.MetaData`
        Meta-data descriptor with ``copy`` set by `_meta_copy`.
    \_meta_copy : bool
        Whether `meta` has ``copy=True``.
        This is set with the class argument ``meta_copy``

        >>> class Child(MetaDataBase, meta_copy=False):
        ...     pass

    Examples
    --------
    Making a child class

        >>> class Child(MetaDataBase, meta_copy=False):
        ...     pass

    """

    _meta = OrderedDict()

    def __init_subclass__(cls, meta_copy: bool = True):
        """Control subclass creation.

        Parameters
        ----------
        meta_copy : bool, optional
            Whether the `~astropy.utils.metadata.MetaData` instance uses
            ``copy=True``.
            The value is stored in ``self._meta_copy``

        """
        cls.meta = MetaData(copy=meta_copy)
        cls._meta_copy = meta_copy
        super().__init_subclass__()

    # /def

    def __new__(cls, *args, **kwargs):
        if cls == MetaDataBase:
            raise TypeError(f"Must subclass {cls.__name__} to use.")
        return super().__new__(cls)

    # /def

    def __init__(self, **metadata):
        """Initialize Metadata.

        Parameters
        ----------
        **metadata : Any
            added to ``meta``

        """
        super().__init__()
        self.meta.update(metadata)

    # /def


# /class


# -------------------------------------------------------------------


class ReferenceBase(MetaDataBase):
    """Superclass for objects with references.

    Accepts the class argument ``meta_copy``.

    Attributes
    ----------
    meta : `~astropy.utils.metadata.MetaData`
        Meta-data descriptor with ``copy=False``.
        Always has a key "reference"
    __reference__  : Any
        A property attribute to access the key-value "reference" in `meta`.

    """

    def __new__(cls, *args, **kwargs):
        if cls == ReferenceBase:
            raise TypeError(f"Must subclass {cls.__name__} to use.")
        return super().__new__(cls, *args, **kwargs)

    # /def

    def __init__(self, *, reference: T.Union[None, str] = None, **metadata):
        """Initialize Reference Metadata.

        Parameters
        ----------
        reference : str, optional
            reference, added to metadata.
            accessible by ``__reference__``
        **metadata
            To add to metadata.

        """
        super().__init__(reference=reference, **metadata)

    # /def

    @property
    def __reference__(self):
        """Get reference from metadata, if exists."""
        return self.meta.get("reference", None)

    # /def


# /class


##########################################################################
# ObjDict


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

    def __init__(self, name: str = "", **kw: T.Any):
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
        self, keys: T.Union[str, T.Sequence[str]], as_generator: bool = False
    ) -> T.Any:
        """Override __getitem__.

        Parameters
        ----------
        keys: str, list of str
            the keys into ObjDict
            if str: just the value from key-value pair
            if list: list of values
        as_generator: bool  (default False)
            whether to return as a generator
            only if keys is a list

        Returns
        -------
        value(s): anything
            if str, just the value from key-value pair
            if list, list of values
            if as_generator, generator for list

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
        if as_generator:  # return generator
            return (OrderedDict.__getitem__(self, k) for k in keys)
        return [OrderedDict.__getitem__(self, k) for k in keys]

    # /def

    @format_doc(__getitem__.__doc__)
    def getitem(
        self, keys: T.Union[str, T.Sequence[str]], as_generator: bool = False
    ) -> T.Any:
        """Docstring from __getitem__."""
        return self.__getitem__(keys, as_generator=as_generator)

    # /def

    # ----------------------------------
    # attribute get / set
    # redirects to item get / set

    def __getattr__(self, key: T.Any) -> T.Any:
        """Getattr -> getitem."""
        return self[key]

    # /def

    def __setattr__(self, key: T.Any, value: T.Any) -> None:
        """Setattr -> setitem."""
        self[key] = value

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

    def values(self, *keys: T.Any) -> T.Union[odict_values, tuple]:
        """Values.

        Parameters
        ----------
        *keys: keys for values subset, default is all keys

        Returns
        -------
        values: list
            list of values for `*keys`

        """
        if keys:  # keys provided
            allkeys = self.keys()
            return tuple([self[k] for k in allkeys if k in keys])
        return super().values()

    # /def

    def items(self, *keys: T.Any) -> T.Union[odict_items, dict]:
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
        return self.fromkeys(keys).items()

    # /def

    def fromkeys(self, keys: T.Any = [], name: str = None) -> T.Any:
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
        else:
            allkeys = self.keys()

            if name is None:
                name = self.name + " subset"

            return ObjDict(
                name=name, **{k: self[k] for k in allkeys if k in keys}
            )

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

    def __reduce__(self) -> T.Tuple[T.Callable, T.Tuple[str], odict_items]:
        """Reduction method for serialization.

        structured as:
        1. the class
        2. (ObjDict name, )
        3. items

        """
        return (self.__class__, (self.name,), OrderedDict(self.items()))

    # /def

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
        protocol: T.Optional[int] = None,
        *,
        fopt: str = "b",
        fix_imports: bool = True,
    ):
        """Dump to pickle file.

        uses :func:`~utilipy.utils.pickle.dump`

        """
        _dump(
            self, fname, protocol=protocol, fopt=fopt, fix_imports=fix_imports
        )

    # /def

    @format_doc(dump.__doc__)
    def save(
        self,
        fname: str,
        protocol: T.Optional[int] = None,
        *,
        fopt: str = "b",
        fix_imports: bool = True,
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
        errors: str = "strict",
    ):
        """Load from pickle file.

        uses :func:`~utilipy.utils.pickle.load`

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

    # /def


# /class


##############################################################################
# END
