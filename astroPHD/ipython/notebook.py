#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : notebook
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkython
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""functions for jupyter notebook / lab / hub
"""

__credits__ = ["Jo Bovy"]


##############################################################################
### IMPORTS

## General
from IPython.display import HTML

## Project-Specific

##############################################################################
### PARAMETERS


##############################################################################
### CODE

# --------------------------------------------------------------------------

def add_raw_code_toggle():  # TODO test works as a function
    """

    Info
    ----
    code from Jo Bovy
    """

    return HTML("""<script>
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
    <form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>"""
    )
# /def

##############################################################################
### END
