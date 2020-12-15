# -*- coding: utf-8 -*-

"""Test contents of :mod:`~utilipy.data_utils.fitting.lmfit_utils`."""


__all__ = [
    # functions
    "test_scipy_residual_to_lmfit_raises",
    "test_scipy_residual",
    "test_lmfit_residual",
]


##############################################################################
# IMPORTS

# THIRD PARTY
import numpy as np
import pytest

# PROJECT-SPECIFIC
from utilipy.data_utils.fitting.lmfit_utils import scipy_residual_to_lmfit

##############################################################################
# PARAMETERS


##############################################################################
# CODE
##############################################################################


def _model(x, amp, phaseshift, freq, decay):
    return amp * np.sin(x * freq + phaseshift) * np.exp(-(x ** 2) * decay)


# /def


@scipy_residual_to_lmfit.decorator(
    param_order=["amp", "phaseshift", "freq", "decay"]
)
def _residual(variables, x, data, eps_data):
    """Model a decaying sine wave and subtract data."""
    amp = variables[0]
    phaseshift = variables[1]
    freq = variables[2]
    decay = variables[3]

    model = _model(x, amp=amp, freq=freq, phaseshift=phaseshift, decay=decay)

    return (data - model) / eps_data


# /def

# -------------------------------------------------------------------


def test_scipy_residual_to_lmfit_raises():
    """Test Exceptions `~utilipy.data_utils.fitting.scipy_residual_to_lmfit`."""
    with pytest.raises(ValueError):
        scipy_residual_to_lmfit(param_order=None)


# /def

# -------------------------------------------------------------------


def test_scipy_residual():
    """"""
    x = np.arange(0, 10)
    variables = [1, 2, 3, 4]  # amp, phaseshift, freq, decay

    data = _model(x, *variables)
    eps_data = 1.0

    assert all(_residual(variables, x=x, data=data, eps_data=eps_data) == 0.0)


# /def

# -------------------------------------------------------------------


def test_lmfit_residual():
    """"""
    x = np.arange(0, 10)

    class _ParameterProxy:
        def __init__(self, name, value):
            self.name = name
            self.value = value

    class _ParametersProxy(dict):
        def __init__(self, *params):
            for p in params:
                self[p.name] = p

        def add_many(self, params_list):
            for (n, v) in params_list:
                self[n] = _ParameterProxy(n, v)

        def valuesdict(self):
            return {n: p.value for n, p in self.items()}

    params = _ParametersProxy()
    params.add_many([("amp", 1), ("phaseshift", 2), ("freq", 3), ("decay", 4)])

    data = _model(x, **params.valuesdict())
    eps_data = 1.0

    assert all(
        _residual.lmfit(params, x=x, data=data, eps_data=eps_data) == 0.0
    )


# /def


##############################################################################
# END
