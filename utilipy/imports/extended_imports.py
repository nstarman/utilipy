#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Extending the Standard Import File
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

r"""extending the standard import file.

Routine Listings
----------------
Numpy: imports

    - linalg.norm

Scipy: imports

    - stats.binned_statistic->binned_stats

References
----------
SciPy references are [#]_ and [#]_.
NumPy references are [#]_ and [#]_.
IPython reference is [#]_.
Matplotlib reference is [#]_.

.. [#] Travis E. Oliphant. Python for Scientific Computing, Computing in
    Science and Engineering, 9, 10-20 (2007), DOI:10.1109/MCSE.2007.58
    http://scitation.aip.org/content/aip/journal/cise/9/3/10.1109/MCSE.2007.58

.. [#] K. Jarrod Millman and Michael Aivazis. Python for Scientists and
    Engineers, Computing in Science and Engineering, 13, 9-12 (2011),
    DOI:10.1109/MCSE.2011.36
    http://scitation.aip.org/content/aip/journal/cise/13/2/10.1109/MCSE.2011.36

.. [#] Travis E, Oliphant. A guide to NumPy, USA: Trelgol Publishing, (2006).

.. [#] Stéfan van der Walt, S. Chris Colbert and Gaël Varoquaux.
    The NumPy Array: A Structure for Efficient Numerical Computation,
    Computing in Science and Engineering, 13, 22-30 (2011),
    DOI:10.1109/MCSE.2011.37
    http://scitation.aip.org/content/aip/journal/cise/13/2/10.1109/MCSE.2011.37

.. [#] Fernando Pérez, Brian E. Granger, IPython: A System for Interactive
    Scientific Computing, Computing in Science and Engineering, vol. 9,
    no. 3, pp. 21-29, May/June 2007, doi:10.1109/MCSE.2007.53.
    URL: https://ipython.org

.. [#] John D. Hunter. Matplotlib: A 2D Graphics Environment, Computing in
    Science and Engineering, 9, 90-95 (2007), DOI:10.1109/MCSE.2007.55
    http://scitation.aip.org/content/aip/journal/cise/9/3/10.1109/MCSE.2007.55


"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "extended_imports_help",
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

from numpy.linalg import norm

from scipy.stats import binned_statistic as binned_stats


##############################################################################
# Printing Information


@_set_docstring_import_file_helper("extend", __doc__)  # doc from __doc__
def extended_imports_help():
    """Help for extended base imports."""
    doc = _import_file_docstring_helper(extended_imports_help.__doc__)
    print(doc)


# /def


if __config__.getboolean("verbosity", "verbose-imports"):
    extended_imports_help()


##############################################################################
# END
