from typing import Any, TypeVar

import six

T = TypeVar("T")


def text(v: Any, encoding: six.text_type = ..., errors: six.text_type = ...) -> six.text_type: ...
