# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : config
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Configuration settings for astroPHD.

References
----------
Code modified from galpy ([#]_).

.. [#] galpy: A Python Library for Galactic Dynamics, Jo Bovy (2015),
    Astrophys. J. Supp., 216, 29 (arXiv/1412.3451).

"""

__author__ = 'Nathaniel Starkman'
__credit__ = 'Jo Bovy'


##############################################################################
# IMPORTS

from typing import Union, Any, Optional
from typing_extensions import Literal
import os
from os import path
import configparser

##############################################################################
# DEFAULT CONFIGURATION

# The default configuration
_DEFAULT_CONFIG = {
    'verbosity': {'verbose-imports': 'True',
                  'warnings': 'True'},
    'plot': {'seaborn-defaults': 'False', }
}

_DEFAULT_FILE = os.path.join(os.path.expanduser('~'), '.astroPHDrc')


##############################################################################

def check_config(configuration: configparser.ConfigParser) -> bool:
    """Check that the configuration is a valid astroPHD configuration.

    Parameters
    ----------
    configuration: configparser.ConfigParser
        the configuration file

    Returns
    -------
    bool
        whether the configuration is a valid astroPHD configuration.

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


def write_config(filename: str,
                 configuration:Optional[configparser.ConfigParser]=None) -> None:
    """Write configuration.

    Parameters
    ----------
    filename: str
    configuration: None or configparser.ConfigParser
        configuration to draw from
        defaults to `_DEFAULT_CONFIG` if not in `configuration`

    """
    # Writes default if configuration is None
    writeconfig = configparser.ConfigParser()

    # Write different sections
    for sec_key in _DEFAULT_CONFIG.keys():
        writeconfig.add_section(sec_key)
        for key in _DEFAULT_CONFIG[sec_key]:
            if configuration is None:                    
                writeconfig.set(sec_key, key,
                                _DEFAULT_CONFIG[sec_key][key])
            elif (not configuration.has_section(sec_key) or
                  not configuration.has_option(sec_key, key)):
                writeconfig.set(sec_key, key,
                                _DEFAULT_CONFIG[sec_key][key])
            else:
                writeconfig.set(sec_key, key, configuration.get(sec_key, key))

    with open(filename, 'w') as configfile:
        writeconfig.write(configfile)

    return None
# /def


##############################################################################
# Set configuration variables on the fly

def get_import_verbosity() -> bool:
    """Get whether the full import information is printed or not."""
    return __config__.getboolean('verbosity', 'verbose-imports')
# /def


def set_import_verbosity(verbosity: Union[bool, Literal['True'], Literal['False']]) -> None:
    """Set whether the full import information is printed or not."""
    assert str(verbosity) in {'True', 'False'}
    __config__.set('verbosity', 'verbose-imports', str(verbosity))
    return
# /def


class use_import_verbosity:
    """Docstring for use_import_verbosity."""

    def __init__(self, verbosity: Optional[bool]) -> None:
        """__init__."""
        self.original_verbosity = get_import_verbosity()
        self.verbosity = verbosity
        return
    # /def

    def __enter__(self) -> Any:
        """Enter with statement, using specified import verbosity."""
        if self.verbosity is not None:
            set_import_verbosity(self.verbosity)
        return self
    # /def

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        """Exit  with statement, restoring original import verbosity."""
        # Exception handling here
        set_import_verbosity(self.original_verbosity)
        return
    # /def


# ----------------------------------------------------------------------------

def get_warnings_verbosity() -> None:
    """Get warnings verbosity."""
    __config__.get('verbosity', 'warnings')
    return
# /def


def set_warnings_verbosity(key: Union[bool, str]) -> None:
    """Set warnings verbosity."""
    assert str(key) in {'True', 'False'}
    __config__.set('verbosity', 'warnings', str(key))
    return
# /def


class use_warnings_verbosity:
    """Docstring for use_warnings_verbosity."""

    def __init__(self, verbosity: bool) -> None:
        """__init__."""
        self.original_verbosity = get_import_verbosity()
        self.verbosity = verbosity
        return
    # /def

    def __enter__(self) -> Any:
        """Enter with statement, using specified import verbosity."""
        if self.verbosity is not None:
            set_warnings_verbosity(self.verbosity)
        return self
    # /def

    def __exit__(self, type, value, traceback) -> None:
        """Exit  with statement, restoring original import verbosity."""
        # Exception handling here
        set_warnings_verbosity(self.original_verbosity)
        return
    # /def


##############################################################################
# RUNNING


# Read the configuration file
__config__ = configparser.ConfigParser()
cfilename = __config__.read('.astroPHDrc')

if not cfilename:
    cfilename = __config__.read(_DEFAULT_FILE)
    if not cfilename:
        write_config(_DEFAULT_FILE)
        __config__.read(_DEFAULT_FILE)

if not check_config(__config__):
    write_config(cfilename[-1], __config__)
    __config__.read(cfilename[-1])


##############################################################################
# END
