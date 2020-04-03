# -*- coding: utf-8 -*-

"""Functions for working with autoreload extension.

Routine Listings
----------------
`aimport`
    Jupyter magic aimport.

`set_autoreload`
    Global imports setting.

References
----------
IPython [1]_


.. [1] Fernando Pérez, Brian E. Granger, IPython: A System for Interactive
    Scientific Computing, Computing in Science and Engineering, vol. 9,
    no. 3, pp. 21-29, May/June 2007, doi:10.1109/MCSE.2007.53.
    URL: https://ipython.org

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "set_autoreload",
    "aimport",
]


##############################################################################
# IMPORTS

# GENERAL

from typing import Union, Optional

from IPython import get_ipython


# PROJECT-SPECIFIC

from ..utils.logging import LogPrint


##############################################################################
# PARAMETERS

_LOGFILE = LogPrint(header=False, verbose=0)

try:
    get_ipython()
    if get_ipython() is None:  # double checking
        raise NameError
except NameError:
    _HAS_IPY: bool = False
else:
    _HAS_IPY: bool = True


##############################################################################
# CODE
##############################################################################


def set_autoreload(reload_type: Optional[int] = None):
    """Global imports setting.

    Parameters
    ----------
    reload_type: {0, 1, 2} or None
        (default None)

        - **0**) Disable automatic reloading.
        - **1**) Reload all modules imported with %aimport
                 before executing the Python code typed.
        - **2**) Reload all modules (except those excluded by %aimport)
                 before executing the Python code typed.
        - **None**) null. do not change current setting.

    See Also
    --------
    autoreload: module
        `%load_ext autoreload`
        `%aimport`

    """
    if reload_type is not None:

        # set autoreload type
        get_ipython().magic(f"autoreload {reload_type}")

        _LOGFILE.write(f"set autoreload to {reload_type}")

    return


# /def


##############################################################################


def aimport(*modules: str, autoreload: Union[bool, list, tuple] = True):
    """Jupyter magic aimport.

    Parameters
    ----------
    modules: list of strs
        the modules to be imported
    autoreload: bool or list, optional
        (default True)
        whether the imported modules are marked for autoreloading
        if its a list, it must be the same length as `modules`

    """
    # making autoreload compatible with modules
    if isinstance(autoreload, bool):
        autoreload = [autoreload] * len(modules)
    elif len(autoreload) == len(modules):  # any list
        pass
    else:
        raise ValueError("len(autoreload) != len(modules)")

    for module, reload_type in zip(modules, autoreload):
        # testing correct data types
        assert isinstance(module, str)
        assert isinstance(reload_type, bool)

        if not reload_type:
            module = "-" + module  # mark for not autoreloading

        # import
        get_ipython().magic(f"aimport {module}")

    return


# /def


##############################################################################
# SETTING STATE

if _HAS_IPY is True:
    if get_ipython() is not None:
        get_ipython().magic("load_ext autoreload")  # autoreload extensions
        set_autoreload(1)


##############################################################################
# END
