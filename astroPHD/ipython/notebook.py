# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : ipython.notebook
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""functions for Jupyter notebook / lab / hub.

Routine Listings
----------------
add_raw_code_toggle
    Add a toggle to show/hide code cells when Notebook is exported to HTML

"""

__author__ = "Nathaniel Starkman"
__credits__ = ["Jo Bovy"]


##############################################################################
# IMPORTS

# GENERAL
from IPython.display import HTML

# PROJECT-SPECIFIC


##############################################################################
# CODE


def add_raw_code_toggle() -> HTML:
    """Add a toggle for code cells when Notebook is exported to HTML.

    HTML and Javascript button, placed directly below function execution cell.

    References
    ----------
    code from Jo Bovy

    """
    return HTML(
        """<script>
    code_show=true;
    function code_toggle() {
     if (code_show){
     $('div.input').hide();
     } else {
     $('div.input').show();
     }
     code_show = !code_show
    }
    $( document ).ready(code_toggle);
    </script>
    <form action="javascript:code_toggle()">
    <input type="submit" value="Click here to toggle on/off the raw code.">
    </form>"""
    )


# /def

##############################################################################
# END
