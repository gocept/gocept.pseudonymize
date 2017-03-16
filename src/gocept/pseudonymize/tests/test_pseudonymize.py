# -*- coding: utf-8 -*-
import gocept.pseudonymize
import mock
import pytest


def pseudo(value, pseudonymizer, secret=None, length=None, **kw):
    secret = 'ML' if secret is None else secret
    if isinstance(value, str):
        length = len(value) if length is None else length
    return pseudonymizer(value, secret, length, **kw)


@pytest.mark.parametrize(
    'func_name', [
        x for x in dir(gocept.pseudonymize)
        if not x.startswith('_') and x not in ('tests', 'pseudonymize')])
def test_pseudonymize__1(func_name):
    """It returns an empty string if called with an empty string."""
    assert '' == pseudo('', getattr(gocept.pseudonymize, func_name))
    assert None is pseudo(None, getattr(gocept.pseudonymize, func_name))


def test_text_pseudonymization_uses_length_of_input():
    from gocept.pseudonymize import text
    assert len('foobar') == len(text('foobar', 'secret'))


def test_text_pseudonymization_uses_length_of_input_even_for_longer_texts():
    from gocept.pseudonymize import text
    data = 'Lorem ipsum dolor sit amet, consectetur, adipisci velit, ...'
    assert len(data) == len(text(data, 'secret'))
    assert ('qDJkMNOo1F 3WpbRcD VnIW9w24N 03hES80hJIs9kGs wNTboQvYTk A9S0' ==
            text(data, 'secret'))


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


def test_pseudonymize__name__1():
    """It returns pseudonymized text with only first letter a capital one."""
    from gocept.pseudonymize import name
    assert 'Zg9knqus4gu' == pseudo('Deutschland', name)


def test_pseudonymize__street__1():
    """It returns pseudonymized name and number."""
    from gocept.pseudonymize import street
    assert 'Tgixm4xn0u 657' == pseudo('Oberer Weg 34b', street)


def test_pseudonymize__street__2():
    """It omits a not existing number."""
    from gocept.pseudonymize import street
    assert ('Jaktrnwswyqr7wk92tsjum2abw' ==
            pseudo('Karl-Friedrich-Fischer-Weg', street))


def test_pseudonymize__integer__1():
    """It returns an integer of the same lenght."""
    from gocept.pseudonymize import integer
    assert 1029 == pseudo(4711, integer)


def test_pseudonymize__integer__2():
    """It pseudonymizes the value `0`."""
    from gocept.pseudonymize import integer
    assert 8 == pseudo(0, integer)


def test_pseudonymize__email__1():
    """It returns something what looks like an e-mail address."""
    from gocept.pseudonymize import email
    assert 'ir@7hklpuc.de' == pseudo('sw@gocept.com', email)


def test_pseudonymize__email__2():
    """It returns garbage if the input does not contain an `@` symbol."""
    from gocept.pseudonymize import email
    assert '1n2grmnobxk.p.de' == pseudo('sw-gocept.com', email)


def test_pseudonymize__iban__1():
    """It returns something what looks like an IBAN."""
    from gocept.pseudonymize import iban
    assert 'DE11912270187105821216' == pseudo('US00123456787650047623', iban)


def test_pseudonymize__bic__1():
    """It returns something what looks like a BIC."""
    from gocept.pseudonymize import bic
    assert 'JAJXFPRKNBW' == pseudo('BYLADEM1001', bic)


def test_pseudonymize__phone__1():
    """It returns a number starting with `0`."""
    from gocept.pseudonymize import phone
    assert '0791067988858' == pseudo('0172 34123142', phone)
    assert '0511911912178610' == pseudo('+49 172 34123142', phone)


def test_license_tags():
    from gocept.pseudonymize import license_tag as p
    assert 'Z1Y-YV 784' == pseudo('HAL-AB 123', p)


def test_decimal():
    from decimal import Decimal
    from gocept.pseudonymize import decimal as p
    assert Decimal('47.9010') == pseudo(Decimal('12.3456'), p)
    assert Decimal('-8799.11') == pseudo(Decimal('-123.45'), p)


def test_time():
    from gocept.pseudonymize import time as pseudo_time
    from datetime import time
    assert time(16, 36, 37) == pseudo(time(12, 34, 56), pseudo_time)
    assert time(11, 46, 49) == pseudo(time(23, 59, 59), pseudo_time)
    assert time(17, 10, 21) == pseudo(time(1, 1, 0), pseudo_time)


def test_date():
    from gocept.pseudonymize import date as p
    from datetime import date
    assert date(7676, 1, 25) == pseudo(date(1983, 1, 11), p)


def test_pseudonymize__day__1():
    """It makes sure that the pseudonymized day is not bigger than 28."""
    from gocept.pseudonymize import day
    assert 19 == pseudo(10, day)


def test_pseudonymize__day__2():
    """It replaces a pseudonymized value of 0 with 1."""
    from gocept.pseudonymize import day
    assert 1 == pseudo(6, day, secret='MH')


def test_month():
    from gocept.pseudonymize import month
    assert 3 == pseudo(11, month)


def test_year():
    from gocept.pseudonymize import year
    assert 8699 == pseudo(1976, year)


def test_year_computes_value_greater_than_1900():
    from gocept.pseudonymize import year
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
