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

Code modified From [galpy](https://galpy.readthedocs.io/en/v1.5.0/)
"""

import os
from os import path
try:
    import configparser
except:  # pragma: no cover
    from six.moves import configparser

##############################################################################

# The default configuration
default_configuration = {'verbosity': {'verbose-imports': 'True',
                                       'warnings': 'True'},
                         'plot': {'seaborn-defaults': 'False', }
                         }

default_filename = os.path.join(os.path.expanduser('~'), '.astroPHDrc')


##############################################################################

def check_config(configuration):
    """Check that the configuration is a valid astroPHD configuration."""
    for sec_key in default_configuration.keys():
        if not configuration.has_section(sec_key):
            return False
        for key in default_configuration[sec_key]:
            if not configuration.has_option(sec_key, key):
                return False
    return True
# /def


def write_config(filename, configuration=None):
    """Write configuration."""
    # Writes default if configuration is None
    writeconfig = configparser.ConfigParser()
    # Write different sections
    for sec_key in default_configuration.keys():
        writeconfig.add_section(sec_key)
        for key in default_configuration[sec_key]:
            if configuration is None \
                    or not configuration.has_section(sec_key) \
                    or not configuration.has_option(sec_key, key):
                writeconfig.set(sec_key, key,
                                default_configuration[sec_key][key])
            else:
                writeconfig.set(sec_key, key, configuration.get(sec_key, key))
    with open(filename, 'w') as configfile:
        writeconfig.write(configfile)
    return None
# /def


##############################################################################

# Read the configuration file
__config__ = configparser.ConfigParser()
cfilename = __config__.read('.astroPHDrc')
if not cfilename:
    cfilename = __config__.read(default_filename)
    if not cfilename:
        write_config(default_filename)
        __config__.read(default_filename)
if not check_config(__config__):
    write_config(cfilename[-1], __config__)
    __config__.read(cfilename[-1])


##############################################################################
# Set configuration variables on the fly

def set_import_verbosity(key: (bool, {'True', 'False'})):
    """Set whether the full import information is printed or not."""
    assert str(key) in ('True', 'False')
    __config__.set('verbosity', 'verbose-imports', str(key))
# /def


def set_warnings_verbosity(key: (bool, str)):
    """Set warnings verbosity."""
    assert str(key) in ('True', 'False')
    __config__.set('verbosity', 'warnings', str(key))
# /def
