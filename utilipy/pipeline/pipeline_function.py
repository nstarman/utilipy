# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : pipeline function
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""pipeline function.

TODO
----
Rewrite using Signature objects and binding, etc.

- set the documentation for PipelineFunction
- figure out how to dynamically change the docstring for PipelineFunction
  so that it keeps the defaults set by .initialize in the docstring
- change name _func to __wrapped__?
"""

__author__ = "Nathaniel Starkman"

##############################################################################
# IMPORTS

# BUILT-IN

import os
import typing as T


# THIRD PARTY

from wrapt import ObjectProxy


# PROJECT-SPECIFIC

from ..utils import functools, inspect
from ..utils.inspect import (
    FullerSignature as _FullerSignature,
    Signature as _Signature,
    BoundArguments as _BoundArguments,
)


##############################################################################
# PARAMETERS

RegistryType = T.Dict[T.Union[int, T.Callable], T.Any]
HookType = T.Union[T.Callable, RegistryType]
OutputsType = T.Union[_Signature, T.Sequence]


##############################################################################
# CODE
##############################################################################


def _enable_pf():
    """Check whether pipeline functions are enabled by environment variable.

    TODO also get by configuration file.

    """
    return os.getenv(
        "enable_pipeline_functions", True  # environment variable nmae
    )  # default value


# /def

_ENABLED = _enable_pf()


##########################################################################


class PipelineNode(ObjectProxy):
    """Wrap a function into a pipeline-function.

    Except pipeline-related actions, any actions performed on the proxy
    are passed through to the wrapped node. This includes rich
    comparisons, hashing, duck typing, ``isinstance`` comparison,
    and importantly calling the function.

    To call the pipeline functionality, use the added ``.run`` method.

    Attributes
    ----------
    inputs
    input_defaults
    outputs

    Methods
    -------
    run
        run the pipeline version
    decorator
        pie-syntax decorate a function (use @)
        can also decorate via `PipelineNode`.

    See Also
    --------
    :class:`~wrapt.ObjectProxy`

    Notes
    -----
    The decorator can be globally disabled by setting
    an environment variable ``enable_pipeline_functions``

    .. todo::

        set enabled by config

    """

    # set the attributes here. Needed by ObjectProxy (?)  # TODO
    _hash: int  # base hash of the function
    _inputs: _FullerSignature
    input_defaults: T.Dict[str, T.Any]
    input_hook: HookType
    outputs: OutputsType
    output_hook: HookType

    # ------------------------------
    # create

    def __new__(
        cls,
        wrapped: T.Optional[T.Callable],
        outputs: OutputsType,
        *,  # force kwargs
        input_defaults: T.Dict[str, T.Any] = {},
        input_hook: HookType = None,
        output_hook: HookType = None,
        carry_through_unused: bool = False,
        enabled: bool = _ENABLED,
    ):
        """New PipelineNode. Or Not.

        Parameters
        ----------
        wrapped : Callable
            The node (generally function) to turn into Pipeline node.
            if None, redirects to :func:`PipelineNode.decorator`, so
            this can be used as a decorator.
        outputs : Signature or Sequence
            Sequence must be ordered, elements are strings for output names.
            For detailed control, like defaults, use a Signature node.
        input_defaults: Dict[str, Any], optional
            Parameter name, default value dictionary
            The inputs, including defaults are introspected from `wrapped`
            as a Signature. The `input_defaults` can override these defaults
            and also provide defaults for arguments without.
            The keys in `input_defaults` must match `wrapped`.
        input_hook : Callable or dict, optional
            Specifies the function to apply to the input of the ``run`` method.
            If callable, then applied on every ``run``.
            If dict, then keys specify hook function scope.

            The hook function must have the following signature
            ::

                def input_hook_func(signature):
                    return signature
        output_hook : Callable or dict, optional
            Specifies the function to apply to the ``run`` method output.
            If callable, then applied on every ``run``.
            If dict, then keys specify hook function scope.

            The hook function must have the following signature
            ::

                def output_hook_func(signature):
                    return signature

        carry_through_unused: bool, optional
            whether to carry through the input signature.
        enabled : bool, optional
            Whether the Pipeline should be used at all.
            If False, the decorated node will be return undisturbed.

        Returns
        -------
        PipelineNode or `wrapped`

        """
        # proxy to decorator, so can use @ syntax
        if wrapped is None:
            return cls.decorator(
                outputs=outputs,
                input_defaults=input_defaults,
                input_hook=input_hook,
                output_hook=output_hook,
                carry_through_unused=carry_through_unused,
                # decorator enabled
                enabled=enabled,
            )
        # optionally disable decorator.
        # needs to be after "wrapped is None"  b/c kick back from cls.decorator
        if enabled is False:
            return wrapped

        # else make ObjectProxy
        return super().__new__(cls, wrapped)

    # /def

    @classmethod
    def decorator(
        cls,
        *,
        outputs: OutputsType,
        input_defaults: T.Dict[str, T.Any] = {},
        input_hook: HookType = None,
        output_hook: HookType = None,
        carry_through_unused: bool = False,
        enabled: bool = _ENABLED,
    ):
        """@-Decorate a Callable to create a PipelineNode.

        Parameters
        ----------
        outputs : Signature or Sequence
            Sequence must be ordered, elements are strings for output names.
            For detailed control, like defaults, use a Signature object.
        input_defaults: Dict[str, Any], optional
            Parameter name, default value dictionary
            The inputs, including defaults are introspected from `wrapped`
            as a Signature. The `input_defaults` can override these defaults
            and also provide defaults for arguments without.
            The keys in `input_defaults` must match `wrapped`.
        input_hook : Callable or dict, optional
            Specifies the function to apply to the input of the ``run`` method.
            If callable, then applied on every ``run``.
            If dict, then keys specify hook function scope.

            The hook function must have the following signature
            ::

                def input_hook_func(signature):
                    return signature
        output_hook : Callable or dict, optional
            Specifies the function to apply to the ``run`` method output.
            If callable, then applied on every ``run``.
            If dict, then keys specify hook function scope.

            The hook function must have the following signature
            ::

                def output_hook_func(signature):
                    return signature

        carry_through_unused: bool, optional
            whether to carry through the input signature.
        enabled : bool, optional
            Whether the Pipeline should be used at all.
            If False, the decorated node will be return undisturbed.

        Returns
        -------
        PipelineNode or `wrapped`

        """
        return functools.partial(
            cls,
            # kwargs
            input_defaults=input_defaults,
            input_hook=input_hook,
            outputs=outputs,
            output_hook=output_hook,
            carry_through_unused=carry_through_unused,
            # enabler
            enabled=enabled,
        )

    # /def

    # ------------------------------
    # initialize

    def _outputs_init_helper(
        self, outputs: OutputsType, return_annotation: str
    ):
        if isinstance(outputs, _FullerSignature):
            pass
        elif isinstance(outputs, _Signature):
            outputs = _FullerSignature.from_signature(outputs)
        else:
            params = [
                inspect.Parameter(name=n, kind=inspect.POSITIONAL_OR_KEYWORD)
                for n in outputs
            ]
            outputs = _FullerSignature(
                parameters=params, return_annotation=return_annotation
            )
        return outputs

    # /def

    def __init__(
        self,
        wrapped: T.Optional[T.Callable],
        *,
        outputs: OutputsType,
        input_defaults: T.Dict[str, T.Any] = {},
        input_hook: HookType = None,
        output_hook: HookType = None,
        carry_through_unused: bool = False,
        enabled: bool = _ENABLED,
    ):
        """Initialize PipelineNode.

        Parameters
        ----------
        wrapped : Callable
            The node (generally function) to turn into Pipeline node.
            if None, redirects to :func:`PipelineNode.decorator`, so
            this can be used as a decorator.
        outputs : Signature or Sequence
            Sequence must be ordered, elements are strings for output names.
            For detailed control, like defaults, use a Signature node.
        input_defaults: Dict[str, Any], optional
            Parameter name, default value dictionary
            The inputs, including defaults are introspected from `wrapped`
            as a Signature. The `input_defaults` can override these defaults
            and also provide defaults for arguments without.
            The keys in `input_defaults` must match `wrapped`.
        input_hook : Callable or dict, optional
            Specifies the function to apply to the input of the ``run`` method.
            If callable, then applied on every ``run``.
            If dict, then keys specify hook function scope.

            The hook function must have the following signature
            ::

                def input_hook_func(signature):
                    return signature
        output_hook : Callable or dict, optional
            Specifies the function to apply to the ``run`` method output.
            If callable, then applied on every ``run``.
            If dict, then keys specify hook function scope.

            The hook function must have the following signature
            ::

                def output_hook_func(signature):
                    return signature

        carry_through_unused: bool, optional
            Whether to carry through the input signature.
        enabled : bool, optional
            Whether the Pipeline should be used at all.
            If False, the decorated node will be return undisturbed.

        """
        super().__init__(wrapped)
        self._hash: int = hash(wrapped)
        """Wrapped node hash."""
        self.carry_through_unused: bool = carry_through_unused
        """Whether to carry through the input signature."""

        # Introspect function to make inputs
        self._inputs: _FullerSignature = inspect.fuller_signature(wrapped)
        """Object signature, from introspection."""
        self.input_defaults: T.Dict[str, T.Any] = input_defaults
        # not making BoundArguments here, b/c allow input_defaults to update.

        # input hook
        if input_hook is None:
            self.input_hook: T.Callable = lambda sig: sig
        else:
            self.input_hook: HookType = input_hook

        # make extrospect
        self.outputs: _FullerSignature = self._outputs_init_helper(
            outputs=outputs, return_annotation=str(self._hash)
        )

        # output hook
        if output_hook is None:
            self.output_hook: T.Callable = lambda sig: sig
        else:
            self.output_hook: HookType = output_hook

        # properly document
        self.__doc__ = (self.__doc__ or "") + "\n decorated"

        return

    # /def

    # ------------------------------
    # properties

    @property
    def name(self) -> str:
        """Wrapped Node name."""
        return self.__wrapped__.__name__

    # /def

    @property
    def inputs(self) -> _BoundArguments:
        """:class:`~inspect.BoundArguments` from inputs Signature.

        Uses `input_defaults` and ``apply_defaults``

        """
        ba: _BoundArguments = self._inputs.bind_partial(**self.input_defaults)
        ba.apply_defaults()  # apply unset defaults from wrapped node

        return ba

    # /def

    # ------------------------------
    # call

    def __call__(self, *args: T.Any, **kwargs: T.Any) -> T.Any:
        """Call node normally. See wrapped node for whatever this does."""
        return self.__wrapped__(*args, **kwargs)

    # /def

    def run(self, signature: T.Union[_Signature, None], **kwargs: T.Any):
        """Run wrapped node as pipeline.

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
        # make function input from signature, applying `input_defaults`
        # calling self.inputs does all this
        ba: _BoundArguments = self.inputs

        # override current values from passed arguments
        allowed_keys = ba.arguments.keys()
        if signature is None:
            pass  # do not need to override anything
        else:
            # check if output hook applies to ALL outputs
            if callable(self.input_hook):
                signature = self.input_hook(signature)
            else:
                pass  # per-function basis. hook handled by the Pipeline.
                # TODO

            # assign values from signature
            # only assign if an allowed key
            for k, v in inspect.valuesdict(signature).items():
                if k in allowed_keys:
                    ba.arguments[k] = v
                else:
                    pass  # TODO optionally warn / log if not in allowed key
            # /for

        # Override values from kwargs
        # `kwargs` have highest priority, overriding defaults and sig object.
        # errors if try passing a kwarg not in signature.
        for k, v in kwargs.items():
            if k not in allowed_keys:
                raise ValueError(f"{k} not in {self.name} signature.")
            ba.arguments[k] = v
        # /for

        # Call node
        return_ = self.__call__(*ba.args, **ba.kwargs)

        # Set output signature defaults from node call
        # if only one outputs parameter, set it,
        # else, iter through output sig and node return, updating output sig
        # catches an error when node return is only one item, but there are
        # extra defaults in the output sig, so can't iterate properly.
        out = self.outputs.copy()  # copy output Signature
        if len(self.outputs.parameters) == 1:
            out = out.modify_parameter(param=0, default=return_)
        else:
            try:
                for k, v in zip(out.parameters.keys(), return_):
                    out = out.modify_parameter(param=k, default=v)
            # when have extra output arguments and return has only 1
            except TypeError:
                out = out.modify_parameter(param=0, default=return_)
        # /if

        # Optionally, keep elems from input signature not found in output
        if self.carry_through_unused:
            out_keys = out.parameters.keys()
            for k, p in signature.parameters.items():  # iter though input.
                if k not in out_keys:  # check if should add
                    out = inspect.append_parameter(out, p)
            # /for

        # check if output hook applies to ALL outputs
        if callable(self.output_hook):
            return self.output_hook(out)
        else:
            pass  # per-function basis. hook handled by the Pipeline.

        return out

    # /def

    # ------------------------------


# /class


# -------------------------------------------------------------------


pipeline_function = PipelineNode.decorator


##############################################################################
# END
