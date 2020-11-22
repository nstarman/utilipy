# -*- coding: utf-8 -*-

"""`lmfit <https://lmfit.github.io/lmfit-py/index.html>`_ Interface Utilities.

In particular, the `scipy_residual_to_lmfit` makes
`scipy <https://docs.scipy.org/doc/scipy/reference/optimize.html>`_ residuals
compatible with lmfit
`minimize <https://github.com/lmfit/lmfit-py/blob/master/lmfit/minimizer.py>`_.

"""


##############################################################################
# IMPORTS

# BUILT-IN
import typing as T

# THIRD PARTY
import numpy as np
from wrapt import ObjectProxy

try:
    import lmfit
except ImportError:
    HAS_LMFIT = False
else:
    HAS_LMFIT = True

##############################################################################
# PARAMETERS

if HAS_LMFIT:
    ParametersType = T.TypeVar("ParametersType", bound=lmfit.Parameters)
else:
    ParametersType = T.Any

##############################################################################
# CODE


class scipy_residual_to_lmfit(ObjectProxy):
    """Decorator to make scipy residual functions compatible with lmfit.

    (see https://lmfit.github.io/lmfit-py/fitting.html)

    Parameters
    ----------
    param_order : list of strs
        the variable order used by lmfit
        the strings are the names of the lmfit parameters
        must be in the same order as the scipy residual function

    Returns
    -------
    scipy_residual_to_lmfit : class
        internally constructed class

    Notes
    -----
    the function can be called as normal
    add a .lmfit function for use in lmfit minimizations
    see https://lmfit.github.io/lmfit-py/fitting.html

    >>> @scipy_residual_to_lmfit(param_order=['amp', 'phase', 'freq', 'decay'])
    ... def residual(variables, x, data, eps_data):
    ...     amp, phase, freq, decay = variables
    ...     # calculate residual here
    ...     return res

    .. todo::

        since using ObjectProxy, make it compatible with bound functions
        see https://wrapt.readthedocs.io/en/latest/wrappers.html

    """

    def __new__(
        cls,
        func: T.Callable = None,
        param_order: T.Optional[T.Sequence] = None,
    ):
        """Create Proxy."""
        if param_order is None:
            raise ValueError("param_order cannot be None")

        self = super().__new__(cls)  # inherit class information

        # assigning documentation as function documentation
        self.__doc__ = func.__doc__

        # allowing scipy_residual_to_lmfit to act as a decorator
        if func is None:
            return self.decorator(param_order)
        return self

    # /def

    @classmethod
    def decorator(cls, param_order: T.Sequence) -> T.Callable:
        """Decorator."""
        # @functools.wraps(cls)  # not needed when using ObjectProxy
        def wrapper(func: T.Callable) -> T.Callable:
            """scipy_residual_to_lmfit wrapper."""
            return cls(func, param_order=param_order)

        # /def
        return wrapper

    # /def

    def __init__(self, func: T.Callable, param_order: T.Sequence):
        """Initialize Proxy."""
        super().__init__(func)  # initializing function into ObjectProxy
        self.param_order = param_order
        return

    # /def

    def lmfit(
        self, params: ParametersType, *args: T.Any, **kwargs: T.Any
    ) -> T.Sequence:
        """`lmfit` version of function."""
        variables = [params[n].value for n in self.param_order]
        return self.__wrapped__(variables, *args, **kwargs)

    # /def

    def __call__(self, *args: T.Any, **kwargs: T.Any) -> T.Sequence:
        """Call scipy residual.

        Parameters
        ----------
        *args : Any
            Arguments into ``__wrapped__``, the residual function.
        **kwargs : Any
            Keyword arguments into ``__wrapped__``, the residual function.

        Returns
        -------
        return_ : Any
            Returns from called ``__wrapped__``.

        """
        return self.__wrapped__(*args, **kwargs)

    # /def


# /class


##############################################################################


def report_mcmc_fit(mcmc_res):
    """Report output of MCMC fit.

    Code from https://lmfit.github.io/lmfit-py/fitting.html

    """
    # -----------------------
    # Median of distribution

    print("median of posterior probability distribution")
    print("--------------------------------------------")
    lmfit.report_fit(mcmc_res.params)

    p = mcmc_res.params.copy()

    highest_prob = np.argmax(mcmc_res.lnprob)
    hp_loc = np.unravel_index(highest_prob, mcmc_res.lnprob.shape)
    mle_soln = mcmc_res.chain[hp_loc]
    for i, par in enumerate(p):
        p[par].value = mle_soln[i]

    # -----------------------
    # Max Likelihood

    print("\nMaximum Likelihood Estimation from emcee       ")
    print("-------------------------------------------------")
    print("Parameter  MLE Value   Median Value   Uncertainty")

    fmt = "  {:5s}  {:11.5f} {:11.5f}   {:11.5f}".format
    for name, param in p.items():
        print(
            fmt(
                name,
                param.value,
                mcmc_res.params[name].value,
                mcmc_res.params[name].stderr,
            )
        )

    # -----------------------
    # Error Estimate

    print("\nError Estimates from emcee    ")
    print("------------------------------------------------------")
    print("Parameter  -2sigma  -1sigma   median  +1sigma  +2sigma ")

    for name in p.keys():
        quantiles = np.percentile(
            mcmc_res.flatchain[name], [2.275, 15.865, 50, 84.135, 97.275]
        )
        median = quantiles[2]
        err_m2 = quantiles[0] - median
        err_m1 = quantiles[1] - median
        err_p1 = quantiles[3] - median
        err_p2 = quantiles[4] - median
        fmt = "  {:5s}   {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f}".format
        print(fmt(name, err_m2, err_m1, median, err_p1, err_p2))

    # /for

    return


# /def


##############################################################################
# END
