# -*- coding: utf-8 -*-
# Copyright (c) 2013 gocept gmbh & co. kg
# See also LICENSE.txt

from decimal import Decimal
import crypt
import datetime


def _pseudonymize(text, secret):
    """Pseudonymize a `text` using `secret`."""
    result = []
    for start in range(0, len(text), 11):
        # crypt ignores the text after the 11th byte so we have to split the
        # string into 11 byte blocks
        block = text[start:start + 11]
        crypted = crypt.crypt(block, secret)
        if crypted.startswith('$'):
            # Usage of different hash algorithm: digets in $ signs
            digits, crypted = crypted[1:].split('$')
            digits = int(digits)
        elif secret.startswith('_'):
            # Behavior of Extended crypt: use up to eight bytes of salt
            digits = min(len(secret), 8)
        else:
            # Behaviour for Traditional crypt: use first 2 bytes of salt
            digits = 2
        result.append(crypted[digits:])
    return ''.join(result)


def text(value, secret, size=None):
    result = _pseudonymize(value, secret)
    if size is None:
        size = len(value)
    return result[0:size].replace('/', '.')


def integer(value, secret, size=None):
    if size is None:
        size = len(str(value))
    value = text(str(value), secret, size)
    result = ''
    for char in value:
        try:
            result += str(int(char))
        except ValueError:
            result += str(ord(char))
    return int(result[:size])


def email(value, secret, size=None):
    local, domain = value.split('@')
    return '%s@%s.de' % (text(local, secret, len(local)),
                         text(domain, secret, len(domain)-3))


def iban(value, secret, size=None):
    return 'DE%s' % str(integer(value[2:], secret, len(value)))[:20]


def phone(value, secret, size=None):
    return '0%s' % integer(value, secret, len(value)-1)


def license_tag(value, secret, size=None):
    """License tag of a car."""
    blocks = value.split(' ')
    for i, block in enumerate(blocks):
        subblocks = block.split('-')
        for j, subblock in enumerate(subblocks):
            try:
                int(subblock)
            except ValueError:
                subblocks[j] = text(
                    subblock, secret, len(subblock)).upper()
            else:
                subblocks[j] = str(integer(subblock, secret))
        blocks[i] = '-'.join(subblocks)
    return ' '.join(blocks)


def decimal(value, secret, size=None):
    value = value.to_eng_string()
    if '-' in value:
        negative = True
    else:
        negative = False
    integral, fractional = value.split('.')
    integral = str(integer(integral, secret))
    fractional = str(integer(fractional, secret))
    value = '.'.join([integral, fractional])
    if negative:
        value = '-' + value
    return Decimal(value)


def day(value, secret, size=None):
    day = integer(value, secret)
    if day > 28:
        day = int(day / 4)
    if day == 0:
        day = 1
    return day


def month(value, secret, size=None):
    month = integer(value, secret)
    if month > 12:
        month = int(month / 8)
    if month == 0:
        month = 1
    return month


def year(value, secret, size=None):
    year = integer(value, secret)
    if year < 1900:
        year = year + 1900
    return year


def date(value, secret, size=None):
    return datetime.date(year(value.year, secret),
                         month(value.month, secret),
                         day(value.day, secret))


def datestring(value, secret, size=None, format='DD.MM.YYYY'):
    """Date represended as a string.

    Parts of the date which are 0 are kept zero. (e. g. if the day is '00'
    it is not pseudonymized)

    """
    value = list(value)
    for part, length, func in (('D', 2, day), ('M', 2, month), ('Y', 4, year)):
        assert format.count(part) == length
        start_pos = format.find(part)
        val = value[start_pos:start_pos+length]
        if val != ['0'] * length:
            value[start_pos:start_pos+length] = list(
                str(func(''.join(val), secret)).zfill(length))
    return ''.join(value)


def time(value, secret, size=None):
    value = str(integer(value.strftime('%H%M%S'), secret)).zfill(6)
    hour, minute, second = (
        int(value[:2]), int(value[2:4]), int(value[4:]))
    if hour > 23:
        hour = int(hour / 5)
    if minute > 59:
        minute = int(minute/2)
    if second > 59:
        second = int(second / 2)
    return datetime.time(hour, minute, second)
