==========
Change Log
==========

2.0b1 (11 March 2021)
=====================

- Backwards Incompatible: Migrated backend to ``pydantic``.
  - ``Value`` is replaced by the `Field function <https://pydantic-docs.helpmanual.io/usage/schema/#field-customisation>`__.
    ``help`` is now ``description``
  - ``GoodConf`` is now backed by `BaseSettings <https://pydantic-docs.helpmanual.io/usage/settings/>`__
    Instead of passing keyword args when instantiating the class, they are now defined on a ``Config`` class on the object



1.0.0 (18 July 2018)
====================

- Allow overriding of values in the generate_* methods
- Python 3.7 supported


0.9.1 (10 April 2018)
=====================

- Explicit ``load`` method
- ``django_manage`` method helper on ``GoodConf``
- Fixed a few minor bugs


0.9.0 (8 April 2018)
====================

- Use a declarative class to define GoodConf's values.

- Change description to a docstring of the class.

- Remove the redundant ``required`` argument from ``Values``. To make
  an value optional, give it a default.

- Changed implicit loading to happen during instanciation rather than first
  access. Instanciate with ``load=False`` to avoid loading config initially.

0.8.3 (28 Mar 2018)
===================

- Implicitly load config if not loaded by first access.

0.8.2 (28 Mar 2018)
===================

- ``-c`` is used by Django's ``collectstatic``. Using ``-C`` instead.

0.8.1 (28 Mar 2018)
===================

- Adds ``goodconf.contrib.argparse`` to add a config argument to an existing
  parser.

0.8.0 (27 Mar 2018)
===================

- Major refactor from ``file-or-env`` to ``goodconf``

0.6.1 (16 Mar 2018)
================

- Fixed packaging issue.

0.6.0 (16 Mar 2018)
================

- Fixes bug in stack traversal to find calling file.


0.5.1 (15 March 2018)
==================

- Initial release
