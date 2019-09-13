#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""

    Custom Astropy units, constants, & functions

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

from fractions import Fraction
from astropy.units.core import UnitBase, def_unit
from astropy import units

_ns = globals()

#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2018, "
__credits__ = [""]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"

##########################################################################
# New Units

def_unit(['mps', 'm_s'], represents=units.m / units.s,
         doc='meter per second composite unit',
         format={'latex': r'\frac{m}{s}',
                 'latex_inline': r'm\,s^{-1}'},
         namespace=_ns)

def_unit(['kmps', 'km_s'], represents=units.km / units.s,
         doc='kilometer per second composite unit',
         format={'latex': r'\frac{km}{s}',
                 'latex_inline': r'km\,s^{-1}'},
         namespace=_ns)

def_unit(['kmpspMpc', 'km_sMPc', 'hubble'],
         represents=units.km / units.s / units.Mpc,
         doc='kilometer per second per Megaparsec composite unit',
         format={'latex': r'\frac{km}{s Mpc}',
                 'latex_inline': r'km\,s^{-1}\,{Mpc}^{-1}'},
         namespace=_ns)

def_unit(['kmpspkpc', 'km_skpc'],
         represents=units.km / units.s / units.kpc,
         doc='kilometer per second per kiloparsec composite unit',
         format={'latex': r'\frac{km}{s kpc}',
                 'latex_inline': r'km\,s^{-1}\,{kpc}^{-1}'},
         namespace=_ns)

def_unit(['maspyr', 'mas_yr'], represents=units.mas / units.yr,
         doc='milli-arcseconds / year composite unit',
         format={'latex': r'\frac{mas}{yr}',
                 'latex_inline': r'mas\,yr^{-1}'},
         namespace=_ns)



###########################################################################
# CLEANUP

del UnitBase
del def_unit
del Fraction


###########################################################################
# DOCSTRING

# This generates a docstring for this module that describes all of the
# standard units defined here.
from astropy.units.utils import generate_unit_summary as _generate_unit_summary
if __doc__ is not None:
    __doc__ += _generate_unit_summary(globals())
