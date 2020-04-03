# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : AMUSE imports
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""Base set of imports for the AMUSE code.

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

from utilipy.config import __config__
from utilipy.decorators.docstring import (
    _set_docstring_import_file_helper,
    _import_file_docstring_helper,
)


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


@_set_docstring_import_file_helper("amuse", __doc__)  # doc from __doc__
def amuse_imports_help():
    """Help for amuse base imports."""
    doc = _import_file_docstring_helper(amuse_imports_help.__doc__)
    print(doc)


# /def


if __config__.getboolean("verbosity", "verbose-imports"):
    amuse_imports_help()

##############################################################################
# END
