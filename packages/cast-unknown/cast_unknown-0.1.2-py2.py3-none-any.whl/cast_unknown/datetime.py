# -*- coding=UTF-8 -*-
"""Cast unknown value to datetime type.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime as dt

import dateutil.parser
import six

from .text import text


def datetime_at(v, at):
    """Cast value to datetime use given time.

    Args:
        v (typing.Any): Value

    Returns:
        dt.datetime: convert result
    """
    assert isinstance(at, dt.datetime)
    if isinstance(v, float):
        return dt.datetime.utcfromtimestamp(v)
    if isinstance(v, six.integer_types):
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
    return dateutil.parser.parse(text(v), default=at)


def datetime(v):
    """Cast value to datetime use current time.

    Args:
        v (typing.Any): Value

    Returns:
        dt.datetime: convert result
    """
    today = dt.datetime.now()
    today = dt.datetime(today.year, today.month, today.day)
    return datetime_at(v, today)
