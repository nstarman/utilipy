# AstroPHD

Welcome to 	`astroPHD`, a collection of useful python codes. This is a centralized repository for much of the non project-specific code I have written or come across. There are modules for making advanced decorators, interfacing with IPython environments, miscellaneous astronomical functions, data utilities, making fitting libraries inter-operable, improving astropy units and quantity-enabled functions, and much more. Check out the documentation here, on [readthedocs](https://readthedocs.org/projects/astrophd/badge/?version=latest), and at the [wiki](https://github.com/nstarman/astroPHD/wiki) for more detail.


[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)
[![Build Status](https://travis-ci.org/nstarman/astroPHD.svg?branch=master)](https://travis-ci.org/nstarman/astroPHD)
[![Documentation Status](https://readthedocs.org/projects/astrophd/badge/?version=latest)](https://astrophd.readthedocs.io/en/latest/?badge=latest)

## Attribution

Author: **Nathaniel Starkman** - *Graduate Student @ UofT* - [website](http://www.astro.utoronto.ca/~starkman/) -- [github](https://github.com/nstarman)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3545178.svg)](https://doi.org/10.5281/zenodo.3545178)

If you find this code useful in your research, please let me know. If you significantly use astroPHD in a publication, please acknowledge **10.5281/zenodo.3545178**. Please also send me a reference to the paper.



##  Table of Contents
<!-- MarkdownTOC levels="1,2,3" autolink="true" style="unordered" -->

- [Module Highlights](#module-highlights)
    - [astronomy](#astronomy)
    - [community](#community)
    - [data_utils](#data_utils)
    - [decorators](#decorators)
    - [fitting](#fitting)
    - [imports](#imports)
    - [ipython](#ipython)
        - [autoreload](#autoreload)
        - [imports](#imports-1)
        - [notebook](#notebook)
        - [plot](#plot)
        - [printing](#printing)
    - [math](#math)
    - [plot](#plot-1)
    - [units](#units)
    - [util](#util)
        - [config](#config)
        - [Logging](#logging)
        - [inspect](#inspect)
        - [functools](#functools)
        - [pickle](#pickle)
- [Templates](#templates)
    - [About Text](#about-text)
    - [Python](#python)
    - [Latex](#latex)

<!-- /MarkdownTOC -->


<br><br>

- - -
- - -

<br><br>

<a id="module-highlights"></a>
# Module Highlights
Most of the modules have too much to reasonably document here. These are some of the most useful highlights. Detailed descriptions of everything in `astroPHD` and more can be found at [readthedocs](https://readthedocs.org/projects/astrophd/badge/?version=latest) and at the [wiki](https://github.com/nstarman/astroPHD/wiki).

<a id="astronomy"></a>
## [astronomy](https://astrophd.readthedocs.io/en/latest/astroPHD.astronomy.html#astrophd-astronomy-package)
> Import using `from  astroPHD import astronomy`

This module is very much a work in progress.

<a id="community"></a>
## [community](https://astrophd.readthedocs.io/en/latest/astroPHD.community.html#astrophd-community-package)
> Import using `from  astroPHD import community`

Community codes. These codes are documented elsewhere.

<a id="data_utils"></a>
## [data_utils](https://astrophd.readthedocs.io/en/latest/astroPHD.data_utils.html#astrophd-data-utils-package)
> Import using `from  astroPHD import data_utils`

Data slicing and selection functions.

<a id="decorators"></a>
## [decorators](https://astrophd.readthedocs.io/en/latest/astroPHD.decorators.html#astrophd-decorators-package)
> Import using `from  astroPHD import decorators`


[Example Notebook explaining good decorators](examples/making_decorators.ipynb)

<a id="fitting"></a>
## [fitting](https://astrophd.readthedocs.io/en/latest/astroPHD.fitting.html#astrophd-fitting-package)
> Import using `from  astroPHD import fitting`


<a id="imports"></a>
## [imports](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astrophd-imports-package)
Most of my notebooks or scripts have at leas 30 lines dedicated to just importing the various modules and functions that will be used later. It's cumbersome, a pain to copy between scripts, and means that the code doesn't start until halfway down the screen. This module provides a variety of files that can be `*`-imported to provide all the basic imports so that you can just get started coding.

The provided quick imports are `base`, `extended`, `astropy`, `matplotlib`, `galpy` and `amuse`.

The files will print an import summary. To prevent this summary, set  `verbose-imports=False` in the `.astroPHCrc` config file in your home or local directory. For details, see [config file](#config-file). Each of the imports also provides a helper function that will print out  the import summary (for instance [base_imports_help](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astroPHD.imports.base.base_imports_help)).


<a id="ipython"></a>
## [ipython](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astrophd-ipython-package)
> `from  astroPHD import ipython`

This module contains codes for interacting with IPython environments, like Jupyter Notebooks/Lab.

`ipython` does a few things on import:

1. imports:
    ```
    IPython.display display, Latex, Markdown
           .core.interactiveshell: InteractiveShell
                .debugger: set_trace
    astroPHD.ipython.autoreload: set_autoreload, aimport
                    .imports: run_imports, import_from_file
                    .notebook: add_raw_code_toggle
                    .plot: configure_matplotlib
                    .printing: printmd, printMD, printltx, printLaTeX
    ```
2. makes all non-suppressed lines automatically display
    By setting `IPython.InteractiveShell.ast_node_interactivity='all'`.
    Suppressed lines are lines like `> x = func()` or ending with `;`.
    Displayed lines are just like `x`, where 'x' is an existing variable.

3. configures matplotlib to use the 'inline' & 'retina' backends



<a id="autoreload"></a>
### [autoreload](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#module-astroPHD.ipython.autoreload)
> `from  astroPHD.ipython import autoreload`

This module deals with auto-reloading packages / modules / functions in IPython. With IPython auto-reload, specified (or all) packages will be auto-reloaded to check for code changes. While this slows down code execution, it is enormously useful for real-time code development and testing.

The principal functions are:

- [`.set_autoreload`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.autoreload.set_autoreload): to set the auto-reload state for packages

- [`.aimport`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.autoreload.aimport): import with or without auto-reload


<a id="imports-1"></a>
### [imports](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#module-astroPHD.ipython.imports)
> `from  astroPHD.ipython import imports`

This module is an easy interface for importing the [imports](#imports) files as well as any custom imports files. Rather than \*-importing, all imports are routed through ipython magic commands.

The principal function is:

- [`run_imports`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.run_imports): import file using ipython magic.
    supports custom imports files and also provides key-word arguments to import any of the files in [imports](#imports).

    As example:

    ```python
    from astroPHD import ipython
    ipython.run_imports(base=True)
    ```
    Imports and prints the summary (abridged)
    ```
        Returns
        -------
        Base: imports
            
            * os, sys, time, pdb, warnings,
            * numpy -> np, scipy,
            * tqdm -> TQDM, .tqdm, .tqdm_notebook ->. tqdmn
        
        ...
    ```

The supporting functions are: [`import_from_file`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_from_file), [`aimport`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.autoreload.aimport), [`set_autoreload`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.autoreload.set_autoreload), [`import_base`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_base), [`import_extended`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_extended), [`import_astropy`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_astropy), [`import_matplotlib`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_matplotlib), [`import_galpy`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_galpy), [`import_amuse`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.imports.import_amuse)

<a id="notebook"></a>
### [notebook](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.notebook)
> `from  astroPHD.ipython import notebook`

Currently this only has the function [`add_raw_code_toggle`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.notebook.add_raw_code_toggle), which adds a button toggle to hide/show code cells in an HTML export of a Jupyter notebook.


<a id="plot"></a>
### [plot](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.plot)

functions to configure IPython environments for improved plotting.

Currently this only has the function [`configure_matplotlib`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.plot.configure_matplotlib), which sets Matplotlib Jupyter backend, inline plotting, etc.

<a id="printing"></a>
### [printing](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.printing)
Functions for enhanced printing in an IPython environment.

In addition to importing the standard `display`, `Latex`, `Markdown`, `HTML`

The principal functions are:

- [`printmd`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.printing.printmd): print in Markdown.
    set the text <span style="color:red">color</span>, <span style="font-size:16pt">size</span>, <span style="font-weight:bold">weight</span>, <span style="font-style:italic;">style</span>, <span style="background-color:yellow;">highlight</span>, etc.

- [`printltx`](https://astrophd.readthedocs.io/en/latest/astroPHD.ipython.html#astroPHD.ipython.printing.printltx)
    rapidly make latex math, matrices, etc.


<a id="math"></a>
## [math](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astrophd-imports-package)
> Import using `from  astroPHD import math`

A work in progress.

The principal functions are:

- [quadrature](https://astrophd.readthedocs.io/en/latest/astroPHD.math.html#astroPHD.math.math.quadrature)

- [logsumexp](https://astrophd.readthedocs.io/en/latest/astroPHD.math.html#astroPHD.math.math.quadrature)

<a id="plot-1"></a>
## [plot](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astrophd-imports-package)
> Import using `from  astroPHD import plot`

connects to `astroPHD.community.starkplot`

<a id="units"></a>
## [units](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astrophd-imports-package)
> Import using `from  astroPHD import units`


<a id="util"></a>
## [util](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astrophd-imports-package)
> Import using `from  astroPHD import util`

<a id="config"></a>
### [config](https://astrophd.readthedocs.io/en/latest/astroPHD.util.html#module-astroPHD.util.config)

<a id="logging"></a>
### [Logging](https://astrophd.readthedocs.io/en/latest/astroPHD.util.logging.html#astrophd-util-logging-package)

<a id="inspect"></a>
### [inspect](https://astrophd.readthedocs.io/en/latest/astroPHD.util.inspect.html#astrophd-util-inspect-package)

<a id="functools"></a>
### [functools](https://astrophd.readthedocs.io/en/latest/astroPHD.util.html#module-astroPHD.util.functools)

<a id="pickle"></a>
### [pickle](https://astrophd.readthedocs.io/en/latest/astroPHD.util.html#module-astroPHD.util.pickle)

<br><br>

- - -
- - -

<br><br>

<a id="templates"></a>
# Templates
Templates are useful. Here are some.

<a id="about-text"></a>
## About Text
. [About.txt](templates/ABOUT/ABOUT.txt) : an about text in basic `.txt` format
. [About.md](templates/ABOUT/ABOUT.md) : an about text in Markdown

<a id="python"></a>
## Python

. [\_\_init\_\_](templates/python/__init__.py "initialization file")
. [python.py](templates/python/python.py "standard python file")
. [notebook.ipynb](templates/python/notebook.ipynb "standard Jupter Notebook")

<a id="latex"></a>
## Latex

. [tex file](templates/latex/main.tex)
. [bibtex file](templates/latex/main.bib)

**Stylesheets:**
. [main stylesheet](templates/latex/util/main.cls)
. [astronomy stylesheet](templates/latex/util/astronomy.cls)
. [maths stylesheet](templates/latex/util/maths.cls)
. [base stylesheet](templates/latex/util/base.cls)
