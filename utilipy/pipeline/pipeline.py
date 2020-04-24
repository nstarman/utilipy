# -*- coding: utf-8 -*-

"""Pipeline."""

__author__ = "Nathaniel Starkman"


__all__ = [
    "Pipeline",
    "SequentialPipeline",
    "make_sequential_pipeline",
]


##############################################################################
# IMPORTS

# BUILT-IN

import typing as T


# PROJECT-SPECIFIC

from .pipeline_function import PipelineNode

from ..utils.inspect import (
    FullerSignature as _FullerSignature,
    Signature as _Signature,
)


###############################################################################
# PARAMETERS



##############################################################################
# Pipeline


class Pipeline:
    """Pipeline."""

    pass


# /class


# -------------------------------------------------------------------------


class SequentialPipeline(Pipeline):
    """A purely sequential `Pipeline`, without any loops."""

    def __init__(self, steps: list = []):
        """SequentialPipeline.

        Parameters
        ----------
        steps:
            the order of the Nodes.

        Notes
        -----
        Unique hash for Nodes by hashing internal hash + order added
        this allows a Node to be multiply connected and have a unique hash.

        """
        self._nodes: dict = {}
        self._order: list = []

        i: int
        func: PipelineNode
        for i, func in enumerate(steps):

            key: int = hash((func._hash, i))
            self._nodes[key] = func

            self._order.append(key)

        # /for

        return

    # /def

    # ------------------------------
    # call

    def __call__(self, signature: T.Union[_Signature, None], **kwargs: T.Any):
        """Call run."""
        return self.run(signature, **kwargs)

    # /def

    def run(self, signature: T.Union[_Signature, None], **kwargs: T.Any):
        """Run as pipeline.

        Parameters
        ----------
        signature : :class:`~utilipy.utils.inspect.Signature`
            The input signature node used to run the function.
            Note: passing None will work. Just needs to be done explicitly.
            the signature is constructed by ``self.inputs``,
            a :class:`~inspect.BoundArguments` with the ``self.input_defaults``
            and the wrapped node defaults. `signature` is then used
            to override with any included values.
        kwargs : Any
            key-word arguments, used to modify signature.
            have highest priority, overriding defaults and sig node.
            Most useful for testing, less so when running a real Pipeline.

        Returns
        -------
        :class:`~utilipy.utils.inspect.FullerSignature`
            The wrapped node's output, modified by ``self.output_hook``,
            and composed into a Signature node.

        Raises
        ------
        ValueError
            if kwarg not in self.inputs keys.

        """
        out: _FullerSignature = self._nodes[self._order[0]].run(
            signature, **kwargs
        )

        key: int
        for key in self._order[1:]:
            out = self._nodes[key].run(out)

        return out

    # /def


# /class


# -------------------------------------------------------------------------


def make_sequential_pipeline(steps: T.List[PipelineNode]):
    """Make SequentialPipeline.

    Parameters
    ----------
    steps : list
        list of PipelineNode objects

    Returns
    -------
    SequentialPipeline

    """
    # TODO get name of each step automatically using inspect
    return SequentialPipeline(steps)


# /def


##############################################################################
# END
