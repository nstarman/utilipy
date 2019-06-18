#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""

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

import numpy as np
from functools import wraps

# Custom Imports
from .._domain_factory import domain_factory

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


#############################################################################
# Code


def degreeDecorator(inDegrees=[], outDegrees=[], roof=False):
    """Decorator to transform angles from and to degrees if necessary

    Arguments
    ---------
    inDegrees: list
        list specifitying indices of angle arguments
        ex: [index, index, ...]
        can also include domain information with the index
            (index, lower, upper), where upper > lower
            domain must be in radians
        ex: [index, (index, lower, upper), ...]
    outDegrees: list
        same as inDegrees, but for function return

    HISTORY:

       ____-__-__ - Written - Bovy
       2019-03-02 - including domainDecorator & speedups - Nathaniel Starkman (UofT)

    """
    # speedup if no domain adjustments
    if all(map(np.isscalar, [*inDegrees, *outDegrees])):
        # (modified) old degree decorator
        def wrapper(func):
            @wraps(func)
            def wrapped(*args, **kwargs):
                isdeg = kwargs.get('degree', False)
                # PRE
                if isdeg:
                    args = [arg * np.pi / 180 if i in inDegrees else arg
                            for i, arg in enumerate(args)]

                # CALLING
                out = func(*args, **kwargs)

                # POST
                if isdeg:
                    for i in outDegrees:
                        out[:, i] *= 180. / np.pi
                return out
            # /def
            return wrapped
        # /def
        return wrapper
    # /def

    # else:  # need to adjust domains

    indegs = [(x, lambda x: x) if np.isscalar(x)
              else (x[0], domain_factory(*x[1:], roof=roof))
              for x in inDegrees]
    outdegs = [(x, lambda x: x) if np.isscalar(x)
               else (x[0], domain_factory(*x[1:], roof=roof))
               for x in outDegrees]

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            isdeg = kwargs.get('degree', False)

            # PRE
            newargs = list(args)
            for i, f in indegs:  # adjusting domain of in args
                if isdeg:  # deg -> rad
                    newargs[i] = f(args[i] * np.pi / 180.)
                else:  # already rad
                    newargs[i] = f(args[i])

            # CALLING
            out = func(*newargs, **kwargs)

            # POST
            for i, f in outdegs:
                if isdeg:
                    out[:, i] = f(out[:, i]) * 180 / np.pi
                else:
                    out[:, i] = f(out[:, i])

            return out
        # /def
        return wrapped
    # /def
    return wrapper
# /def
