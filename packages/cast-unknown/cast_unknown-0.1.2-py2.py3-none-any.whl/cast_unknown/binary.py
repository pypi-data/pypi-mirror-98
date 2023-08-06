# -*- coding=UTF-8 -*-
"""Cast unknown value to binary type.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six


def binary(v, encoding='utf-8', errors='strict'):
    """cast value to binary type,

    Args:
        v (typing.Any): value
        encoding (str, optional): encoding when value is not binary. Defaults to 'utf-8'.
        errors (str, optional): errors setting when value is not binary. Defaults to 'strict'.

    Returns:
        six.binary_type: encoded value
    """

    if isinstance(v, six.binary_type):
        return v
    if isinstance(v, six.text_type):
        return v.encode(encoding, errors)
    return six.text_type(v).encode(encoding, errors)
