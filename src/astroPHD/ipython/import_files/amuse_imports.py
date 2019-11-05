# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : amuse_imports
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Base set of imports for the AMUSE code.

Returns
-------
amuse
amuse.lab,
     .units.units, constants
     .couple.bridge


References
----------
AMUSE citatations: [1]_, [2]_, [3]_, [4]_
Additionally, please cite all the codes you used (AMUSE will show you which
papers to cite for these), and the version of AMUSE you were using:
https://doi.org/10.5281/zenodo.3260650

.. [1] Portegies Zwart, S. & McMillan, S.L.W., 2018, “Astrophysical Recipes:
    the art of AMUSE”, AAS IOP Astronomy publishing (411 pages)
.. [2] Portegies Zwart, S. et al., 2013, Multi-physics Simulations Using a
    Hierarchical Interchangeable Software Interface, Computer Physics
    Communications 183, 456-468 [2013CoPhC.183..456P]
.. [3] Pelupessy, F. I. et al., 2013, The Astrophysical Multipurpose Software
    Environment, Astronomy and Astrophysics 557, 84 [2013A&A…557A..84P]
.. [4] Portegies Zwart, S. et al., 2009, A multiphysics and multiscale
    software environment for modeling astrophysical systems, New Astronomy,
    Volume 14, Issue 4, 369-378 [2009NewA…14..369P]

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# HELPER FUNCTIONS

from astroPHD.util.config import __config__
from astroPHD.util.decorators.docstring import (
    _set_docstring_import_file_helper,
    _import_file_docstring_helper
)



##############################################################################
# IMPORTS

if __name__ == '__main__':

    import amuse

    # lab
    from amuse import lab
    from amuse.units import units, constants
    from amuse.couple import bridge

# /if

##############################################################################
# Printing Information

@_set_docstring_import_file_helper('extend', __doc__)  # doc from __doc__
def extend_imports_help():
    """Help for extended base imports."""
    _import_file_docstring_helper(extend_imports_help.__doc__)  # formatting
# /def


if __config__.getboolean('verbosity', 'verbose-imports'):
    extend_imports_help()

##############################################################################
# END
