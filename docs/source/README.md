# Welcome

Welcome to  `astroPHD`, a collection of useful python codes. This is a centralized repository for much of the non project-specific code I have written or come across. There are modules for making advanced decorators, interfacing with IPython environments, miscellaneous astronomical functions, data utilities, making fitting libraries inter-operable, improving astropy units and quantity-enabled functions, and much more. Check out the documentation here, on [readthedocs](https://readthedocs.org/projects/astrophd/badge/?version=latest), and at the [wiki](https://github.com/nstarman/astroPHD/wiki) for more detail.


[![](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)
[![](https://travis-ci.org/nstarman/astroPHD.svg?branch=master)](https://travis-ci.org/nstarman/astroPHD)
[![](https://readthedocs.org/projects/astrophd/badge/?version=latest)](https://astrophd.readthedocs.io/en/latest/?badge=latest)

## Attribution

Author: **Nathaniel Starkman** - *Graduate Student @ UofT* - [website](http://www.astro.utoronto.ca/~starkman/) -- [github](https://github.com/nstarman)

[![](https://zenodo.org/badge/DOI/10.5281/zenodo.3545178.svg)](https://doi.org/10.5281/zenodo.3545178)

If you find this code useful in your research, please let me know. If you significantly use astroPHD in a publication, please acknowledge **10.5281/zenodo.3545178**. Please also send me a reference to the paper.


<br><br>
- - -
- - -
<br><br>

<a id="Module-Highlights"></a>
# Module Highlights
Most of the modules have too much to reasonably document here. These are some of the most useful highlights. Detailed descriptions of everything in `astroPHD` and more can be found at [readthedocs](https://readthedocs.org/projects/astrophd/badge/?version=latest) and at the [wiki](https://github.com/nstarman/astroPHD/wiki).

<a id="astronomy"></a>
## astronomy
> Import using `from  astroPHD import astronomy`


<br><br><br>

<a id="data_utils"></a>
## data_utils
> Import using `from  astroPHD import data_utils`

<br><br><br>

<a id="decorators"></a>
## decorators
> Import using `from  astroPHD import decorators`

<br><br><br>

<a id="fitting"></a>
## fitting
> Import using `from  astroPHD import fitting`

<br><br><br>

<a id="imports"></a>
## imports
Most of my notebooks or scripts have at leas 30 lines dedicated to just importing the various modules and functions that will be used later. It's cumbersome, a pain to copy between scripts, and means that the code doesn't start until halfway down the screen. This module provides a variety of files that can be `*`-imported to provide all the basic imports so that you can just get started coding.

The files will print an import summary. To prevent this summary, set  `verbose-imports=False` in the `.astroPHCrc` config file in your home or local directory. For details on this config file, see [config file](#config-file).


<a id="base"></a>
### base
> Import using `from  astroPHD.imports.base import *`

Imports
```
Base:

    - os, sys, time, pdb, warnings,
    - numpy -> np, scipy,
    - tqdm -> TQDM, .tqdm, .tqdm_notebook ->. tqdmn

IPython: (if in an IPython environment)

    - display, Latex, Markdown, set_trace,
    - printmd, printMD, printltx, printLaTeX,
    - set_autoreload, aimport,
    - run_imports, import_from_file,
    - add_raw_code_toggle

astroPHD: imports

    - LogFile
    - ObjDict
```

Also provides **[base_imports_help](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astroPHD.imports.base.base_imports_help)** function.

<a id="extended"></a>
### extended
> Import using `from  astroPHD.imports.extended import *`

Imports
```
Numpy: imports

    - linalg.norm

Scipy: imports

    - stats.binned_statistic->binned_stats
```

Also provides **[extend_imports_help](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astroPHD.imports.extended.extend_imports_help)** function.

<a id="matplotlib"></a>
### matplotlib
> Import using `from  astroPHD.imports.matplotlib import *`

Imports
```
Matplotlib: imports

    - pyplot->plt
    - matplotlib->mpl, .cm, .colors
    - mpl_toolkits.mplot3d.Axes3D

astroPHD: imports

    - ipython.plot.configure_matplotlib
```

Also provides **[matplotlib_imports_help](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astroPHD.imports.matplotlib.matplotlib_imports_help)** function.

<a id="astropy"></a>
### astropy
> Import using `from  astroPHD.imports.astropy import *`

Imports
```
 Astropy: imports

    - units->u,
    - coordinates->coords, SkyCoord,
    - table.Table, QTable
    - visualization.quantity_support, astropy_mpl_style
```

Also provides **[astropy_imports_help](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astroPHD.imports.astropy.astropy_imports_help)** function.

<a id="extras"></a>
### extras


#### galpy:
> Import using `from  astroPHD.imports.galpy import *`

Imports
```
Galpy : imports

    - potential, .MWPotential2014
    - galpy.orbit.Orbit
    - galpy.util: bovy_conversion, bovy_coords
```

Also provides **[galpy_imports_help](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astroPHD.imports.galpy.galpy_imports_help)** function.

<br>
#### AMUSE:
> Import using `from  astroPHD.imports.amuse import *`

Imports
```
Amuse: imports

    - amuse
    - amuse.lab
    - amuse.units.units, constants
    - amuse.couple.bridge
```

Also provides **[amuse_imports_help](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astroPHD.imports.amuse.amuse_imports_help)** function.

<br><br><br>

<a id="ipython"></a>
## ipython
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
### autoreload
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

<a id="imports"></a>
### imports
> `from  astroPHD.ipython import imports`


<a id="notebook"></a>
### notebook
> `from  astroPHD.ipython import imports`

<a id="plot"></a>
### plot

<a id="printing"></a>
### printing


<br><br><br>

<a id="math"></a>
## math
> Import using `from  astroPHD import math`

<br><br><br>

<a id="plot"></a>
## plot
> Import using `from  astroPHD import plot`

<br><br><br>

<a id="units"></a>
## units
> Import using `from  astroPHD import units`

<br><br><br>

<a id="util"></a>
## util
> Import using `from  astroPHD import util`

<a id="config-file"></a>
### config file


<br><br>

- - -
- - -

<br><br>

<a id="Templates"></a>
# Templates
Templates are useful. Here are some.

<a id="About-Text"></a>
## About Text
. [About.txt](templates/ABOUT/ABOUT.txt) : an about text in basic `.txt` format
. [About.md](templates/ABOUT/ABOUT.md) : an about text in Markdown

<a id="Python"></a>
## Python

. [\_\_init\_\_](templates/python/__init__.py "initialization file")
. [python.py](templates/python/python.py "standard python file")
. [notebook.ipynb](templates/python/notebook.ipynb "standard Jupter Notebook")

<a id="Latex"></a>
## Latex

. [tex file](templates/latex/main.tex)
. [bibtex file](templates/latex/main.bib)

**Stylesheets:**
. [main stylesheet](templates/latex/util/main.cls)
. [astronomy stylesheet](templates/latex/util/astronomy.cls)
. [maths stylesheet](templates/latex/util/maths.cls)
. [base stylesheet](templates/latex/util/base.cls)
