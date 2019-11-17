# -*- coding: utf-8 -*-

"""initialization file for `inspect`."""

__author__ = "Nathaniel Starkman"

##############################################################################
# IMPORTS

# General
import inspect as _inspect
from inspect import *

# Project-Specific
from ._getfullerargspec import FullerArgSpec, getfullerargspec
from ._signature import (Signature, signature,
                         get_annotations_from_signature,
                         get_defaults_from_signature,
                         get_kwdefaults_from_signature,
                         get_kwonlydefaults_from_signature,
                         _POSITIONAL_OR_KEYWORD, _VAR_POSITIONAL,
                         _KEYWORD_ONLY, _VAR_KEYWORD)


##############################################################################
# END
