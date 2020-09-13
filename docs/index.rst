#######
utilipy
#######

Welcome to ``utilipy``, a collection of useful python codes. This is a centralized repository for non project-specific code. There are modules for making advanced decorators, interfacing with IPython environments, data utilities, making fitting libraries inter-operable, and much more.

The package is being actively developed in a `public repository on GitHub <https://github.com/nstarman/utilipy>`_ so if you have any trouble, `open an issue <https://github.com/nstarman/utilipy/issues>`_ there.

.. container::

   |DOI| |PyPI| |Build Status| |Codecov| |astropy|


*************
Documentation
*************

.. toctree::
   :maxdepth: 1

   utilipy/index
   documentation/installation
   documentation/benefits
   documentation/testing
   whatsnew/1.0


***********
Subpackages
***********

.. toctree::
   :maxdepth: 1

   utilipy/data_utils/index
   utilipy/decorators/index
   utilipy/imports/index
   utilipy/ipython/index
   utilipy/math/index
   utilipy/plot/index
   utilipy/scripts/index
   utilipy/utils/index


********
Examples
********

.. toctree::
   :maxdepth: 1

   examples/datagraph.ipynb
   examples/ipython-imports.ipynb
   examples/making-decorators.ipynb


*****************
How to contribute
*****************

|Milestones| |Open Issues| |Last Commit|

We welcome contributions from anyone via pull requests on `GitHub
<https://github.com/nstarman/utilipy>`_. If you don't feel comfortable modifying or
adding functionality, we also welcome feature requests and bug reports as
`GitHub issues <https://github.com/nstarman/utilipy/issues>`_.

The development process follows that of the `astropy-package-template <https://docs.astropy.org/en/latest/development/astropy-package-template.html>`_ from Astropy's `release procedure <https://docs.astropy.org/en/latest/development/releasing.html#release-procedure>`_.


***********
Attribution
***********

|DOI| |License|

Copyright 2018- Nathaniel Starkman and contributors.

``utilipy`` is free software made available under the BSD-3 License. For details see the `LICENSE <https://github.com/nstarman/utilipy/blob/master/LICENSE>`_ file.

If you make use of this code, please consider citing the Zenodo DOI as a software citation::

   @software{utilipy:zenodo,
     author       = {nstarman},
     title        = {utilipy},
     publisher    = {Zenodo},
     doi          = {10.5281/zenodo.3491011},
     url          = {https://doi.org/10.5281/zenodo.3491011}
   }



***************
Project details
***************

.. toctree::
   :maxdepth: 1

   credits
   whatsnew/index.rst
   documentation/code_quality



.. |astropy| image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
   :target: http://www.astropy.org/

.. |Build Status| image:: https://travis-ci.com/nstarman/utilipy.svg?branch=master
    :target: https://travis-ci.com/nstarman/utilipy

.. |Documentation Status| image:: https://readthedocs.org/projects/utilipy/badge/?version=latest
   :target: https://utilipy.readthedocs.io/en/latest/?badge=latest

.. |DOI| image:: https://zenodo.org/badge/192425953.svg
   :target: https://zenodo.org/badge/latestdoi/192425953

.. |License| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

.. |PyPI| image:: https://badge.fury.io/py/utilipy.svg
   :target: https://badge.fury.io/py/utilipy

.. |Milestones| image:: https://img.shields.io/github/milestones/open/nstarman/utilipy?style=flat
   :alt: GitHub milestones

.. |Open Issues| image:: https://img.shields.io/github/issues-raw/nstarman/utilipy?style=flat
   :alt: GitHub issues

.. |Last Commit| image:: https://img.shields.io/github/last-commit/nstarman/utilipy/master?style=flat
   :alt: GitHub last commit (branch)

.. |Codecov| image:: https://codecov.io/gh/nstarman/utilipy/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/nstarman/utilipy
