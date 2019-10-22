# AstroPHD

Welcome to 	`astroPHD`, a collection of useful python codes.

## Attribution

[![DOI](https://zenodo.org/badge/192425953.svg)](https://zenodo.org/badge/latestdoi/192425953)
[![Build Status](https://travis-ci.org/nstarman/astroPHD.svg?branch=master)](https://travis-ci.org/nstarman/astroPHD)

Author: **Nathaniel Starkman** - *Graduate Student @ UofT* - [website](http://www.astro.utoronto.ca/~starkman/) -- [github](https://github.com/nstarman)


##  Table of Contents
<!-- MarkdownTOC levels="1,2" autolink="true" -->

- [Modules](#modules)
    - [astronomy](#astronomy)
    - [data_utils](#data_utils)
    - [fitting](#fitting)
    - [imports](#imports)
    - [ipython](#ipython)
    - [math](#math)
    - [plot](#plot)
    - [units](#units)
    - [util](#util)
- [Templates](#templates)
    - [About Text](#about-text)
    - [Python](#python)
    - [Latex](#latex)

<!-- /MarkdownTOC -->



<a id="modules"></a>
# Modules

<a id="astronomy"></a>
## astronomy
> Import using `from  astroPHD import astronomy`


<a id="data_utils"></a>
## data_utils
> Import using `from  astroPHD import data_utils`


<a id="fitting"></a>
## fitting
> Import using `from  astroPHD import fitting`


<a id="imports"></a>
## imports
> Import using `from  astroPHD import imports`


<a id="ipython"></a>
## ipython
> `from  astroPHD import ipython`

This module contains codes for interacting with ipython environments, like Jupyter Notebooks/Lab.

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
### autoreload,
> `from  astroPHD.ipython import autoreload`

This module deals with auto-reloading packages / modules / functions in IPython. With IPython auto-reload, specified (or all) packages will be auto-reloaded to check for code changes. While this slows down code execution, it is enormously useful for real-time code development and testing.

- `.set_autoreload`: set the auto-reload state for packages
    > signature :: reload_type: int

    reload_type: IPython reload state

    + 0: nothing auto-reloads
    + 1: things imported with `.aimport` will auto-reload
    + 2: all imports will auto-reload

- `.aimport`: import with auto-reload
    > signature :: \*modules: \*str, autoreload: (bool, list, tuple)= True
    
    + \*modules: string(s) for the module to import  
        ```python
        'matplotlib.pyplot'
        ```
        
        cannot (yet) do 'from matplotlib import pyplot'

    + autoreload: whether to override autoreload global state for this import.
      Can be a single boolean for all '\*modules', or a list of booleans for each 'module'.
          ```python
          set_autoreload(2)  # everything autoreloads
          aimport('matplotlib.pyplot', 'scipy.special',
                 autoreload=[True,  # matplotlib will autroreload
                            False])  # scipy will not, even though set_autoreload=2
          ```

<a id="imports-1"></a>
### imports
> `from  astroPHD.ipython import imports`


<a id="notebook"></a>
### notebook
> `from  astroPHD.ipython import imports`

<a id="plot"></a>
### plot

<a id="printing"></a>
### printing


<a id="math"></a>

<a id="math"></a>
## math
> Import using `from  astroPHD import math`


<a id="plot"></a>
## plot
> Import using `from  astroPHD import plot`


<a id="units"></a>
## units
> Import using `from  astroPHD import units`


<a id="util"></a>
## util
> Import using `from  astroPHD import util`



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
