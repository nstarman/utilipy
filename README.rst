AstroPHD
========

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge

Welcome to ``astroPHD``, a collection of useful python codes. This is a
centralized repository for much of the non project-specific code I have
written or come across. There are modules for making advanced
decorators, interfacing with IPython environments, miscellaneous
astronomical functions, data utilities, making fitting libraries
inter-operable, improving astropy units and quantity-enabled functions,
and much more. Check out the documentation here, on
`readthedocs <https://readthedocs.org/projects/astrophd/badge/?version=latest>`__,
and at the `wiki <https://github.com/nstarman/astroPHD/wiki>`__ for more
detail.

.. container::

   |astropy| |Build Status| |Documentation Status| |License| |Code
   style: black|

License & Attribution
---------------------

Author: **Nathaniel Starkman** - *Graduate Student @ UofT* -
`website <http://www.astro.utoronto.ca/~starkman/>`__ –
`github <https://github.com/nstarman>`__

If you find this code useful in your research, please let me know. If
you significantly use astroPHD in a publication, please acknowledge
**10.5281/zenodo.3545178** and send me a reference to the paper.

This project is Copyright (c) Nathaniel Starkman and licensed under
the terms of the BSD 3-Clause license. This package is based upon
the `Astropy package template <https://github.com/astropy/package-template>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.


Standard of Simplicity
----------------------

It is easy for a repository to become a house of cards – code building
on top of code, until the whole fragile edifice collapses with a package
dependency update. To prevent this ``astroPHD`` intends to only provide
a few common tools and have all other code, as much as possible, be
stand-alone. Code for which ``astroPHD`` makes no promise of stability
is stored in the ``community`` module. The common tools are: decorators,
associated underlying machinary for signatures and docstrings, and
Logging. The stand-alone code will use these common tools, but should
minimally interact otherwise. For instance, the ``ipython`` module will
never be imported by the ``astro`` module, and vice versa. The
``community`` packages will never be imported in any ``astroPHD``
module.

--------------

--------------

# Module Highlights Most of the modules have too much to reasonably
document here. These are some of the most useful highlights. Detailed
descriptions of everything in ``astroPHD`` and more can be found at
`readthedocs <https://readthedocs.org/projects/astrophd/badge/?version=latest>`__
and at the `wiki <https://github.com/nstarman/astroPHD/wiki>`__.

##
`astronomy <https://astrophd.readthedocs.io/en/latest/astroPHD.astronomy.html#astrophd-astronomy-package>`__
> Import using ``from  astroPHD import astronomy``

This module is very much a work in progress.

##
`community <https://astrophd.readthedocs.io/en/latest/astroPHD.community.html#astrophd-community-package>`__
> Import using ``from  astroPHD import community``

Community codes. These codes are documented elsewhere.

##
`data_utils <https://astrophd.readthedocs.io/en/latest/astroPHD.data_utils.html#astrophd-data-utils-package>`__
> Import using ``from  astroPHD import data_utils``

Data slicing and selection functions.

##
`decorators <https://astrophd.readthedocs.io/en/latest/astroPHD.decorators.html#astrophd-decorators-package>`__
> Import using ``from  astroPHD import decorators``

`Example Notebook explaining good
decorators <examples/making_decorators.ipynb>`__

##
`fitting <https://astrophd.readthedocs.io/en/latest/astroPHD.fitting.html#astrophd-fitting-package>`__
> Import using ``from  astroPHD import fitting``

##
`imports <https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astrophd-imports-package>`__
Most of my notebooks or scripts have at leas 30 lines dedicated to just
importing the various modules and functions that will be used later.
It’s cumbersome, a pain to copy between scripts, and means that the code
doesn’t start until halfway down the screen. This module provides a
variety of files that can be ``*``-imported to provide all the basic
imports so that you can just get started coding.

The provided quick imports are ``base_imports``, ``extended_imports``,
``astropy_imports``, ``matplotlib_imports``, ``galpy_imports`` and
``amuse_imports``.

The files will print an import summary. To prevent this summary, set
``verbose-imports=False`` in the ``.astroPHCrc`` config file in your
home or local directory. For details, see `config
file <#config-file>`__. Each of the imports also provides a helper
function that will print out the import summary (for instance
`base_imports_help <https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astroPHD.imports.base.base_imports_help>`__).

##
`ipython <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astrophd-ipython-package>`__
> ``from  astroPHD import ipython``

This module contains codes for interacting with IPython environments,
like Jupyter Notebooks/Lab.

``ipython`` does a few things on import:

1. imports:
   ``IPython.display display, Latex, Markdown            .core.interactiveshell: InteractiveShell                 .debugger: set_trace     astroPHD.ipython.autoreload: set_autoreload, aimport                     .imports: run_imports, import_from_file                     .notebook: add_raw_code_toggle                     .plot: configure_matplotlib                     .printing: printmd, printMD, printltx, printLaTeX``

2. makes all non-suppressed lines automatically display By setting
   ``IPython.InteractiveShell.ast_node_interactivity='all'``. Suppressed
   lines are lines like ``> x = func()`` or ending with ``;``. Displayed
   lines are just like ``x``, where ‘x’ is an existing variable.

3. configures matplotlib to use the ‘inline’ & ‘retina’ backends

###
`autoreload <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#module-astroPHD.ipython.autoreload>`__
> ``from  astroPHD.ipython import autoreload``

This module deals with auto-reloading packages / modules / functions in
IPython. With IPython auto-reload, specified (or all) packages will be
auto-reloaded to check for code changes. While this slows down code
execution, it is enormously useful for real-time code development and
testing.

The principal functions are:

-  ```.set_autoreload`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.autoreload.set_autoreload>`__:
   to set the auto-reload state for packages

-  ```.aimport`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.autoreload.aimport>`__:
   import with or without auto-reload

###
`imports <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#module-astroPHD.ipython.imports>`__
> ``from  astroPHD.ipython import imports``

This module is an easy interface for importing the
`imports <#imports>`__ files as well as any custom imports files. Rather
than \*-importing, all imports are routed through ipython magic
commands.

The principal function is:

-  ```run_imports`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.run_imports>`__:
   import file using ipython magic. supports custom imports files and
   also provides key-word arguments to import any of the files in
   `imports <#imports>`__.

   As example:

   .. code:: python

      from astroPHD import ipython
      ipython.run_imports(base=True)

   Imports and prints the summary (abridged) \``\` Returns ——- Base:
   imports

   ::

            * os, sys, time, pdb, warnings,
            * numpy -> np, scipy,
            * tqdm -> TQDM, .tqdm, .tqdm_notebook ->. tqdmn

        ...

   \``\`

The supporting functions are:
```import_from_file`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_from_file>`__,
```aimport`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.autoreload.aimport>`__,
```set_autoreload`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.autoreload.set_autoreload>`__,
```import_base`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_base>`__,
```import_extended`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_extended>`__,
```import_astropy`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_astropy>`__,
```import_matplotlib`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_matplotlib>`__,
```import_galpy`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_galpy>`__,
```import_amuse`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_amuse>`__

###
`notebook <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.notebook>`__
> ``from  astroPHD.ipython import notebook``

Currently this only has the function
```add_raw_code_toggle`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.notebook.add_raw_code_toggle>`__,
which adds a button toggle to hide/show code cells in an HTML export of
a Jupyter notebook.

###
`plot <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.plot>`__

functions to configure IPython environments for improved plotting.

Currently this only has the function
```configure_matplotlib`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.plot.configure_matplotlib>`__,
which sets Matplotlib Jupyter backend, inline plotting, etc.

###
`printing <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.printing>`__
Functions for enhanced printing in an IPython environment.

In addition to importing the standard ``display``, ``Latex``,
``Markdown``, ``HTML``

The principal functions are:

-  ```printmd`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.printing.printmd>`__:
   print in Markdown. set the text color, size, weight, style,
   highlight, etc.

-  ```printltx`` <https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.printing.printltx>`__
   rapidly make latex math, matrices, etc.

##
`math <https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astrophd-imports-package>`__
> Import using ``from  astroPHD import math``

A work in progress.

The principal functions are:

-  `quadrature <https://astrophd.readthedocs.io/en/latest/astroPHD.math.html#astroPHD.math.math.quadrature>`__

-  `logsumexp <https://astrophd.readthedocs.io/en/latest/astroPHD.math.html#astroPHD.math.math.quadrature>`__

##
`plot <https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astrophd-imports-package>`__
> Import using ``from  astroPHD import plot``

connects to ``astroPHD.community.starkplot``

##
`units <https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astrophd-imports-package>`__
> Import using ``from  astroPHD import units``

##
`util <https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astrophd-imports-package>`__
> Import using ``from  astroPHD import util``

###
`config <https://astrophd.readthedocs.io/en/latest/astroPHD.util.html#module-astroPHD.util.config>`__

###
`Logging <https://astrophd.readthedocs.io/en/latest/astroPHD.util.logging.html#astrophd-util-logging-package>`__

###
`inspect <https://astrophd.readthedocs.io/en/latest/astroPHD.util.inspect.html#astrophd-util-inspect-package>`__

###
`functools <https://astrophd.readthedocs.io/en/latest/astroPHD.util.html#module-astroPHD.util.functools>`__

###
`pickle <https://astrophd.readthedocs.io/en/latest/astroPHD.util.html#module-astroPHD.util.pickle>`__

--------------

--------------

# Templates Templates are useful. Here are some.

## About Text . `About.txt <templates/ABOUT/ABOUT.txt>`__ : an about
text in basic ``.txt`` format . `About.md <templates/ABOUT/ABOUT.md>`__
: an about text in Markdown

## Python

. `\__init_\_ <templates/python/__init__.py>`__ .
`python.py <templates/python/python.py>`__ .
`notebook.ipynb <templates/python/notebook.ipynb>`__

## Latex

. `tex file <templates/latex/main.tex>`__ . `bibtex
file <templates/latex/main.bib>`__

**Stylesheets:** . `main stylesheet <templates/latex/util/main.cls>`__ .
`astronomy stylesheet <templates/latex/util/astronomy.cls>`__ . `maths
stylesheet <templates/latex/util/maths.cls>`__ . `base
stylesheet <templates/latex/util/base.cls>`__

.. |astropy| image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
   :target: http://www.astropy.org/
.. |Build Status| image:: https://travis-ci.org/nstarman/astroPHD.svg?branch=master
   :target: https://travis-ci.org/nstarman/astroPHD
.. |Documentation Status| image:: https://readthedocs.org/projects/astrophd/badge/?version=latest
   :target: https://astrophd.readthedocs.io/en/latest/?badge=latest
.. |License| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3545178.svg
   :target: https://doi.org/10.5281/zenodo.3545178
