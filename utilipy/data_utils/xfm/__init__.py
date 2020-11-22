# -*- coding: utf-8 -*-
# see LICENSE.rst

"""Data Transformation.

The plan is to build an analog to astropy's TransformGraph, which is only for
coordinate frames, but for converting between arbitrary data types.
The advantage of this kind of system is that many DataTransformGraphs can be
created, each of which is intended for different use. For instance, the xmatch
functions need to find the reference epoch in a data set and ensure that the
information is converted in a particular way. This conversion is need-specific
and would not be present in a very general converter, like PanDoc.

Notes
-----
These are dev notes for my thoughts on building the TransformGraph.

- What about subclasses? how can a subclass be recognized to use a particular
  conversion?
- What about Any-to-something conversions, like trying Table(x) or array(y)?
  these should have lower priority than a registered conversion, but should
  work.

    - have a Any-to-this registry function to add these catch-all converters.
    - Maybe have an option for pre-populating these in the graph?

"""

__author__ = "Nathaniel Starkman"
__credits__ = ["Astropy"]


__all__ = [
    # modules
    "graph",
    "transformations",
    # functions
    "TransformGraph",
    # transformations
    "DataTransform",
    "CompositeTransform",
    # Parameters
    "data_graph",
]


##############################################################################
# IMPORTS

# BUILT IN

# PROJECT-SPECIFIC
from . import graph, transformations
from .graph import TransformGraph
from .transformations import CompositeTransform, DataTransform

##############################################################################
# PARAMETERS

data_graph = TransformGraph(seed_basic=True)


##############################################################################
# END
