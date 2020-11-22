# -*- coding: utf-8 -*-

"""Data Transformer Classes."""

__author__ = "Nathaniel Starkman"
__credits__ = ["Astropy"]


__all__ = [
    "DataTransform",
    "CompositeTransform",
]


##############################################################################
# IMPORTS

# BUILT-IN
import inspect
import typing as T
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from contextlib import suppress

##############################################################################
# CODE
##############################################################################

#####################################################################
# Built-In Transform Classes


class DataTransformBase(metaclass=ABCMeta):
    """Base Class for Data Transformations.

    An object that transforms a coordinate from one system to another.
    Subclasses must implement `__call__` with the provided signature.
    They should also call this superclass's ``__init__`` in their
    ``__init__``.

    Parameters
    ----------
    fromtype : class
        The coordinate frame class to start from.
    totype : class
        The coordinate frame class to transform into.
    priority : number
        The priority if this transform when finding the shortest
        coordinate transform path - large numbers are lower priorities.
    register_graph : `TransformGraph` or `None`
        A graph to register this transformation with on creation, or
        `None` to leave it unregistered.

    """

    def __init__(self, fromtype, totype, priority=1, register_graph=None):
        if not inspect.isclass(fromtype) and fromtype is not None:
            raise TypeError("fromtype must be a class")
        if not inspect.isclass(totype) and totype is not None:
            raise TypeError("totype must be a class")

        self.fromtype = fromtype
        self.totype = totype
        self.priority = float(priority)

        if register_graph:
            # this will do the type-checking when it adds to the graph
            self.register(register_graph)
        else:
            if not (inspect.isclass(fromtype) or fromtype is None) or not (
                inspect.isclass(totype) or totype is None
            ):
                raise TypeError("fromtype and totype must be classes")

    # /def

    def register(self, graph):
        """Register this transformation into graph.

        Add this transformation to the requested Transformation graph,
        replacing anything already connecting these two data types.

        Parameters
        ----------
        graph : a TransformGraph object
            The graph to register this transformation with.

        """
        graph.add_transform(self.fromtype, self.totype, self)

    # /def

    def unregister(self, graph):
        """Remove transformation from the graph.

        Parameters
        ----------
        graph : a TransformGraph object
            The graph to unregister this transformation from.

        Raises
        ------
        ValueError
            If this is not currently in the transform graph.

        """
        graph.remove_transform(self.fromtype, self.totype, self)

    # /def

    @abstractmethod
    def __call__(self, fromdata, totype):
        """Perform the transformation from ``fromtype`` to ``totype``.

        Parameters
        ----------
        fromdata : fromtype object
            An object of class matching ``fromtype`` that is to be transformed.
        totype : object
            An object that has the attributes necessary to fully specify the
            frame.  That is, it must have attributes with names that match the
            keys of the dictionary that ``totype.get_frame_attr_names()``
            returns. Typically this is of class ``totype``, but it *might* be
            some other class as long as it has the appropriate attributes.

        Returns
        -------
        tocoord : totype object
            The new coordinate after the transform has been applied.

        """

    # /def


# /class


# -------------------------------------------------------------------


class DataTransform(DataTransformBase):
    """A transformation defined by a function.

    A transformation defined by a function that accepts a
    type and returns the transformed object.

    Parameters
    ----------
    func : callable
        The transformation function. Should have a call signature
        ``func(fromdata, *args, **kwargs)``.
    fromtype : class
        The coordinate frame class to start from.
    totype : class
        The coordinate frame class to transform into.
    priority : number
        The priority if this transform when finding the shortest
        coordinate transform path - large numbers are lower priorities.
    register_graph : `TransformGraph` or `None`
        A graph to register this transformation with on creation, or
        `None` to leave it unregistered.

    Raises
    ------
    TypeError
        If ``func`` is not callable.
    ValueError
        If ``func`` cannot accept two arguments.

    """

    def __init__(
        self,
        func: T.Callable,
        fromtype,
        totype,
        priority: int = 1,
        register_graph=None,
        func_args: T.Optional[T.Sequence] = None,
        func_kwargs: T.Optional[T.Mapping] = None,
    ):
        """Create a data transformer."""
        if not callable(func):
            raise TypeError("func must be callable")

        with suppress(TypeError):
            sig = inspect.signature(func)
            kinds = [x.kind for x in sig.parameters.values()]
            if (
                len(x for x in kinds if x == sig.POSITIONAL_ONLY) != 2
                and sig.VAR_POSITIONAL not in kinds
            ):
                raise ValueError(
                    "provided function does not accept two arguments"
                )

        self.func = func
        self.func_args = list(func_args or [])  # None -> [], keeps full
        self.func_kwargs = func_kwargs  # None -> {}, keeps full

        # TODO store these or make each time in __call__?
        self.func_sig = inspect.signature(func)
        self.func_spec = inspect.getfullargspec(func)

        super().__init__(
            fromtype, totype, priority=priority, register_graph=register_graph
        )

    # /def

    def __call__(self, fromdata, *args, _override_kws: bool = False, **kwargs):
        """Run transformation.

        Parameters
        ----------
        fromdata : Any
        *args : Any
            arguments into the transformation
        _override_kws : bool
            whether to permit the default kwargs, or completely override by any
            supplied kwargs (if any are given here). If they are permitted,
            individual arguments are still overriden by ones supplied here.
        **kwargs : Any
            keyword argument into the transformation

        Returns
        -------
        todata : Any
            The result of running `fromdata` through the transformation

        """
        # create BoundArgument
        # have None here in `fromdata` b/c will update later
        ba = self.func_sig.bind_partial(
            None, *self.func_args, **self.func_kwargs
        )
        ba.apply_defaults()  # and the defaults

        # have to override with provided arguments
        _ba = self.func_sig.bind_partial(fromdata, *args, **kwargs)
        # propagate default kwargs (unless `_override_kws`)
        vkw = self.func_spec.varkw  # the name of the varkw param
        if vkw in _ba.arguments and not _override_kws:
            keys = _ba.arguments[vkw].keys()  # do not override these keys
            _ba.arguments[vkw].update(  # update arguments
                {
                    k: ba.arguments[vkw][k]
                    for k in keys
                    if k not in keys  # filtering out locked keys
                }
            )
        ba.arguments.update(_ba.arguments)

        # call function
        todata = self.func(*ba.args, **ba.kwargs)

        totype = self.totype if self.totype is not None else type(None)

        if not isinstance(todata, totype):
            raise TypeError(
                f"the transformation function yielded {todata} but "
                f"should have been of type {totype}"
            )

        return todata

    # /def


# /class


# -------------------------------------------------------------------


class CompositeTransform(DataTransformBase):
    """A transformation from a series of single-step transformations.

    .. todo::

        - support passed arguments to steps within the transform list

    Parameters
    ----------
    transforms : sequence of `DataTransform` objects
        The sequence of transformations to apply.
    fromtype : class
        The coordinate frame class to start from.
    totype : class
        The coordinate frame class to transform into.
    priority : number
        The priority if this transform when finding the shortest
        coordinate transform path - large numbers are lower priorities.
    register_graph : `TransformGraph` or `None`
        A graph to register this transformation with on creation, or
        `None` to leave it unregistered.

    """

    def __init__(
        self,
        transforms: T.Sequence,
        fromtype,
        totype,
        priority: int = 1,
        register_graph=None,
    ):
        """Create Composite Data Transformer."""
        super().__init__(
            fromtype, totype, priority=priority, register_graph=register_graph
        )

        self.transforms = tuple(transforms)

    # /def

    def __call__(self, fromdata, *args, _override_kws: bool = False, **kwargs):
        """Run transformation.

        Parameters
        ----------
        fromdata : Any
        *args : Any
            arguments into the first transformation
        _override_kws : bool
            whether to permit the default kwargs in the first transformation,
            or completely override by any supplied kwargs (if any are given
            here). If they are permitted, individual arguments are still
            overriden by ones supplied here.
        **kwargs : Any
            keyword argument into the first transformation

        Returns
        -------
        todata : Any
            The result of running `fromdata` through the transformation series
            listed in ``self.transforms``

        """
        todata = fromdata
        for i, t in enumerate(self.transforms):
            if i == 0:  # TODO what if doesn't accept args/kwargs?
                todata = t(
                    todata, *args, _override_kws=_override_kws, **kwargs
                )
            else:
                todata = t(todata)

        return todata

    # /def


# /class


#####################################################################
# Default Transformation Set
# TODO seed many more basics
#    - can do astropy and numpy ones
# AND do in separate file?


_default_xfm_set = defaultdict(
    dict,
    {
        None: {  # TODO replace this with an Any-to-None function
            k: DataTransform(lambda x: None, k, None)
            for k in (str, list, tuple, dict)
        },
        tuple: {  # TODO replace this with a many-to-tuple function
            k: DataTransform(lambda x: tuple(x), k, tuple)
            for k in (str, list, dict)
        },
        list: {  # TODO replace this with a many-to-list function
            k: DataTransform(lambda x: list(x), k, list)
            for k in (str, tuple, dict)
        },
        str: {  # TODO replace this with a many-to-str function
            k: DataTransform(lambda x: str(x), k, str)
            for k in (tuple, list, dict)
        },
        dict: {
            **{  # TODO replace this with a many-to-dict function
                k: DataTransform(lambda x: dict(x), k, dict)
                for k in (tuple, list, dict)
            },
            **{
                None: DataTransform(lambda x: dict(), None, dict)
            },  # None to dict
        },
    },
)


# # # map class names to colorblind-safe colors
# trans_to_color = OrderedDict()
# # trans_to_color[AffineTransform] = '#555555'  # gray
# trans_to_color[DataTransform] = "#783001"  # dark red-ish/brown
# # trans_to_color[FunctionTransformWithFiniteDifference] = '#d95f02'  # red-ish
# # trans_to_color[StaticMatrixTransform] = '#7570b3'  # blue-ish
# # trans_to_color[DynamicMatrixTransform] = '#1b9e77'  # green-ish


##############################################################################
# END
