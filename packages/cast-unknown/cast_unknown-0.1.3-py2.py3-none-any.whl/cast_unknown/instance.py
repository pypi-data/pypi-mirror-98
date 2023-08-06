# -*- coding=UTF-8 -*-
"""Cast unknown value to instance of given type.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from .error import CastError


def instance(object, class_or_tuple):
    """raise CastError when object is not isinstance of given class.

    Args:
        object: object to test
        class_or_tuple: second arg of `isinstance`

    Raises:
        CastError: When object is not match

    Returns:
        object unchanged
    """
    if not isinstance(object, class_or_tuple):
        raise CastError(
            "can not cast object to instance",
            object,
            class_or_tuple,
        )
    return object
