#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""initialization file for `inspect`
"""

__author__ = "Nathaniel Starkman"

##############################################################################
# IMPORTS

# General
from inspect import *

# Project-Specific
from ._getfullerargspec import FullerArgSpec, getfullerargspec
from .signature import (Signature,
                        get_annotations_from_signature,
                        get_defaults_from_signature,
                        get_kwdefaults_from_signature,
                        get_kwonlydefaults_from_signature)


##############################################################################
# END
