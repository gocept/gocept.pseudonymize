# -*- coding: utf-8 -*-
# Copyright (c) 2013 gocept gmbh & co. kg
# See also LICENSE.txt

from decimal import Decimal
import crypt
import datetime


def text(value, secret, size=None):
    if size is None:
        size = len(value)
    result = crypt.crypt(value, secret)
    if result.startswith('$'):
        digits, result = result[1:].split('$')
        digits = int(digits)
    else:
        digits, result = (2, result)  # Default crypt behaviour
    return result[digits:size+digits].replace('/', '.')


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


def date(value, secret, size=None):
    value = str(integer(value.strftime('%d%m%Y'), secret)).zfill(8)
    day, month, year = (
        int(value[:2]), int(value[2:4]), int(value[4:]))
    if day > 28:
        day = int(day / 4)
    if month > 12:
        month = int(month / 8)
    day = 1 if day == 0 else day
    month = 1 if month == 0 else month
    return datetime.date(year, month, day)


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
