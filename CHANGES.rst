1.0 (2020-04-01)
================

New Features
------------

Version 1.0 is a reboot of ``utilipy``, so all features can be considered new.

utilipy.config
^^^^^^^^^^^^^^

- ``utilipy`` has a config file ``.utilipyrc`` that governs import verbosity, 


API Changes
-----------

astropy.constants
^^^^^^^^^^^^^^^^^

- Deprecated ``set_enabled_constants`` context manager. Use
  ``astropy.physical_constants`` and ``astropy.astronomical_constants``.
  [#9025]


Bug Fixes
---------

astropy.coordinates
^^^^^^^^^^^^^^^^^^^

- The ``QuantityAttribute`` class now supports a None default value if a unit
  is specified. [#9345]



Other Changes and Additions
---------------------------

- Versions of Python <3.6 are no longer supported. [#8955]


Pre 1.0
=======