# -*- coding: utf-8 -*-
# Copyright (c) 2013 gocept gmbh & co. kg
# See also LICENSE.txt
import mock


def pseudo(value, pseudonymizer, secret=None, length=None):
    secret = 'ML' if secret is None else secret
    if isinstance(value, str):
        length = len(value) if length is None else length
    return pseudonymizer(value, secret, length)


def test_removes_secret_from_pseudonymization_result():
    from gocept.pseudonymize import text as p
    assert not pseudo('asdf', p).startswith('MT')
    with mock.patch('crypt.crypt') as crypt:
        crypt.return_value = '$3$FOOpseudonymized'
        assert 'pseudonymized' == pseudo('asdf', p, length=13)


def test_same_result_for_same_value_and_secret():
    from gocept.pseudonymize import text as p
    pseudo1 = pseudo('asdf', p)
    pseudo2 = pseudo('asdf', p)
    assert pseudo1 == pseudo2


def test_different_result_for_same_value_and_other_secret():
    from gocept.pseudonymize import text as p
    pseudo1 = pseudo('asdf', p, secret='ML')
    pseudo2 = pseudo('asdf', p, secret='SW')
    assert pseudo1 != pseudo2


def test_different_result_for_different_value_and_same_secret():
    from gocept.pseudonymize import text as p
    pseudo1 = pseudo('asdf', p)
    pseudo2 = pseudo('bsdf', p)
    assert pseudo1 != pseudo2


def test_different_result_for_different_value_and_different_secret():
    from gocept.pseudonymize import text as p
    pseudo1 = pseudo('asdf', p, secret='ML')
    pseudo2 = pseudo('bsdf', p, secret='SW')
    assert pseudo1 != pseudo2


def test_integer():
    from gocept.pseudonymize import integer as p
    assert 1029 == pseudo(4711, p)


def test_email_adresses():
    from gocept.pseudonymize import email as p
    assert 'iR@7HKlpUc.de' == pseudo('sw@gocept.com', p)


def test_ibans():
    from gocept.pseudonymize import iban as p
    assert 'DE11912270187105821216' == pseudo(
        'US00123456787650047623', p)


def test_phone_numbers():
    from gocept.pseudonymize import phone as p
    assert '0791067988858' == pseudo('0172 34123142', p)
    assert '0511911912178610' == pseudo('+49 172 34123142', p)


def test_license_tags():
    from gocept.pseudonymize import license_tag as p
    assert 'Z1Y-YV 784' == pseudo('HAL-AB 123', p)


def test_decimal():
    from decimal import Decimal
    from gocept.pseudonymize import decimal as p
    assert Decimal('47.9010') == pseudo(Decimal('12.3456'), p)
    assert Decimal('-8799.11') == pseudo(Decimal('-123.45'), p)


def test_time():
    from gocept.pseudonymize import time as p
    from datetime import time
    assert time(16, 36, 37) == pseudo(time(12, 34, 56), p)
    assert time(11, 46, 49) == pseudo(time(23, 59, 59), p)


def test_date():
    from gocept.pseudonymize import date as p
    from datetime import date
    assert date(9867, 7, 11) == pseudo(date(1983, 1, 11), p)


def test_date_computes_year_greater_than_1900():
    from gocept.pseudonymize import date as p
    from datetime import date
    with mock.patch('crypt.crypt') as crypt:
        crypt.return_value = '11011899'
        assert date(3799, 1, 1) == pseudo(date(1983, 1, 11), p)
