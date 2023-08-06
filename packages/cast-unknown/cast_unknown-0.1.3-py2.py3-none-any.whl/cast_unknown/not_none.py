# -*- coding=UTF-8 -*-
"""Cast unknown value to non null.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from .error import CastError

def not_none(value, default=None):
    if value is not None:
        return value
    if default is not None:
        return default
    raise CastError("value and default both None ")
