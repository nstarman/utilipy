#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""

    json functions
    also located in gaia_tools **Make sure both updated**

#############################################################################

Copyright (c) 2018 - Nathaniel Starkman
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  The name of the author may not be used to endorse or promote products
     derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

#############################################################################
Planned Features
"""

#############################################################################
# Imports

from json import *
import textwrap

#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2018, "
__credits__ = ["json package"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"

#############################################################################
# Code


def strjoinall(dct, joinstr='\n'):
    r"""iterate through dictionary entries, applying str.join

    Arguments
    ---------
    dct: dictionary
        product of json.load
    joinstr: str  (default: '\n')
        the string by which to join

    Returns
    -------
    same dictionary
    """

    for key, val in dct.items():
        dct[key] = joinstr.join(val)

    return dct


def strjoinkeys(dct, keys, joinstr='\n'):
    r"""iterate through dictionary entries, applying str.join

    Arguments
    ---------
    dct: dictionary
        product of json.load
    keys: list
        list of keys in dct to apply str.join
    joinstr: str  (default: '\n')
        the string by which to join

    Returns
    -------
    same dictionary
    """

    for key, val in dct.items():
        if key in keys:
            dct[key] = joinstr.join(val)

    return dct


def prettyprint(dct):
    r"""dictionary printing function
    """
    print('{')
    for key, val in dct.items():
        print(" '{}':".format(key))
        if isinstance(val, str):
            print(textwrap.indent(val, '  \t'))
        else:
            print(textwrap.indent(val.__repr__(), '  \t'))
    print('}')

    return
# /def
