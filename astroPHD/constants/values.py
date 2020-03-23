# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : values
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring
"""Constants, sourced from Astropy.

References
----------
References [#]_.

.. [#] Astropy Collaboration et al., 2018, AJ, 156, 123.


TODO
----
generate summary like from astropy.units.utils.generate_unit_summary

"""

__author__ = "Nathaniel Starkman"
__credits__ = ["astropy"]

__all_constants__ = (
    "AU_to_pc",
    "G",
    "GM_earth",
    "GM_jup",
    "GM_sun",
    "L_bol0",
    "L_sun",
    "M_earth",
    "M_jup",
    "M_sun",
    "N_A",
    "R",
    "R_earth",
    "R_jup",
    "R_sun",
    "Ryd",
    "_G",
    "_GM_earth",
    "_GM_jup",
    "_GM_sun",
    "_L_bol0",
    "_L_sun",
    "_M_earth",
    "_M_jup",
    "_M_sun",
    "_N_A",
    "_R",
    "_R_earth",
    "_R_jup",
    "_R_sun",
    "_Ryd",
    "_a0",
    "_alpha",
    "_atm",
    "_au",
    "_c",
    "_e",
    "_eps0",
    "_g0",
    "_h",
    "_hbar",
    "_k_B",
    "_kpc",
    "_m_e",
    "_m_n",
    "_m_p",
    "_mu0",
    "_muB",
    "_pc",
    "_sigma_T",
    "_sigma_sb",
    "_u",
    "a0",
    "alpha",
    "atm",
    "au",
    "b_wien",
    "c",
    "c_kms",
    "c_ms",
    "e",
    "eps0",
    "g0",
    "h",
    "hbar",
    "k_B",
    "kpc",
    "m_e",
    "m_n",
    "m_p",
    "mu0",
    "muB",
    "pc",
    "pc_to_AU",
    "sigma_T",
    "sigma_sb",
    "u",
)

__all__ = [
    # "values",
    "default_values",
    "_set_enabled_constants",
    "ConstantsValues",
] + list(__all_constants__)


###############################################################################
# IMPORTS

# GENERAL
import importlib
import warnings
from contextlib import contextmanager
from typing import Union
import astropy
from astropy.utils import find_current_module
from astropy import constants as _c
from astropy.constants import utils as _utils

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
from .. import units as u
from ..config import __config__


###############################################################################
# FUNCITONS


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
        _c.utils._set_c(
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
            _c.utils._set_c(
                _codata,
                _iaudata,
                module,
                not_in_module_only=False,
                set_class=True,
            )


# /def


###############################################################################
# Values


class ConstantsValues:
    """Constants."""

    def __setattr__(self, name, value):
        """Attributes are locked."""
        if name in __all_constants__:
            super().__setattr__(name, value)
        return

    # /def

    def __init__(self, frozen=__config__.get("util", "frozen-constants")):
        """__init__."""
        # frozen
        F = bool(frozen) if frozen.lower() in ("true", "false") else False
        frozen = (
            bool(frozen) if frozen.lower() in ("true", "false") else frozen
        )

        #######################################################################
        # Constants

        with _set_enabled_constants(frozen):

            # G
            self._G = _c.G
            self.G: float = 6.67408e-11 if F else _c.G.value
            # self.G: float = 6.67408e-11 if F else _c.G.to_value('m3 / kg / s2')

            # N_A
            self._N_A: u.Quantity = _c.N_A
            self.N_A: float = 6.02214086e23 if F else _c.N_A.value

            # R
            self._R: u.Quantity = _c.R
            self.R: float = 8.3144598 if F else _c.R.value

            # Ryd
            self._Ryd: u.Quantity = _c.Ryd
            self.Ryd: float = 10973731.6 if F else _c.Ryd.value

            # a0
            self._a0: u.Quantity = _c.a0
            self.a0: float = 5.29177211e-11 if F else _c.a0.value

            # alpha
            self._alpha: u.Quantity = _c.alpha
            self.alpha: float = 0.00729735257 if F else _c.alpha.value

            # atm
            self._atm: u.Quantity = _c.atm
            self.atm: float = 101325

            # b_wien
            self.b_wien = 0.0028977729 if F else _c.b_wien.value

            # speed of light
            self._c: u.Quantity = _c.c
            self.c: float = 299792458.0 if F else _c._c.value
            self.c_ms: float = 299792458.0 if F else _c._c.to_value("m/s")
            self.c_kms: float = 299792.4580 if F else _c._c.to_value("km/s")

            # e
            self._e: u.Quantity = _c.e
            self.e: float = 1.60217662e-19 if F else _c.e.value

            # eps0
            self._eps0: u.Quantity = _c.eps0
            self.eps0: float = 8.85418782e-12 if F else _c.eps0.value

            # g0
            self._g0: u.Quantity = _c.g0
            self.g0: float = 9.80665 if F else _c.g0.value

            # h
            self._h: u.Quantity = _c.h
            self.h: float = 6.62607004e-34 if F else _c.h.value

            # hbar
            self._hbar: u.Quantity = _c.hbar
            self.hbar: float = 1.0545718e-34 if F else _c.hbar.value

            # k_B
            self._k_B: u.Quantity = _c.k_B
            self.k_B: float = 1.38064852e-23 if F else _c.k_B.value

            # m_e
            self._m_e: u.Quantity = _c.m_e
            self.m_e: float = 9.10938356e-31 if F else _c.m_e.value

            # m_n
            self._m_n: u.Quantity = _c.m_n
            self.m_n: float = 1.67492747e-27 if F else _c.m_n.value

            # m_p
            self._m_p: u.Quantity = _c.m_p
            self.m_p: float = 1.6726219e-27 if F else _c.m_p.value

            # mu0
            self._mu0: u.Quantity = _c.mu0
            self.mu0: float = 1.25663706e-06 if F else _c.mu0.value

            # muB
            self._muB: u.Quantity = _c.muB
            self.muB: float = 9.27400999e-24 if F else _c.muB.value

            # sigma_T
            self._sigma_T: u.Quantity = _c.sigma_T
            self.sigma_T: float = 6.65245872e-29 if F else _c.sigma_T.value

            # sigma_sb
            self._sigma_sb: u.Quantity = _c.sigma_sb
            self.sigma_sb: float = 5.670367e-08 if F else _c.sigma_sb.value

            # u
            self._u: u.Quantity = _c.u
            self.u: float = 1.66053904e-27 if F else _c.u.value

            # GM_earth
            self._GM_earth: u.Quantity = _c.GM_earth
            self.GM_earth: float = 3.986004e14 if F else _c.GM_earth.value

            # GM_jup
            self._GM_jup: u.Quantity = _c.GM_jup
            self.GM_jup: float = 1.2668653e17 if F else _c.GM_jup.value

            # GM_sun
            self._GM_sun: u.Quantity = _c.GM_sun
            self.GM_sun: float = 1.3271244e20 if F else _c.GM_sun.value

            # L_bol0
            self._L_bol0: u.Quantity = _c.L_bol0
            self.L_bol0: float = 3.0128e28 if F else _c.L_bol0.value

            # L_sun
            self._L_sun: u.Quantity = _c.L_sun
            self.L_sun: float = 3.828e26 if F else _c.L_sun.value

            # M_earth
            self._M_earth: u.Quantity = _c.M_earth
            self.M_earth: float = 5.97236473e24 if F else _c.M_earth.value

            # M_jup
            self._M_jup: u.Quantity = _c.M_jup
            self.M_jup: float = 1.89818717e27 if F else _c.M_jup.value

            # M_sun
            self._M_sun: u.Quantity = _c.M_sun
            self.M_sun: float = 1.98847542e30 if F else _c.M_sun.value

            # R_earth
            self._R_earth: u.Quantity = _c.R_earth
            self.R_earth: float = 6378100 if F else _c.R_earth.value

            # R_jup
            self._R_jup: u.Quantity = _c.R_jup
            self.R_jup: float = 71492000 if F else _c.R_jup.value

            # R_sun
            self._R_sun: u.Quantity = _c.R_sun
            self.R_sun: float = 695700000 if F else _c.R_sun.value

            # au
            self._au: u.Quantity = _c.au
            self.au: float = 1.49597871e11 if F else _c.au.value

            # kpc
            self._kpc: u.Quantity = _c.kpc
            self.kpc: float = 3.08567758e19 if F else _c.kpc.value

            # pc
            self._pc: u.Quantity = _c.pc
            self.pc: float = 3.08567758e16 if F else _c.pc.value

        # /with

        #######################################################################
        # Conversions

        with _set_enabled_constants(frozen):

            # AU / pc
            self.AU_to_pc: float = 4.848136811133344e-06 if F else _c.au.to_value(
                "pc"
            )
            self.pc_to_AU: float = 206264.80624548031 if F else _c.pc.to_value(
                "AU"
            )

        # /with

        return

    # /def


# /class


###############################################################################
# Values


default_values = ConstantsValues()

# add contents to module
for attr in __all_constants__:
    locals()[attr] = getattr(default_values, attr)


###############################################################################
# END
