# -*- coding=UTF-8 -*-
"""Cast unknown value to text type.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

def text(v, encoding='utf-8', errors='strict'):
    """Cast value  to text type, 

    Args:
        v (typing.Any): value
        encoding (str, optional): encoding when value is binary. Defaults to 'utf-8'.
        errors (str, optional): decode error setting when value is binary. Defaults to 'strict'.

    Returns:
        str: decoded value.
    """

    if isinstance(v, six.text_type):
        return v
    if isinstance(v, six.binary_type):
        return v.decode(encoding, errors)
    return six.text_type(v)
