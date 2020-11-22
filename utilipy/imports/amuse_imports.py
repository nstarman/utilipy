# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : AMUSE imports
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Base set of imports for :mod:`~amuse`.

Routine Listings
----------------
Amuse: imports

    - amuse
    - amuse.lab
    - amuse.units.units, constants
    - amuse.couple.bridge

Notes
-----
If you are using this import, please cite all the references from the codes
you used (AMUSE will show you which papers to cite for these),
and the version of AMUSE you were using
(https://doi.org/10.5281/zenodo.3260650)

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3260650.svg
   :target: https://doi.org/10.5281/zenodo.3260650


References
----------
AMUSE citations [#]_, [#]_, [#]_, [#]_

.. [#] Portegies Zwart, S. and McMillan, S.L.W., 2018, “Astrophysical Recipes:
   the art of AMUSE", AAS IOP Astronomy publishing (411 pages).

.. [#] Portegies Zwart, S. et al., 2013, "Multi-physics Simulations Using a
   Hierarchical Interchangeable Software Interface", Computer Physics
   Communications 183, 456-468 (2013CoPhC.183..456P).

.. [#] Pelupessy, F. I. et al., 2013, "The Astrophysical Multipurpose Software
   Environment", Astronomy and Astrophysics 557, 84 (2013AandA…557A..84P).

.. [#] Portegies Zwart, S. et al., 2009, "A multiphysics and multiscale
   software environment for modeling astrophysical systems", New Astronomy,
   Volume 14, Issue 4, 369-378 (2009NewA…14..369P).

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "amuse_imports_help",
]


##############################################################################
# HELPER FUNCTIONS

# PROJECT-SPECIFIC
from utilipy.imports import conf
from utilipy.utils import make_help_function

##############################################################################
# IMPORTS

try:

    import amuse

except ImportError:

    import warnings

    warnings.warn("Cannot import amuse")

else:

    from amuse import lab
    from amuse.units import units, constants
    from amuse.couple import bridge

    __all__ += [
        "amuse",
        "lab",
        "units",
        "constants",
        "bridge",
    ]

# /if

##############################################################################
# Printing Information

amuse_imports_help = make_help_function(
    "amuse", __doc__, look_for="Routine Listings"
)


if conf.verbose_imports:
    amuse_imports_help()


##############################################################################
# END
