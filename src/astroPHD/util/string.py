# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   :
# AUTHOR  :
# PROJECT :
#
# ----------------------------------------------------------------------------

# Docstring
"""**DOCSTRING**.

description

"""

__author__ = "Nathaniel Starkman"
# __copyright__ = "Copyright 2019, "
# __credits__ = [""]
# __license__ = "MIT"
# __version__ = "0.0.0"
# __maintainer__ = ""
# __email__ = ""
# __status__ = "Production"

# __all__ = [
#     ""
# ]


###############################################################################
# IMPORTS

# GENERAL
import string
import re

# CUSTOM

# PROJECT-SPECIFIC


###############################################################################
# CODE
###############################################################################


class FormatTemplate(string.Template):
    """Make Template with string in Template, not `.format`, syntax.

    Examples
    --------
    >>> re.sub('$a ${b} {c}', r'${', s)
    '$a ${b} ${c}'

    """

    def __new__(cls, s):
        """Make Template with string in Template, not `.format`, syntax.

        Examples
        --------
        >>> re.sub('$a ${b} {c}', r'${', s)
        '$a ${b} ${c}'

        """
        s = re.sub(r'(?<!\$)({)', r'${', s)  # replace '{' with '${'
        return string.Template(s)

    # /def

# /class


###############################################################################
# END
