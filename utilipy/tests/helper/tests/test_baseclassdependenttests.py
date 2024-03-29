# -*- coding: utf-8 -*-

"""Tests for `~utilipy.tests.helper.BaseClassDependentTests`."""

__all__ = [
    "Test_BaseClassDependentTests",
]


##############################################################################
# IMPORTS

# THIRD PARTY
import pytest

# PROJECT-SPECIFIC
from utilipy.tests import helper

##############################################################################
# CODE
##############################################################################


class Test_BaseClassDependentTests:
    """Test `~utilipy.tests.helper.BaseClassDependentTests`."""

    @classmethod
    def setup_class(cls):
        """Setup fixtures for testing."""
        cls.klass = helper.BaseClassDependentTests

    # /def

    def test_fail_make_subclass(self):
        """Test make subclass without passing klass."""
        with pytest.raises(TypeError) as e:
            # make class
            class SubClass(helper.BaseClassDependentTests):
                pass

        assert "klass" in str(e.value)

    # /def

    def test_make_subclass(self):
        """Test make subclass with klass."""

        # make class
        class SubClass(helper.BaseClassDependentTests, klass=int):
            pass

        # tests
        assert SubClass.klass is int

        subclass = SubClass()
        assert subclass.klass == int

    # /def

    def test_fail_make_subsubclass(self):
        """Test make subclass without passing klass."""

        # make class
        class SubClass(helper.BaseClassDependentTests, klass=int):
            pass

        with pytest.raises(TypeError) as e:

            class SubSubClass(SubClass):
                pass

        assert "klass" in str(e.value)

    # /def

    def test_make_subsubclass(self):
        """Test make sub-subclass with klass."""

        # make class
        class SubClass(helper.BaseClassDependentTests, klass=int):
            pass

        # make subclass
        class SubSubClass(SubClass, klass=int):
            pass

        # tests
        assert SubSubClass.klass is int

        subsubclass = SubSubClass()
        assert subsubclass.klass == int

    # /def


# /class


# -------------------------------------------------------------------


##############################################################################
# END
