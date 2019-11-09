# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : PBH_in_galaxy
# AUTHOR  : Nathaniel Starkman
# PROJECT : Eridanus_PBH
#
# ----------------------------------------------------------------------------

# Docstring
"""Warnings and Exceptions.

code modified from galpy.

"""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL
import warnings

# CUSTOM

# PROJECT-SPECIFIC
from .config import __config__


##############################################################################
# PARAMETERS

_SHOW_WARNINGS = __config__.getboolean('verbosity', 'warnings')

###############################################################################
# CODE
###############################################################################


class astroPHDWarning(Warning):
    pass
# /class


# ----------------------------------------------------------------------------

class astroPHDWarningVerbose(Warning):
    pass
# /class


# ----------------------------------------------------------------------------

def _warning(message, category=astroPHDWarning, filename='',
             lineno=-1, file=None, line=None):
    if issubclass(category, astroPHDWarning):
        if not issubclass(category, astroPHDWarningVerbose) or _SHOW_WARNINGS:
            print("astroPHDWarning: " + str(message))
    else:
        print(warnings.formatwarning(message, category, filename, lineno))


##############################################################################
# END
