# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : values
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring
"""Constants, sourced from Astropy.

References
----------
References [#]_.

.. [#] Astropy Collaboration et al., 2018, AJ, 156, 123.

"""

__author__ = "Nathaniel Starkman"
__credits__ = ["astropy"]


__all__ = [
    "values",
    "ConstantsValues",
]


###############################################################################
# IMPORTS

# GENERAL

import importlib
import warnings
from contextlib import contextmanager
from typing import Union

# astropy
import astropy
from astropy.utils import find_current_module
from astropy import constants as consts

try:
    astropy.physical_constants
except AttributeError:  # astropy version too early for physical_constants
    _codata = astropy.constants.codata2014
    _iaudata = astropy.constants.iau2015
else:
    _phys_version = astropy.physical_constants.get()
    _astro_version = astropy.astronomical_constants.get()

    _codata = importlib.import_module(".constants." + _phys_version, "astropy")
    _iaudata = importlib.import_module(
        ".constants." + _astro_version, "astropy"
    )


# PROJECT-SPECIFIC

from . import data
from ._frozen import frozen as frozenconstants

from .. import units as u
from ..config import __config__


###############################################################################
# __ALL__

__all__ += data.__all_constants__


###############################################################################
# CODE
###############################################################################


@contextmanager
def _set_enabled_constants(modname: Union[str, bool]):
    """_set_enabled_constants."""
    try:
        if isinstance(modname, bool):
            codata_context = _codata
            iaudata_context = _iaudata

        else:
            modmodule = importlib.import_module(
                ".constants." + modname, "astropy"
            )
            codata_context = modmodule.codata
            iaudata_context = modmodule.iaudata

    except ImportError as exc:
        exc.args += (
            "Context manager does not currently handle {}".format(modname),
        )
        raise

    module = find_current_module()

    # Ignore warnings about "Constant xxx already has a definition..."
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "Constant .*already has a definition"
        )
        consts.utils._set_c(
            codata_context,
            iaudata_context,
            module,
            not_in_module_only=False,
            set_class=True,
        )

    try:
        yield
    finally:
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", "Constant .*already has a definition"
            )
            consts.utils._set_c(
                _codata,
                _iaudata,
                module,
                not_in_module_only=False,
                set_class=True,
            )


# /def


###############################################################################


class ConstantsValues:
    """Constants."""

    def __setattr__(self, name, value):
        """Set Attribute and add to names."""
        super().__setattr__(name, value)
        self._names.add((name))  # add to names

        return

    # /def

    def __getitem__(self, name):
        return getattr(self, name)

    # /def

    def __init__(
        self, frozen=bool(__config__.get("util", "frozen-constants"))
    ):
        """__init__.

        Parameters
        ----------
        frozen: bool
            whether to use frozen constants

        """
        super().__setattr__("from_frozen", frozen)
        super().__setattr__("_names", set())

        # C = FrozenUnitSet()
        C = frozenconstants

        ##################################################################
        # Constants

        with _set_enabled_constants(frozen):

            for name in data.__all_constants__:
                if frozen:
                    setattr(self, name, C[name].value)
                else:
                    setattr(
                        self,
                        name,
                        getattr(consts, name).to_value(u.Unit(C[name].unit)),
                    )

            # extra
            self.c_ms: float = (C.c if frozen else consts.c).to_value("m/s")
            self.c_kms: float = (C.c if frozen else consts.c).to_value("km/s")

        # /with

        ##################################################################
        # Conversions

        with _set_enabled_constants(frozen):

            # AU / pc
            self.AU_to_pc: float = (C.au if frozen else consts.au).to_value(
                "pc"
            )
            self.pc_to_AU: float = (C.pc if frozen else consts.pc).to_value(
                "AU"
            )

        # /with

        return

    # /def


# /class


###############################################################################
# Values

# default_values = ConstantsValues()
values = ConstantsValues()

# add contents to module
for attr in values._names:
    locals()[attr] = getattr(values, attr)

__all__ += values._names


###############################################################################
# END
