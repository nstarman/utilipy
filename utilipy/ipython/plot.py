# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ipython.plot
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Plotting in an IPython environment.

Routine Listings
----------------
configure_matplotlib
    configure matplotlib Jupyter magic setting.

References
----------
Ipython [1]_

.. [1] Fernando Pérez, Brian E. Granger, IPython: A System for Interactive
    Scientific Computing, Computing in Science and Engineering, vol. 9,
    no. 3, pp. 21-29, May/June 2007, doi:10.1109/MCSE.2007.53.
    URL: https://ipython.org

"""

__author__ = "Nathaniel Starkman"


__all__ = [
    "configure_matplotlib",
]


##############################################################################
# IMPORTS

from IPython import get_ipython
import warnings


##############################################################################
# CODE


def configure_matplotlib(
    backend: str = "inline", figure_format: str = "retina"
) -> None:
    """Configure Matplotlib Jupyter magic setting.

    Parameters
    ----------
    backend : str, optional
        (defualt 'inline')
        set the matplotlib backend

    """
    if get_ipython() is None:
        warnings.warn(
            "not in an IPython environment," "cannot configure matplotlib"
        )
        return

    from IPython.terminal.pt_inputhooks import UnknownBackend

    try:
        # set matplotlib backend
        get_ipython().magic(f"matplotlib {backend}")

    except UnknownBackend:
        warnings.warn("not a valid backed. Please try again.")

    else:
        # set the resolution
        get_ipython().magic(
            "config InlineBackend.figure_format" f"='{figure_format}'"
        )

    return


# /def

##############################################################################
# END
