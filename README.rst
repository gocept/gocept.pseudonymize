===================
gocept.pseudonymize
===================

This package provides helper functions to pseudonymize data like text,
integers, email addresses or license tags.

It uses the ``crypt.crypt()`` function for pseudonymization, which means,
longer text blocks require multiple ``crypt.crypt()`` calls.


Usage
=====

``gocept.pseudonymize`` provides single functions for pseudonymization of
various data types. Each function takes the ``value``, which should be
pseudonymized, and a ``secret``, which is passed as a ``salt`` to the
``crypt`` module.  If ``secret`` and ``value`` do not change the
pseudonymize function returns the exact same result when called again::

    >>> import gocept.pseudonymize
    >>> gocept.pseudonymize.text('Here is my little text', 'secret')
    'u7YJWz RqdYkfNUFgZii2Y'
    >>> gocept.pseudonymize.text('Here is my little text', 'secret')
    'u7YJWz RqdYkfNUFgZii2Y'

The result has always the same string length as the input. But there is no
guaranty that it is still valid in the domain of the input value. For
example the checksum of the pseudonymized IBAN is not correct.


This package is tested to be compatible with Python version 2.7 and 3.3.


Detailed usage examples
=======================

There are different pseudonymization function because it is not always
possible to guess the correct one by looking at the input data.

* For a name use the ``name`` function::

    >>> gocept.pseudonymize.name('Vimladil', 'secret')
    'R5lprkud'

* For an address consisting of street and house number use the ``street``
  function::

    >>> gocept.pseudonymize.street('Testweg 34a', 'secret')
    'Kui1xre 723'

* For an integer value use the ``integer`` function::

    >>> gocept.pseudonymize.integer(4711, 'secret')
    2111

* For a decimal value use the ``decimal`` function::

    >>> from decimal import Decimal
    >>> gocept.pseudonymize.decimal(Decimal('-123.45'), 'secret')
    Decimal('-8772.11')

* For an email address use the ``email`` function::

    >>> gocept.pseudonymize.email('mail@gocept.com', 'secret')
    'w6ba@ng7ngno.de'

* For an IBAN account number use the ``iban`` function::

    >>> gocept.pseudonymize.iban('US00123456787650047623', 'secret')
    'DE10312010975100119998'

* For a BIC (Business Identifier Code) use the ``bic`` function::

    >>> gocept.pseudonymize.bic('PBNKDEFFXXX', 'secret')
    'GTY1BPG8PE2'

* For a license tag of a car use  the ``license_tag`` function::

    >>> gocept.pseudonymize.license_tag('HAL-AB 123', 'secret')
    'PUD-AM 117'

* For a phone number use the ``phone`` function::

    >>> gocept.pseudonymize.phone('+49 172 34123142', 'secret')
    '0104118118111676'

* For a date use the ``date`` function::

    >>> from datetime import date
    >>> gocept.pseudonymize.date(date(1983, 1, 11), 'secret')
    datetime.date(3021, 1, 18)

* For a date represented as string use the ``datestring`` function. It takes
  a format string and keeps zeros date parts as zero.::

    >>> gocept.pseudonymize.datestring('00/03/2003', 'secret', format='DD/MM/YYYY')
    '00/10/7399'

* For a time value use the ``time`` function::

    >>> from datetime import time
    >>> gocept.pseudonymize.time(time(23, 59, 59), 'secret')
    datetime.time(13, 11, 49)

There are some additional pseudonymizer functions and helper functions in
this package.
