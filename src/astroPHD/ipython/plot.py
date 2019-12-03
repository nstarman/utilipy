# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ipython.plot
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Plotting in an IPython environment.

Routine Listings
----------------
configure_matplotlib
    configure matplotlib Jupyter magic setting.

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL
from IPython import get_ipython
import warnings

# PROJECT-SPECIFIC


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
        warnings.warn("not in an IPython environment," "cannot configure matplotlib")
        return

    from IPython.terminal.pt_inputhooks import UnknownBackend

    try:
        # set matplotlib backend
        get_ipython().magic(f"matplotlib {backend}")

    except UnknownBackend:
        warnings.warn("not a valid backed. Please try again.")

    else:
        # set the resolution
        get_ipython().magic("config InlineBackend.figure_format" f"='{figure_format}'")

    return


# /def

##############################################################################
# END
