===================
1.1dev (unreleased)
===================

- No changes yet

================
1.1 (unreleased)
================


==================
1.0.1 (2020-04-05)
==================

- fixed import inspect in ``utilipy.decorators.func_io`` from buit-in to utilipy's inspect module (``utilipy.utils.inspect``) since the function ``store_function_input`` needs ```fuller_signature`` <https://utilipy.readthedocs.io/en/latest/api/utilipy.decorators.store_function_input.html#utilipy.decorators.store_function_input>`_.


================
1.0 (2020-04-01)
================

New Features
------------

Version 1.0 is a reboot of ``utilipy``, so all features can be considered new.

utilipy.__init__
^^^^^^^^^^^^^^^^^

- Set up top-level namespace: `help`, `online_help`, 
  `wraps` from ``util.functools.wraps``,
  `LogFile` from `util.logging`,
  `config` from configurations,
  and `ObjDict` from `util.collections`.
- Also import all the subpackages:
	- `astro`
	- `constants`
	- `data_utils`
	- `decorators`
	- `imports`
	- `ipython`
	- `math`
	- `plot`
	- `scripts`


utilipy.config
^^^^^^^^^^^^^^

- ``utilipy`` has a config file ``.utilipyrc`` that governs import verbosity, warnings verbosity, and what type of frozen constants to use.
- all the configurations can be get / set during run-time.
- there is a `with` version of all the configurations, for running code with a temporarily changed configurations.


utilipy.astro
^^^^^^^^^^^^^

- distance modulus functions (`distanceModulus`, `distanceModulus_distance`, `distanceModulus-magnitude`)
- angular separation function (`max_angular_separation`)
- parralax functions (`parallax`, `parallax_angle`, `parallax_distance`)
- fast and SkyCoord versions of these functions


utilipy.astro.instruments
^^^^^^^^^^^^^^^^^^^^^^^^^

- filter transformation functions
- MegaCam to PanSTARRS


utilipy.constants
^^^^^^^^^^^^^^^^^

Astropy constants, with a frozen version for reproducibility.

float versions of the constants accessible through values module this includes frozen version for reproducibility to access frozen version, set frozen-constants=True in `utilipy` config.

- `FrozenConstants` for frozen constants
- `ConstantsValues` for the values of constants.


utilipy.data_utils
^^^^^^^^^^^^^^^^^^

- `idxDecorator` to control whether a fnction returns boolean arrays or indices.
- `inRange`: multidimensional box selection.
- `outRange`: multidimensional box exclusion.
- `ioRange`: multidimensional box selection and exclusion.
- `ellipse`: elliptical selection of data in many dimensions.
-  `circle`: circular selection of data in many dimensions.
   
utilipy.data_utils.fitting
^^^^^^^^^^^^^^^^^^^^^^^^^^

- `scipy_residual_to_lmfit` decorator to make scipy residual functions compatible with `lmfit <https://lmfit.github.io/lmfit-py/index.html>`_.

utilipy.decorators
^^^^^^^^^^^^^^^^^^

Decorators


utilipy.decorators.baseclass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A set of baseclasses to make improved decorators. This module requires further testing.

utilipy.decorators.docstrings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- astropy's "format_doc"

utilipy.decorators.func\_io
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Function input / output.

- function `store_function_input` to store all the input to a function as a BoundArgument
- function `add_folder_backslash` to add a backslash to directory path inputs.
- `dtypeDecoratorMaker` function to make a dtype decorator.
- `dtypeDecorator` function to ensure arguments are type dtype.
- `boolDecorator`, `intDecorator`, `floatDecorator`, `strDecorator`, `ndarrayDecorator`, `ndfloat64Decorator`, which enforce their respective dtypes.


utilipy.imports
^^^^^^^^^^^^^^^

This module provides a variety of files that can be \*-imported to provide basic set of imports.

The quick imports are `base_imports`, `extended_imports`, `astropy_imports`, `matplotlib_imports`, `galpy_imports` and `amuse_imports`.

utilipy.imports.base
^^^^^^^^^^^^^^^^^^^^

helper function `base_imports_help`

Base imports

    - os, sys, time, pdb, warnings,
    - numpy -> np, scipy,
    - tqdm -> TQDM, tqdm, .tqdm_notebook -> tqdmn

IPython imports

    - display, Latex, Markdown, set_trace,
    - printmd, printMD, printltx, printLaTeX,
    - set_autoreload, aimport,
    - run_imports, import_from_file,
    - add_raw_code_toggle

utilipy imports

    - LogFile
    - ObjDict

utilipy.imports.extended
^^^^^^^^^^^^^^^^^^^^^^^^

helper function `extended_imports_help`

Numpy imports

    - linalg.norm

Scipy imports

    - stats.binned_statistic->binned_stats


utilipy.imports.matplotlib
^^^^^^^^^^^^^^^^^^^^^^^^^^

helper function `matplotlib_imports_help`

Matplotlib imports

    - pyplot->plt
    - matplotlib->mpl, .cm, .colors
    - mpl_toolkits.mplot3d.Axes3D

utilipy imports

    - ipython.plot.configure_matplotlib

utilipy.imports.plotly
^^^^^^^^^^^^^^^^^^^^^^

helper function `plotly_imports_help`

plotly imports

    - plotly
    - express -> px
    - graph_objs -> go
    - io -> pio
    - subplots -> make_subplots

utilipy.imports.astropy
^^^^^^^^^^^^^^^^^^^^^^^

helper function `astropy_imports_help`

Astropy imports

    - units->u,
    - coordinates->coords, SkyCoord,
    - table.Table, QTable
    - visualization.quantity_support, astropy_mpl_style

utilipy.imports.galpy
^^^^^^^^^^^^^^^^^^^^^

helper function `galpy_imports_help`

Galpy imports

    - potential, .MWPotential2014
    - galpy.orbit.Orbit
    - galpy.util: bovy_conversion, bovy_coords

utilipy.imports.amuse
^^^^^^^^^^^^^^^^^^^^^

helper function `amuse_imports_help`

- imports `amuse`, `amuse.lab`, `amuse.units.units`, `amuse.units.constants`, `amuse.couple.bridge`
- provides a help function, `amuse_imports_help`


utilipy.ipython
^^^^^^^^^^^^^^^

Functions for interacting with the IPython environment. If in the IPython, sets the `ast_node_interactivity` to "all" and configures matplotlib, via `configure_matplotlib`, to an inline backend and retina resolution.

loads into the top-level namespace:

- help function
- modules: `autoreload` , `imports`, `notebook`, `plot`, `printing`
- functions: `set_autoreload`, `aimport`, `run_imports`, `import_from_file`, `add_raw_code_toggle`, `configure_matplotlib`, `printMD`, `printLTX`
	  
utilipy.ipython.autoreload
^^^^^^^^^^^^^^^^^^^^^^^^^^

If in an IPython environment, sets the autoreload state to 1 (autoreload anything imported by `aimport`).

- `set_autoreload` function to change the global imports setting.
- `aimport` for autoreloading individual modules
  

utilipy.ipython.imports
^^^^^^^^^^^^^^^^^^^^^^^

Module for running `utilipy.imports` in an IPython environment.

- `import_from_file` function to run any import file, from `utilipy` or a custom file.
- `run_imports` function to import a file using IPython magic. Uses `import_from_file` on custom files. Has built-in options for a set of basic imports (by keyword `base`), extended imports (by keyword `extended`), astropy, matplotlib, plotly, galpy, and amuse import sets by the respective keywords.

utilipy.ipython.notebook
^^^^^^^^^^^^^^^^^^^^^^^^

Functions for Jupyter notebook / lab / hub.

- `add_raw_code_toggle` function to show/hide code cells when Notebook is exported to HTML
  
utilipy.ipython.plot
^^^^^^^^^^^^^^^^^^^^

- `configure_matplotlib` function to control plotting in an IPython environment.

utilipy.ipython.printing
^^^^^^^^^^^^^^^^^^^^^^^^

- `printMD` function to print in Markdown.
- `printLTX` function to print in Latex.


utilipy.math
^^^^^^^^^^^^

- `quadrature`, arguments summed in quadrature.


utilipy.plot
^^^^^^^^^^^^

- created folder, nothing implemented yet. See :ref:`whatsnew-planned`.
  

utilipy.scripts
^^^^^^^^^^^^^^^

- created folder, nothing implemented yet. See :ref:`whatsnew-planned`.

utilipy.utils
^^^^^^^^^^^^^

.. code-block:: python
	:linenos:

	from .logging import LogPrint, LogFile
	from .collections import ObjDict

	from . import functools, pickle

	# import top level packages
	from . import (
	    collections,
	    doc_parse_tools,
	    logging,
	    metaclasses,
	)


utilipy.utils.exceptions
^^^^^^^^^^^^^^^^^^^^^^^^

- `utilipyWarning`
- `utilipyWarningVerbose`

utilipy.utils.functools
^^^^^^^^^^^^^^^^^^^^^^^

- `makeFunction`: make a function from an existing code object.
- `copy_function`: Copy a function.
- `update_wrapper`: this overrides the default ``functools`` `update_wrapper` and adds signature and docstring overriding

- `wraps`: overrides the default ``functools`` `update_wrapper` and adds signature and docstring overriding

utilipy.utils.inspect
^^^^^^^^^^^^^^^^^^^^^

added FullerArgSpec which better separates parts of a signature, like arguments with and without defaults. Also a FullerSignature object which has much finer control over signatures and itself appears to have the signature of the function to which it is a signature.

- `POSITIONAL_ONLY`
- `POSITIONAL_OR_KEYWORD`
- `VAR_POSITIONAL`
- `KEYWORD_ONLY`
- `VAR_KEYWORD`
- `_void`
- `_empty`
- `_placehold`
- `_is_empty`
- `_is_void`
- `_is_placehold`
- `_is_placeholder`
- `FullerArgSpec`
- `getfullerargspec`
- `get_annotations_from_signature`
- `get_defaults_from_signature`
- `get_kwdefaults_from_signature`
- `get_kwonlydefaults_from_signature`
- `get_kinds_from_signature`
- `modify_parameter`
- `replace_with_parameter`
- `insert_parameter`
- `prepend_parameter`
- `append_parameter`
- `drop_parameter`
- `FullerSignature`
- `fuller_signature`
  
utilipy.utils.pickle
^^^^^^^^^^^^^^^^^^^^

dump and load many objects

utilipy.utils.string
^^^^^^^^^^^^^^^^^^^^

- `FormatTemplate` with string supporting `.format`, syntax.
  
utilipy.utils.typing
^^^^^^^^^^^^^^^^^^^^

- `array_like`: typing.Sequence
  
utilipy.utils.logging
^^^^^^^^^^^^^^^^^^^^^

Basic loggers that can both print and/or record to a file.

- LogPrint: print logger 
- LogFile: This class uses `open`
  
utilipy.utils.doc_parse_tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Docstring inheritance-style implementations. Supports numpy and google docstrings. 

To implement your own inheritance file, simply write a function that fits the template

.. code-block:: python

    def your_style(prnt_doc, child_doc):
        ''' Merges parent and child docstrings

            Parameters
            ----------
            prnt_cls_doc: Optional[str]
            child_doc: Optional[str]

            Returns
            ------
            Optional[str]
                The merged docstring that will be utilized.'''
        return final_docstring

and log this using `custom_inherit.add_style(your_style)`.
To permanently save your function

1. define your function within `custom_inherit/_style_store.py`
2. log it in `custom_inherit.style_store.__all__`.
   
utilipy.utils.collections
^^^^^^^^^^^^^^^^^^^^^^^^^

- `ObjDict`: Dictionary-like object intended to store information. Instantiated with a name (str)


API Changes
-----------

Everything



=======
Pre 1.0
=======

The package formerly known as `astroPHD`. Many of the features in v1.0 were present here, but poorly documented and not in Pypi.

API Changes
-----------

N/A


Bug Fixes
---------

N/A


Other Changes and Additions
---------------------------

N/A