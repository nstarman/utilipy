# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE  : test config
#
# ----------------------------------------------------------------------------

"""Tests for config.py."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL
import os
from typing import Union, Dict
import configparser

# PROJECT-SPECIFIC
from utilipy import config  # TODO relative import

##############################################################################
# PARAMETERS

localrc = os.path.join(
    os.path.split(os.path.abspath(__file__))[0],  # absolute directory
    ".utilipyrc",  # RC file
)

# set config to local for testing
config.__config__ = configparser.ConfigParser()
config.__config__.read(localrc)


##############################################################################
# TEST FUNCTIONS
##############################################################################


def test_unchanged_DEFAULT_CONFIG():
    """Test _DEFAULT_CONFIG.

    test config._DEFAULT_CONFIG against a template

    """
    _DEFAULT_CONFIG: Dict[str, Union[str, Dict[str, str]]] = {
        "verbosity": {"verbose-imports": "True", "warnings": "True"},
        "plot": {"seaborn-defaults": "False"},
    }

    sec_key: str
    key: str
    for sec_key in _DEFAULT_CONFIG.keys():  # iter through expected keys
        # check if section exists
        assert config._DEFAULT_CONFIG.get(sec_key)
        # check if options within section exist
        for key in _DEFAULT_CONFIG[sec_key]:
            assert (
                config._DEFAULT_CONFIG[sec_key][key]
                == _DEFAULT_CONFIG[sec_key][key]
            )

    return


# /def


def test_has_DEFAULT_FILE():
    """Test _DEFAULT_FILE.

    .utilipyrc in home folder

    """
    file = os.path.join(os.path.expanduser("~"), ".utilipyrc")
    assert os.path.exists(file), "~/.utilipyrc doesn't exist"

    return


# /def


# def test_check_config():
#     return
# # /def


# def test_write_config():
#     return
# # /def


# --------------------------------------------------------------------------


def test_get_import_verbosity():
    """Test get_import_verbosity.

    All options set to true.

    """
    assert ~config.get_import_verbosity()
    return


# /def


def test_set_import_verbosity():
    """Test set_import_verbosity.

    Change to false

    """
    config.set_import_verbosity(False)
    assert not config.get_import_verbosity()
    return


# /def


def test_use_import_verbosity():
    """Test use_import_verbosity.

    Change to false

    """
    verbose = config.get_import_verbosity()

    with config.use_import_verbosity(bool(~verbose)):
        # test changed
        assert config.get_import_verbosity() == bool(~verbose)

    # test changed back
    assert config.get_import_verbosity() == verbose

    return


# /def


# --------------------------------------------------------------------------


def test_get_warnings_verbosity():
    """Test get_warnings_verbosity.

    All set to true

    """
    assert config.get_warnings_verbosity()
    return


# /def


def test_set_warnings_verbosity():
    """Test set_warnings_verbosity.

    Change to false

    """
    config.set_warnings_verbosity(False)
    assert not config.get_warnings_verbosity()
    return


# /def


def test_use_warnings_verbosity():
    """Test use_warnings_verbosity.

    Change to false

    """
    verbose = config.get_warnings_verbosity()

    with config.use_warnings_verbosity(bool(~verbose)):
        # test changed
        assert config.get_warnings_verbosity() == bool(~verbose)

    # test changed back
    assert config.get_warnings_verbosity() == verbose

    return


# /def


# --------------------------------------------------------------------------


def test_get_frozen_constants():
    """Test get_frozen_constants.

    All set to false

    """
    assert ~config.get_frozen_constants()
    return


# /def


def test_set_frozen_constants():
    """Test set_frozen_constants.

    Change to true

    """
    config.set_frozen_constants(True)
    assert config.get_frozen_constants()
    return


# /def


def test_use_frozen_constants():
    """Test use_frozen_constants.

    Change to true

    """
    frozen = config.get_frozen_constants()

    with config.use_frozen_constants(bool(~frozen)):
        # test changed
        assert config.get_frozen_constants() == bool(~frozen)

    # test changed back
    assert config.get_frozen_constants() == frozen

    return


# /def


##############################################################################
# Test Files


def test_valid_configurations():
    """Test check_config."""
    # test default file
    configuration = configparser.ConfigParser()
    configuration.read(config._DEFAULT_FILE)
    assert config.check_config(configuration), "config not valid"

    # test current file
    assert config.check_config(config.__config__), "config not valid"

    # test local test file
    configuration = configparser.ConfigParser()
    configuration.read(localrc)
    assert config.check_config(configuration), "config not valid"

    return


# /def


# --------------------------------------------------------------------------

# def test_write_config():
#     """Test write_config."""
#     # from tempfile import NamedTemporaryFile

#     # file = NamedTemporaryFile()
#     # config.write_config(file.name)

#     return
# # /def

##############################################################################
# END
