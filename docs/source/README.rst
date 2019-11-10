AstroPHD
========

Welcome to ``astroPHD``, a collection of useful python codes.

Attribution
-----------

Author: **Nathaniel Starkman** - *Graduate Student @ UofT* -
`website <http://www.astro.utoronto.ca/~starkman/>`__ --
`github <https://github.com/nstarman>`__

|DOI| |Build Status|

Table of Contents
-----------------

.. raw:: html

   <!-- MarkdownTOC levels="1,2" autolink="true" -->

-  `Modules <#modules>`__

   -  `astronomy <#astronomy>`__
   -  `data\_utils <#data_utils>`__
   -  `fitting <#fitting>`__
   -  `imports <#imports>`__
   -  `ipython <#ipython>`__
   -  `math <#math>`__
   -  `plot <#plot>`__
   -  `units <#units>`__
   -  `util <#util>`__

-  `Templates <#templates>`__

   -  `About Text <#about-text>`__
   -  `Python <#python>`__
   -  `Latex <#latex>`__

.. raw:: html

   <!-- /MarkdownTOC -->

 - - - - - -

 # Modules

 ## astronomy > Import using ``from  astroPHD import astronomy``

 ## data\_utils > Import using ``from  astroPHD import data_utils``

 ## fitting > Import using ``from  astroPHD import fitting``

 ## imports > Import using ``from  astroPHD import imports``

 ## ipython > ``from  astroPHD import ipython``

This module contains codes for interacting with ipython environments,
like Jupyter Notebooks/Lab.

``ipython`` does a few things on import:

1. imports:
   ``IPython.display display, Latex, Markdown            .core.interactiveshell: InteractiveShell                 .debugger: set_trace     astroPHD.ipython.autoreload: set_autoreload, aimport                     .imports: run_imports, import_from_file                     .notebook: add_raw_code_toggle                     .plot: configure_matplotlib                     .printing: printmd, printMD, printltx, printLaTeX``
2. makes all non-suppressed lines automatically display By setting
   ``IPython.InteractiveShell.ast_node_interactivity='all'``. Suppressed
   lines are lines like ``> x = func()`` or ending with ``;``. Displayed
   lines are just like ``x``, where 'x' is an existing variable.

3. configures matplotlib to use the 'inline' & 'retina' backends

 ### autoreload, > ``from  astroPHD.ipython import autoreload``

This module deals with auto-reloading packages / modules / functions in
IPython. With IPython auto-reload, specified (or all) packages will be
auto-reloaded to check for code changes. While this slows down code
execution, it is enormously useful for real-time code development and
testing.

-  ``.set_autoreload``: set the auto-reload state for packages >
   signature :: reload\_type: int

   reload\_type: IPython reload state

   -  0: nothing auto-reloads
   -  1: things imported with ``.aimport`` will auto-reload
   -  2: all imports will auto-reload

-  ``.aimport``: import with auto-reload > signature :: \*modules:
   \*str, autoreload: (bool, list, tuple)= True

   -  | \*modules: string(s) for the module to import
      |  ``python     'matplotlib.pyplot'``

      cannot (yet) do 'from matplotlib import pyplot'

   -  autoreload: whether to override autoreload global state for this
      import. Can be a single boolean for all '\*modules', or a list of
      booleans for each 'module'.
      ``python       set_autoreload(2)  # everything autoreloads       aimport('matplotlib.pyplot', 'scipy.special',              autoreload=[True,  # matplotlib will autroreload                         False])  # scipy will not, even though set_autoreload=2``

 ### imports > ``from  astroPHD.ipython import imports``

 ### notebook > ``from  astroPHD.ipython import imports``

 ### plot

 ### printing

 ## math > Import using ``from  astroPHD import math``

 ## plot > Import using ``from  astroPHD import plot``

 ## units > Import using ``from  astroPHD import units``

 ## util > Import using ``from  astroPHD import util``

 - - - - - -

 # Templates Templates are useful. Here are some.

 ## About Text . `About.txt <templates/ABOUT/ABOUT.txt>`__ : an about
text in basic ``.txt`` format . `About.md <templates/ABOUT/ABOUT.md>`__
: an about text in Markdown

 ## Python

. `\_\_init\_\_ <templates/python/__init__.py>`__ .
`python.py <templates/python/python.py>`__ .
`notebook.ipynb <templates/python/notebook.ipynb>`__

 ## Latex

. `tex file <templates/latex/main.tex>`__ . `bibtex
file <templates/latex/main.bib>`__

**Stylesheets:** . `main stylesheet <templates/latex/util/main.cls>`__ .
`astronomy stylesheet <templates/latex/util/astronomy.cls>`__ . `maths
stylesheet <templates/latex/util/maths.cls>`__ . `base
stylesheet <templates/latex/util/base.cls>`__

.. |DOI| image:: https://zenodo.org/badge/192425953.svg
   :target: https://zenodo.org/badge/latestdoi/192425953
.. |Build Status| image:: https://travis-ci.org/nstarman/astroPHD.svg?branch=master
   :target: https://travis-ci.org/nstarman/astroPHD
