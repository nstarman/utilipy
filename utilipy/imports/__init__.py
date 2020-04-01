# -*- coding: utf-8 -*-

"""Imports Sets.

Most python scripts have a large number of lines dedicated to just
importing various modules and functions. While it is good to be explicit,
sometimes it's nice to just start coding. Also, its a pain to copy the
same set of imports between scripts, and scrolling through all the imports
to reach the start of the code is aggravating.

This module provides a variety of files that can be ``*``-imported to provide
basic set of imports so that you can just get started coding.


The provided quick imports are ``base_imports``, ``extended_imports``,
``astropy_imports``, ``matplotlib_imports``, ``galpy_imports`` and
``amuse_imports``.

The files will print an import summary. To prevent this summary, set
``verbose-imports=False`` in the ``.astroPHCrc`` config file in your
home or local directory. For details, see `config
file <#config-file>`__. Each of the imports also provides a helper
function that will print out the import summary.


Package-Specific Import Sets
----------------------------

Most packages have a standard set of imports. Often these imports are not
populated directly in the top-level namespace of the package, so that a
`from package import *` would suffice to import the standard set of imports.
The purpose of this module is to provide such sets of standard imports,
so that, for the `matplotlib` package as an example, the following are
imported with one line

    `from utilipy.imports.matplotlib_ import *`

    - pyplot->plt
    - matplotlib->mpl, .cm, .colors
    - mpl_toolkits.mplot3d.Axes3D



"""

__author__ = "Nathaniel Starkman"


##############################################################################
# END
