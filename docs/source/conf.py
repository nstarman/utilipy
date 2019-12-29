# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


"""astroPHD sphinx configuration file.

modelled off of the matplotlib conf.py

"""

# -- Path setup --------------------------------------------------------------

import os
import sys

# import astroPHD  # TODO need to make pip-able first
import sphinx

from datetime import datetime

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../../src'))
sys.path.insert(0, os.path.abspath('../../templates'))
# sys.path.append(os.path.abspath('sphinxext'))


# -- Project information -----------------------------------------------------

project = 'astroPHD'
copyright = '2019, Nathaniel Starkman'
author = 'Nathaniel Starkman'

# version = astroPHD.__version__  # TODO need to make pip-able first
version = '0.1.1'
release = version

github_project_url = "https://github.com/nstarman/astroPHD/"


# -- General configuration ---------------------------------------------------

master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # sphinx
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    # docstrings
    'numpydoc',
    # sphinx_gallery
    # 'sphinx_gallery.gen_gallery',
    # ipython
    'IPython.sphinxext.ipython_directive',
    'IPython.sphinxext.ipython_console_highlighting',
    # matplotlib
    'matplotlib.sphinxext.mathmpl',
    'matplotlib.sphinxext.plot_directive',
    # for markdown
    'recommonmark',
    'sphinx_markdown_tables',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


# source_parsers = {
#     '.md': 'recommonmark.parser.CommonMarkParser',
# }

# The suffix(es) of source filenames.
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['Thumbs.db', '.DS_Store',
                    # community codes
                    '../../src/src/astroPHD/community/starkplot',
                    '../src/src/astroPHD/community/starkplot']


# -- Options for HTML output -------------------------------------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
html_style = 'default.css'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinxdoc'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If false, no module index is generated.
#html_use_modindex = True
html_domain_indices = ["py-modindex"]

# Output file base name for HTML help builder.
htmlhelp_basename = 'astroPHDdoc'


# -- Extension configuration -------------------------------------------------

napoleon_numpy_docstring = True

numpydoc_use_plots = True  # Whether to produce plot:: directives for Examples sections that contain import matplotlib or from matplotlib import.
numpydoc_xref_param_type = True  # Whether to create cross-references for the parameter types in the Parameters, Other Parameters, Returns and Yields sections of the docstring. False by default.

# SPHINX_APIDOC_OPTIONS = ['members', 'undoc-members']


# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'Pillow': ('https://pillow.readthedocs.io/en/stable/', None),
    'cycler': ('https://matplotlib.org/cycler', None),
    'dateutil': ('https://dateutil.readthedocs.io/en/stable/', None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for LaTeX output ---------------------------------------

# The paper size ('letter' or 'a4').
latex_paper_size = 'a4'



# Show both class-level docstring and __init__ docstring in class
# documentation
autoclass_content = 'both'


# -- Options for numpydoc extension ---------------------------------------

numpydoc_show_class_members = False

latex_engine = 'xelatex'  # or 'lualatex'

latex_elements = {
    'babel': r'\usepackage{babel}',
    'fontpkg': r'\setmainfont{DejaVu Serif}',
}

html4_writer = True

inheritance_node_attrs = dict(fontsize=16)


def setup(app):
    if any(st in version for st in ('post', 'alpha', 'beta')):
        bld_type = 'dev'
    else:
        bld_type = 'rel'
    app.add_config_value('releaselevel', bld_type, 'env')



##############################################################################
# END
