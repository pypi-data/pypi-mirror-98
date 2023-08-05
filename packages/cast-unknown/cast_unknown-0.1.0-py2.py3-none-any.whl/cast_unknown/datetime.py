# -*- coding=UTF-8 -*-
"""Cast unknown value to datetime type.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime as dt

import dateutil.parser

from .text import text


def datetime_at(v, at):
    assert isinstance(at, dt.datetime)
    if isinstance(v, float):
        return dt.datetime.utcfromtimestamp(v)
    if isinstance(v, int):
        return dt.datetime.utcfromtimestamp(v/1e3)
    if isinstance(v, dt.datetime):
        return v
    if isinstance(v, dt.date):
        return dt.datetime(v.year, v.month, v.day)
    if isinstance(v, dt.time):
        return dt.datetime(
            at.year,
            at.month,
            at.day,
            v.hour,
            v.minute,
            v.second,
            v.microsecond,
            v.tzinfo
        )
    return dateutil.parser.parse(text(v))


def datetime(v):
    return datetime_at(v, dt.datetime.now())
