# -*- coding: utf-8 -*-

"""Data Transformation Graph."""

__author__ = "Nathaniel Starkman"
__credits__ = ["Astropy"]


__all__ = [
    "TransformGraph",
]


##############################################################################
# IMPORTS

# BUILT-IN
import heapq
import typing as T
from collections import defaultdict

# PROJECT-SPECIFIC
from .transformations import CompositeTransform, _default_xfm_set
from utilipy.utils import functools, inspect

##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


class TransformGraph:
    """Graph representing the paths between data types.

    Notes
    -----
    Note that the _graph key-value order is "totype": "fromtype".
    This is the opposite type as Astropy's since this TransformGraph
    needs to support:

    - catch-all conversions, such as converting from any sequence ``data``
      to type ``list`` by applying ``list(data)``
    - sub-type conversions, where the conversion a -> b (with types A, B)
      works on any subtype of A (like A1(A)).


    .. todo::

        - catch-all conversions to a specific type
        - multiple input option conversions to a specific type
        - multiple output option conversions by choosing one with shortest path
        - pre-register basic conversions like None->None, list->tuple

    """

    def __init__(self, seed_basic: bool = True):
        """Data Transformation Graph.

        Parameters
        ----------
        seed_basic : bool
            whether to start with a basic set of transformations

            .. todo::

                Generate documentation / colored graph like Astropy's

        """
        # graph, in reverse order
        self._graph = _default_xfm_set if seed_basic else defaultdict(dict)
        self.invalidate_cache()  # generates cache entries

    # /def

    @property
    def _cached_names(self):
        if self._cached_names_dct is None:
            self._cached_names_dct = dct = {}
            for c in self.type_set:
                nm = getattr(c, "name", None)
                if nm is not None:
                    if not isinstance(nm, list):
                        nm = [nm]
                    for name in nm:
                        dct[name] = c

        return self._cached_names_dct

    # /def

    @property
    def type_set(self):
        """A `set` of all data types present in this `TransformGraph`."""
        if self._cached_type_set is None:
            self._cached_type_set = set()
            for a in self._graph:
                self._cached_type_set.add(a)
                for b in self._graph[a]:
                    self._cached_type_set.add(b)

        return self._cached_type_set.copy()

    # /def

    def invalidate_cache(self):
        """Clears all caching attributes.

        Invalidates the cache that stores optimizations for traversing the
        transform graph.  This is called automatically when transforms
        are added or removed, but will need to be called manually if
        weights on transforms are modified inplace.

        """
        self._cached_names_dct: T.Optional[dict] = None
        self._cached_type_set: T.Optional[set] = None
        # self._cached_frame_attributes = None
        # self._cached_component_names = None
        self._shortestpaths = {}
        self._composite_cache = {}

    # /def

    def add_transform(self, fromtype, totype, transform):
        """Add a new data transformation to the graph.

        .. todo::

           - support an "Any" option in fromtype
           - support adding a tuple of types as the "fromtype"
           - support subtypes in "fromtype"

        Parameters
        ----------
        fromtype : class
            The data class to start from.
        totype : class
            The data class to transform into.
        transform : DataTransform or similar callable
            The transformation object. Typically a `DataTransform` object,
            although it may be some other callable that is called with the same
            signature.

        Raises
        ------
        TypeError
            If ``fromtype`` or ``totype`` are not classes or ``transform`` is
            not callable.

        """
        if not inspect.isclass(fromtype) and fromtype is not None:
            raise TypeError("fromtype must be a class")
        if not inspect.isclass(totype) and totype is not None:
            raise TypeError("totype must be a class")
        if not callable(transform):
            raise TypeError("transform must be callable")

        type_set = self.type_set.copy()
        type_set.add(fromtype)
        type_set.add(totype)

        self._graph[totype][fromtype] = transform
        self.invalidate_cache()

    # /def

    def remove_transform(self, fromtype, totype, transform):
        """Removes a data transform from the graph.

        .. todo::

            - support removing catch-all transformations

        Parameters
        ----------
        fromtype : class or `None`
            The coordinate frame *class* to start from. If `None`,
            ``transform`` will be searched for and removed (``totype`` must
            also be `None`).
        totype : class or `None`
            The coordinate frame *class* to transform into. If `None`,
            ``transform`` will be searched for and removed (``fromtype`` must
            also be `None`).
        transform : callable or `None`
            The transformation object to be removed or `None`.  If `None`
            and ``totype`` and ``fromtype`` are supplied, there will be no
            check to ensure the correct object is removed.

        """
        if fromtype is None or totype is None:
            if not (totype is None and fromtype is None):
                raise ValueError(
                    "fromtype and totype must both be None if either are"
                )
            if transform is None:
                raise ValueError("cannot give all Nones to remove_transform")

            # search for the requested transform by brute force and remove it
            for a in self._graph:
                agraph = self._graph[a]
                for b in agraph:
                    if agraph[b] is transform:
                        del agraph[b]
                        fromtype = a
                        break

                # If transform was found, need to break out of outer loop
                if fromtype:
                    break
            else:
                raise ValueError(
                    "Could not find transform {} in the "
                    "graph".format(transform)
                )

        else:
            if transform is None:
                self._graph[totype].pop(fromtype, None)
            else:
                curr = self._graph[totype].get(fromtype, None)
                if curr is transform:
                    self._graph[totype].pop(fromtype)
                else:
                    raise ValueError(
                        "Current transform from {} to {} is not "
                        "{}".format(fromtype, totype, transform)
                    )

        # Remove the subgraph if it is now empty
        if self._graph[totype] == {}:
            self._graph.pop(totype)

        self.invalidate_cache()

    # /def

    def _construct_path(self, fromtype, totype):
        """Construct path using Dijkstra's algorithm.

        Parameters
        ----------
        fromtype
        totype

        Returns
        -------
        path : list
        priority : int

        """
        inf = float("inf")

        nodes = []
        # first make the list of nodes
        for a in self._graph:
            if a not in nodes:
                nodes.append(a)
            for b in self._graph[a]:
                if b not in nodes:
                    nodes.append(b)

        if fromtype not in nodes or totype not in nodes:
            # fromtype or totype are isolated or not registered, so there's
            # certainly no way to get from one to the other
            return None, inf

        edgeweights = {}
        # construct another graph that is a dict of dicts of priorities
        # (used as edge weights in Dijkstra's algorithm)
        for a in self._graph:
            edgeweights[a] = aew = {}
            agraph = self._graph[a]
            for b in agraph:
                aew[b] = float(
                    agraph[b].priority if hasattr(agraph[b], "priority") else 1
                )

        # entries in q are [distance, count, nodeobj, pathlist]
        # count is needed because in py 3.x, tie-breaking fails on the nodes.
        # this way, insertion order is preserved if the weights are the same
        # q = [[inf,i,n,[]] for i, n in enumerate(nodes) if n is not fromtype]
        # q.insert(0, [0, -1, fromtype, []])
        q = [[inf, i, n, []] for i, n in enumerate(nodes) if n is not totype]
        q.insert(0, [0, -1, totype, []])

        # this dict stores the distance to node from ``fromtype`` and the path
        result = {}

        # definitely starts as a valid heap because of the insert line;
        # from the node to itself is always the shortest distance
        while len(q) > 0:
            d, orderi, n, path = heapq.heappop(q)

            if d == inf:
                # everything left is unreachable from fromtype,
                # just copy them to the results and jump out of the loop
                result[n] = (None, d)
                for d, orderi, n, path in q:
                    result[n] = (None, d)
                break
            else:
                result[n] = (path, d)
                path.append(n)
                if n not in edgeweights:
                    # a system that can be transformed to, but not from.
                    continue
                for n2 in edgeweights[n]:
                    if n2 not in result:  # already visited
                        # find where n2 is in the heap
                        for i in range(len(q)):
                            if q[i][2] == n2:
                                break
                        else:
                            raise ValueError(
                                "n2 not in heap - this should be impossible!"
                            )

                        newd = d + edgeweights[n][n2]
                        if newd < q[i][0]:
                            q[i][0] = newd
                            q[i][3] = list(path)
                            heapq.heapify(q)

        # cache for later use
        # self._shortestpaths[totype] = result # FIXME
        # return result[fromtype]
        # FIXME
        path, d = result[fromtype]
        return path[::-1], d

    # /def

    def find_shortest_path(self, fromtype, totype):
        """Compute shortest path along graph from one system to another.

        Parameters
        ----------
        fromtype : class
            The coordinate frame class to start from.
        totype : class
            The coordinate frame class to transform into.

        Returns
        -------
        path : list of classes or `None`
            The path from ``fromtype`` to ``totype`` as an in-order sequence
            of classes.  This list includes *both* ``fromtype`` and
            ``totype``. Is `None` if there is no possible path.
        distance : number
            The total distance/priority from ``fromtype`` to ``totype``.  If
            priorities are not set this is the number of transforms
            needed. Is ``inf`` if there is no possible path.

        """
        # ----------------------------------
        # special-case the 0 or 1-path

        if totype is fromtype:
            if fromtype not in self._graph[totype]:
                # Means there's no transform necessary to go from it to itself.
                return [totype], 0

        if fromtype in self._graph[totype]:
            # this will also catch the case where totype is fromtype, but has
            # a defined transform.
            t = self._graph[totype][fromtype]
            return (
                [fromtype, totype],
                float(t.priority if hasattr(t, "priority") else 1),
            )

        # ----------------------------------
        # otherwise, need to construct the path:

        inf = float("inf")

        # TODO verify this works for catch-alls
        if totype in self._shortestpaths:
            # already have a cached result
            fpaths = self._shortestpaths[totype]
            if fromtype in fpaths:
                return fpaths[fromtype]
            else:
                path, priority = None, inf

        path, priority = self._construct_path(fromtype, totype)

        return path, priority

    # /def

    def get_transform(self, fromtype, totype):
        """Generate `CompositeTransform` for a datatype transformation.

        Parameters
        ----------
        fromtype : class
            The coordinate frame class to start from.
        totype : class
            The coordinate frame class to transform into.

        Returns
        -------
        trans : `CompositeTransform` or `None`
            If there is a path from ``fromtype`` to ``totype``, this is a
            transform object for that path. If no path could be found, this is
            `None`.

        Notes
        -----
        This function always returns a `CompositeTransform`, because
        `CompositeTransform` is slightly more adaptable in the way it can be
        called than other transform classes. Specifically, it takes care of
        intermediate steps of transformations in a way that is consistent with
        1-hop transformations.

        """
        if not inspect.isclass(fromtype) and fromtype is not None:
            raise TypeError("fromtype is not a class")
        if not inspect.isclass(totype) and totype is not None:
            raise TypeError("totype is not a class")

        path, distance = self.find_shortest_path(fromtype, totype)

        if path is None:
            return None

        transforms = []
        currtype = path[0]
        for p in path[1:]:  # first element is fromtype so we skip it
            transforms.append(self._graph[p][currtype])
            currtype = p

        fttuple = (fromtype, totype)
        if fttuple not in self._composite_cache:
            comptrans = CompositeTransform(
                transforms, fromtype, totype, register_graph=False
            )
            self._composite_cache[fttuple] = comptrans

        return self._composite_cache[fttuple]

    # /def

    def lookup_name(self, name: str):
        """Tries to locate the class with the provided alias.

        Parameters
        ----------
        name : str
            The alias to look up.

        Returns
        -------
        datacls
            The data class corresponding to the ``name`` or `None` if
            no such class exists.

        """
        return self._cached_names.get(name, None)

    # /def

    def get_names(self):
        """Returns all available transform names.

        Returns
        -------
        nms : list
            The aliases for coordinate systems.
            They will all be valid arguments to `lookup_name`.

        """
        return list(self._cached_names.keys())

    # /def

    def register(
        self, transcls, fromtype, totype, priority: int = 1, **kwargs
    ):
        """A function decorator for defining a transformation.

        .. note::
            If decorating a static method of a class, ``@staticmethod``
            should be  added *above* this decorator.

        Parameters
        ----------
        transcls : class
            The class of the transformation object to create.
        fromtype : class
            The data class to start from.
        totype : class
            The data class to transform into.
        priority : number
            The priority if this transform when finding the shortest
            coordinate transform path - large numbers are lower priorities.

        Additional keyword arguments are passed into the ``transcls``
        constructor.

        Returns
        -------
        deco : function
            A function that can be called on another function as a decorator
            (see example).

        Notes
        -----
        This decorator assumes the first argument of the ``transcls``
        initializer accepts a callable, and that the second and third
        are ``fromtype`` and ``totype``. If this is not true, you should just
        initialize the class manually and use `add_transform` instead of
        using this decorator.

        Examples
        --------
        ::

            graph = TransformGraph()

            @graph.transform(DataTransform, list, tuple)
            def list_to_tuple(data):
                return tuple(data)

        """
        # create decorator
        def register_xfm_decorator(func: T.Callable):
            # this doesn't do anything directly with the transform because
            # ``register_graph=self`` stores it in the transform graph
            # automatically
            transcls(
                func,
                fromtype,
                totype,
                priority=priority,
                register_graph=self,
                **kwargs,
            )
            return func

        # /def

        return register_xfm_decorator

    # /def

    transform = register  # for similarity to Astropy's
    # /def

    def function_decorator(
        self,
        function: T.Optional[T.Callable] = None,
        *,
        _doc_style: str = "numpy",
        _doc_fmt: T.Dict[str, T.Any] = {},
        **arguments,
    ):
        """Apply data transformations to function arguments.

        Parameters
        ----------
        function : T.Callable or None, optional
            the function to be decoratored
            if None, then returns decorator to apply.

        **arguments: dict
            argument information, where keyword is the argument parameter
            name in `function`. The values are either the desired output type
            or a 3-element *tuple* in the following order
            (outtype, (args), dict(kwargs)). The args and kwargs are passed
            into the transformation.

        Returns
        -------
        wrapper : T.Callable
            wrapper for `function` that manage input catalog tables.
            includes the original function in a method `.__wrapped__`

        Other Parameters
        ----------------
        _doc_style: str or formatter, optional
            `function` docstring style. Parameter to `wraps`.
        _doc_fmt: dict, optional
            `function` docstring format arguments. Parameter to `wraps`.

        Notes
        -----
        .. todo::

            - scrape output type from function argument annotation
            - support a multiple possible output types (Union[etc]), choosing
              the one with the shortest path

        """
        if function is None:  # allowing for optional arguments
            return functools.partial(
                self.function_decorator,
                _doc_style=_doc_style,
                _doc_fmt=_doc_fmt,
                **arguments,
            )

        sig = inspect.fuller_signature(function)
        _doc_fmt.update({"argkeys": ", ".join(arguments.keys())})

        @functools.wraps(function, _doc_style=_doc_style, _doc_fmt=_doc_fmt)
        def wrapper(*args, _skip_decorator=False, **kwargs):
            """Wrapper docstring.

            Other Parameters
            ----------------
            _skip_decorator : bool, optional
                Whether to skip the decorator.
                default {_skip_decorator}

            Notes
            -----
            This function is wrapped with a data `~TransformGraph` decorator.
            See `~TransformGraph.function_decorator` for details.
            The transformation arguments are also attached to this function
            as the attribute ``._transforms``.
            The affected arguments are: {argkeys}

            """
            if _skip_decorator:  # whether to skip decorator or keep going
                return function(*args, **kwargs)
            # else:

            ba = sig.bind_partial_with_defaults(*args, **kwargs)

            for name, outtype in arguments.items():

                data = ba.arguments[name]  # get the data to be transformed

                # The values are either the desired output type
                # or a 3-element *tuple* in the following order
                # (outtype, (args), dict(kwargs)). The args and kwargs
                # are passed into the transformation.
                t_args, t_kw = (), {}  # assume no input (kw)args
                if isinstance(outtype, tuple):  # output type or info tuple
                    if len(outtype) == 3:  # it's an info tuple
                        outtype, t_args, t_kw = outtype

                # get transformation
                fromtype = type(data) if data is not None else None
                t = self.get_transform(fromtype, outtype)
                # print(t, type(data), outtype)
                # apply transformation
                ba.arguments[name] = t(data, *t_args, **t_kw)

            # /def

            return_ = function(*ba.args, **ba.kwargs)

            return return_

        # /def

        wrapper._transforms = arguments

        return wrapper

        # /def

    decorate = function_decorator
    # /def

    # def copy(self):
    #     """Deep-copy self"""
    #     return copy.deepcopy(self)

    # # /def


# /class


##############################################################################
# END
