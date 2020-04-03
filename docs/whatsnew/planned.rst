.. _whatsnew-planned:

***************************
What's Planned for utilipy?
***************************

Planned Features
----------------

full code coverage in tests
generalized help function class that can be implemented in all subpackages.

utilipy.config
^^^^^^^^^^^^^^

- for `use_`, adopt a `contextmanager <https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager>`_, possibly using a `ContextDecorator <https://docs.python.org/3/library/contextlib.html#contextlib.ContextDecorator>`_.

utilipy.astro
^^^^^^^^^^^^^

move to separate package


utilipy.constants
^^^^^^^^^^^^^^^^^

get the `values` module to include the proper documentation from imported astropy constants


utilipy.data_utils.fitting
^^^^^^^^^^^^^^^^^^^^^^^^^^

Decoratory to add support for `symfit <https://symfit.readthedocs.io/en/stable/>` with `scipy.optimize` functions.

utilipy.decorators.baseclass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Full baseclass for converting any function to a BaseClass decorator.

utilipy.decorators.docstrings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Properly import from astropy and include in RTD.

utilipy.decorators.func\_io
^^^^^^^^^^^^^^^^^^^^^^^^^^^

implement with signature method to be more robust.

utilipy.imports
^^^^^^^^^^^^^^^

better docstring method for help functions.

utilipy.plot
^^^^^^^^^^^^

stacked Coxcomb plot

utilipy.pipeline
^^^^^^^^^^^^^^^^
In the development pipeline