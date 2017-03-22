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
            # Usage of glibc2 additional  encryption algorithm, notation is:
            # $id$salt$encrypted
            _, _, _, crypted = crypted.split('$')
            digits = 0
        elif secret.startswith('_'):
            # Behavior of Extended crypt: use up to eight bytes of salt
            digits = min(len(secret), 8)
        else:
            # Behaviour for Traditional crypt: use first 2 bytes of salt
            digits = 2
        result.append(crypted[digits:])
    return ''.join(result)


def string(value, secret, size=None):
    """Pseudonymize as string. Contains [A-Za-z0-9.]."""
    if not value:
        return value
    result = _pseudonymize(value, secret)
    if size is None:
        size = len(value)
    return result[0:size].replace('/', '.')


def text(value, secret, size=None):
    """Pseudonymize text. Contains letter, numbers and spaces."""
    if not value:
        return value
    return string(value, secret, size).replace('.', ' ')


def name(value, secret, size=None):
    """A name is a text which has only one capital letter as the first one."""
    if not value:
        return value
    result = text(value, secret, size)
    return result[0].upper() + result[1:].lower()


def street(value, secret, size=None):
    """A street is a name (maybe containing spaces) followed by a number."""
    if not value:
        return value
    source_name, sep, source_value = value.rpartition(' ')
    if not source_name:
        source_name = source_value
        source_value = ''
    return sep.join(
        [name(source_name, secret), str(integer(source_value, secret))])


def integer(value, secret, size=None):
    if not value and value != 0:
        return value
    if size is None:
        size = len(str(value))
    value = string(str(value), secret, size)
    result = ''
    for char in value:
        try:
            result += str(int(char))
        except ValueError:
            result += str(ord(char))
    return int(result[:size])


def email(value, secret, size=None):
    """Return something what could be an e-mail address."""
    if not value:
        return value
    local, at, domain = value.partition('@')
    return '%s%s%s.de' % (string(local, secret, len(local)).lower(),
                          at,
                          string(domain, secret, len(domain) - 3).lower())


def iban(value, secret, size=None):
    if not value:
        return value
    return 'DE%s' % str(integer(value[2:], secret, len(value)))[:20]


def bic(value, secret, size=None):
    """Return something what looks mostly like a BIC."""
    if not value:
        return value
    return string(value, secret, size).upper().replace('/', '0')


def phone(value, secret, size=None):
    if not value:
        return value
    return ('0%s' % integer(value, secret, size))[:-1]


def license_tag(value, secret, size=None):
    """License tag of a car."""
    if not value:
        return value
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
    if not value:
        return value
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
    if not value:
        return value
    day = integer(value, secret)
    if day > 28:
        day = int(day / 4)
    if day == 0:
        day = 1
    return day


def month(value, secret, size=None):
    if not value:
        return value
    month = integer(value, secret)
    if month > 12:
        month = int(month / 8)
    if month == 0:
        month = 1
    return month


def year(value, secret, size=None):
    if not value:
        return value
    year = integer(value, secret)
    if year < 1900:
        year = year + 1900
    return year


def date(value, secret, size=None):
    if not value:
        return value
    return datetime.date(year(value.year, secret),
                         month(value.month, secret),
                         day(value.day, secret))


def datestring(value, secret, size=None, format='DD.MM.YYYY'):
    """Date represended as a string.

    Parts of the date which are 0 are kept zero. (e. g. if the day is '00'
    it is not pseudonymized)

    """
    if not value:
        return value
    value = list(value)
    for part, length, func in (('D', 2, day), ('M', 2, month), ('Y', 4, year)):
        assert format.count(part) == length
        start_pos = format.find(part)
        val = value[start_pos:start_pos + length]
        if val != ['0'] * length:
            value[start_pos:start_pos + length] = list(
                str(func(''.join(val), secret)).zfill(length))
    return ''.join(value)


def time(value, secret, size=None):
    if not value:
        return value
    value = str(integer(value.strftime('%H%M%S'), secret)).zfill(6)
    hour, minute, second = (
        int(value[:2]), int(value[2:4]), int(value[4:]))
    if hour > 23:
        hour = int(hour / 5)
    if minute > 59:
        minute = int(minute / 2)
    if second > 59:
        second = int(second / 2)
    return datetime.time(hour, minute, second)
