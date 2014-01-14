# -*- coding: utf-8 -*-
# Copyright (c) 2013 gocept gmbh & co. kg
# See also LICENSE.txt
import mock
import pytest


def pseudo(value, pseudonymizer, secret=None, length=None, **kw):
    secret = 'ML' if secret is None else secret
    if isinstance(value, str):
        length = len(value) if length is None else length
    return pseudonymizer(value, secret, length, **kw)


def test_text_pseudonymization_uses_length_of_input():
    from gocept.pseudonymize import text
    assert len('foobar') == len(text('foobar', 'secret'))


def test_text_pseudonymization_uses_length_of_input_even_for_longer_texts():
    from gocept.pseudonymize import text
    data = 'Lorem ipsum dolor sit amet, consectetur, adipisci velit, ...'
    assert len(data) == len(text(data, 'secret'))


def test_text_pseudonymization_returns_different_results_for_longer_texts():
    from gocept.pseudonymize import text
    data1 = 'Lorem ipsum dolor sit amet, consectetur, adipisci velit, ..1'
    data2 = 'Lorem ipsum dolor sit amet, consectetur, adipisci velit, ..2'
    assert text(data1, 'secret') != text(data2, 'secret')


def test_removes_secret_from_pseudonymization_result_traditional():
    from gocept.pseudonymize import text
    with mock.patch('crypt.crypt') as crypt:
        crypt.return_value = 'STpseudonymized'
        assert 'pseudonymized' == text('asdf', 'ST', size=13)


def test_removes_secret_from_pseudonymization_result_extended():
    from gocept.pseudonymize import text
    with mock.patch('crypt.crypt') as crypt:
        crypt.return_value = '_123SALTpseudonymized'
        assert 'pseudonymized' == text('asdf', '_123SALT', size=13)


def test_removes_secret_from_pseudonymization_result_glibc2():
    from gocept.pseudonymize import text
    with mock.patch('crypt.crypt') as crypt:
        crypt.return_value = '$5$SALT$pseudonymized'
        assert 'pseudonymized' == text('asdf', '$5$SALT$', size=13)


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
    assert date(7676, 1, 25) == pseudo(date(1983, 1, 11), p)


def test_day():
    from gocept.pseudonymize import day
    assert 11 == pseudo(15, day)


def test_month():
    from gocept.pseudonymize import month
    assert 3 == pseudo(11, month)


def test_year():
    from gocept.pseudonymize import year
    assert 8699 == pseudo(1976, year)


def test_year_computes_value_greater_than_1900():
    from gocept.pseudonymize import year
    from datetime import date
    with mock.patch('crypt.crypt') as crypt:
        crypt.return_value = '1899'
        assert 1999 == pseudo(1983, year)


def test_datestring():
    from gocept.pseudonymize import datestring
    assert '21.03.7110' == pseudo(
        '03.05.2003', datestring, format='DD.MM.YYYY')


def test_datestring_returns_zero_parts_as_zero():
    from gocept.pseudonymize import datestring
    assert '00007110' == pseudo('00002003', datestring, format='DDMMYYYY')
    assert '22100000' == pseudo('20030000', datestring, format='DDMMYYYY')


def test_datestring_raises_exception_on_invalid_format():
    from gocept.pseudonymize import datestring
    with pytest.raises(AssertionError):
        pseudo('000020', datestring, format='DDMMYY')
