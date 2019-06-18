#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   :
# AUTHOR  : Nathaniel Starkman
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General

## Custom

## Project-Specific

##############################################################################
### PARAMETERS


##############################################################################
### CODE

def split_dictionary(dct, keys=[]):
    """split_dictionary

    split a dictionary into one containing the specified keys,
    and another with the remaining items.

    Parameters
    ----------
    dct : dict
        the dictionary to split into two smaller dictionaries
    keys : list, tuple, etc
        the keys to extract for the dictionary subset

    Returns
    -------
    sub_dict : dict
        the dictionary with keys = *keys*
    sup_dict : dict
        the dictionary with all the remaining items
    """
    sub_dict = {k: v for k, v in dct.items() if k in keys}
    sup_dict = {k: v for k, v in dct.items() if k not in keys}
    return sub_dict, sup_dict

##############################################################################
### END
