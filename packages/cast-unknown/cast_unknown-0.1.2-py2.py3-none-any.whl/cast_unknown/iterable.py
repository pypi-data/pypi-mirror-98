# -*- coding=UTF-8 -*-
"""Cast unknown value to iterable.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import Iterable


def iterable(v):
    """Cast value to iterable, return empty iterable when value is none

    Args:
        v (typing.Any): value

    Returns:
        typing.Iterable: iterable that contains value
    """

    if v is None:
        return []

    if isinstance(v, Iterable):
        return v

    return [v]
