# -*- coding=UTF-8 -*-
"""Cast unknown value to exact one item.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .iterable import iterable


def one(v):
    """one and exact one item from value.

    Args:
        v (typing.Any): value

    Returns:
        typing.Any: First item if value is a length 1 iterable,
            value itself if value is not iterable,
            None otherwise. 
    """
    ret = None
    for index, i in enumerate(iterable(v)):
        if index > 0:
            return None
        ret = i
    return ret
