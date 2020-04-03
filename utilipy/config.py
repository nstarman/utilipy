# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : config
# PROJECT : utilipy
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Configuration settings for `utilipy`.

TODO
----
Adopt astropy affiliate package configuration style.

"""

__author__ = "Nathaniel Starkman"

__all__ = [
    "__config__",
    "_DEFAULT_CONFIG",
    "_DEFAULT_FILE",
    "check_config",
    "write_config",
    "get_import_verbosity",
    "set_import_verbosity",
    "use_import_verbosity",
    "get_warnings_verbosity",
    "set_warnings_verbosity",
    "use_warnings_verbosity",
    "get_frozen_constants",
    "set_frozen_constants",
    "use_frozen_constants",
    "cfilename",
]


##############################################################################
# IMPORTS

from typing import Union, Any, Optional, Dict
from typing_extensions import Literal
import os.path
from configparser import ConfigParser


##############################################################################
# DEFAULT CONFIGURATION

# The default configuration
_DEFAULT_CONFIG: Dict[str, Union[str, Dict[str, str]]] = {
    "verbosity": {"verbose-imports": "True", "warnings": "True"},
    "plot": {"seaborn-defaults": "False"},
    "util": {"frozen-constants": "True"},
}

_DEFAULT_FILE: str = os.path.join(os.path.expanduser("~"), ".utilipyrc")


##############################################################################
# PARAMETERS

__config__ = ConfigParser()


##############################################################################


def check_config(configuration: ConfigParser) -> bool:
    """Check that the configuration is a valid utilipy configuration.

    Parameters
    ----------
    configuration: ConfigParser
        the configuration file

    Returns
    -------
    bool
        whether the configuration is a valid utilipy configuration.

    """
    sec_key: str
    for sec_key in _DEFAULT_CONFIG.keys():  # iter through expected keys
        # check if section exists
        if not configuration.has_section(sec_key):
            return False
        # check if options within section exist
        for key in _DEFAULT_CONFIG[sec_key]:
            if not configuration.has_option(sec_key, key):
                return False

    return True


# /def


def write_config(
    filename: str, configuration: Optional[ConfigParser] = None
) -> None:
    """Write configuration.

    Parameters
    ----------
    filename: str
    configuration: ConfigParser, optional
        configuration to draw from
        defaults to `_DEFAULT_CONFIG` if not in `configuration`

    """
    # Writes default if configuration is None
    writeconfig = ConfigParser()

    # Write different sections
    sec_key: str
    for sec_key in _DEFAULT_CONFIG.keys():
        writeconfig.add_section(sec_key)
        for key in _DEFAULT_CONFIG[sec_key]:
            if configuration is None:
                writeconfig.set(sec_key, key, _DEFAULT_CONFIG[sec_key][key])
            elif not configuration.has_section(
                sec_key
            ) or not configuration.has_option(sec_key, key):
                writeconfig.set(sec_key, key, _DEFAULT_CONFIG[sec_key][key])
            else:
                writeconfig.set(sec_key, key, configuration.get(sec_key, key))

    with open(filename, "w") as configfile:
        writeconfig.write(configfile)

    return None


# /def


##############################################################################
# Set configuration variables on the fly


def get_import_verbosity() -> bool:
    """Get whether the full import information is printed or not."""
    return __config__.getboolean("verbosity", "verbose-imports")


# /def


def set_import_verbosity(
    verbosity: Union[bool, Literal["True", "False"]]
) -> None:
    """Set whether the full import information is printed or not."""
    assert str(verbosity) in {"True", "False"}, f"{str(verbosity)}"
    __config__.set("verbosity", "verbose-imports", str(verbosity))
    return


# /def


class use_import_verbosity:
    """Docstring for use_import_verbosity."""

    def __init__(
        self, verbosity: Union[bool, Literal["True", "False"]]
    ) -> None:
        """__init__."""
        self.original_verbosity = get_import_verbosity()
        self.verbosity = verbosity
        return

    # /def

    def __enter__(self):
        """Enter with statement, using specified import verbosity."""
        if self.verbosity is not None:
            set_import_verbosity(self.verbosity)
        return self

    # /def

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        """Exit  with statement, restoring original import verbosity."""
        # Exception handling here
        traceback  # pragma: no cover
        set_import_verbosity(self.original_verbosity)
        return

    # /def


# ----------------------------------------------------------------------------


def get_warnings_verbosity() -> bool:
    """Get warnings verbosity."""
    return __config__.getboolean("verbosity", "warnings")


# /def


def set_warnings_verbosity(key: Union[bool, str]) -> None:
    """Set warnings verbosity."""
    assert str(key) in {"True", "False"}
    __config__.set("verbosity", "warnings", str(key))
    return


# /def


class use_warnings_verbosity:
    """Docstring for use_warnings_verbosity."""

    def __init__(self, verbosity: Optional[bool] = None) -> None:
        """__init__."""
        self.original_state = get_warnings_verbosity()
        self.state = verbosity
        return

    # /def

    def __enter__(self) -> Any:
        """Enter with statement, using specified import verbosity."""
        if self.state is not None:
            set_warnings_verbosity(self.state)
        return self

    # /def

    def __exit__(self, type, value, traceback) -> None:
        """Exit  with statement, restoring original import verbosity."""
        # Exception handling here
        set_warnings_verbosity(self.original_state)
        return

    # /def


# ----------------------------------------------------------------------------


def get_frozen_constants() -> bool:
    """Get warnings verbosity."""
    return __config__.getboolean("util", "frozen-constants")


# /def


def set_frozen_constants(key: Union[bool, str]) -> None:
    """Set warnings verbosity."""
    assert str(key) in {"True", "False"}
    __config__.set("util", "frozen-constants", str(key))
    return


# /def


class use_frozen_constants:
    """docstring for use_frozen_constants."""

    def __init__(self, frozen: Optional[bool] = None) -> None:
        """__init__."""
        self.original_state = get_frozen_constants()
        self.state = frozen
        return

    # /def

    def __enter__(self) -> Any:
        """Enter with statement, using specified state."""
        if self.state is not None:
            set_frozen_constants(self.state)
        return self

    # /def

    def __exit__(self, type, value, traceback) -> None:
        """Exit  with statement, restoring original state."""
        # Exception handling here
        set_frozen_constants(self.original_state)
        return

    # /def


##############################################################################
# RUNNING

# Read the local configuration file
cfilename = __config__.read(".utilipyrc")

# if it doesn't exist
if not cfilename:
    cfilename = __config__.read(_DEFAULT_FILE)  # read default config
    if not cfilename:  # no default config
        write_config(_DEFAULT_FILE)  # make default config
        __config__.read(_DEFAULT_FILE)  # and read in

# check config is valid
if not check_config(__config__):
    write_config(cfilename[-1], __config__)
    __config__.read(cfilename[-1])


##############################################################################
# END
