==========
Change log
==========

2.0 (2017-03-20)
================

Backwards incompatible changes
------------------------------

- A value pseudonymized by ``text()`` no longer contains full stops, they are
  converted to spaces. Thus the pseudonymized values may change since version
  1.1. (``string()`` now has the former behavior of ``text()``, see below.)

- ``email()``  now returns its result in all lower case.

Features
--------

- Add ``string()`` pseudonymizer returning a string containing numbers, digits
  and full stops. (This is what ``text()`` formerly did.)

Bug fixes
---------

- Fix all pseudonymizers: if called with a value which evaluates to `False` the
  value is returned. But ``integer()`` still pseudonymizes `0`.

- Fix ``email()`` so it does not break on an input value which does not contain
  an `@` symbol.


1.1 (2017-03-16)
================

- Add ``street()`` pseudonymizer.

- Add ``bic()`` (business identifier code) pseudonymizer.


1.0 (2017-03-16)
================

New features
------------

- Add ``name()`` pseudonymizer.

Other changes
-------------

- Claim support for PyPy.

- Officially support Python 3.4, 3.5 and 3.6.

- Bring test coverage to 100 % even for code branches and enforce it for the
  future.

- Re-license from ZPL to MIT.


0.4.1 (2014-01-14)
==================

- Fix handling of usage of glibc2 supported additional encryption algorithms (
  signalled using $<id>$<salt>$ as salt).


0.4 (2014-01-14)
================

- Bugfix: ``text()`` pseudonymizer now works as expected for texts longer
  than 11 bytes. Previously it returned an 11 byte result for longer texts
  ignoring the part after the 11th byte (default behavior of the used
  ``crypt`` implementation). (#1296)

- Fixed handling of `Extended crypt` (signalled by starting the salt with an
  underscore): Salt is now correctly stripped from result. **Caution:** This
  leads to different pseudonymization results when using a secret starting
  with underscore than in version 0.3.


0.3 (2013-10-09)
================

- Fix tests in documentation + testing documentation now.

- Add new pseudonymizers:

  - ``datestring()``

  - ``day()``

  - ``month()``

  - ``year()``

- **Caution:** Due to changed implementation of the ``date()`` function it
  returns different values than in version 0.2.


0.2 (2013-09-06)
================

- ``date()`` does not return pseudonymized years smaller than `1900` anymore as
  ``datetime.date`` can not handle years smaller that `1900`.


0.1 (2013-09-05)
================

- Initial release.
