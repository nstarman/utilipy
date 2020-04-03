# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : String
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

"""String Utilities.

Routine Listings
----------------
FormatTemplate

"""

__author__ = "Nathaniel Starkman"

__all__ = ["FormatTemplate"]


###############################################################################
# IMPORTS

# GENERAL

import re
import string
from string import *

# CUSTOM

# PROJECT-SPECIFIC

###############################################################################
# __ALL__

# if hasattr(string, "__all__"):
#     __all__ += string.__all__
# else:
#     __all__ += list(dir(string))


###############################################################################
# CODE
###############################################################################


class FormatTemplate(string.Template):
    """Make Template with string in Template, not `.format`, syntax.

    Examples
    --------
    >>> s = FormatTemplate('$a ${b} {c}')
    >>> s.format(a=1, b=2, c=3)
    '1 2 3'

    """

    def __init__(self, s):
        r"""Make Template with string in Template, not `.format`, syntax.

        Examples
        --------
        >>> re.sub(r"(?<!\$)({)", r"${", '$a ${b} {c}')
        '$a ${b} ${c}'

        """
        s = re.sub(r"(?<!\$)({)", r"${", s)  # replace '{' with '${'
        super().__init__(s)

    # /def

    def format(self, *args, **kw):
        """Format str.

        proxy for safe_substitute.

        """
        return self.safe_substitute(*args, **kw)

    # /def

    def __str__(self):
        """Return a string with str()."""
        return self.safe_substitute()

    # /def


# /class


###############################################################################
# END
